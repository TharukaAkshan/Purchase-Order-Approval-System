# Purchase Order Approval System

An AI-powered automation system that monitors emails for purchase orders, extracts structured data, checks for duplicates, and makes intelligent approval decisions.

## 🏗️ Architecture Overview

```
Email Inbox → Extraction Agent → Vector DB Search → Approval Agent → Decision
```

### Key Components

| Component | Function |
|-----------|----------|
| **Email Listener** | Monitors Gmail for unread emails with "purchase order" in subject |
| **Extraction Agent** | Uses GPT-4V to parse PDF attachments and extract structured PO data (vendor, items, amounts, dates, etc.) |
| **Knowledge Base** | Vector database stores historical POs for similarity matching |
| **Approval Agent** | Compares current PO against matched records; auto-approves unique orders or flags duplicates for review |
| **FastAPI Server** | REST API to control email monitoring and system health |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Gmail account with app password
- OpenAI API key (GPT-4V access)

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:
```
EMAIL=your-gmail@gmail.com
APP_PASSWORD=your-app-password
OPENAI_API_KEY=your-openai-key
```

### Run

```bash
python main.py
```

The API will start at `http://localhost:5000`

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/start-email-reading-process` | POST | Begin monitoring emails |
| `/stop-email-reading-process` | POST | Stop monitoring emails |

## 📁 Project Structure

```
├── main.py                          # FastAPI app & email process controller
├── python/
│   ├── email.py                     # Gmail IMAP connection & email listener
│   ├── preprocess.py                # PDF → Base64 image conversion
│   ├── agents/
│   │   ├── extraction/              # PO data extraction agent
│   │   │   ├── llm.py              # GPT-4V configuration
│   │   │   └── process.py          # Extraction logic
│   │   └── approval/                # PO approval decision agent
│   │       ├── llm.py              # GPT configuration
│   │       └── process.py          # Approval logic
│   └── knowledgebase/               # Vector database & similarity search
│       ├── db.py                    # Database operations
│       └── vector.py                # Vector embeddings & search
└── Test/                            # Jupyter notebooks for testing
```

## 🔄 How It Works

1. **Email Monitoring**: System continuously scans Gmail for unseen emails containing "purchase order"
2. **Document Extraction**: PDF attachments are converted to images and sent to GPT-4V for structured data extraction
3. **Similarity Check**: Extracted data is vectorized and compared against historical POs in the knowledge base
4. **Auto-Approval**: 
   - ✅ **PASS**: New/unique PO → approved for processing
   - ❌ **FAIL**: Duplicate detected → flagged for manual review
5. **Result Storage**: Approved records are saved to the database for future reference

## 📦 Tech Stack

- **LLM**: OpenAI GPT-4V (document parsing & decision making)
- **Embeddings**: FlagEmbedding (vector similarity search)
- **Database**: PostgreSQL with AsyncPG
- **API**: FastAPI + Uvicorn
- **Document Processing**: PDF2Image, PIL

## 🎯 Key Features

✨ Real-time email monitoring  
✨ AI-powered document parsing  
✨ Intelligent duplicate detection  
✨ Async processing with background tasks  
✨ RESTful API for control & monitoring  

---

**Version**: 1.1.1