import os
import json
import re
from typing import Dict, List
import pdfplumber
import requests


def extract_requirements(content: str) -> Dict[str, List[str]]:
    requirements = {'mandatory': [], 'recommended': []}
    
    # Extract Mandatory Requirements
    mandatory_match = re.search(r'(Mandatory requirements.*?)(Recommended requirements|FAQs:|Applicable to:|$)', content, re.DOTALL | re.IGNORECASE)
    if mandatory_match:
        mandatory_text = mandatory_match.group(1)
        requirements['mandatory'] = [req.strip() for req in re.findall(r'(?:\([a-z]\)|\•|\-)\s*(.+?)(?:\n|$)', mandatory_text)]
    
    # Extract Recommended Requirements
    recommended_match = re.search(r'(Recommended requirements.*?)(FAQs:|Applicable to:|$)', content, re.DOTALL | re.IGNORECASE)
    if recommended_match:
        recommended_text = recommended_match.group(1)
        requirements['recommended'] = [req.strip() for req in re.findall(r'(?:\([a-z]\)|\•|\-)\s*(.+?)(?:\n|$)', recommended_text)]
    
    return requirements


def extract_applicable_products(content: str) -> List[str]:
    applicable_match = re.search(r'Applicable (?:to|products):(.*?)(?:FAQs:|$)', content, re.DOTALL | re.IGNORECASE)
    if applicable_match:
        products_text = applicable_match.group(1)
        return [product.strip() for product in re.split(r',|\n', products_text) if product.strip()]
    return []


def extract_faqs(content: str) -> Dict[str, str]:
    faqs = {}
    faq_match = re.search(r'FAQs:(.*?)(?:Additional requirements:|Disclaimer:|$)', content, re.DOTALL | re.IGNORECASE)
    if faq_match:
        faq_text = faq_match.group(1)
        qa_pairs = re.findall(r'(\d+[\.\)]\s+.*?)(?=\d+[\.\)]|$)', faq_text, re.DOTALL)
        for qa in qa_pairs:
            question, _, answer = qa.partition('\n')
            if question and answer:
                faqs[question.strip()] = answer.strip()
    return faqs


def extract_links(content: str) -> List[str]:
    cleaned_content = re.sub(r"\n(?! )", "", content)  # Preserve proper formatting
    links = re.findall(r'(https://.*?)([\s\(\n|]|Disclaimer)', cleaned_content)
    links = [link.strip('.,:;)') for link, _ in links]
    return links


def process_pdfs_from_folder(folder_path: str) -> List[Dict]:
    processed_data = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            try:
                content = ""
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        content += page.extract_text() + "\n"
                
                source = filename
                category = source.split('-')[0].strip()
                subcategory = source.split('-')[1].split('_')[0].strip() if '-' in source else ''
                
                requirements = extract_requirements(content)
                applicable_products = extract_applicable_products(content)
                faqs = extract_faqs(content)
                links = extract_links(content)
                
                doc_data = {
                    'source': source,
                    'category': category,
                    'subcategory': subcategory,
                    'mandatory_requirements': requirements['mandatory'],
                    'recommended_requirements': requirements['recommended'],
                    'applicable_products': applicable_products,
                    'faqs': faqs,
                    'links': links
                }
                processed_data.append(doc_data)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    return processed_data


def search_hts(keywords):
    """
    Search the HTS API using a combined keyword query and return only HS codes.
    """
    BASE_URL = "https://hts.usitc.gov/reststop/search"
    params = {"keyword": keywords}
    results = []

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):  # Check if valid data returned
            results = [result.get("htsno", "N/A") for result in data if "htsno" in result]

        return list(set(results))  # Ensure unique HS codes
    except Exception as e:
        print(f"Error searching HTS for '{keywords}': {e}")
        return []


def map_hs_codes(processed_data: List[Dict]) -> List[Dict]:
    """
    Map HS codes to processed data entries using HTS API.
    """
    for entry in processed_data:
        # Combine category, subcategory, and applicable products into a single search string
        keywords = f"{entry.get('category', '')} {entry.get('subcategory', '')} " + \
                   " ".join(entry.get("applicable_products", []))

        if keywords.strip():
            print(f"Searching for HS codes related to: {keywords}")
            entry["hs_codes"] = search_hts(keywords)  # Append only the HS codes

    return processed_data


def save_to_json(data: List[Dict], output_file: str = 'processed_documents_with_hs_codes.json'):
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)


def main():
    folder_path = 'pdfs'  # Replace with your folder path
    processed_data = process_pdfs_from_folder(folder_path)
    print(f"Processed {len(processed_data)} documents.")

    # Map HS codes automatically
    processed_data = map_hs_codes(processed_data)

    # Save the final data
    save_to_json(processed_data, "dataset.json")
    print(f"HS Code mapping completed and saved to processed_documents_with_hs_codes.json")


if __name__ == "__main__":
    main()
