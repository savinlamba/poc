import streamlit as st
import google.generativeai as genai
import os
from pygments.lexers import guess_lexer, ClassNotFound
from dotenv import load_dotenv

# Load environment variables for API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API key if available
if api_key:
    try:
        genai.configure(api_key=api_key)
        st.success("API key configured successfully.")
    except Exception as e:
        st.error(f"Configuration error: {e}")
else:
    st.error("API key not found. Make sure GEMINI_API_KEY is set in your environment.")

def detect_language(code_snippet):
    """Detects the programming language of a code snippet."""
    try:
        lexer = guess_lexer(code_snippet)
        language = lexer.name.lower()
        return language
    except ClassNotFound:
        return None

def generate_unit_test(code_snippet, language):
    """Generates a unit test for the given code snippet in the detected language."""
    prompt = f"Write unit test cases for the following {language} code:\n\n{code_snippet}\n\n"
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with appropriate model name
        response = model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text  # Adjust according to response structure
    except Exception as e:
        st.error(f"Error generating unit tests: {e}")
        return None

# Streamlit App Layout
st.title("Unit Test Generator")
st.write("Enter your code snippet below and click 'Generate Unit Tests'.")

# Code input box
code_snippet = st.text_area("Code Snippet", height=200)

# Button to generate unit tests
if st.button("Generate Unit Tests") and code_snippet:
    # Detect language
    language = detect_language(code_snippet)
    
    if language:
        # Generate unit test based on the detected language
        unit_tests = generate_unit_test(code_snippet, language)
        
        if unit_tests:
            st.write("### Generated Unit Tests:")
            st.code(unit_tests, language='python')  # Adjust language for syntax highlighting
        else:
            st.error("Failed to generate unit tests.")
    else:
        st.error("Could not detect the language of the code snippet.")
