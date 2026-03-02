# CUD Course Scraper Portal

An AI-powered browser automation system that logs into the Canadian University Dubai portal and extracts structured course offering data.

Built with Streamlit for the interface and LLM-driven automation for intelligent data extraction.

---

## Features

* Automated login to CUD portal
* Navigation to Course Offerings section
* SEAST filter application
* Structured extraction of:

  * Course code
  * Course name
  * Credits
  * Instructor
  * Room
  * Days
  * Start time
  * End time
  * Maximum enrollment
  * Total enrollment
* Multi-page scraping (Pages 1–3)
* Cloud (Gemini) or Local (Ollama) LLM backend
* CSV and Excel export
* Interactive filtering inside the app

---

## Tech Stack

* Python
* Streamlit
* LangChain
* Google Gemini API
* Ollama (Local LLM)
* Pydantic
* Pandas
* browser-use agent framework

---

## Project Structure

```
.
├── app.py            # Streamlit UI
├── Scraper.py        # AI scraping agent
├── Support.py        # Data models (Pydantic schemas)
├── CUD Logo.jpg      # Logo asset
├── .env              # API keys (not committed)
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/Ahnaddd-y/CUD-Course-Scraper-AI.git
cd CUD-Course-Scraper-AI
```

### 2. Install dependencies

```
pip install streamlit pandas python-dotenv langchain langchain-google-genai langchain-ollama langchain-openai pydantic browser-use openpyxl
```

### 3. Configure API Key (for Gemini backend)

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Application

```
streamlit run app.py
```

The app will launch in your browser.

---

## How It Works

1. User provides portal credentials and semester.
2. AI agent logs into the CUD portal.
3. Navigates to Course Offering and applies filters.
4. Extracts structured data using schema validation.
5. Displays results with filtering and export options.

---

## Academic Context

Developed as a university project demonstrating AI-driven browser automation, structured LLM outputs, and interactive data processing using Streamlit.
