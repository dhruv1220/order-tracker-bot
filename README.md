# **Order Status Chatbot (FastAPI + OpenAI)**
🚀 **A FastAPI-based chatbot that tracks and cancels orders using OpenAI's GPT API with function calling.**  
This API allows users to:
- Check **order status** using an `order_id`.
- Cancel an **existing order**.
- Maintain **conversation flow** for follow-up queries.

---

## **📌 Features**
✅ **FastAPI Backend** – Lightweight and high-performance API.  
✅ **OpenAI GPT Function Calling** – Dynamically understands and processes requests.  
✅ **CSV-Based Order Database** – Loads orders from a `orders.csv` file.  
✅ **Conversation History** – Maintains chat flow using `conversation_id`.  

---

## **🛠️ Setup Instructions**
### **1️⃣ Install Dependencies**
Make sure you have Python 3.8+ installed. Then, install the required libraries:
```bash
pip install fastapi uvicorn openai pydantic python-dotenv
```

### **2️⃣ Set Up Your OpenAI API Key**
Before running the app, set your OpenAI API key as an environment variable:

- **On Mac/Linux (Terminal)**
  ```bash
  export OPENAI_API_KEY="your_openai_api_key"
  ```

- **On Windows (Command Prompt)**
  ```cmd
  setx OPENAI_API_KEY "your_openai_api_key"
  ```

- **On Windows (PowerShell)**
  ```powershell
  $env:OPENAI_API_KEY="your_openai_api_key"
  ```

Replace `"your_openai_api_key"` with your actual OpenAI API key.

### **3️⃣ Ensure `orders.csv` Exists**
The file `orders.csv` should be present in the same directory as `main.py`.  
Example structure:
```
order_id,status,item
12345,shipped,Sneakers
23456,processing,Laptop
34567,canceled,Headphones
```

### **4️⃣ Run the FastAPI Server**
```bash
uvicorn main:app --reload
```
This will start the API at:  
```
http://127.0.0.1:8000
```

---

## **📡 API Endpoints**
| Method | Endpoint | Description |
|---------|----------------|-------------|
| `POST` | `/conversations` | Start a new conversation |
| `GET` | `/conversations/{conversation_id}/messages` | Get message history |
| `POST` | `/conversations/{conversation_id}/messages` | Query order status/cancel order |

---

## **🚀 Usage**
### **1️⃣ Start a New Conversation**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/conversations'
```
🔹 **Response:**
```json
{ "conversation_id": "123e4567-e89b-12d3-a456-426614174000" }
```

### **2️⃣ Ask About an Order**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/conversations/123e4567-e89b-12d3-a456-426614174000/messages' \
-H 'Content-Type: application/json' \
-d '{"content": "What is the status of order 12345?"}'
```
🔹 **Response:**
```json
{
  "role": "assistant",
  "content": "Order 12345: Sneakers is currently shipped."
}
```

### **3️⃣ Cancel an Order**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/conversations/123e4567-e89b-12d3-a456-426614174000/messages' \
-H 'Content-Type: application/json' \
-d '{"content": "Cancel my order 12345"}'
```
🔹 **Response:**
```json
{
  "role": "assistant",
  "content": "Order 12345 has been canceled."
}
```

### **4️⃣ Retrieve Full Conversation**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/conversations/123e4567-e89b-12d3-a456-426614174000/messages'
```
🔹 **Response (Full Chat History):**
```json
[
  { "role": "user", "content": "What is the status of order 12345?" },
  { "role": "assistant", "content": "Order 12345: Sneakers is currently shipped." },
  { "role": "user", "content": "Cancel my order 12345" },
  { "role": "assistant", "content": "Order 12345 has been canceled." }
]
```

---

## **📌 Project Structure**
```
📂 order-status-chatbot
│── main.py             # FastAPI backend code
│── orders.csv          # Sample order data
│── requirements.txt    # Required Python packages
│── README.md           # Project documentation
```

---

## **💡 Next Steps**
🔹 Add **database support (PostgreSQL, Redis, MongoDB)** for persistent storage.  
🔹 Deploy to **AWS Lambda, GCP, or Azure** for cloud hosting.  
🔹 Build a **frontend UI (React/Streamlit)** for an interactive experience.  

---

## **🛠 Troubleshooting**
### **⚠ Rate Limit / Quota Exceeded**
- **Check API usage**: [OpenAI Usage Dashboard](https://platform.openai.com/account/usage)
- **Upgrade your OpenAI plan**: [Billing Page](https://platform.openai.com/account/billing)
- **Implement rate limiting** to avoid too many requests in a short time.

### **⚠ OpenAI API Key Not Set**
- Run `echo $OPENAI_API_KEY` (Mac/Linux) or `echo %OPENAI_API_KEY%` (Windows) to verify it's set.
- Restart your terminal and rerun `uvicorn main:app --reload`.

---

## **👨‍💻 Contributors**
👤 **Dhruv Arora** – Developer  

---

## **📜 License**
This project is licensed under the **MIT License**.