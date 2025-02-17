# ui.py
import streamlit as st
import requests
import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Fake Product Review Detector",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a professional dark theme
st.markdown(
    """
    <style>
    /* Main theme colors and fonts */
    :root {
        --background: #0e1117;
        --secondary-background: #1a1c24;
        --accent: #4b57db;
        --text: #e0e0e0;
        --text-secondary: #9ca3af;
        --success: #1db954;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    
    body {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(90deg, #1a1c24, #272935, #1a1c24);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
    }
    
    .header h1 {
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    .header p {
        color: var(--text-secondary);
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Main sections styling */
    .card {
        background-color: var(--secondary-background);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.05);
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
    }
    
    .card-title {
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        color: white;
        display: flex;
        align-items: center;
    }
    
    .card-title svg {
        margin-right: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: var(--accent);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #5b68e8;
        box-shadow: 0 4px 12px rgba(75, 87, 219, 0.3);
    }
    
    /* Text area styling */
    .stTextArea>div>div>textarea {
        background-color: #272935;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        color: var(--text);
        font-size: 1rem;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 2px rgba(75, 87, 219, 0.2);
    }
    
    /* Result containers */
    .result-container {
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .result-genuine {
        background-color: rgba(29, 185, 84, 0.1);
        border-left: 4px solid var(--success);
    }
    
    .result-fake {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid var(--error);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #272935;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #2d303e;
    }
    
    .streamlit-expanderContent {
        background-color: var(--secondary-background);
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
    }
    
    /* Spinner */
    .stSpinner {
        text-align: center;
        padding: 2rem;
    }
    
    /* Custom badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .badge-fake {
        background-color: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }
    
    .badge-genuine {
        background-color: rgba(29, 185, 84, 0.1);
        color: #1db954;
    }

    /* Add custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #272935;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4b57db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5b68e8;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Responsive layouts */
    @media (max-width: 768px) {
        .header h1 {
            font-size: 1.8rem;
        }
        .card {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with logo and description
st.markdown(
    """
    <div class="header animate-fade-in">
        <h1>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:10px;">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <path d="M12 8v4"></path>
                <path d="M12 16h.01"></path>
            </svg>
            Fake Product Review Detector
        </h1>
        <p>Advanced AI-powered tool to identify fraudulent product reviews with detailed explanations</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Main layout with columns
col1, col2 = st.columns([3, 2])

# Input Section (Left Column)
with col1:
    st.markdown(
        """
        <div class="card animate-fade-in">
            <div class="card-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
                Enter Product Review
            </div>
        """,
        unsafe_allow_html=True
    )
    
    # Review input area
    review_input = st.text_area(
        "Paste or type the review text below",
        height=250,
        help="Enter the complete review text you want to analyze",
        key="review_input"
    )
    
    # Analysis button using streaming endpoint
    # ... inside the Analyze Review button click handler in ui.py ...

    if st.button("Analyze Review", key="analyze_button"):
        if review_input:
            with st.spinner("Analyzing review... This may take a few seconds"):
                try:
                    api_url = "http://localhost:8000/predict_with_explanation_stream"
                    response = requests.post(api_url, json={"review": review_input}, stream=True)
                    
                    if response.status_code == 200:
                        # Placeholder to update results in real time
                        header_placeholder = st.empty()
                        # Initialize variables
                        label = ""
                        summary = ""
                        explanation_text = ""
                        result_class = ""
                        badge_class = ""
                        
                        for line in response.iter_lines():
                            if line:
                                decoded_line = line.decode("utf-8")
                                if decoded_line.startswith("data: "):
                                    data_json = decoded_line[6:]
                                    data = json.loads(data_json)
                                    if data["type"] == "header":
                                        label = data["label"]
                                        summary = data["summary"]
                                        result_class = "result-genuine" if label == "Genuine" else "result-fake"
                                        badge_class = "badge-genuine" if label == "Genuine" else "badge-fake"
                                        header_html = f"""
                                        <div class="card {result_class} animate-fade-in">
                                            <h3>Analysis Results</h3>
                                            <p><span class="badge {badge_class}">{label}</span></p>
                                            <h4>Summary</h4>
                                            <p>{summary}</p>
                                            <h4>Detailed Explanation</h4>
                                            <p id="explanation">Waiting for explanation...</p>
                                        </div>
                                        """
                                        header_placeholder.markdown(header_html, unsafe_allow_html=True)
                                    elif data["type"] == "token":
                                        explanation_text += data["token"]
                                        updated_html = f"""
                                        <div class="card {result_class} animate-fade-in">
                                            <h3>Analysis Results</h3>
                                            <p><span class="badge {badge_class}">{label}</span></p>
                                            <h4>Summary</h4>
                                            <p>{summary}</p>
                                            <h4>Detailed Explanation</h4>
                                            <p id="explanation">{explanation_text}</p>
                                        </div>
                                        <script>
                                            window.scrollTo({{ top: document.body.scrollHeight, behavior: 'smooth' }});
                                        </script>
                                        """
                                        header_placeholder.markdown(updated_html, unsafe_allow_html=True)
                                    elif data["type"] == "end":
                                        break
                        # Save complete result to history
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.history.append({
                            "timestamp": timestamp,
                            "review": review_input,
                            "label": label,
                            "summary": summary,
                            "explanation": explanation_text
                        })
                    else:
                        st.error(f"Error: Unable to get prediction. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"Request failed: {str(e)}")
        else:
            st.warning("Please enter a review before clicking Analyze.")

    
    st.markdown("</div>", unsafe_allow_html=True)

# History Section (Right Column)
with col2:
    st.markdown(
        """
        <div class="card animate-fade-in">
            <div class="card-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 8v4l3 3"></path>
                    <circle cx="12" cy="12" r="10"></circle>
                </svg>
                Analysis History
            </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history), start=1):
            badge_class = "badge-genuine" if item['label'] == "Genuine" else "badge-fake"
            with st.expander(f"#{i} - {item['timestamp'][:10]}"):
                st.markdown(f"<span class='badge {badge_class}'>{item['label']}</span>", unsafe_allow_html=True)
                st.markdown("**Review:**")
                st.text(item['review'][:150] + "..." if len(item['review']) > 150 else item['review'])
                st.markdown("**Summary:**")
                st.markdown(item['summary'])
                st.markdown("**Explanation:**")
                st.markdown(item['explanation'])
    else:
        st.markdown("<p class='text-secondary'>No analysis history yet. Submit a review to see results here.</p>", unsafe_allow_html=True)
    
    if st.session_state.history:
        if st.button("Clear History", key="clear_history"):
            st.session_state.history = []
            st.experimental_rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 3rem; padding: 1rem; border-top: 1px solid rgba(255,255,255,0.05);">
        <p style="color: #9ca3af; font-size: 0.9rem;">
            Powered by advanced AI technology. For demonstration purposes only.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
