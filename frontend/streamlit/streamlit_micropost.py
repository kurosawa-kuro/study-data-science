import streamlit as st
import requests

def get_microposts():
    """
    Retrieve microposts from the external REST API endpoint.
    """
    api_url = "http://localhost:3000/api/v1/microposts"  # API endpoint
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Parse JSON response into Python data structure
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

# Main Streamlit UI
st.title("GET /api/v1/microposts Demo")

if st.button("Fetch Microposts"):
    microposts = get_microposts()
    if microposts is not None:
        # Display the fetched microposts in a pretty JSON format
        st.json(microposts)

