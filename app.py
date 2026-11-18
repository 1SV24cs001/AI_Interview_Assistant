
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🫡",
    layout="centered"
)

# Application title
st.title("🫡 AI Interview Assistant")
st.caption("Your AI-powered platform for interview preparation")

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error(
        "Groq API Key is missing. "
        "Please add GROQ_API_KEY in Streamlit Secrets."
    )
    st.stop()

# Job role selection
role = st.selectbox(
    "JOB TITLE",
    [
        "Software Engineer",
        "Senior Software Engineer",
        "Data Analyst",
        "Prompt Engineer",
        "DevOps Engineer",
        "Other"
    ]
)

# Custom job title
if role == "Other":
    role = st.text_input("Enter your job title")

# Model selection
model = st.selectbox(
    "Select Model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-safeguard-20b"
    ]
)

# Difficulty level
difficulty = st.selectbox(
    "Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# Activity selection
mode = st.radio(
    "Choose Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answer",
        "Improve Answer"
    ]
)

# Activity-specific inputs
if mode == "Generate Questions":

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

elif mode == "Generate Code Questions":

    topic = st.selectbox(
        "Select Topic",
        [
            "SQL",
            "AI/ML",
            "Python",
            "DSA",
            "C++/C",
            "Java",
            "Cyber Security",
            "Machine Learning"
        ]
    )

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

else:

    question = st.text_area(
        "Enter Interview Question",
        placeholder="Enter your interview question here..."
    )

    answer = st.text_area(
        "Enter Your Answer",
        height=160,
        placeholder="Write your answer here..."
    )

# Generate button
if st.button("Generate / Submit", type="primary"):

    if not role.strip():
        st.warning("Please enter a valid job title.")

    elif mode in ["Evaluate Answer", "Improve Answer"] and (
        not question.strip() or not answer.strip()
    ):
        st.warning("Please enter both the question and your answer.")

    else:

        # Create prompt according to activity
        if mode == "Generate Questions":

            prompt = f"""
            Act as an experienced technical interviewer.

            Generate {count} interview questions for the role of {role}.

            Difficulty level: {difficulty}

            Include a mixture of technical and practical questions.
            Number the questions clearly.
            """

        elif mode == "Generate Code Questions":

            prompt = f"""
            Act as an experienced technical interviewer.

            Generate {count} coding interview questions.

            Job Role: {role}
            Topic: {topic}
            Difficulty: {difficulty}

            Include clear problem statements and examples
            wherever appropriate.

            Do not provide solutions unless requested.
            """

        elif mode == "Evaluate Answer":

            prompt = f"""
            Act as a professional interview evaluator.

            Job Role: {role}
            Difficulty: {difficulty}

            Interview Question:
            {question}

            Candidate Answer:
            {answer}

            Evaluate the answer based on:
            1. Technical accuracy
            2. Clarity
            3. Completeness
            4. Relevance

            Give:
            - Score out of 10
            - Strengths
            - Weaknesses
            - Suggestions for improvement
            - An example of a better answer
            """

        else:

            prompt = f"""
            Act as an expert interview coach.

            Job Role: {role}
            Difficulty: {difficulty}

            Interview Question:
            {question}

            Candidate Answer:
            {answer}

            Improve the candidate's answer.

            Make it:
            1. Professional
            2. Clear and concise
            3. Technically accurate
            4. Relevant to the job role

            Also explain what you improved.
            """

        # Call Groq API
        try:
            with st.spinner("AI is working on your request..."):

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert interview coach "
                                "and technical interviewer."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )

                result = response.choices[0].message.content

            # Display result
            st.success("Response generated successfully!")

            st.subheader("AI Interview Assistant Response")

            st.markdown(result)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

