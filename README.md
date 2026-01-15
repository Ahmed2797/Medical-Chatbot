# 🏥 Medical ChatApp

An AI-powered **Medical Chat Application** that allows users to query medical documents (PDFs) and receive intelligent, context-aware answers using **LLMs, embeddings, and vector databases**.

This project is built for learning and practical implementation of **RAG (Retrieval-Augmented Generation)** concepts using tools like **LangChain / CrewAI, FAISS/ChromaDB, and Sentence Transformers**.

---

## 🚀 Features

* 📄 Upload and process medical PDF documents
* 🔍 Semantic search using vector embeddings
* 🧠 Context-aware medical Q&A (RAG)
* ⚡ Fast similarity search with FAISS / ChromaDB
* 🧩 Modular and scalable project structure
* 🧪 Jupyter notebooks for experimentation
* ✅ GitHub Actions CI for automated code checks

---

## 🗂️ Project Structure

```bash
Medical-ChatApp/
│
├── app.py                 # Main application file
├── main.py                # Entry point (if applicable)
├── app.ipynb              # Notebook version of the app
├── medical.ipynb          # Medical RAG experiments
├── medical_chatbot.ipynb  # Chatbot notebook
│
├── data/
│   └── Medical_book.pdf   # Medical source document
│
├── faiss_index/           # FAISS vector index
│   ├── index.faiss
│   └── index.pkl
│
├── ml_faiss_index/        # Alternative FAISS index
│   ├── index.faiss
│   └── index.pkl
│
├── project/
│   ├── chatmodel/         # LLM/chat logic
│   ├── embed/             # Embedding logic
│   ├── chunk/             # Text chunking utilities
│   └── data/              # Internal data handling
│
├── .github/
│   └── workflows/
│       └── ci.yaml        # GitHub Actions CI workflow
│
├── requirements.txt       # Project dependencies
├── requirements.lock
├── .env                   # Environment variables
└── README.md              # Project documentation
```

---

## 🧠 Tech Stack

* **Python 3.10+**
* **LangChain / CrewAI**
* **Sentence-Transformers** (`all-MiniLM-l6-v2`, `all-mpnet-base-v2`)
* **FAISS / ChromaDB** (Vector Databases)
* **OpenAI / Local LLMs**
* **Jupyter Notebook**
* **GitHub Actions** for CI/CD

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Ahmed2797/Medical-Chatbot.git
cd medical-chatapp
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


conda create -n chatapp python=3.12
conda activate chatapp
conda deactivate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## ▶️ How to Run

### Run using Python

```bash
python app.py
```

### Or explore via Jupyter Notebook

```bash
jupyter notebook
```

Open `medical_chatbot.ipynb`

### GitHub Actions CI

* The workflow `ci.yaml` automatically checks your Python environment and dependencies on every push or pull request.
* You can view CI results on the **Actions** tab in your GitHub repository.

---

## 🔍 Embedding Notes (Important)

* **Embedding dimension must match the vector DB**

  * `all-MiniLM-l6-v2` → **384 dimensions**
  * `all-mpnet-base-v2` → **768 dimensions**

⚠️ If you change the embedding model, **rebuild the FAISS / ChromaDB index**.

---

## ⚠️ Disclaimer

This application is for **educational and experimental purposes only**.
It **does not provide medical advice**. Always consult a licensed medical professional.

---

## 🌱 Future Improvements

* 🧑‍⚕️ Doctor-style answer formatting
* 🌐 Web UI (Streamlit / FastAPI)
* 🧾 Multi-PDF support
* 🧠 Memory-based conversations
* 🔐 Authentication & logging

---

## 🙌 Acknowledgements

* LangChain & CrewAI community
* Sentence-Transformers
* FAISS & ChromaDB
* Open-source AI ecosystem

---

## 📬 Contact

**Author:** github.com/Ahmed2797
**Interest:** Machine Learning, Medical AI, RAG Systems

⭐ If you find this project helpful, give it a star!
