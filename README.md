# Smart AI Interviewer

An AI-powered interview preparation tool built with **LangChain**, **Ollama**, and **Streamlit**.  
This app helps candidates parse resumes & job descriptions, generate tailored interview questions, get AI-driven feedback, and evaluate job fit.

---

## 🚀 Features
- **Resume & Job Description Parsing**  
  Extracts:
  - 5–7 key skills from resume  
  - 3 major job experiences  
  - 5 required competencies from JD  

- **Interview Question Generator**  
  - Creates 10 custom questions (technical, behavioral, situational)  
  - Tags each question clearly  

- **Mock Interview Feedback**  
  - Scores answers out of 10  
  - Highlights strengths & weaknesses  
  - Rewrites answers using **STAR (Situation, Task, Action, Result)** format  

- **Job Match Evaluation**  
  - Provides a **match score (0–100%)**  
  - Lists strong alignment areas & gaps  
  - Gives a short recommendation (Good Match, Moderate Fit, Needs Improvement)  

---

## 🛠️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/smart-ai-interviewer.git
   cd smart-ai-interviewer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/Mac
   .venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure **Ollama** is installed and running:
   ```bash
   ollama run llama3
   ```

---

## ▶️ Usage

Run the Streamlit app:
```bash
streamlit run Agent.py
```

Then open the provided local URL (default: `http://localhost:8501`) in your browser.

---

## 📂 File Structure
```
smart-ai-interviewer/
│-- Agent.py          # Main Streamlit app
│-- requirements.txt  # Python dependencies
│-- README.md         # Project documentation
```

---

## ✅ Requirements
- Python 3.9+
- Streamlit
- LangChain
- langchain-ollama
- pdfplumber
- Ollama (with Llama3 model)

---

## 📌 Future Improvements
- Save parsed results & feedback for multiple sessions  
- Add support for more LLMs  
- Export interview feedback as PDF  
