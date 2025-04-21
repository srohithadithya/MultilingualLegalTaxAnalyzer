import re

def analyze_and_structure_parsed_data(text):
    """
    Extracts structured data using regex patterns.
    """
    def extract_field(pattern, text, default="Not Found"):
        match = re.search(pattern, text)
        return match.group(1) if match else default

    structured_data = {
        "Client Name": extract_field(r"Client Name:\s*(.+)", text),
        "PII Data": {
            "PAN": extract_field(r"PAN:\s*([A-Z]{5}[0-9]{4}[A-Z])", text),
            "GSTIN": extract_field(r"GSTIN:\s*(\d{2}[A-Z]{5}\d{4}[A-Z]\d[Z]\d)", text),
        },
        "Nature of Notice": extract_field(r"Nature of Notice:\s*(.+)", text),
        "Deadlines and Penalties": {
            "Deadline": extract_field(r"Deadline:\s*(\d{4}-\d{2}-\d{2})", text),
            "Penalty": extract_field(r"Penalty:\s*(₹[0-9,]+)", text),
        },
        "Reporting Officer/Office": extract_field(r"Reporting Officer:\s*(.+)", text),
        "Relevant Legal Sections": re.findall(r"Section\s\d+\(\d+\)", text),
    }
    return structured_data