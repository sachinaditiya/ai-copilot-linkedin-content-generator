import streamlit as st
import openai
import os

# --- Page Config ---
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📢",
    layout="centered"
)

# --- Sidebar Branding ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/174/174857.png", width=60)
    st.markdown("### About Me")
    st.write("""
    Hi! I'm **Sachin Aditiya B**,  
    Data Science graduate, passionate about ML, GenAI, and teaching.  
    [🔗 Connect on LinkedIn](https://www.linkedin.com/in/sachin-aditiya-b)
    """)
    st.markdown("---")
    st.markdown("⚡ Powered by **OpenAI**")

# --- API Key Handling ---
# Try to load from environment variable first
openai_api_key = os.getenv("OPENAI_API_KEY")

# Ask user input if key not found
if not openai_api_key:
    user_api_key = st.text_input("Enter your OpenAI API Key (optional for local testing):", type="password")
    openai_api_key = user_api_key if user_api_key else None

# Assign key if available
if openai_api_key:
    openai.api_key = openai_api_key

# --- Main Heading ---
st.title("📢 LinkedIn Post Generator")
st.markdown("Easily generate professional, engaging LinkedIn posts with AI.")

# --- User Inputs ---
topic = st.text_input("Enter your topic:")
tone = st.selectbox(
    "Choose a tone:",
    ["Professional", "Inspirational", "Casual", "Funny", "Motivational"]
)
audience = st.text_input("Target Audience (Optional):", "")
cta = st.text_input("📢 Call to Action (Optional):", "")

# --- Generate Button ---
if st.button("Generate LinkedIn Post"):
    if not openai_api_key:
        st.error("Cannot generate posts without an OpenAI API key.")
    elif topic.strip() == "":
        st.error("Please enter a topic!")
    else:
        with st.spinner("Generating your LinkedIn post..."):
            prompt = f"""
Write a {tone.lower()} LinkedIn post about '{topic}'.
Target audience: {audience if audience else 'General'}.
Include a strong call-to-action: {cta if cta else 'Encourage engagement'}.
Keep it concise, engaging, and add relevant hashtags.
            """
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=180,
                temperature=0.7
            )
            
            post = response.choices[0].text.strip()
        
        st.subheader("🎯 Your LinkedIn Post:")
        st.write(post)
        st.success("✅ Copy & Share this on LinkedIn!")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center>Built with ❤️ by Sachin Aditiya | Powered by OpenAI</center>",
    unsafe_allow_html=True
)
