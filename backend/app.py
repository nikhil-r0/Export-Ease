from flask import Flask, request, jsonify
from flask_cors import CORS
from hs_code import search_hs_code
from summarizer import query_gemini
from market_analysis import get_market_analysis  # Import market analysis module
import json

app = Flask(__name__)
CORS(app)

with open("data/dataset.json", "r") as f:
    DATASET = json.load(f)


def find_entry_by_hs_code(hs_code):
    """
    Search for an entry in the dataset by HS code.
    """
    for entry in DATASET:
        if hs_code in entry.get("hs_codes", []):
            return entry
    return None


@app.route('/submit-form', methods=['POST'])
def submit_form():
    """
    Handle form submission and process the data.
    """
    data = request.get_json()
    print("Received Form Data:", data)

    product_name = data.get("productName", "")
    hs_code = data.get("hsCode", "")
    country_code = data.get("targetCountries", ["us"])[0]  # Default to 'us'

    # Step 1: Search for HS Code details
    hs_code_matches = search_hs_code(hs_code)

    # Step 2: Match dataset entry
    matched_entry = find_entry_by_hs_code(hs_code)

    if matched_entry:
        summary_prompt = (
            f"Convert this info into a proper document with relevant data from web if required, helping a small or middle scale business understand how to go about exporting, give proper instructions:\n"
            f"- Category: {matched_entry.get('category', 'Unknown')}\n"
            f"- Subcategory: {matched_entry.get('subcategory', 'Unknown')}\n"
            f"- Mandatory Requirements: {', '.join(matched_entry.get('mandatory_requirements', []))}\n"
            f"- Recommended Requirements: {', '.join(matched_entry.get('recommended_requirements', []))}\n"
            f"- Applicable Products: {', '.join(matched_entry.get('applicable_products', []))}\n"
            f"- FAQs: {json.dumps(matched_entry.get('faqs', {}), indent=2)}\n"
            f"- Reference Links: {', '.join(matched_entry.get('links', []))}\n"
        )
        product_summary = query_gemini(summary_prompt)
    else:
        product_summary = {"error": f"No matching entry found for HS Code {hs_code}"}

    # Step 3: Perform market analysis
    market_analysis = get_market_analysis(product_name, country_code)

    # Prepare response
    response = {
        "hsCodeDetails": hs_code_matches,
        "productSummary": product_summary,
        "marketAnalysis": market_analysis
    }

    return jsonify(response)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
