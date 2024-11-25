import requests
import json

# API Base URL
BASE_URL = "http://127.0.0.1:5000"  # Change this to your server's URL if not running locally

def test_submit_form():
    """
    Test the `/submit-form` endpoint.
    """
    # Sample input payload
    sample_payload = {
        "productName": "Handmade Leather Wallets",
        "productDescription": "High-quality leather wallets handcrafted by local artisans. Made with 100% genuine cowhide leather, featuring multiple card slots, a coin pouch, and a sleek design suitable for all genders. Available in various colors and finishes.",
        "hsCode": "4202.31.30",
        "category": "Fashion Accessories",
        "targetCountries": ["us", "eu"],
        "certifications": "ISO 9001, Leather Working Group Certification",
        "unitValue": "25"
    }

    try:
        # Send POST request to `/submit-form` endpoint
        response = requests.post(f"{BASE_URL}/submit-form", json=sample_payload)

        # Check the response status
        if response.status_code == 200:
            print("Test Passed: Status Code 200")
        else:
            print(f"Test Failed: Unexpected Status Code {response.status_code}")
            return

        # Parse and display the response
        response_data = response.json()
        print("\n=== Response Data ===")
        print(json.dumps(response_data, indent=4))
        with open("output.json", 'w', encoding='utf-8') as jsonfile:
            json.dump(response_data, jsonfile, ensure_ascii=False, indent=4)

        # Additional validation checks (optional)
        assert "hsCodeDetails" in response_data, "Missing `hsCodeDetails` in response"
        assert "productSummary" in response_data, "Missing `productSummary` in response"
        assert "marketAnalysis" in response_data, "Missing `marketAnalysis` in response"

        print("\nAll checks passed!")

    except requests.exceptions.RequestException as e:
        print(f"Test Failed: Request Exception - {e}")
    except AssertionError as e:
        print(f"Test Failed: {e}")


if __name__ == "__main__":
    print("Running API Tests...\n")
    test_submit_form()
