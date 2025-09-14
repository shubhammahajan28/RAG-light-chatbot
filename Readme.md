# Light Chatbot (Lighting) - Flask + LangChain + FAISS

A friendly AI chatbot for **Lighting** products built with **Flask**, **LangChain**, **FAISS**, and **OpenAI GPT**.
The chatbot answers questions about lighting products based on PDF documentation.

---

## Features

* User authentication: **Register** and **Login**
* Retrieval-Augmented Generation (RAG) using:

  * PDFs as document source
  * FAISS vector store for embeddings
  * OpenAI GPT (`gpt-4o-mini`) as LLM
* Chatbot API to answer product questions
* Auto-builds FAISS index from PDFs if missing

---

## Project Structure

```
light_chatbot_flask/
│
├── app/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── routes/
│   │   ├── chat.py
│   │   └── users.py
│   └── models.py
│
├── pdfs/                  # Put all product PDFs here
├── faiss_index/           # FAISS index (auto-generated)
├── run.py                 # Flask entrypoint
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the project

```bash
git clone <your-repo-url>
cd light_chatbot_flask
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate:

* **Windows**: `venv\Scripts\activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -U langchain-community langchain-openai
```

### 4. Set environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Flask App

```bash
python run.py
```

* Default: `http://127.0.0.1:5000/`
* First run: automatically creates FAISS index from PDFs.
* Later runs: loads existing FAISS index (`faiss_index/index.faiss`).

---

## Managing PDFs and FAISS Index

* Place all product PDFs in `pdfs/`.
* First run builds FAISS index automatically.
* If you add new PDFs, delete the old index:

```powershell
Remove-Item -Recurse -Force faiss_index
```

Then rerun the app to rebuild the index.

---

## API Endpoints

### 1. Register User

* **POST** `/api/users/register`
* **Body:**

```json
{
  "username": "shubham",
  "password": "mypassword"
}
```

* **Response:**

```json
{
  "message": "User registered successfully"
}
```

---

### 2. Login User

* **POST** `/api/users/login`
* **Body:**

```json
{
  "username": "shubham",
  "password": "mypassword"
}
```

* **Response:**

```json
{
  "message": "Login successful"
}
```

---

### 3. Chat with Bot

* **POST** `/api/chat/`
* **Body:**

```json
{
  "question": "Tell me about Recessed Commercial lighting"
}
```

* **Response:**

```json
{
  "answer": "🤖 Bot Answer: ..."
}
```

---

## Testing with Postman

You can import a Postman collection or test APIs manually.
Sequence:

1. Register → `/api/users/register`
2. Login → `/api/users/login`
3. Chat → `/api/chat/`

> Make sure your Flask app is running at `http://127.0.0.1:5000/`.

---

## Dependencies

* Flask
* Flask-SQLAlchemy
* Flask-Bcrypt
* python-dotenv
* LangChain (community + openai)
* FAISS (faiss-cpu)
* OpenAI Python SDK

---



