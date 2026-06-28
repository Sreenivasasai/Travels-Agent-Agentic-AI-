# ============================
# tools.py
# Custom LangChain tools for the AI Travel Agent
# ============================

from langchain.tools import tool


@tool
def itinerary_planner_tool(input: str) -> str:
    """
    Plans a detailed day-wise travel itinerary.
    Input format: 'start_location|destination|days|budget|preferences'
    Returns a structured day-by-day travel plan with places to visit.
    """
    try:
        parts = input.split("|")
        start      = parts[0].strip() if len(parts) > 0 else "Unknown"
        destination = parts[1].strip() if len(parts) > 1 else "Unknown"
        days       = parts[2].strip() if len(parts) > 2 else "3"
        budget     = parts[3].strip() if len(parts) > 3 else "moderate"
        prefs      = parts[4].strip() if len(parts) > 4 else "general sightseeing"

        return (
            f"Itinerary Planning Request:\n"
            f"- From: {start}\n"
            f"- To: {destination}\n"
            f"- Duration: {days} days\n"
            f"- Budget: {budget}\n"
            f"- Preferences: {prefs}\n\n"
            f"Please create a complete day-wise itinerary for this trip including "
            f"morning, afternoon, and evening activities for each day, "
            f"top attractions, local experiences, and hidden gems."
        )
    except Exception as e:
        return f"Error parsing itinerary input: {str(e)}"


@tool
def budget_estimator_tool(input: str) -> str:
    """
    Estimates travel costs and provides budget breakdown.
    Input format: 'destination|days|budget_range'
    Returns estimated costs for accommodation, food, transport, and activities.
    """
    try:
        parts       = input.split("|")
        destination = parts[0].strip() if len(parts) > 0 else "Unknown"
        days        = parts[1].strip() if len(parts) > 1 else "3"
        budget      = parts[2].strip() if len(parts) > 2 else "moderate"

        return (
            f"Budget Estimation Request:\n"
            f"- Destination: {destination}\n"
            f"- Duration: {days} days\n"
            f"- Budget Range: {budget}\n\n"
            f"Please provide a detailed budget breakdown including:\n"
            f"1. Accommodation costs per night (budget/mid-range/luxury options)\n"
            f"2. Daily food expenses (street food, mid-range restaurants, fine dining)\n"
            f"3. Local transportation costs\n"
            f"4. Entry fees for major attractions\n"
            f"5. Miscellaneous expenses\n"
            f"6. Total estimated cost for {days} days\n"
            f"7. Money-saving tips for {destination}"
        )
    except Exception as e:
        return f"Error parsing budget input: {str(e)}"


@tool
def travel_tips_tool(input: str) -> str:
    """
    Provides essential travel tips, food suggestions, and local advice.
    Input format: 'destination|preferences'
    Returns safety tips, local customs, best food spots, and practical advice.
    """
    try:
        parts       = input.split("|")
        destination = parts[0].strip() if len(parts) > 0 else "Unknown"
        prefs       = parts[1].strip() if len(parts) > 1 else "general"

        return (
            f"Travel Tips Request:\n"
            f"- Destination: {destination}\n"
            f"- Traveller Preferences: {prefs}\n\n"
            f"Please provide:\n"
            f"1. Top local foods and must-try dishes in {destination}\n"
            f"2. Best local restaurants and street food spots\n"
            f"3. Safety tips and precautions\n"
            f"4. Local customs and etiquette\n"
            f"5. Best time to visit each attraction\n"
            f"6. Transportation tips (local buses, metro, taxis, etc.)\n"
            f"7. Packing suggestions for {destination}\n"
            f"8. Emergency contacts and useful local phrases"
        )
    except Exception as e:
        return f"Error parsing travel tips input: {str(e)}"
