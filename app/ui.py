import streamlit as st
import requests
import datetime
import json
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

# Page configuration with custom favicon
st.set_page_config(
    page_title="Fake Review Detector Pro",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = []
if "theme_color" not in st.session_state:
    st.session_state.theme_color = "#4b57db"
if "statistics" not in st.session_state:
    st.session_state.statistics = {
        "total_analyzed": 0,
        "genuine_count": 0,
        "fake_count": 0,
        "avg_confidence": 0
    }

# Custom CSS with dynamic theme color
def get_custom_css():
    return f"""
    <style>
    /* Main theme colors and fonts */
    :root {{
        --background: #0e1117;
        --secondary-background: #1a1c24;
        --accent: {st.session_state.theme_color};
        --text: #e0e0e0;
        --text-secondary: #9ca3af;
        --success: #1db954;
        --warning: #f59e0b;
        --error: #ef4444;
    }}
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    body {{
        background-color: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Header styling */
    .header {{
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #181a1f, #222531, #181a1f);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }}
    
    .header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(75, 87, 219, 0.15), transparent 70%);
    }}
    
    .header h1 {{
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    .header p {{
        color: var(--text-secondary);
        max-width: 800px;
        margin: 0 auto;
    }}
    
    /* Main sections styling */
    .card {{
        background-color: var(--secondary-background);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .card::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--accent);
        opacity: 0.7;
    }}
    
    .card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
    }}
    
    .card-title {{
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        color: white;
        display: flex;
        align-items: center;
    }}
    
    .card-title svg {{
        margin-right: 0.5rem;
        color: var(--accent);
    }}
    
    /* Button styling */
    .stButton>button {{
        background: var(--accent);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }}
    
    .stButton>button:hover {{
        background: linear-gradient(90deg, var(--accent), {adjust_color_brightness(st.session_state.theme_color, 30)});
        box-shadow: 0 4px 12px {adjust_color_brightness(st.session_state.theme_color, -30, 0.3)};
    }}
    
    .stButton>button:active {{
        transform: translateY(1px);
    }}
    
    /* Text area styling */
    .stTextArea>div>div>textarea {{
        background-color: #272935;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        color: var(--text);
        font-size: 1rem;
        transition: all 0.3s ease;
    }}
    
    .stTextArea>div>div>textarea:focus {{
        border-color: var(--accent);
        box-shadow: 0 0 0 2px {adjust_color_brightness(st.session_state.theme_color, 0, 0.2)};
    }}
    
    /* Result containers */
    .result-container {{
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }}
    
    .result-genuine {{
        background-color: rgba(29, 185, 84, 0.05);
        border-left: 4px solid var(--success);
    }}
    
    .result-genuine::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at top right, rgba(29, 185, 84, 0.1), transparent 70%);
        pointer-events: none;
    }}
    
    .result-fake {{
        background-color: rgba(239, 68, 68, 0.05);
        border-left: 4px solid var(--error);
    }}
    
    .result-fake::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at top right, rgba(239, 68, 68, 0.1), transparent 70%);
        pointer-events: none;
    }}
    
    /* Spinner */
    .stSpinner {{
        text-align: center;
        padding: 2rem;
    }}
    
    /* Custom badges */
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }}
    
    .badge-fake {{
        background-color: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }}
    
    .badge-genuine {{
        background-color: rgba(29, 185, 84, 0.1);
        color: #1db954;
        border: 1px solid rgba(29, 185, 84, 0.2);
    }}
    
    /* Statistics cards */
    .stat-card {{
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
    }}
    
    .stat-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin: 0.5rem 0;
    }}
    
    .stat-label {{
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Add custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #272935;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--accent);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {adjust_color_brightness(st.session_state.theme_color, 30)};
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(10px);}}
        to {{opacity: 1; transform: translateY(0);}}
    }}
    
    @keyframes pulseGlow {{
        0% {{box-shadow: 0 0 0 0 {adjust_color_brightness(st.session_state.theme_color, 0, 0.4)};}}
        70% {{box-shadow: 0 0 0 10px {adjust_color_brightness(st.session_state.theme_color, 0, 0)};}}
        100% {{box-shadow: 0 0 0 0 {adjust_color_brightness(st.session_state.theme_color, 0, 0)};}}
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.5s ease-out forwards;
    }}
    
    /* Different fade-in delays for cascading effect */
    .delay-1 {{animation-delay: 0.1s;}}
    .delay-2 {{animation-delay: 0.2s;}}
    .delay-3 {{animation-delay: 0.3s;}}
    
    /* Pulse animation for new results */
    .pulse-glow {{
        animation: pulseGlow 2s infinite;
    }}
    
    /* Tooltip styling */
    .tooltip {{
        position: relative;
        display: inline-block;
        cursor: help;
    }}
    
    .tooltip .tooltiptext {{
        visibility: hidden;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.85rem;
        width: 200px;
    }}
    
    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}
    
    /* Tab styling for the dashboard */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #1a1c24;
        border-radius: 8px;
        padding: 0.5rem;
        gap: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.5rem 1rem;
        border-radius: 6px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: var(--accent) !important;
        color: white !important;
    }}
    
    /* Theme selector */
    .theme-option {{
        display: inline-block;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        margin: 0 5px;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }}
    
    .theme-option:hover {{
        transform: scale(1.1);
    }}
    
    .theme-option.active {{
        border-color: white;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.2);
    }}
    
    /* Dashboard layout enhancements */
    .dashboard-layout {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
    }}
    
    /* Help tooltips and documentation styling */
    .help-icon {{
        color: var(--text-secondary);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        font-size: 10px;
        margin-left: 0.5rem;
        cursor: help;
    }}
    
    .help-icon:hover {{
        background: rgba(255,255,255,0.2);
        color: white;
    }}
    
    /* Status indicator */
    .status-indicator {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
    }}
    
    .status-online {{
        background-color: #1db954;
        box-shadow: 0 0 0 2px rgba(29, 185, 84, 0.2);
    }}
    
    /* Responsive layouts */
    @media (max-width: 768px) {{
        .header h1 {{
            font-size: 1.8rem;
        }}
        .card {{
            padding: 1rem;
        }}
        .dashboard-layout {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>
    """

# Helper function to adjust color brightness
def adjust_color_brightness(hex_color, brightness_offset=0, opacity=1):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgb = [max(0, min(255, c + brightness_offset)) for c in rgb]
    if opacity < 1:
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {opacity})"
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Header with logo and description
st.markdown(
    """
    <div class="header animate-fade-in">
        <h1>
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:10px; color:var(--accent)">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <path d="M12 8v4"></path>
                <path d="M12 16h.01"></path>
            </svg>
            Fake Review Detector Pro
        </h1>
        <p>Advanced AI-powered analysis to identify fraudulent product reviews with detailed explanations and insights</p>
    </div>
    """,
    unsafe_allow_html=True
)

def update_statistics(result):
    st.session_state.statistics["total_analyzed"] += 1
    if result["label"] == "Genuine":
        st.session_state.statistics["genuine_count"] += 1
    else:
        st.session_state.statistics["fake_count"] += 1
    
    # Update average confidence if available
    if "confidence" in result:
        current_avg = st.session_state.statistics["avg_confidence"]
        current_count = st.session_state.statistics["total_analyzed"] - 1
        new_confidence = result["confidence"]
        
        if current_count == 0:
            st.session_state.statistics["avg_confidence"] = new_confidence
        else:
            st.session_state.statistics["avg_confidence"] = (
                (current_avg * current_count) + new_confidence
            ) / st.session_state.statistics["total_analyzed"]

# Dashboard tab with statistics and visualizations
def render_dashboard():
    st.markdown(
        """
        <div class="card animate-fade-in delay-1">
            <div class="card-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="3" y1="9" x2="21" y2="9"></line>
                    <line x1="9" y1="21" x2="9" y2="9"></line>
                </svg>
                Analysis Dashboard
            </div>
        """,
        unsafe_allow_html=True
    )
    
    # Statistics cards
    cols = st.columns(4)
    
    # Total analyzed reviews
    with cols[0]:
        st.markdown(
            f"""
            <div class="stat-card animate-fade-in delay-1">
                <div class="stat-label">Total Analyzed</div>
                <div class="stat-value">{st.session_state.statistics["total_analyzed"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Genuine reviews count
    with cols[1]:
        genuine_percent = 0 if st.session_state.statistics["total_analyzed"] == 0 else \
            (st.session_state.statistics["genuine_count"] / st.session_state.statistics["total_analyzed"] * 100)
        
        st.markdown(
            f"""
            <div class="stat-card animate-fade-in delay-2" style="border-left: 3px solid #1db954;">
                <div class="stat-label">Genuine Reviews</div>
                <div class="stat-value">{st.session_state.statistics["genuine_count"]}</div>
                <div style="font-size: 0.9rem; color: #1db954;">{genuine_percent:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Fake reviews count
    with cols[2]:
        fake_percent = 0 if st.session_state.statistics["total_analyzed"] == 0 else \
            (st.session_state.statistics["fake_count"] / st.session_state.statistics["total_analyzed"] * 100)
        
        st.markdown(
            f"""
            <div class="stat-card animate-fade-in delay-3" style="border-left: 3px solid #ef4444;">
                <div class="stat-label">Fake Reviews</div>
                <div class="stat-value">{st.session_state.statistics["fake_count"]}</div>
                <div style="font-size: 0.9rem; color: #ef4444;">{fake_percent:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Average confidence
    with cols[3]:
        avg_conf = st.session_state.statistics["avg_confidence"] * 100
        
        st.markdown(
            f"""
            <div class="stat-card animate-fade-in delay-4" style="border-left: 3px solid var(--accent);">
                <div class="stat-label">Avg Confidence</div>
                <div class="stat-value">{avg_conf:.1f}%</div>
                <div class="tooltip" style="font-size: 0.9rem; color: var(--text-secondary);">
                    <span>Reliability Score</span>
                    <span class="tooltiptext">Higher values indicate more confident predictions</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Chart: Distribution of genuine vs fake reviews
    if st.session_state.statistics["total_analyzed"] > 0:
        st.markdown("<h4 style='margin-top:2rem'>Review Distribution</h4>", unsafe_allow_html=True)
        
        # Prepare data for the chart
        chart_data = pd.DataFrame({
            'category': ['Genuine', 'Fake'],
            'count': [st.session_state.statistics["genuine_count"], 
                      st.session_state.statistics["fake_count"]]
        })
        
        # Create a horizontal bar chart
        bar_chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('count:Q', title='Number of Reviews'),
            y=alt.Y('category:N', title=None, sort=None),
            color=alt.Color('category:N', 
                          scale=alt.Scale(
                              domain=['Genuine', 'Fake'],
                              range=['#1db954', '#ef4444']
                          ),
                          legend=None),
            tooltip=['category', 'count']
        ).properties(
            height=100
        ).configure_axis(
            labelColor='#9ca3af',
            titleColor='#9ca3af',
            grid=False
        ).configure_view(
            strokeWidth=0
        )
        
        st.altair_chart(bar_chart, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Analysis tab for submitting reviews
def render_analysis_tab():
    col1, col2 = st.columns([3, 2])
    
    # Input Section (Left Column)
    with col1:
        st.markdown(
            """
            <div class="card animate-fade-in delay-1">
                <div class="card-title">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                    Review Analysis
                    <span class="help-icon" title="Paste a product review to analyze its authenticity">?</span>
                </div>
            """,
            unsafe_allow_html=True
        )
        
        review_input = st.text_area(
            "Review Text",
            height=250,
            help="Enter the complete review text you want to analyze",
            key="review_input"
        )
        
        # Analysis button
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
                            
                            result = {
                                "label": label,
                                "summary": summary,
                                "explanation": explanation_text,
                                "confidence": 0.85  # Placeholder value
                            }

                            # Save complete result to history
                            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.history.append({
                                "timestamp": timestamp,
                                "review": review_input,
                                "label": label,
                                "summary": summary,
                                "explanation": explanation_text,
                                "confidence": result.get("confidence", 0.85)
                            })
                            
                            # Update statistics
                            update_statistics(result)
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
            <div class="card animate-fade-in delay-2">
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
                # Determine badge class
                badge_class = "badge-genuine" if item["label"] == "Genuine" else "badge-fake"
                
                # Add confidence display if available
                confidence_html = ""
                if "confidence" in item:
                    confidence_pct = item["confidence"] * 100
                    confidence_html = f'<div style="margin-top:0.25rem"><small>Confidence: <strong>{confidence_pct:.1f}%</strong></small></div>'
                
                with st.expander(f"#{i} - {item['timestamp'][:10]}"):
                    st.markdown(f"<span class='badge {badge_class}'>{item['label']}</span>", unsafe_allow_html=True)
                    if confidence_html:
                        st.markdown(confidence_html, unsafe_allow_html=True)
                    st.markdown("**Review:**")
                    st.text(item["review"][:150] + "..." if len(item["review"]) > 150 else item["review"])
                    st.markdown("**Summary:**")
                    st.markdown(item["summary"])
                    st.markdown("**Explanation:**")
                    st.markdown(item["explanation"])
        else:
            st.markdown("<p class='text-secondary'>No analysis history yet. Submit a review to see results here.</p>", unsafe_allow_html=True)
        
        # Clear history button at the bottom
        if st.session_state.history:
            if st.button("Clear History", key="clear_history"):
                st.session_state.history = []
                st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Main application layout with tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "🔍 Analysis"])

with tab1:
    # Import time for demo mode delay simulation
    import time
    render_dashboard()

with tab2:
    render_analysis_tab()

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