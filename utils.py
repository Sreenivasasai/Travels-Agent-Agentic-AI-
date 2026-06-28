# ============================
# utils.py
# Helper / utility functions for the AI Travel Agent
# ============================

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_groq_api_key() -> str:
    """
    Reads the GROQ_API_KEY from environment variables.
    Returns the key string, or an empty string if not found.
    """
    return os.getenv("GROQ_API_KEY", "")


def validate_inputs(
    start_location: str,
    destination: str,
    num_days: int,
    budget: str,
) -> tuple[bool, str]:
    """
    Validates user inputs before sending them to the AI agent.

    Returns:
        (True, "")               – all inputs are valid
        (False, error_message)   – something is missing or out of range
    """
    if not start_location.strip():
        return False, "⚠️ Please enter your trip start location."

    if not destination.strip():
        return False, "⚠️ Please enter your travel destination."

    if num_days < 1:
        return False, "⚠️ Number of days must be at least 1."

    if num_days > 30:
        return False, "⚠️ Number of days should not exceed 30 for a single itinerary."

    if not budget.strip():
        return False, "⚠️ Please enter your budget."

    return True, ""


def build_travel_prompt(
    start_location: str,
    destination: str,
    num_days: int,
    budget: str,
    preferences: str,
) -> str:
    """
    Builds the main prompt string that is sent to the LangChain agent.
    """
    pref_text = preferences.strip() if preferences.strip() else "general sightseeing and local experiences"

    prompt = f"""
You are an expert AI Travel Agent. Create a comprehensive and detailed travel plan for the following trip:

**Trip Details:**
- Starting Location: {start_location}
- Destination: {destination}
- Duration: {num_days} days
- Total Budget: {budget}
- Travel Preferences: {pref_text}

Please provide a COMPLETE travel itinerary that includes ALL of the following sections:

## 🗓️ Day-wise Itinerary
Create a detailed plan for each of the {num_days} days with:
- Morning activities
- Afternoon activities  
- Evening activities
- Recommended places to visit each day

## 📍 Top Places to Visit
List the must-visit attractions and locations in {destination}.

## 💰 Estimated Cost Breakdown
Provide a realistic budget breakdown for {num_days} days covering:
- Accommodation
- Food & Drinks
- Local Transportation
- Entry Fees & Activities
- Miscellaneous
- **Total Estimated Cost**

## 🍽️ Food Suggestions
- Must-try local dishes
- Recommended restaurants (budget-friendly and mid-range)
- Street food spots

## ✈️ Travel Tips
- Best ways to travel from {start_location} to {destination}
- Local transportation options
- Safety tips
- Best time to visit attractions

## 💡 Budget-Friendly Recommendations
- Free or low-cost activities
- Money-saving tips
- Affordable accommodation options

## 📝 Final Summary
A brief summary of the complete trip with key highlights.

Use the available tools (itinerary_planner_tool, budget_estimator_tool, travel_tips_tool) to gather 
information and compile a thorough, well-structured response. Make it practical, specific, and helpful.
"""
    return prompt.strip()


def format_itinerary_output(raw_output: str) -> str:
    """
    Lightly cleans up the agent's raw output string before displaying it
    in Streamlit.  Currently just strips leading/trailing whitespace; extend
    this function if post-processing is ever needed.
    """
    if not raw_output:
        return "No itinerary was generated. Please try again."
    return raw_output.strip()
