from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st
import warnings
import pdfplumber


# Suppress LangChain warnings
warnings.filterwarnings("ignore", category=UserWarning, module='langchain')

# LLM setup
llm = ChatOllama(model="llama3")

st.title("Smart AI Interviewer")

# Initial Greeting
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Say Hello to me")
])
st.write(getattr(response, "content", str(response)))

st.write("### Upload your resume and job description to begin:")

# File Uploads
resume_file = st.file_uploader("Upload your Resume (.txt or .pdf)", type=["txt", "pdf"])
jd_file = st.file_uploader("Upload Job Description (.txt or .pdf)", type=["txt", "pdf"])

# Helper: robust PDF text extraction
def read_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text.strip()

if resume_file and jd_file:
    # Handle Resume
    if resume_file.name.endswith(".txt"):
        resume_text = resume_file.read().decode("utf-8", errors="ignore")
    elif resume_file.name.endswith(".pdf"):
        resume_text = read_pdf(resume_file)
    else:
        st.error("Unsupported resume format.")
        st.stop()

    # Handle Job Description
    if jd_file.name.endswith(".txt"):
        jd_text = jd_file.read().decode("utf-8", errors="ignore")
    elif jd_file.name.endswith(".pdf"):
        jd_text = read_pdf(jd_file)
    else:
        st.error("Unsupported job description format.")
        st.stop()

    # -------------------- Resume & JD Parsing --------------------
    st.subheader("Resume & JD Parsing")
    st.markdown("""
    **Purpose:**
    This agent extracts important details from your resume and job description. It will:
    - Identify 5–7 key skills from your resume
    - Highlight 3 major job experiences
    - Extract 5 required competencies from the job description
    - Present everything in clear bullet points
    """)

    parser_prompt = [
        SystemMessage(content="You are a Resume & JD Parsing Agent. Extract structured information."),
        HumanMessage(content=f"""
        Resume:
        {resume_text}
        Job Description:
        {jd_text}
        Your Task:
        1. Extract 5–7 core skills from the resume.
        2. Mention 3 key job experiences.
        3. From the JD, extract 5 required competencies or qualifications.
        4. Output everything in bullet points.
        """)
    ]
    with st.spinner("Parsing resume and job description..."):
        parse_response = llm.invoke(parser_prompt)
    st.text_area("Parsed Summary", parse_response.content, height=300)

    # -------------------- Question Generator --------------------
    st.subheader("Interview Question Generator")
    st.markdown("""
    **Purpose:**
    This agent creates custom interview questions based on your resume and job
    description. It will:
    - Generate 10 questions (technical, behavioral, situational)
    - Clearly tag each type of question
    - Make all questions job-relevant
    """)

    question_prompt = [
        SystemMessage(content="You are an Interview Question Generator Agent."),
        HumanMessage(content=f"""
        Based on the resume and job description below, generate 10 interview questions.
        - Include a mix of technical, behavioral, and situational questions.
        - Tag each question like this: [Technical], [Behavioral], [Situational].
        - Make the questions relevant to the candidate’s profile and job role.
        Resume:
        {resume_text}
        Job Description:
        {jd_text}
        """)
    ]
    with st.spinner("Generating interview questions..."):
        question_response = llm.invoke(question_prompt)
    st.text_area("Interview Questions", question_response.content, height=300)

    # -------------------- Feedback Section --------------------
    st.subheader("Mock Interview Feedback")
    st.markdown("""
    **Purpose:**
    Paste your answer to any one question above. This agent will:
    - Score your answer out of 10
    - Highlight strengths and weaknesses
    - Rewrite your answer using the STAR format (Situation, Task, Action, Result)
    - Help you improve for real interviews
    """)

    user_answer = st.text_area("Type your answer to any one question from above:")
    if st.button("Get Feedback") and user_answer.strip():
        feedback_prompt = [
            SystemMessage(content="You are an Interview Feedback Agent."),
            HumanMessage(content=f"""
            Candidate's Answer:
            {user_answer}
            Your Task:
            1. Score the answer out of 10.
            2. Explain what was good and what can be improved.
            3. Rewrite the answer using the STAR method (Situation, Task, Action, Result).
            4. Make your feedback clear and easy to follow.
            """)
        ]
        with st.spinner("Analyzing your answer..."):
            feedback_response = llm.invoke(feedback_prompt)
        st.text_area("AI Feedback", feedback_response.content, height=300)

    # -------------------- Job Match Evaluation --------------------
    st.subheader("Job Suitability Score")
    st.markdown("""
    **Purpose:**
    This agent checks how well your resume fits the job. It will:
    - Give a job match score out of 100%
    - Highlight 2–3 strong alignment areas
    - Identify 2–3 skill or experience gaps
    - Provide a short recommendation (e.g., Good Match, Moderate Fit, Needs Improvement)
    """)

    if st.button("Check My Job Match Score"):
        match_prompt = [
            SystemMessage(content="You are a Job Match Evaluation Agent."),
            HumanMessage(content=f"""
            Your task is to evaluate how suitable the candidate is for the given job.
            Resume:
            {resume_text}
            Job Description:
            {jd_text}
            Instructions:
            1. Give a job match score out of 100%.
            2. Mention 2–3 strong match points.
            3. Mention 2–3 gaps or mismatches.
            4. End with a short overall recommendation (e.g. Good match, Moderate fit, Needs improvement).
            Format everything clearly.
            """)
        ]
        with st.spinner("Evaluating your job fit..."):
            match_response = llm.invoke(match_prompt)
        st.text_area("Job Fit Report", match_response.content, height=300)

else:
    st.warning("Please upload both Resume and Job Description to continue.")
