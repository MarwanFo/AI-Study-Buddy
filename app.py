"""
AI Study Buddy - Complete UI Redesign
Design Direction: "Cozy Study Cafe" - Warm, inviting, perfect for long study sessions

Typography: DM Sans (headings) + Inter (body) + JetBrains Mono (code)
Palette: Warm neutrals with terracotta accent
"""

import streamlit as st
from datetime import datetime
from config import check_ollama_available, check_ollama_models
from rag_engine import RAGEngine
from document_processor import get_supported_formats

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Study Buddy",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN SYSTEM - COMPLETE CUSTOM CSS
# ============================================================
# 
# COLOR PALETTE (Cozy Study Cafe)
# --------------------------------
# --bg-primary: #FAF8F5      Warm off-white (like aged paper)
# --bg-secondary: #F3EDE7    Slightly darker warm cream
# --bg-tertiary: #EBE3DA     Card backgrounds
# --surface: #FFFFFF         Pure white for inputs
# --border: #E2D9CD          Warm gray border
# --border-light: #EFE9E1    Subtle borders
# 
# --text-primary: #2D2A26    Warm black (not pure black)
# --text-secondary: #6B6560  Muted text
# --text-tertiary: #9C9590   Placeholder text
# 
# --accent: #C45D3E          Terracotta (warm, earthy)
# --accent-hover: #A84E32    Darker terracotta
# --accent-light: #FDF3F0    Very light terracotta tint
# 
# --success: #5B8A5F         Muted sage green
# --warning: #D4A254         Warm amber
# --error: #C45D3E           Uses accent
# 
# TYPOGRAPHY
# ----------
# Headings: DM Sans (friendly, modern)
# Body: Inter (excellent readability)
# Mono: JetBrains Mono (for code/technical)
# ============================================================

st.markdown("""
<style>
    /* ========================================
       FONT IMPORTS
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* ========================================
       CSS VARIABLES (Design Tokens)
       ======================================== */
    :root {
        /* Backgrounds */
        --bg-primary: #FAF8F5;
        --bg-secondary: #F3EDE7;
        --bg-tertiary: #EBE3DA;
        --surface: #FFFFFF;
        
        /* Borders */
        --border: #E2D9CD;
        --border-light: #EFE9E1;
        --border-focus: #C45D3E;
        
        /* Text */
        --text-primary: #2D2A26;
        --text-secondary: #6B6560;
        --text-tertiary: #9C9590;
        --text-inverse: #FAF8F5;
        
        /* Accent (Terracotta) */
        --accent: #C45D3E;
        --accent-hover: #A84E32;
        --accent-light: #FDF3F0;
        --accent-muted: #E8D4CE;
        
        /* Semantic */
        --success: #5B8A5F;
        --success-light: #F0F5F0;
        --warning: #D4A254;
        --warning-light: #FEF9F0;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px rgba(45, 42, 38, 0.04);
        --shadow-md: 0 4px 12px rgba(45, 42, 38, 0.08);
        --shadow-lg: 0 8px 24px rgba(45, 42, 38, 0.12);
        --shadow-glow: 0 0 0 3px rgba(196, 93, 62, 0.15);
        
        /* Typography */
        --font-heading: 'DM Sans', -apple-system, sans-serif;
        --font-body: 'Inter', -apple-system, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
        
        /* Spacing */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 32px;
        --space-2xl: 48px;
        
        /* Radius */
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 14px;
        --radius-xl: 20px;
        --radius-full: 9999px;
        
        /* Transitions */
        --transition-fast: 150ms ease;
        --transition-normal: 250ms ease;
        --transition-slow: 350ms ease;
    }
    
    /* ========================================
       GLOBAL RESETS & BASE STYLES
       ======================================== */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: var(--font-body) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    
    /* Smooth scrolling */
    html {scroll-behavior: smooth;}
    
    /* ========================================
       TYPOGRAPHY
       ======================================== */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: var(--font-heading) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        letter-spacing: -0.02em !important;
    }
    
    p, span, div, label {
        font-family: var(--font-body) !important;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    code, .stCode, pre {
        font-family: var(--font-mono) !important;
    }
    
    /* ========================================
       SIDEBAR STYLING
       ======================================== */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-light) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: var(--space-lg) !important;
    }
    
    /* Sidebar section headers */
    .sidebar-header {
        font-family: var(--font-heading);
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-tertiary);
        margin-bottom: var(--space-md);
        padding-left: 2px;
    }
    
    /* ========================================
       CUSTOM CARDS
       ======================================== */
    .card {
        background: var(--surface);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-normal);
    }
    
    .card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--border);
    }
    
    /* Document card */
    .doc-card {
        background: var(--surface);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        padding: var(--space-md) var(--space-lg);
        margin-bottom: var(--space-sm);
        display: flex;
        align-items: center;
        gap: var(--space-md);
        transition: all var(--transition-fast);
        cursor: pointer;
    }
    
    .doc-card:hover {
        background: var(--bg-tertiary);
        transform: translateX(4px);
    }
    
    .doc-icon {
        width: 36px;
        height: 36px;
        background: var(--accent-light);
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }
    
    .doc-info {
        flex: 1;
        min-width: 0;
    }
    
    .doc-name {
        font-family: var(--font-heading);
        font-weight: 500;
        font-size: 14px;
        color: var(--text-primary);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .doc-meta {
        font-size: 12px;
        color: var(--text-tertiary);
        margin-top: 2px;
    }
    
    /* ========================================
       HERO HEADER
       ======================================== */
    .hero {
        text-align: center;
        padding: var(--space-xl) 0 var(--space-lg);
        border-bottom: 1px solid var(--border-light);
        margin-bottom: var(--space-xl);
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        margin: -1rem -1rem var(--space-xl) -1rem;
        padding: var(--space-2xl) var(--space-xl);
    }
    
    .hero-title {
        font-family: var(--font-heading);
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: var(--space-sm);
        letter-spacing: -0.03em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        font-weight: 400;
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* ========================================
       UPLOAD AREA
       ======================================== */
    .upload-zone {
        background: var(--surface);
        border: 2px dashed var(--border);
        border-radius: var(--radius-xl);
        padding: var(--space-2xl);
        text-align: center;
        transition: all var(--transition-normal);
        cursor: pointer;
    }
    
    .upload-zone:hover {
        border-color: var(--accent);
        background: var(--accent-light);
    }
    
    .upload-icon {
        font-size: 48px;
        margin-bottom: var(--space-md);
        opacity: 0.6;
    }
    
    .upload-title {
        font-family: var(--font-heading);
        font-size: 18px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--space-xs);
    }
    
    .upload-hint {
        font-size: 14px;
        color: var(--text-tertiary);
    }
    
    /* Streamlit file uploader override */
    [data-testid="stFileUploader"] {
        background: var(--surface) !important;
        border: 2px dashed var(--border) !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--space-xl) !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent) !important;
        background: var(--accent-light) !important;
    }
    
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: var(--accent) !important;
        color: var(--text-inverse) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-sm) var(--space-lg) !important;
        font-family: var(--font-heading) !important;
        font-weight: 500 !important;
        transition: all var(--transition-fast) !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: var(--accent-hover) !important;
        transform: translateY(-1px) !important;
    }
    
    /* ========================================
       CHAT MESSAGES
       ======================================== */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* User message */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: var(--space-lg);
        animation: slideInRight 0.3s ease;
    }
    
    .user-bubble {
        background: var(--accent);
        color: var(--text-inverse);
        padding: var(--space-md) var(--space-lg);
        border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg);
        max-width: 70%;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: var(--shadow-sm);
    }
    
    /* Assistant message */
    .assistant-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: var(--space-lg);
        animation: slideInLeft 0.3s ease;
    }
    
    .assistant-bubble {
        background: var(--surface);
        color: var(--text-primary);
        padding: var(--space-lg);
        border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm);
        max-width: 80%;
        font-size: 15px;
        line-height: 1.6;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
    }
    
    .assistant-avatar {
        width: 32px;
        height: 32px;
        background: var(--accent-light);
        border-radius: var(--radius-full);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: var(--space-md);
        flex-shrink: 0;
        font-size: 16px;
    }
    
    /* Message timestamp */
    .msg-time {
        font-size: 11px;
        color: var(--text-tertiary);
        margin-top: var(--space-xs);
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* ========================================
       SOURCES / CITATIONS
       ======================================== */
    .sources-container {
        margin-top: var(--space-md);
        padding-top: var(--space-md);
        border-top: 1px solid var(--border-light);
    }
    
    .sources-header {
        font-family: var(--font-heading);
        font-size: 12px;
        font-weight: 600;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--space-sm);
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }
    
    .sources-header:hover {
        color: var(--text-secondary);
    }
    
    .source-card {
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
        padding: var(--space-md);
        margin-top: var(--space-sm);
        font-size: 13px;
        line-height: 1.5;
    }
    
    .source-meta {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        margin-bottom: var(--space-sm);
    }
    
    .source-badge {
        font-size: 11px;
        font-weight: 500;
        padding: 2px 8px;
        border-radius: var(--radius-full);
        background: var(--accent-muted);
        color: var(--accent);
    }
    
    .source-text {
        color: var(--text-secondary);
        font-size: 13px;
    }
    
    /* ========================================
       INPUT AREA
       ======================================== */
    .stChatInput {
        border-top: 1px solid var(--border-light) !important;
        padding-top: var(--space-lg) !important;
        background: var(--bg-primary) !important;
    }
    
    .stChatInput > div {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--space-sm) !important;
        box-shadow: var(--shadow-md) !important;
        transition: all var(--transition-fast) !important;
    }
    
    .stChatInput > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: var(--shadow-glow), var(--shadow-md) !important;
    }
    
    .stChatInput textarea {
        font-family: var(--font-body) !important;
        font-size: 15px !important;
        color: var(--text-primary) !important;
        background: transparent !important;
        border: none !important;
    }
    
    .stChatInput textarea::placeholder {
        color: var(--text-tertiary) !important;
    }
    
    .stChatInput button {
        background: var(--accent) !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition-fast) !important;
    }
    
    .stChatInput button:hover {
        background: var(--accent-hover) !important;
        transform: scale(1.05) !important;
    }
    
    /* ========================================
       BUTTONS
       ======================================== */
    .stButton > button {
        font-family: var(--font-heading) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-sm) var(--space-lg) !important;
        transition: all var(--transition-fast) !important;
        border: none !important;
    }
    
    /* Primary button */
    .stButton > button[kind="primary"],
    .stButton > button:not([kind]) {
        background: var(--accent) !important;
        color: var(--text-inverse) !important;
    }
    
    .stButton > button[kind="primary"]:hover,
    .stButton > button:not([kind]):hover {
        background: var(--accent-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: var(--surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: var(--bg-secondary) !important;
        border-color: var(--accent) !important;
    }
    
    /* Icon buttons (small) */
    .icon-btn {
        background: transparent !important;
        padding: var(--space-sm) !important;
        min-width: 36px !important;
        min-height: 36px !important;
        border-radius: var(--radius-md) !important;
    }
    
    .icon-btn:hover {
        background: var(--bg-tertiary) !important;
    }
    
    /* ========================================
       BADGES & PILLS
       ======================================== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: var(--radius-full);
    }
    
    .badge-accent {
        background: var(--accent-light);
        color: var(--accent);
    }
    
    .badge-success {
        background: var(--success-light);
        color: var(--success);
    }
    
    .badge-muted {
        background: var(--bg-tertiary);
        color: var(--text-secondary);
    }
    
    .format-pill {
        font-size: 10px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: var(--radius-sm);
        background: var(--accent-muted);
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    /* ========================================
       STATS CARDS
       ======================================== */
    .stat-row {
        display: flex;
        gap: var(--space-md);
        margin-bottom: var(--space-lg);
    }
    
    .stat-card {
        flex: 1;
        background: var(--surface);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        padding: var(--space-md);
        text-align: center;
    }
    
    .stat-value {
        font-family: var(--font-heading);
        font-size: 24px;
        font-weight: 700;
        color: var(--accent);
        line-height: 1;
    }
    
    .stat-label {
        font-size: 11px;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: var(--space-xs);
    }
    
    /* ========================================
       STATUS INDICATORS
       ======================================== */
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: var(--radius-full);
        display: inline-block;
        margin-right: var(--space-sm);
    }
    
    .status-online {
        background: var(--success);
        box-shadow: 0 0 0 3px var(--success-light);
    }
    
    .status-offline {
        background: var(--error);
        box-shadow: 0 0 0 3px var(--accent-light);
    }
    
    /* ========================================
       EXPANDER STYLING
       ======================================== */
    .stExpander {
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        background: var(--surface) !important;
    }
    
    .stExpander > div:first-child {
        background: transparent !important;
        padding: var(--space-md) !important;
    }
    
    .stExpander > div:first-child:hover {
        background: var(--bg-secondary) !important;
    }
    
    /* ========================================
       SPINNER / LOADING
       ======================================== */
    .stSpinner > div {
        border-color: var(--accent) transparent transparent !important;
    }
    
    /* Custom thinking indicator */
    .thinking {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-md);
        color: var(--text-secondary);
    }
    
    .thinking-dots span {
        width: 6px;
        height: 6px;
        background: var(--accent);
        border-radius: var(--radius-full);
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .thinking-dots span:nth-child(1) { animation-delay: -0.32s; }
    .thinking-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    /* ========================================
       EMPTY STATE
       ======================================== */
    .empty-state {
        text-align: center;
        padding: var(--space-2xl);
        color: var(--text-tertiary);
    }
    
    .empty-icon {
        font-size: 64px;
        margin-bottom: var(--space-lg);
        opacity: 0.4;
    }
    
    .empty-title {
        font-family: var(--font-heading);
        font-size: 20px;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: var(--space-sm);
    }
    
    .empty-text {
        font-size: 15px;
        max-width: 300px;
        margin: 0 auto;
        line-height: 1.5;
    }
    
    /* ========================================
       DIVIDERS & SPACING
       ======================================== */
    .divider {
        height: 1px;
        background: var(--border-light);
        margin: var(--space-lg) 0;
    }
    
    .section-gap {
        height: var(--space-xl);
    }
    
    /* ========================================
       STREAMLIT COMPONENT OVERRIDES
       ======================================== */
    /* Success/Info/Warning/Error Messages */
    .stAlert {
        border-radius: var(--radius-md) !important;
        border: none !important;
        font-family: var(--font-body) !important;
    }
    
    .stSuccess {
        background: var(--success-light) !important;
        color: var(--success) !important;
    }
    
    .stWarning {
        background: var(--warning-light) !important;
        color: var(--warning) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    /* Status component */
    [data-testid="stStatusWidget"] {
        background: var(--surface) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: var(--surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        font-size: 13px !important;
    }
    
    .stDownloadButton > button:hover {
        background: var(--bg-secondary) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }
    
    /* Chat message avatars */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: var(--space-md) 0 !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        flex-direction: row-reverse;
    }
    
    /* ========================================
       RESPONSIVE ADJUSTMENTS
       ======================================== */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.8rem; }
        .hero-subtitle { font-size: 1rem; }
        .user-bubble, .assistant-bubble { max-width: 90%; }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
def init_session_state():
    if "rag_engine" not in st.session_state:
        st.session_state.rag_engine = RAGEngine()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_document" not in st.session_state:
        st.session_state.selected_document = "All Documents"


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        # Status section
        st.markdown('<div class="sidebar-header">System</div>', unsafe_allow_html=True)
        
        model_status = check_ollama_models()
        
        if model_status["available"] and model_status["llm_ready"] and model_status["embedding_ready"]:
            st.markdown('''
                <div style="display: flex; align-items: center; margin-bottom: 16px;">
                    <span class="status-dot status-online"></span>
                    <span style="font-size: 13px; color: var(--text-secondary);">Ready</span>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
                <div style="display: flex; align-items: center; margin-bottom: 16px;">
                    <span class="status-dot status-offline"></span>
                    <span style="font-size: 13px; color: var(--text-secondary);">Ollama offline</span>
                </div>
            ''', unsafe_allow_html=True)
            st.code("ollama serve", language="bash")
            if model_status.get("missing_models"):
                for m in model_status["missing_models"]:
                    st.code(f"ollama pull {m}", language="bash")
            return False
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Documents section
        st.markdown('<div class="sidebar-header">Documents</div>', unsafe_allow_html=True)
        
        rag = st.session_state.rag_engine
        documents = rag.get_documents()
        
        if documents:
            # Stats
            st.markdown(f'''
                <div class="stat-row">
                    <div class="stat-card">
                        <div class="stat-value">{len(documents)}</div>
                        <div class="stat-label">Files</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{rag.chunk_count}</div>
                        <div class="stat-label">Chunks</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Document list
            for doc in documents:
                info = rag.get_document_info(doc)
                chunks = info['chunk_count'] if info else '?'
                ext = doc.split('.')[-1].upper() if '.' in doc else 'FILE'
                
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f'''
                        <div class="doc-card">
                            <div class="doc-icon">📄</div>
                            <div class="doc-info">
                                <div class="doc-name">{doc[:22]}{'...' if len(doc) > 22 else ''}</div>
                                <div class="doc-meta">{chunks} chunks · <span class="format-pill">{ext}</span></div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                with col2:
                    if st.button("×", key=f"del_{doc}", help="Remove"):
                        rag.remove_document(doc)
                        st.rerun()
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Search filter
            st.markdown('<div class="sidebar-header">Search In</div>', unsafe_allow_html=True)
            st.session_state.selected_document = st.selectbox(
                "Filter",
                ["All Documents"] + documents,
                label_visibility="collapsed"
            )
            
            # Memory & Export
            conv_len = rag.conversation_length
            if conv_len > 0:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="sidebar-header">Session</div>', unsafe_allow_html=True)
                
                st.markdown(f'<span class="badge badge-accent">🧠 {conv_len} exchanges</span>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Clear", key="clear_mem"):
                        rag.clear_conversation()
                        st.session_state.messages = []
                        st.rerun()
                with col2:
                    export_md = rag.export_conversation("markdown")
                    st.download_button(
                        "Export",
                        export_md,
                        file_name=f"notes_{datetime.now().strftime('%m%d_%H%M')}.md",
                        mime="text/markdown"
                    )
            
            # Danger zone
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.expander("⚠️ Reset"):
                if st.button("Clear Everything", type="secondary"):
                    rag.clear_all()
                    st.session_state.messages = []
                    st.rerun()
        else:
            st.markdown('''
                <div class="empty-state" style="padding: 24px 0;">
                    <div style="font-size: 32px; opacity: 0.3; margin-bottom: 8px;">📚</div>
                    <div style="font-size: 13px; color: var(--text-tertiary);">No documents yet</div>
                </div>
            ''', unsafe_allow_html=True)
        
        return True


# ============================================================
# MAIN CONTENT
# ============================================================
def render_hero():
    st.markdown('''
        <div class="hero">
            <div class="hero-title">📖 Study Buddy</div>
            <div class="hero-subtitle">Your cozy AI study companion. Upload notes, ask anything.</div>
        </div>
    ''', unsafe_allow_html=True)


def render_upload():
    st.markdown("#### Upload Materials")
    
    formats = list(get_supported_formats().keys())
    uploaded_files = st.file_uploader(
        "Drop your study materials here",
        type=formats,
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Supports PDF, DOCX, TXT, MD"
    )
    
    if uploaded_files:
        rag = st.session_state.rag_engine
        
        for uploaded_file in uploaded_files:
            if uploaded_file.name in rag.get_documents():
                continue
            
            with st.status(f"Processing {uploaded_file.name}...", expanded=True) as status:
                try:
                    result = rag.process_document(uploaded_file)
                    status.update(label=f"✓ {uploaded_file.name} ready", state="complete")
                except Exception as e:
                    status.update(label=f"Failed", state="error")
                    st.error(str(e))


def render_chat():
    rag = st.session_state.rag_engine
    
    if not rag.is_ready:
        st.markdown('''
            <div class="empty-state">
                <div class="empty-icon">📚</div>
                <div class="empty-title">Ready to study?</div>
                <div class="empty-text">Upload your notes, textbooks, or articles above. Then ask me anything about them!</div>
            </div>
        ''', unsafe_allow_html=True)
        
        # Example prompts
        st.markdown("#### Try asking...")
        cols = st.columns(2)
        examples = [
            "What are the key concepts?",
            "Explain this in simple terms",
            "Summarize the main points", 
            "Compare X and Y"
        ]
        for i, ex in enumerate(examples):
            with cols[i % 2]:
                st.markdown(f'<div style="background: var(--bg-tertiary); padding: 10px 14px; border-radius: 8px; font-size: 13px; color: var(--text-secondary); margin-bottom: 8px;">"{ex}"</div>', unsafe_allow_html=True)
        return
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        filter_doc = st.session_state.selected_document
        if filter_doc != "All Documents":
            st.markdown(f'<span class="badge badge-muted">Searching in: {filter_doc[:20]}</span>', unsafe_allow_html=True)
    with col2:
        if st.button("Clear chat"):
            st.session_state.messages = []
            rag.clear_conversation()
            st.rerun()
    
    # Messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander(f"📚 {len(msg['sources'])} sources"):
                    for src in msg["sources"]:
                        st.markdown(f'''
                            <div class="source-card">
                                <div class="source-meta">
                                    <span class="source-badge">Page {src['page']}</span>
                                    <span style="font-size: 11px; color: var(--text-tertiary);">{src['document']}</span>
                                </div>
                                <div class="source-text">{src['content']}</div>
                            </div>
                        ''', unsafe_allow_html=True)
    
    # Input
    if question := st.chat_input("Ask about your documents..."):
        st.session_state.messages.append({"role": "user", "content": question})
        
        with st.chat_message("user"):
            st.markdown(question)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                doc_filter = st.session_state.selected_document
                if doc_filter == "All Documents":
                    doc_filter = None
                result = rag.ask_question(question, document_filter=doc_filter)
            
            st.markdown(result["answer"])
            
            if result["sources"]:
                with st.expander(f"📚 {len(result['sources'])} sources"):
                    for src in result["sources"]:
                        st.markdown(f'''
                            <div class="source-card">
                                <div class="source-meta">
                                    <span class="source-badge">Page {src['page']}</span>
                                    <span style="font-size: 11px; color: var(--text-tertiary);">{src['document']}</span>
                                </div>
                                <div class="source-text">{src['content']}</div>
                            </div>
                        ''', unsafe_allow_html=True)
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result["answer"],
            "sources": result.get("sources", [])
        })


# ============================================================
# MAIN
# ============================================================
def main():
    init_session_state()
    
    system_ready = render_sidebar()
    
    if not system_ready:
        st.warning("Please start Ollama first")
        return
    
    render_hero()
    render_upload()
    render_chat()


if __name__ == "__main__":
    main()
