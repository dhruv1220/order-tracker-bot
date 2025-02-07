from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import csv
from openai import OpenAI
import os
import json

# Load OpenAI API key from environment variable
client = OpenAI(api_key="<Enter API Key>") 

# Initialize FastAPI app
app = FastAPI()

# Load CSV Data into Memory
orders = {}

def load_orders():
    """Load orders from CSV file into memory."""
    global orders
    orders = {}
    
    try:
        with open("orders.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                orders[row["order_id"]] = {
                    "status": row["status"],
                    "item": row["item"]
                }
    except FileNotFoundError:
        print("Error: orders.csv not found. Make sure the file is in the same directory.")

load_orders()

# In-memory conversation storage
conversations = {}

# Pydantic models for request and response handling
class MessageRequest(BaseModel):
    content: str

class ConversationResponse(BaseModel):
    conversation_id: str

class MessageResponse(BaseModel):
    role: str
    content: str

@app.post("/conversations", response_model=ConversationResponse)
def start_conversation():
    """Start a new conversation and return a conversation ID."""
    conversation_id = str(uuid.uuid4())
    conversations[conversation_id] = {"messages": []}
    return {"conversation_id": conversation_id}

@app.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
def get_messages(conversation_id: str):
    """Retrieve messages from a conversation."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversations[conversation_id]["messages"]

@app.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
def post_message(conversation_id: str, request: MessageRequest):
    """Process a user message and generate a response using OpenAI GPT function calling."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    user_message = {"role": "user", "content": request.content}
    conversations[conversation_id]["messages"].append(user_message)

    response_content = generate_gpt_response(request.content)
    assistant_message = {"role": "assistant", "content": response_content}

    conversations[conversation_id]["messages"].append(assistant_message)

    return assistant_message

def generate_gpt_response(user_input: str):
    """Uses OpenAI GPT with function calling to handle user queries."""
    functions = [
        {
            "name": "lookup_order_status",
            "description": "Retrieve the status of an order by order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID to lookup."}
                },
                "required": ["order_id"]
            }
        },
        {
            "name": "cancel_order",
            "description": "Cancel an order by order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID to cancel."}
                },
                "required": ["order_id"]
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}],
        functions=functions
    )

    # Check if GPT wants to call a function
    if response.get("choices") and response["choices"][0].get("message", {}).get("function_call"):
        function_call = response["choices"][0]["message"]["function_call"]
        function_name = function_call["name"]
        arguments = json.loads(function_call["arguments"])

        if function_name == "lookup_order_status":
            return lookup_order_status(arguments["order_id"])
        elif function_name == "cancel_order":
            return cancel_order(arguments["order_id"])

    return response["choices"][0]["message"]["content"]

def lookup_order_status(order_id: str):
    """Retrieve order status from memory."""
    if order_id in orders:
        order_info = orders[order_id]
        return f"Order {order_id}: {order_info['item']} is currently {order_info['status']}."
    return f"Order {order_id} not found."

def cancel_order(order_id: str):
    """Simulate order cancellation."""
    if order_id in orders:
        orders[order_id]["status"] = "canceled"
        return f"Order {order_id} has been canceled."
    return f"Order {order_id} not found."

# Running the app (if executed as a script)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
