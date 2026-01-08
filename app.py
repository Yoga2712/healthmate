import streamlit as st
import time
from datetime import datetime
import base64
from pathlib import Path

# Page config
st.set_page_config(
    page_title="HealthMate",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to load and encode image as base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Custom CSS - USER & EMERGENCY BUTTONS REMOVED
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* ==================== ANIMATIONS ==================== */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInUp {
        from {
            transform: translateY(30px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-30px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes heartbeat {
        0%, 100% {
            transform: scale(1);
        }
        25% {
            transform: scale(1.1);
        }
        50% {
            transform: scale(1);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* ==================== RESPONSIVE DESIGN ==================== */
    
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    @media screen and (max-width: 1024px) {
        .main .block-container {
            padding: 1rem 1.5rem;
            max-width: 900px;
        }
        
        .card {
            padding: 1.5rem !important;
        }
        
        .main-header {
            font-size: 2rem !important;
        }
        
        .sub-header {
            font-size: 1rem !important;
        }
        
        .stButton > button {
            font-size: 0.95rem !important;
            padding: 0.7rem 1.5rem !important;
        }
    }
    
    @media screen and (max-width: 767px) {
        .main .block-container {
            padding: 0.5rem 1rem !important;
        }
        
        .card {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border-radius: 15px !important;
        }
        
        .main-header {
            font-size: 1.5rem !important;
        }
        
        .sub-header {
            font-size: 0.9rem !important;
        }
        
        .healthmate-centered {
            font-size: 1.3rem !important;
            padding: 1rem 0 !important;
        }
        
        .profile-avatar {
            width: 80px !important;
            height: 80px !important;
            font-size: 2.5rem !important;
        }
        
        .icon-circle {
            width: 50px !important;
            height: 50px !important;
        }
        
        .stButton > button {
            font-size: 0.9rem !important;
            padding: 0.75rem 1.2rem !important;
            min-height: 48px !important;
        }
        
        .emergency-icon {
            font-size: 3.5rem !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        div[data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
        }
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .stApp {
        background: transparent !important;
        animation: fadeIn 0.5s ease-in;
    }
    
    .main .block-container {
        background: transparent !important;
        backdrop-filter: none;
    }
    
    .top-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .right-buttons {
        display: flex;
        gap: 2px;
        align-items: center;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0D47A1;
        animation: slideInLeft 0.6s ease-out;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #1976D2;
        font-weight: normal;
        font-style: normal;
        animation: slideInLeft 0.7s ease-out;
        margin-top: 0.5rem;
    }
    
    .card {
        padding: 2rem;
        border-radius: 25px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(13, 71, 161, 0.15);
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: slideInUp 0.6s ease-out;
        border: 2px solid #0D47A1;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(13, 71, 161, 0.2);
        background: rgba(255, 255, 255, 0.92);
        border-color: #01579B;
    }
    
    .healthmate-centered {
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        font-style: italic;
        color: #0D47A1;
        padding: 1.5rem 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .healthmate-box {
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        font-style: italic;
        color: #0D47A1;
        padding: 1.5rem 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 80px;
    }
    
    .profile-separator {
        width: 100%;
        height: 2px;
        background: linear-gradient(to right, transparent, #0D47A1, transparent);
        margin: 1.5rem 0;
    }
    
    .caregiver-card {
        background: rgba(227, 242, 253, 0.7);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        animation: slideInUp 0.5s ease-out;
        transition: all 0.3s ease;
        border: 1px solid rgba(13, 71, 161, 0.15);
    }
    
    .caregiver-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(13, 71, 161, 0.2);
        background: rgba(227, 242, 253, 0.85);
    }
    
    .icon-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .icon-circle-blue {
        background: linear-gradient(135deg, #E3F2FD 0%, #90CAF9 100%);
        color: #0D47A1;
    }
    
    .icon-circle-lightblue {
        background: linear-gradient(135deg, #B3E5FC 0%, #81D4FA 100%);
        color: #01579B;
    }
    
    .profile-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: white;
        font-weight: bold;
        margin-bottom: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .fa-icon {
        font-size: 1.5rem;
    }
    
    .fa-icon-large {
        font-size: 2rem;
    }
    
    .emergency-icon {
        font-size: 5rem;
        color: white;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    /* ==================== UNIFIED SUBMIT BUTTON STYLE ==================== */
    
    .stButton > button,
    .stForm button[type="submit"],
    button[kind="primary"] {
        all: unset !important;
        box-sizing: border-box !important;
        
        background: linear-gradient(135deg, #0D47A1 0%, #01579B 100%) !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        
        font-size: 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 3px 12px rgba(13, 71, 161, 0.3) !important;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        margin: 0 auto !important;
        width: 100% !important;
        min-height: 48px !important;
        
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        
        text-transform: none !important;
        letter-spacing: 0.3px !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }
    
    .stButton > button:hover,
    .stForm button[type="submit"]:hover,
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 18px rgba(13, 71, 161, 0.4) !important;
    }
    
    .stButton,
    div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* USER & EMERGENCY BUTTON CSS REMOVED */
    
    @media screen and (max-width: 767px) {
        .stButton > button,
        .stForm button[type="submit"],
        button[kind="primary"] {
            padding: 0.85rem 1.2rem !important;
            font-size: 0.95rem !important;
            min-height: 52px !important;
        }
    }
    
    /* ==================== EMERGENCY PAGE BUTTONS ==================== */
    
    .stButton > button[key="call_108_btn"] {
        background: white !important;
        color: #FF4444 !important;
        border: 2px solid white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 0.9rem 2rem !important;
    }
    
    .stButton > button[key="call_108_btn"]:hover {
        background: #f8f8f8 !important;
        color: #FF2222 !important;
        transform: translateY(-3px) !important;
    }
    
    .stButton > button[key="close_emergency"] {
        background: white !important;
        color: #555 !important;
        border: 2px solid white !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 0.9rem !important;
        min-height: 40px !important;
        width: auto !important;
    }
    
    /* ==================== ALERT & NOTIFICATION ==================== */
    
    .stAlert {
        background: white !important;
        border: 2px solid white !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stAlert p, 
    .stAlert div,
    .stAlert > div {
        color: black !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
    }
    
    .stAlert > div > div {
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    /* POSITION FIXED NAV BUTTONS - USER & EMERGENCY REMOVED */
    
    div[data-testid="column"]:has(button[key="back_chat"]),
    div[data-testid="column"]:has(button[key="back_profile"]),
    div[data-testid="column"]:has(button[key="back_edit"]) {
        position: fixed;
        top: 15px;
        right: 130px;
        z-index: 1001;
    }
    
    div[data-testid="column"]:has(button[key="home_chat"]),
    div[data-testid="column"]:has(button[key="home_profile"]),
    div[data-testid="column"]:has(button[key="home_edit"]) {
        position: fixed;
        top: 15px;
        right: 30px;
        z-index: 1001;
    }
    
    .edit-form-label {
        font-weight: 600;
        color: #0D47A1;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .login-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(rgba(13, 71, 161, 0.7), rgba(1, 87, 155, 0.7)),
                    url('https://images.unsplash.com/photo-5194940268928-80bbd2d6fd0d?w=1920');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        z-index: -1;
        animation: fadeIn 1s ease-in;
    }
    
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        animation: slideInUp 0.8s ease-out;
    }
    
    .login-header {
        text-align: center;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, #0D47A1 0%, #01579B 100%);
        border-radius: 25px;
        animation: shimmer 3s linear infinite;
        background-size: 1000px 100%;
        background-image: linear-gradient(
            90deg,
            #0D47A1 0%,
            #1565C0 50%,
            #0D47A1 100%
        );
    }
    
    .heartbeat-icon {
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: white !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    .chat-message {
        animation: slideInUp 0.4s ease-out;
        border-radius: 15px;
    }
    
    .block-container {
        padding-top: 5rem !important;
        padding-bottom: 1rem !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(13, 71, 161, 0.2) !important;
    }
    
    .stMarkdown {
        color: #0D47A1;
    }
    
    .top-spacer {
        height: 80px;
    }
    
    .timer-display {
        background: rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': 'Alex Thompson',
        'email': 'alex@example.com',
        'phone': '+1234-567-890',
        'blood_type': 'O+',
        'age': 28
    }
if 'caregivers' not in st.session_state:
    st.session_state.caregivers = [
        {
            'name': 'Sarah Thompson',
            'relation': 'Spouse',
            'phone': '+1555-0123',
            'email': 'sarah.t@example.com'
        }
    ]
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

# ==================== BACKGROUND ====================
def set_background():
    bg_image = get_base64_image('istockphoto-1327568875-1024x1024.jpg')
    if bg_image:
        st.markdown(f"""
        <style>
            .stApp {{
                background: url('data:image/jpeg;base64,{bg_image}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                background-repeat: no-repeat;
            }}
            
            .stApp::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.88);
                z-index: -1;
            }}
        </style>
        """, unsafe_allow_html=True)

# ==================== NAVIGATION - USER & EMERGENCY BUTTONS REMOVED ====================
def top_navigation():
    """Top navigation bar - User & Emergency buttons removed"""
    st.markdown(f"""
    <div class='top-nav'>
        <div style='display: flex; align-items: center;'>
            <i class="fas fa-heartbeat" style="font-size: 2rem; color: #0D47A1; margin-right: 15px;"></i>
            <h2 style='margin: 0; color: #0D47A1; font-weight: bold;'>HealthMate</h2>
        </div>
    </div>
    <div class='top-spacer'></div>
    """, unsafe_allow_html=True)

def page_navigation():
    """Back and Home navigation for other pages"""
    col1, col2, col3 = st.columns([10, 1, 1])
    
    with col2:
        if st.button("Back", key=f"back_{st.session_state.current_page}"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col3:
        if st.button("Home", key=f"home_{st.session_state.current_page}"):
            st.session_state.current_page = 'dashboard'
            st.rerun()

# ==================== PAGES ====================
def login_page():
    st.markdown("""
    <div class='login-background'></div>
    <style>
        .stApp {
            background: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='login-card'>
            <div class='login-header'>
                <i class="fas fa-heartbeat heartbeat-icon" style="font-size: 3.5rem; color: white;"></i>
                <h1 style='color: white; margin: 0.5rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>HealthMate</h1>
                <p style='color: white; font-size: 1.2rem; margin: 0;'>Your Health, Reimagined</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            tab1, tab2 = st.tabs(["Log In", "Sign Up"])
            
            with tab1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem;"><i class="fas fa-envelope"></i> EMAIL ADDRESS</p>', unsafe_allow_html=True)
                email = st.text_input("Email", placeholder="name@example.com", key="login_email", label_visibility="collapsed")
                
                st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;"><i class="fas fa-lock"></i> PASSWORD</p>', unsafe_allow_html=True)
                password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password", label_visibility="collapsed")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Log In", use_container_width=True, type="primary"):
                    if email and password:
                        st.session_state.authenticated = True
                        st.session_state.current_page = 'dashboard'
                        st.rerun()
                    else:
                        st.error("Please enter valid credentials")
            
            with tab2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem;"><i class="fas fa-user"></i> FULL NAME</p>', unsafe_allow_html=True)
                new_name = st.text_input("Name", placeholder="Enter your name", label_visibility="collapsed")
                
                st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;"><i class="fas fa-envelope"></i> EMAIL ADDRESS</p>', unsafe_allow_html=True)
                new_email = st.text_input("Email2", placeholder="name@example.com", key="signup_email", label_visibility="collapsed")
                
                st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;"><i class="fas fa-lock"></i> PASSWORD</p>', unsafe_allow_html=True)
                new_password = st.text_input("Pass", type="password", placeholder="••••••••", key="signup_password", label_visibility="collapsed")
                
                st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;"><i class="fas fa-lock"></i> CONFIRM PASSWORD</p>', unsafe_allow_html=True)
                confirm_password = st.text_input("ConfPass", type="password", placeholder="••••••••", label_visibility="collapsed")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Create Account", use_container_width=True, type="primary"):
                    if new_email and new_password and new_password == confirm_password:
                        st.session_state.user_data['name'] = new_name if new_name else 'User'
                        st.session_state.user_data['email'] = new_email
                        st.session_state.authenticated = True
                        st.session_state.current_page = 'dashboard'
                        st.rerun()
                    else:
                        st.error("Please fill all fields correctly")
        
        st.markdown("</div>", unsafe_allow_html=True)

def dashboard_page():
    set_background()
    top_navigation()
    
    first_name = st.session_state.user_data['name'].split()[0]
    st.markdown(f"<h1 class='main-header'>Hello, {first_name}</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Manage your wellness in real-time.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class='card' style='min-height: 250px;'>
                <div style='text-align: center; margin-bottom: 1rem;'>
                    <div class='icon-circle icon-circle-blue'>
                        <i class="fas fa-heart fa-icon-large"></i>
                    </div>
                </div>
                <h2 style='text-align: center; margin-bottom: 0.5rem; color: #0D47A1;'>General Queries</h2>
                <p style='text-align: center; color: #1976D2; margin-bottom: 1.5rem;'>Daily health & Wellness</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ENTER CONSULTATION", key="general_query", use_container_width=True):
                st.session_state.current_page = 'chatbot'
                st.session_state.chat_type = 'general'
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            <div class='card' style='min-height: 250px;'>
                <div style='text-align: center; margin-bottom: 1rem;'>
                    <div class='icon-circle icon-circle-lightblue'>
                        <i class="fas fa-chart-line fa-icon-large"></i>
                    </div>
                </div>
                <h2 style='text-align: center; margin-bottom: 0.5rem; color: #01579B;'>Symptom Triage</h2>
                <p style='text-align: center; color: #1976D2; margin-bottom: 1.5rem;'>Medical assessment</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ENTER CONSULTATION", key="symptom_triage", use_container_width=True):
                st.session_state.current_page = 'chatbot'
                st.session_state.chat_type = 'triage'
                st.rerun()

def chatbot_page():
    set_background()
    page_navigation()
    
    st.markdown("""
    <div class='card' style='min-height: 80px; padding: 0;'>
        <div class='healthmate-centered'>HealthMate</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div class='chat-message' style='background: rgba(227, 242, 253, 0.7); 
                 padding: 1.5rem; border-radius: 20px; margin: 1rem 0; backdrop-filter: blur(10px);'>
                <i class="fas fa-robot" style="color: #0D47A1; font-size: 1.5rem;"></i>
                <strong> Hi! I'm your HealthMate assistant. How can I help you today?</strong>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class='chat-message' style='background: rgba(245, 245, 245, 0.8); padding: 1rem; border-radius: 20px; margin: 0.5rem 0; backdrop-filter: blur(10px);'>
                    <i class="fas fa-user" style="color: #0D47A1;"></i>
                    <strong> You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='chat-message' style='background: rgba(227, 242, 253, 0.7); 
                     padding: 1rem; border-radius: 20px; margin: 0.5rem 0; backdrop-filter: blur(10px);'>
                    <i class="fas fa-robot" style="color: #0D47A1;"></i>
                    <strong> HealthMate:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([9, 1])
        with col1:
            user_input = st.text_input("Type your health details...", label_visibility="collapsed", 
                                      placeholder="Type your health details...")
        with col2:
            submit = st.form_submit_button("Send")
        
        if submit and user_input:
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            text = user_input.lower()
            if 'fever' in text or 'cold' in text:
                response = ("I understand you're experiencing cold/fever symptoms. "
                            "Please rest, stay hydrated, and monitor your temperature. "
                            "If symptoms persist for more than 3 days or worsen, please consult a doctor.")
            elif 'headache' in text:
                response = ("Headaches can have various causes. Try resting in a quiet, dark room and stay hydrated. "
                            "If severe or persistent, please seek medical attention.")
            else:
                response = ("Thank you for sharing. I recommend consulting with a healthcare professional for proper "
                            "diagnosis and treatment. Would you like me to help you find nearby clinics?")
            
            st.session_state.chat_history.append({'role': 'bot', 'content': response})
            st.rerun()

def edit_profile_page():
    set_background()
    page_navigation()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        user_initial = st.session_state.user_data['name'][0] if st.session_state.user_data['name'] else 'U'
        st.markdown(f"""
        <div style='text-align: center;'>
            <div class='profile-avatar'>
                {user_initial}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #0D47A1;'>User Details</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card' style='min-height: 80px; padding: 0;'>
            <div class='healthmate-box'>HealthMate</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        with st.form("edit_profile_form"):
            st.markdown("<p class='edit-form-label'>FULL NAME</p>", unsafe_allow_html=True)
            new_name = st.text_input(
                "Full Name",
                value=st.session_state.user_data['name'],
                placeholder="Enter your full name",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p class='edit-form-label'>EMAIL ADDRESS</p>", unsafe_allow_html=True)
            new_email = st.text_input(
                "Email",
                value=st.session_state.user_data['email'],
                placeholder="Enter your email",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_blood, col_age = st.columns(2)
            
            with col_blood:
                st.markdown("<p class='edit-form-label'>BLOOD TYPE</p>", unsafe_allow_html=True)
                blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                current_blood_type = st.session_state.user_data['blood_type']
                blood_type_index = blood_types.index(current_blood_type) if current_blood_type in blood_types else 6
                new_blood_type = st.selectbox(
                    "Blood Type",
                    options=blood_types,
                    index=blood_type_index,
                    label_visibility="collapsed"
                )
            
            with col_age:
                st.markdown("<p class='edit-form-label'>AGE</p>", unsafe_allow_html=True)
                new_age = st.number_input(
                    "Age",
                    min_value=1,
                    max_value=120,
                    value=st.session_state.user_data['age'],
                    step=1,
                    label_visibility="collapsed"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p class='edit-form-label'>PHONE NUMBER</p>", unsafe_allow_html=True)
            new_phone = st.text_input(
                "Phone",
                value=st.session_state.user_data['phone'],
                placeholder="Enter your phone number",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_save, col_cancel = st.columns(2)
            
            with col_save:
                submit = st.form_submit_button("Save Changes", use_container_width=True, type="primary")
            
            with col_cancel:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit:
                if new_name and new_email and new_phone:
                    st.session_state.user_data['name'] = new_name
                    st.session_state.user_data['email'] = new_email
                    st.session_state.user_data['blood_type'] = new_blood_type
                    st.session_state.user_data['age'] = new_age
                    st.session_state.user_data['phone'] = new_phone
                    
                    st.success("Profile updated successfully!")
                    time.sleep(1)
                    st.session_state.current_page = 'profile'
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")
            
            if cancel:
                st.session_state.current_page = 'profile'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def profile_page():
    set_background()
    page_navigation()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col2:
            user_initial = st.session_state.user_data['name'][0]
            st.markdown(f"""
            <div style='text-align: center;'>
                <div class='profile-avatar'>
                    {user_initial}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #0D47A1;'>User Details</h2>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='card' style='min-height: 80px; padding: 0;'>
                <div class='healthmate-box'>HealthMate</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_name, col_blood = st.columns(2)
            with col_name:
                st.markdown("**NAME**")
                st.markdown(f"### {st.session_state.user_data['name']}")
            with col_blood:
                st.markdown("**BLOOD TYPE**")
                st.markdown(f"### {st.session_state.user_data['blood_type']}")
            
            st.markdown('<div class="profile-separator"></div>', unsafe_allow_html=True)
            
            col_phone, col_age = st.columns(2)
            with col_phone:
                st.markdown("**PHONE**")
                st.markdown(f"### {st.session_state.user_data['phone']}")
            with col_age:
                st.markdown("**AGE**")
                st.markdown(f"### {st.session_state.user_data['age']} Years")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                if st.button("Edit Details", key="edit_details_btn", use_container_width=True):
                    st.session_state.current_page = 'edit_profile'
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h3><i class="fas fa-user-friends" style="color: #0D47A1;"></i> Caregivers</h3>', 
                   unsafe_allow_html=True)
    with col2:
        if st.button("Add New", key="add_caregiver_btn", use_container_width=True):
            st.session_state.adding_caregiver = True
    
    for idx, caregiver in enumerate(st.session_state.caregivers):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"""
            <div class='caregiver-card'>
                <h3 style='margin: 0; color: #0D47A1;'>
                    <i class="fas fa-user" style="color: #1976D2;"></i> {caregiver['name']}
                </h3>
                <div class='profile-separator' style='margin: 0.8rem 0;'></div>
                <p style='color: #0D47A1; margin: 0.5rem 0;'>
                    <i class="fas fa-heart" style="font-size: 0.9rem;"></i> {caregiver['relation']}
                </p>
                <p style='margin: 0.25rem 0; color: #0D47A1;'>
                    <i class="fas fa-phone"></i> {caregiver['phone']}
                </p>
                <p style='margin: 0.25rem 0; color: #0D47A1;'>
                    <i class="fas fa-envelope"></i> {caregiver['email']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Delete", key=f"delete_{idx}"):
                st.session_state.caregivers.pop(idx)
                st.rerun()
    
    if 'adding_caregiver' in st.session_state and st.session_state.adding_caregiver:
        st.markdown('<h3><i class="fas fa-user-plus" style="color: #0D47A1;"></i> New Caregiver Profile</h3>', 
                   unsafe_allow_html=True)
        with st.form("caregiver_form"):
            name = st.text_input("NAME", placeholder="Enter caregiver name...")
            relation = st.text_input("RELATION", placeholder="Enter caregiver relation...")
            phone = st.text_input("PHONE", placeholder="Enter caregiver phone...")
            email = st.text_input("EMAIL", placeholder="Enter caregiver email...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save Caregiver", use_container_width=True):
                    if name and relation and phone and email:
                        st.session_state.caregivers.append({
                            'name': name,
                            'relation': relation,
                            'phone': phone,
                            'email': email
                        })
                        st.session_state.adding_caregiver = False
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.adding_caregiver = False
                    st.rerun()

def emergency_page():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #FF4444 0%, #CC0000 100%) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([8, 1, 1])
    with col3:
        if st.button("Close", key="close_emergency"):
            st.session_state.current_page = 'dashboard'
            st.session_state.timer_running = False
            st.session_state.timer_start = None
            st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: white;'>
            <i class="fas fa-shield-alt emergency-icon"></i>
            <h1 style='color: white; font-size: 3rem; margin: 1rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>EMERGENCY</h1>
            <p style='font-size: 1.3rem; margin: 1rem 0;'>Contact medical professionals now.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # COUNTDOWN TIMER
        if st.session_state.timer_running and st.session_state.timer_start:
            elapsed = int(time.time() - st.session_state.timer_start)
            remaining = max(300 - elapsed, 0)
            
            mins = remaining // 60
            secs = remaining % 60
            timer_text = f"{mins}:{secs:02d}"
            timer_label = "TIME REMAINING"
            
            if remaining == 0:
                st.session_state.timer_running = False
        else:
            timer_text = "5:00"
            timer_label = "READY"
        
        timer_placeholder = st.empty()
        
        timer_placeholder.markdown(f"""
        <div class='timer-display'>
            <p style='color: white; margin: 0; opacity: 0.9; font-size: 1.1rem;'>
                <i class="fas fa-clock"></i> {timer_label}
            </p>
            <h1 style='color: white; font-size: 4rem; margin: 1rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{timer_text}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.timer_running:
            time.sleep(1)
            st.rerun()
        
        if st.button("CALL 108", key="call_108_btn", use_container_width=True):
            if not st.session_state.timer_running:
                st.session_state.timer_running = True
                st.session_state.timer_start = time.time()
            st.success("✅ Calling emergency services... (108)")
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("NOTIFY CAREGIVER", key="notify_btn", use_container_width=True):
            if st.session_state.caregivers:
                caregiver_names = [cg['name'] for cg in st.session_state.caregivers]
                names_list = ', '.join(caregiver_names)
                st.success(f"✅ Caregiver has been notified: {names_list}")
                st.info("📧 Emergency notification sent successfully!")
            else:
                st.warning("⚠️ No caregivers found. Please add caregivers in your profile.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("BACK TO HOME", key="back_to_home_btn", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.session_state.timer_running = False
            st.session_state.timer_start = None
            st.rerun()

# ==================== MAIN ====================
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        if st.session_state.current_page == 'dashboard':
            dashboard_page()
        elif st.session_state.current_page == 'chatbot':
            chatbot_page()
        elif st.session_state.current_page == 'profile':
            profile_page()
        elif st.session_state.current_page == 'edit_profile':
            edit_profile_page()
        elif st.session_state.current_page == 'emergency':
            emergency_page()

if __name__ == "__main__":
    main()
