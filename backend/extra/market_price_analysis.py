import json
from typing import Dict, List, Union
import re
from statistics import mean, median
from datetime import datetime
import requests

with open("../apikeys.json", "r") as f:
    KEYS = json.load(f)


SERPAPI_API_KEY = KEYS["serpapi"]

serpapi_api_key = KEYS["serpapi"]  # Replace with your actual key


def get_google_search_results(product_name: str, country_code: str, serpapi_api_key: str) -> Dict:
    """
    Fetch Google search results for a product using SerpAPI with improved query structure.
    """
    url = "https://serpapi.com/search"
    query = f"{product_name} average price {datetime.now().year} retail"
    params = {
        "engine": "google",
        "q": query,
        "gl": country_code,
        "hl": "en",
        "api_key": serpapi_api_key,
        "num": 20,  # Fetch up to 20 results for sampling
        "tbs": "qdr:m"  # Results from the past month
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_price_info(json_data: Dict) -> List[Dict]:
    """
    Extract price-related information with improved price detection and validation.
    """
    price_pattern = r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?)'
    relevant_info = []
    
    for result in json_data.get('organic_results', []):
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        full_text = f"{title} {snippet}"
        
        # Find all prices in the text
        prices = []
        for match in re.finditer(price_pattern, full_text):
            try:
                price_str = match.group(1).replace(',', '')
                price = float(price_str)
                if 0.01 <= price <= 10000:  # Exclude unrealistic prices
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


def analyze_prices(relevant_info: List[Dict]) -> Dict:
    """
    Analyze extracted prices using statistical methods.
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


def get_price(product_name: str, country_code: str) -> Union[Dict, None]:
    """
    Fetch product prices, extract, and analyze price information, returning a JSON-friendly result.
    """
    try:
        search_results = get_google_search_results(product_name, country_code, serpapi_api_key)
        relevant_info = extract_price_info(search_results)
        
        if not relevant_info:
            return {"error": "No relevant price information found"}
        
        price_analysis = analyze_prices(relevant_info)
        
        if "error" in price_analysis:
            return {"error": price_analysis["error"]}
        
        # Include additional context about the product and search
        return {
            "product_name": product_name,
            "country_code": country_code,
            "price_analysis": price_analysis,
            "relevant_entries": relevant_info  # Optional: Return for debugging or transparency
        }
    
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


# For standalone testing
if __name__ == "__main__":
    product_name = "Handmade Leather Wallets"
    country_code = "us"
    result = get_price(product_name, country_code)
    print(result)
