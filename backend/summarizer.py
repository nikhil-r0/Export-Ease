import google.generativeai as genai
import os

# Configure the API key for Gemini
genai.configure(api_key=os.environ["API_KEY"])


def query_gemini(prompt):
    """
    Query Google's Gemini API with the given prompt using the `gemini-1.5-flash` model.
    """
    try:
        # Instantiate the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return {"generated_text": response.text}
    except Exception as e:
        return {"error": f"An error occurred while querying Gemini: {e}"}
