import streamlit as st
from openai import OpenAI

# UI layout
st.title("🤖 AI Prompt Enhancer")

# API key input with password masking
api_key = st.text_input("Enter your OpenAI API key:", type="password", help="Your API key will not be stored")

role = st.text_input("Role of the assistant", placeholder="e.g., experienced coder")
context = st.text_area("Context", placeholder="e.g., I'm building my first AI app")
task = st.text_area("Task", placeholder="e.g., Help me debug my code")

if st.button("Enhance Prompt"):
    # Check for API key first
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif role and context and task:
        # Initialize client with user-provided API key
        try:
            client = OpenAI(api_key=api_key)
            
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
            
            # Add a download button for convenience
            st.download_button(
                label="Download Prompt as Text",
                data=enhanced_prompt,
                file_name="enhanced_prompt.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please check if your API key is valid and you have access to the GPT-4 model.")
    else:
        st.warning("Please fill in all fields.")

# Add a note about API key security
st.sidebar.markdown("""
### About API Keys
- Your API key is used only for making requests to OpenAI
- It is not stored or logged by this application
- You will need to enter it each time you use this app
""")