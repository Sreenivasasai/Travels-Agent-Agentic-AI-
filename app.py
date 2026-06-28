# ============================
# app.py
# AI Powered Travel Agent – Main Streamlit Application
# ============================

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

# Import our custom tools and utility helpers
from tools import itinerary_planner_tool, budget_estimator_tool, travel_tips_tool
from utils import (
    get_groq_api_key,
    validate_inputs,
    build_travel_prompt,
    format_itinerary_output,
)

# ── Load .env ──────────────────────────────────────────────────────────────────
load_dotenv()

# ── Streamlit page configuration ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Powered Travel Agent",
    page_icon="✈️",
    layout="centered",
)

# ── Custom CSS for a cleaner look ──────────────────────────────────────────────
st.markdown(
    """
    <style>
        .main-title  { font-size: 2.4rem; font-weight: 700; color: #1f2328; margin-bottom: 0; }
        .sub-title   { font-size: 1.05rem; color: #57606a; margin-top: 0.2rem; }
        .section-box {
            background: #f7f8fa;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1.2rem;
        }
        .result-box  {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 1.6rem 1.8rem;
            margin-top: 1rem;
        }
        .stButton > button {
            width: 100%;
            background-color: #3b82d4;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            padding: 0.65rem 1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton > button:hover { background-color: #2563ab; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── App header ─────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">✈️ AI Powered Travel Agent</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Plan your perfect trip with the help of AI — '
    "day-wise itinerary, budget breakdown, food tips, and more.</p>",
    unsafe_allow_html=True,
)
st.divider()

# ── API key check ──────────────────────────────────────────────────────────────
api_key = get_groq_api_key()

if not api_key or api_key == "your_groq_api_key_here":
    st.error(
        "🔑 **Groq API key not found.**\n\n"
        "Please add your key to the `.env` file:\n"
        "```\nGROQ_API_KEY=your_actual_key_here\n```\n\n"
        "Get a free key at [console.groq.com](https://console.groq.com).",
        icon="🚨",
    )
    st.stop()   # Don't render anything else until the key is present

# ── Input form ─────────────────────────────────────────────────────────────────
st.markdown("### 🗺️ Enter Your Trip Details")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        start_location = st.text_input(
            "📍 Start Location",
            placeholder="e.g. New York, USA",
            help="The city or country you are travelling from.",
        )

    with col2:
        destination = st.text_input(
            "🌍 Destination",
            placeholder="e.g. Paris, France",
            help="The city or country you want to visit.",
        )

    col3, col4 = st.columns(2)

    with col3:
        num_days = st.number_input(
            "📅 Number of Days",
            min_value=1,
            max_value=30,
            value=5,
            step=1,
            help="How many days is your trip?",
        )

    with col4:
        budget = st.text_input(
            "💰 Total Budget",
            placeholder="e.g. $1500 or ₹50,000",
            help="Enter your total budget (include currency symbol).",
        )

    preferences = st.text_area(
        "🎯 Travel Preferences (Optional)",
        placeholder=(
            "e.g. Adventure activities, historical sites, vegetarian food, "
            "budget hotels, romantic getaway, family-friendly attractions..."
        ),
        height=100,
        help="Describe what kind of experiences you enjoy. Leave blank for a general itinerary.",
    )

# ── Generate button ────────────────────────────────────────────────────────────
st.markdown("")   # small spacer
generate = st.button("🚀 Generate Itinerary")

# ── Agent logic ────────────────────────────────────────────────────────────────
if generate:
    # 1. Validate inputs
    is_valid, error_msg = validate_inputs(start_location, destination, num_days, budget)
    if not is_valid:
        st.warning(error_msg)
        st.stop()

    # 2. Build the prompt
    travel_prompt = build_travel_prompt(
        start_location, destination, num_days, budget, preferences
    )

    # 3. Set up ChatGroq model
    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",   # Fast, capable Groq model — change if desired
        temperature=0.7,
    )

    # 4. Register custom tools
    tools = [itinerary_planner_tool, budget_estimator_tool, travel_tips_tool]

    # 5. Create the LangGraph ReAct agent (compatible with LangChain 1.x)
    #    The system prompt is passed via the 'prompt' parameter.
    system_prompt = (
        "You are an expert AI Travel Agent. Use the provided tools to gather "
        "information and always produce a detailed, well-structured travel itinerary. "
        "Be specific, practical, and helpful."
    )
    agent_executor = create_react_agent(llm, tools, prompt=system_prompt)

    # 6. Run the agent with a spinner
    with st.spinner("🤖 Your AI Travel Agent is planning your trip… this may take a moment."):
        try:
            result = agent_executor.invoke({"messages": [("human", travel_prompt)]})
            # LangGraph returns a list of messages; the last one is the AI response
            last_message = result["messages"][-1]
            raw_output = getattr(last_message, "content", str(last_message))
            itinerary = format_itinerary_output(raw_output)
        except Exception as e:
            st.error(f"❌ An error occurred while generating the itinerary:\n\n`{str(e)}`")
            st.stop()

    # 8. Display the itinerary
    st.success("✅ Your travel itinerary is ready!")
    st.divider()
    st.markdown("## 🗺️ Your Personalised Travel Itinerary")
    st.markdown(
        f'<div class="result-box">{itinerary}</div>',
        unsafe_allow_html=True,
    )

    # Download button so users can save their itinerary
    st.download_button(
        label="📥 Download Itinerary",
        data=itinerary,
        file_name=f"itinerary_{destination.replace(' ', '_')}.txt",
        mime="text/plain",
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; font-size:12px; color:#57606a;'>"
    "Made with IBM Bob &nbsp;|&nbsp; Powered by Groq &amp; LangChain"
    "</p>",
    unsafe_allow_html=True,
)
