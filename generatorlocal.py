import os
import streamlit as st
import openai
from io import BytesIO
from dotenv import load_dotenv
import pyperclip

# ========================
# Load environment
# ========================
load_dotenv()
IS_LOCAL = "STREAMLIT_SERVER_PORT" not in os.environ  # True for local

# ========================
# Default API Key
# ========================
try:
    if IS_LOCAL:
        DEFAULT_API_KEY = os.getenv("OPENAI_API_KEY")  # local from .env
    else:
        DEFAULT_API_KEY = st.secrets.get("OPENAI_API_KEY")  # deployed
except Exception:
    DEFAULT_API_KEY = None

# ========================
# Page config
# ========================
st.set_page_config(
    page_title="AI Co-Pilot for LinkedIn Content Creation",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ========================
# Header
# ========================
st.markdown(
    "<h1 style='text-align: center; color:#4B0082; font-size:48px; font-weight:bold;'>💼 AI Co-Pilot for LinkedIn Content Creation</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color:#555; font-size:18px;'>Generate professional LinkedIn posts quickly and effortlessly.</p>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# ========================
# Topic Input
# ========================
st.markdown("Topic <span style='color:red'>*</span>", unsafe_allow_html=True)
topic = st.text_input("", placeholder="Example: Teamwork in Startups", help="This field is mandatory")

# ========================
# Prompt Templates
# ========================
templates = [
    "Write an inspiring LinkedIn post about {topic}.",
    "Create a professional post highlighting {topic} for career growth.",
    "Write a creative and engaging post about {topic} for LinkedIn audience."
]
selected_template = st.selectbox("Choose a prompt template", templates)

# ========================
# Preset Categories
# ========================
st.markdown("📚 Preset Categories (optional)", unsafe_allow_html=True)
category = st.selectbox(
    "Select a category to auto-fill prompt:",
    ["None", "Leadership", "Startups", "Career Growth", "Teamwork", "Innovation"]
)
preset_prompts = {
    "Leadership": "Write a professional LinkedIn post about leadership and inspiring teams.",
    "Startups": "Write an engaging LinkedIn post highlighting startup culture and entrepreneurship.",
    "Career Growth": "Create a professional LinkedIn post about career growth and personal development.",
    "Teamwork": "Write a LinkedIn post emphasizing teamwork and collaboration.",
    "Innovation": "Create a LinkedIn post about innovation and creative thinking in business."
}

# ========================
# Final Custom Prompt
# ========================
if category != "None":
    final_prompt = preset_prompts.get(category, selected_template.format(topic=topic if topic else "your topic"))
else:
    final_prompt = selected_template.format(topic=topic if topic else "your topic")

st.markdown("✏️ Custom Prompt <span style='color:red'>*</span>", unsafe_allow_html=True)
custom_prompt = st.text_area("", value=final_prompt, height=180, help="This field is mandatory")
st.markdown("<br>", unsafe_allow_html=True)

# ========================
# Language Selection
# ========================
st.markdown("🌐 Select Language (optional):", unsafe_allow_html=True)
language = st.selectbox(
    "Choose the language for your LinkedIn post",
    ["English", "Hindi", "Spanish", "French", "German", "Chinese", "Tamil", "Telugu", "Malayalam"]
)

# ========================
# Advanced Options
# ========================
with st.expander("⚙️ Advanced Options"):
    model_choice = st.selectbox(
        "Choose a model (optional)",
        [
            "gpt-3.5-turbo (Recommended, low cost)",
            "gpt-3.5-turbo-16k (Long prompts)",
            "text-davinci-003 (High cost, creative)"
        ],
        index=0
    )
    model_mapping = {
        "gpt-3.5-turbo (Recommended, low cost)": "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k (Long prompts)": "gpt-3.5-turbo-16k",
        "text-davinci-003 (High cost, creative)": "text-davinci-003"
    }
    selected_model = model_mapping[model_choice]

    col1, col2 = st.columns([1,1])
    with col1:
        tone = st.slider("Tone (0=formal,1=creative)", 0.0,1.0,0.7)
    with col2:
        max_tokens = st.slider("Max tokens", 3, 800, 400)  # minimum 3 tokens

if 'selected_model' not in locals():
    selected_model = "gpt-3.5-turbo"

# ========================
# API Key Input
# ========================
user_api_key = st.text_input(
    "Enter OpenAI API key (optional for unlimited posts):",
    type="password",
    help="Optional: Provide your own key for unlimited posts"
)

api_key = user_api_key.strip() or DEFAULT_API_KEY

# ========================
# Free post limit for deployment
# ========================
if not IS_LOCAL:
    MAX_FREE_POSTS = 3
    if "posts_generated" not in st.session_state:
        st.session_state.posts_generated = 0
    if not user_api_key and st.session_state.posts_generated >= MAX_FREE_POSTS:
        st.warning(f"⚠️ Free limit reached. Enter your own OpenAI API key for unlimited posts.")
        st.stop()

# ========================
# Check API Key
# ========================
if not api_key:
    st.warning("⚠️ OpenAI API key is required to generate posts.")
    st.stop()

openai.api_key = api_key

# ========================
# Utility Functions
# ========================
def generate_post(prompt, model="gpt-3.5-turbo", tone=0.7, max_tokens=400, language="English"):
    lang_prompt = f"Write this LinkedIn post in {language}:\n{prompt}"
    if "turbo" in model:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional LinkedIn content creator."},
                {"role": "user", "content": lang_prompt}
            ],
            temperature=tone,
            max_tokens=max_tokens
        )
        return response.choices[0].message['content'].strip()
    else:
        response = openai.Completion.create(
            model=model,
            prompt=f"You are a professional LinkedIn content creator.\n{lang_prompt}",
            temperature=tone,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()

def word_count(text):
    return len(text.split())

# ========================
# Generate Post Button
# ========================
if st.button("🚀 Generate Post"):
    if not topic.strip() or not custom_prompt.strip():
        st.warning("⚠️ Please enter BOTH a topic AND a custom prompt before generating the post.")
    else:
        try:
            with st.spinner("Generating your LinkedIn post..."):
                generated_text = generate_post(
                    prompt=custom_prompt,
                    model=selected_model,
                    tone=tone,
                    max_tokens=max_tokens,
                    language=language
                )

            # Increment free post count if using default key
            if not user_api_key and not IS_LOCAL:
                st.session_state.posts_generated += 1

            wc = word_count(generated_text)
            st.markdown(f"<p style='font-size:14px; color:#555;'>Estimated word count: {wc} words</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div style="background-color:#FFFACD;padding:15px;border-radius:10px;margin-bottom:10px;">
                    <p style='font-size:18px; font-weight:bold; margin:0;'>✨ Editable LinkedIn Post Preview</p>
                </div>
                """, unsafe_allow_html=True
            )

            edited_post = st.text_area(
                "You can edit your LinkedIn post below before copying or downloading:",
                value=generated_text,
                height=300
            )

            # Buttons: Copy & Download
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button("📋 Copy Edited Post"):
                    try:
                        pyperclip.copy(edited_post)
                        st.success("✅ Your LinkedIn post has been copied to clipboard!")
                    except Exception as e:
                        st.error(f"⚠️ Failed to copy: {str(e)}")
            with col2:
                buffer = BytesIO()
                buffer.write(edited_post.encode("utf-8"))
                buffer.seek(0)
                st.download_button(
                    label="📥 Download Edited Post",
                    data=buffer,
                    file_name="linkedin_post.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"⚠️ An error occurred while generating the post:\n{str(e)}")

# ========================
# Footer
# ========================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 13px; color:#555;">
        <a href='https://www.linkedin.com/in/sachin-aditiya-b-7691b314b/' target='_blank' 
           style="color:#0A66C2; text-decoration:none; font-weight:500;">
           Connect with me on LinkedIn
        </a><br>
        Made with ❤️ by Sachin Aditiya B | Powered by OpenAI
    </div>
    """,
    unsafe_allow_html=True
)
