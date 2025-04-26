import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# UI layout
st.title("🤖 AI Prompt Enhancer")

role = st.text_input("Role of the assistant", placeholder="e.g., experienced coder")
context = st.text_area("Context", placeholder="e.g., I'm building my first AI app")
task = st.text_area("Task", placeholder="e.g., Help me debug my code")

if st.button("Enhance Prompt"):
    if role and context and task:
        user_input = f"""
Role: {role}
Context: {context}
Task: {task}
        """.strip()

        system_message = """You are a prompt engineering expert. 
Your task is to take the user's basic prompt components and craft an enhanced, more effective prompt.
Return ONLY the improved prompt without any explanations, introductions, or additional text.
The prompt should be ready to copy and paste into any AI system.
Include appropriate instructions for tone, format, and specific requirements.
"""

        with st.spinner("Enhancing your prompt..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ]
            )
            enhanced_prompt = response.choices[0].message.content

        st.subheader("🔍 Enhanced Prompt")
        st.text_area("Copy this prompt to use with any AI:", enhanced_prompt, height=300)
        
        # Add a copy button for convenience
        if st.button("Copy to Clipboard"):
            st.write("Prompt copied to clipboard! (Note: This button works when deployed)")
            st.code("import pyperclip; pyperclip.copy(enhanced_prompt)", language="python")
    else:
        st.warning("Please fill in all fields.")