import json
import requests
import re
from statistics import mean, median
from datetime import datetime

# Load API keys from configuration file
with open("apikeys.json", "r") as f:
    KEYS = json.load(f)

SERPAPI_API_KEY = KEYS["serpapi"]

def get_google_search_results(product_name: str, country_code: str) -> dict:
    """
    Fetch Google search results for a product using SerpAPI.
    """
    url = "https://serpapi.com/search"
    query = f"{product_name} average price {datetime.now().year} retail"
    params = {
        "engine": "google",
        "q": query,
        "gl": country_code,
        "hl": "en",
        "api_key": SERPAPI_API_KEY,
        "num": 20,
        "tbs": "qdr:m"  # Results from the last month
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return {"error": str(e)}


def extract_price_info(json_data: dict) -> list:
    """
    Extract price-related information from SerpAPI results.
    """
    price_pattern = r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?)'
    relevant_info = []

    for result in json_data.get('organic_results', []):
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        full_text = f"{title} {snippet}"

        # Extract prices
        prices = []
        for match in re.finditer(price_pattern, full_text):
            try:
                price_str = match.group(1).replace(',', '')
                price = float(price_str)
                if 0.01 <= price <= 10000:  # Filter out unrealistic values
                    prices.append(price)
            except (ValueError, IndexError):
                continue

        if prices:
            relevant_info.append({
                "title": title,
                "link": result.get('link', ''),
                "snippet": snippet,
                "found_prices": prices
            })

    return relevant_info


def analyze_prices(relevant_info: list) -> dict:
    """
    Analyze prices using statistical methods.
    """
    all_prices = [price for info in relevant_info for price in info['found_prices']]

    if not all_prices:
        return {"error": "No valid prices found"}

    return {
        "median_price": median(all_prices),
        "average_price": mean(all_prices),
        "min_price": min(all_prices),
        "max_price": max(all_prices),
        "price_count": len(all_prices),
        "suggested_price": median(all_prices)  # Use median for robustness
    }


def get_market_analysis(product_name: str, country_code: str) -> dict:
    """
    Perform market analysis for the product by fetching and analyzing prices.
    """
    serp_results = get_google_search_results(product_name, country_code)
    if "error" in serp_results:
        return {"error": serp_results["error"]}

    relevant_info = extract_price_info(serp_results)
    return analyze_prices(relevant_info)

if __name__ == "__main__":
    product_name = "Handmade Leather Wallets"
    country_code = "us"
    result = get_market_analysis(product_name, country_code)
    print(result)
