# P.A.S.T. — Personalized Assessment System for Tutoring

## Project Overview

P.A.S.T. is an AI-powered tutoring assistant designed to reduce academic stress and enhance self-guided learning. It dynamically generates multiple-choice questions and personalized feedback based on topics provided by the student.

This tool helps students:
- Practice subject material in an interactive way  
- Receive AI-generated feedback on their answers  
- Reinforce understanding through guided correction  

Originally developed for the AI Remove Barriers term project, this system demonstrates how artificial intelligence can help students overcome challenges like test anxiety, poor feedback access, and inconsistent study strategies.

## How It Works

1. The student enters a topic they want to study.
2. The app uses Google's Gemini Pro 1.5 API to generate a multiple-choice question.
3. The student selects an answer (A–D).
4. Gemini provides personalized, constructive feedback, including a helpful learning tip.

## Tech Stack

| Component   | Technology                      |
|------------|----------------------------------|
| Interface   | PyQt6 GUI (Python, PyCharm)     |
| AI Engine   | Gemini Pro 1.5 (via API)        |
| Language    | Python 3.11+                    |
| Libraries   | google-generativeai, dotenv     |

## Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/sredh01/AI-Final.git
cd AI-Final
```

### 2. Set Up Environment
Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install google-generativeai python-dotenv pyqt6
```

### 4. Configure Your API Key

1. Create a `.env` file in the root directory:
```ini
GEMINI_API_KEY=your_api_key_here
```

2. Do not commit this file to GitHub.

## Running the App

In the root folder:

```bash
python main.py
```

The app will launch a PyQt GUI where you can enter a topic, generate a question, select an answer, and receive AI feedback.

## Security Notice

To protect your API key:
- Store it in a `.env` file
- Add `.env` to your `.gitignore`
- Never hardcode API keys in your scripts

## Features

- Multiple-choice quiz generation by Gemini
- Feedback loop powered by generative AI
- Beginner/intermediate/hard difficulty selection
- Lightweight GUI using PyQt6

## Future Improvements

- Support for code-related question types
- Exportable quiz history
- Web-based version (Flask or Streamlit)

## Author

Built by Eric and Redhouse for the AI Remove Barriers term project at TAMUSA.
