import requests

HTS_BASE_URL = "https://hts.usitc.gov/reststop/search"

def search_hs_code(hs_code):
    """
    Search for the HS code in the dataset and return matching data including tariff rates.
    """
    try:
        params = {"keyword": hs_code}
        response = requests.get(HTS_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract descriptions and tariff rates
        results = []
        for result in data:
            if "description" in result:
                results.append({
                    "description": result.get("description", ""),
                    "tariff_rates": {
                        "general": result.get("general", "N/A"),
                        "special": result.get("special", "N/A"),
                        "other": result.get("other", "N/A")
                    }
                })
        return results
    except Exception as e:
        print(f"Error searching HS code: {e}")
        return []

if __name__ == "__main__":
    # Example HS code to test
    hs_code = "4202.31.30"
    results = search_hs_code(hs_code)

    # Print the results
    print("=== Search Results ===")
    for result in results:
        print(f"Description: {result['description']}")
        print(f"Tariff Rates:")
        print(f"  General: {result['tariff_rates']['general']}")
        print(f"  Special: {result['tariff_rates']['special']}")
        print(f"  Other: {result['tariff_rates']['other']}")
        print("-" * 40)
