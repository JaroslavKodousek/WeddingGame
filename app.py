import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Svatební Hra",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Read the HTML file
with open('game.html', 'r', encoding='utf-8') as file:
    html_code = file.read()

custom_css = """
<style>
    /* Background color for the app */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Title styling */
    h1 {
        font-family: 'Playfair Display', serif;
        color: #D8A9A4 !important;
        text-align: center;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        font-size: 14px;
        color: #6c757d;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #dee2e6;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        font-size: 18px;
        color: #4a5043;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #dee2e6;
    }
    
    /* Emoticon styling */
    .emoticons {
        text-align: center;
        font-size: 24px;
        margin: 10px 0;
    }
    
    /* Decoration styling - for the emoticons */
    .decoration {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-size: 28px;
        padding: 15px 0;
        width: 100%;
        margin: 10px auto;
    }
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Header with decorative elements
st.markdown('<div class="decoration">💍 💝 🕊️</div>', unsafe_allow_html=True)

st.title("Hra pro svatební web")

st.markdown('<div class="game-container">', unsafe_allow_html=True)
components.html(html_code, height=600, scrolling=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with decorative elements
st.markdown('<div class="decoration">🥂 💐 ❤️</div>', unsafe_allow_html=True)