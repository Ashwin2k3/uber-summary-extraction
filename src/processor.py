import json
import re
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import openai
from src.config import OPENAI_API_KEY
from src.utility import save_uploaded_files
import tiktoken  # Import tiktoken for token counting
import json
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import openai
from src.config import OPENAI_API_KEY
from src.utility import save_uploaded_files
import tiktoken
import os
import os

# openai.api_key = OPENAI_API_KEY

# def convert_pdf_to_images(pdf_path):
#     """Convert a PDF into images."""
#     images = convert_from_path(pdf_path)
#     return images

# def convert_images_to_text(images):
#     """Convert extracted images to text using OCR."""
#     return " ".join(pytesseract.image_to_string(img) for img in images).strip()

import csv
import os

# Flattening function
def flatten_didi_data(structured_data, csv_file_path):
    flat_rows = []

    for entry in structured_data:
        for data_list in entry["data"]:
            for record in data_list:
                row = {
                    "Name": record.get("Name", ""),
                    "Address": record.get("Address", ""),
                    "Postal Code": record.get("Postal Code", ""),
                    "Country": record.get("Country", ""),
                    "ABN": record.get("ABN", ""),
                    "Tax Period": record.get("Tax Period", ""),
                    "Transportation Income": record.get("Transportation Income", ""),
                    "Delivery Income": record.get("Delivery Income", ""),
                    "Other Payments": record.get("Other Payments", ""),
                    "Total Payments": record.get("Total Payments", ""),
                    "On Trip Mileage": record.get("On Trip Mileage", ""),
                    "Trips": record.get("Trips", ""),
                    "Tips": record.get("Tips", ""),
                    
                    "Gross Transportation Fare": record.get("Gross Transportation Fare", ""),
                    "Split Fare": record.get("Split Fare", ""),
                    "Safe Rides Fee": record.get("Safe Rides Fee", ""),
                    "Tolls Reimbursement (Transport)": record.get("Tolls Reimbursement (Transport)", ""),
                    "Miscellaneous (Transport)": record.get("Miscellaneous (Transport)", ""),
                    "City Fee": record.get("City Fee", ""),
                    "Airport Fee": record.get("Airport Fee", ""),
                    "Booking Fee": record.get("Booking Fee", ""),
                    "Total Transportation Income": record.get("Total Transportation Income", ""),
                    
                    "Delivery Fee": record.get("Delivery Fee", ""),
                    "Delivery Incentives": record.get("Delivery Incentives", ""),
                    "Tolls Reimbursement (Delivery)": record.get("Tolls Reimbursement (Delivery)", ""),
                    "Total Delivery Income": record.get("Total Delivery Income", ""),
                    
                    "Miscellaneous (Other Payments)": record.get("Miscellaneous (Other Payments)", ""),
                    "Referral / Incentives": record.get("Referral / Incentives", ""),
                    "Tips (Other Payments)": record.get("Tips (Other Payments)", ""),
                    "Total Other Payments": record.get("Total Other Payments", ""),
                    
                    "Uber Service Fee (Transportation Leads)": record.get("Uber Service Fee (Transportation Leads)", ""),
                    "Other Charges from Uber": record.get("Other Charges from Uber", ""),
                    "Charges from 3rd Parties": record.get("Charges from 3rd Parties", ""),
                    "Total Potential Tax Deductions": record.get("Total Potential Tax Deductions", ""),
                    
                    "Tax Summary URL": record.get("Tax Summary URL", ""),
                    "Payout Details URL": record.get("Payout Details URL", "")
                }
                flat_rows.append(row)

    # Write to CSV
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=flat_rows[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(flat_rows)

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF, fallback to OCR if text is empty."""
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        text = page.get_text()
        if text.strip():  # If extractable text exists, use it
            full_text += text
        else:
            # Fallback to OCR
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            full_text += pytesseract.image_to_string(img)

    return full_text.strip()
import re
import json

import re

# def parse_tax_summary(text: str, request_id: str):
#     text = re.sub(r'[ ]{2,}', ' ', text)

#     def extract(pattern, group=1, default="", source=None):
#         src = source if source is not None else text
#         match = re.search(pattern, src, re.IGNORECASE)
#         return match.group(group).strip() if match and match.lastindex and match.lastindex >= group else default

#     def extract_amount(field, source_text):
#         pattern = rf"{re.escape(field)}\s*A?\$([\d.,]+)"
#         match = re.search(pattern, source_text, re.IGNORECASE)
#         return f"A${match.group(1)}" if match else "A$0.00"

#     data = {
#         "Name": extract(r"NAME:\s*(.*)"),
#         "Address": extract(r"ADDRESS:\s*(.*)"),
#         "Postal Code": extract(r"POSTAL\s*CODE:\s*(\d+)"),
#         "Country": extract(r"COUNTRY:\s*(.*)"),
#         "ABN": extract(r"ABN:\s*(\d+)"),
#         "Tax Period": extract(r"Tax Summary for the Period\s+(\d{2}/\d{4})"),
#         "Transportation Income": extract_amount("Transportation Income", text),
#         "Delivery Income": extract_amount("Delivery Income", text),
#         "Other Payments": extract_amount("Other Payments", text),
#         "Total Payments": extract_amount("Total Payments", text),
#         "On Trip Mileage": extract(r"ON TRIP DISTANCE\s+([\d.,]+\s*Km)"),
#         "Trips": extract(r"TRIPS\s*:\s*(\d+)"),
#         "Tips": extract_amount("Tips", text),

#         "Gross Transportation Fare": extract_amount("Gross Transportation Fare", text),
#         "Split Fare": extract_amount("Split Fare", text),
#         "Safe Rides Fee": extract_amount("Safe Rides Fee", text),
#         "Tolls Reimbursement (Transport)": extract_amount("Tolls Reimbursement \(Transport\)", text),
#         "Miscellaneous (Transport)": extract_amount("Miscellaneous \(Transport\)", text),
#         "City Fee": extract_amount("City Fee", text),
#         "Airport Fee": extract_amount("Airport Fee", text),
#         "Booking Fee": extract_amount("Booking Fee", text),
#         "Total Transportation Income": extract_amount("Total Transportation Income", text),

#         "Delivery Fee": extract_amount("Delivery Fee", text),
#         "Delivery Incentives": extract_amount("Delivery Incentives", text),
#         "Tolls Reimbursement (Delivery)": extract_amount("Tolls Reimbursement \(Delivery\)", text),
#         "Total Delivery Income": extract_amount("Total Delivery Income", text),

#         "Miscellaneous (Other Payments)": extract_amount("Miscellaneous \(Other Payments\)", text),
#         "Referral / Incentives": extract_amount("Referral / Incentives", text),
#         "Tips (Other Payments)": extract_amount("Tips \(Other Payments\)", text),
#         "Total Other Payments": extract_amount("Total Other Payments", text),

#         "Uber Service Fee (Transportation Leads)": extract_amount("Uber Service Fee \(Transportation Leads\)", text),
#         "Other Charges from Uber": extract_amount("Other Charges from Uber", text),
#         "Charges from 3rd Parties": extract_amount("Charges from 3rd Parties", text),
#         "Total Potential Tax Deductions": extract_amount("Total Potential Tax Deductions", text),

#         "Tax Summary URL": extract(r"Tax Summary URL:\s*(\S+)"),
#         "Payout Details URL": extract(r"Payout Details URL:\s*(\S+)")
#     }

#     return {
#         "message": "File uploaded and processed successfully",
#         "status": "success",
#         "status_code": 200,
#         "data": [[data]]
#     }


import re
#best 
# def parse_tax_summary(text: str, request_id: str):
#     # Normalize spaces
#     text = re.sub(r'[ ]{2,}', ' ', text)
#     lines = text.strip().splitlines()

#     def extract(pattern, group=1, default="", source=None):
#         src = source if source is not None else text
#         match = re.search(pattern, src, re.IGNORECASE)
#         return match.group(group).strip() if match and match.lastindex and match.lastindex >= group else default

#     def extract_amount(field, source_text):
#         pattern = rf"{re.escape(field)}\s*A?\$([\d.,]+)"
#         match = re.search(pattern, source_text, re.IGNORECASE)
#         return f"A${match.group(1)}" if match else "A$0.00"

#     # Extract Name from first line
#     name = lines[0].strip() if lines else ""

#     # Extract Address between Name and ABN
#     abn_match = re.search(r"(?:ABN|Australian Business Number \(ABN\))\s*:\s*(\d+)", text, re.IGNORECASE)
#     abn = abn_match.group(1) if abn_match else ""

#     address = ""
#     if abn_match:
#         abn_index = text.find(abn_match.group(0))
#         name_index = text.find(name)
#         address_section = text[name_index + len(name):abn_index]
#         address = re.sub(r'\s+', ' ', address_section).strip()

#     # Tax Period line comes after "Update tax information"
#     tax_period = ""
#     for idx, line in enumerate(lines):
#         if "Update tax information" in line:
#             if idx + 1 < len(lines):
#                 period_match = re.search(r"(\d{2}/\d{4})", lines[idx + 1])
#                 if period_match:
#                     tax_period = period_match.group(1)
#             break

#     data = {
#         "Name": name,
#         "Address": address,
#         "Postal Code": extract(r"POSTAL\s*CODE:\s*(\d+)"),
#         "Country": extract(r"COUNTRY:\s*(.*)"),
#         "ABN": abn,
#         "Tax Period": tax_period,

#         "Transportation Income": extract_amount("Transportation Income", text),
#         "Delivery Income": extract_amount("Delivery Income", text),
#         "Other Payments": extract_amount("Other Payments", text),
#         "Total Payments": extract_amount("Total Payments", text),
#         "On Trip Mileage": extract(r"ON TRIP DISTANCE\s+([\d.,]+\s*Km)"),
#         "Trips": extract(r"TRIPS\s*:\s*(\d+)"),
#         "Tips": extract_amount("Tips", text),

#         "Gross Transportation Fare": extract_amount("Gross Transportation Fare", text),
#         "Split Fare": extract_amount("Split Fare", text),
#         "Safe Rides Fee": extract_amount("Safe Rides Fee", text),
#         "Tolls Reimbursement (Transport)": extract_amount(r"Tolls Reimbursement \(Transport\)", text),
#         "Miscellaneous (Transport)": extract_amount(r"Miscellaneous \(Transport\)", text),
#         "City Fee": extract_amount("City Fee", text),
#         "Airport Fee": extract_amount("Airport Fee", text),
#         "Booking Fee": extract_amount("Booking Fee", text),
#         "Total Transportation Income": extract_amount("Total Transportation Income", text),

#         "Delivery Fee": extract_amount("Delivery Fee", text),
#         "Delivery Incentives": extract_amount("Delivery Incentives", text),
#         "Tolls Reimbursement (Delivery)": extract_amount(r"Tolls Reimbursement \(Delivery\)", text),
#         "Total Delivery Income": extract_amount("Total Delivery Income", text),

#         "Miscellaneous (Other Payments)": extract_amount(r"Miscellaneous \(Other Payments\)", text),
#         "Referral / Incentives": extract_amount("Referral / Incentives", text),
#         "Tips (Other Payments)": extract_amount(r"Tips \(Other Payments\)", text),
#         "Total Other Payments": extract_amount("Total Other Payments", text),

#         "Uber Service Fee (Transportation Leads)": extract_amount(r"Uber Service Fee \(Transportation Leads\)", text),
#         "Other Charges from Uber": extract_amount("Other Charges from Uber", text),
#         "Charges from 3rd Parties": extract_amount("Charges from 3rd Parties", text),
#         "Total Potential Tax Deductions": extract_amount("Total Potential Tax Deductions", text),

#         "Tax Summary URL": extract(r"Tax Summary URL:\s*(\S+)"),
#         "Payout Details URL": extract(r"Payout Details URL:\s*(\S+)")
#     }

#     return {
#         "message": "File uploaded and processed successfully",
#         "status": "success",
#         "status_code": 200,
#         "data": [[data]]
#     }


import re

# def parse_tax_summary(text: str, request_id: str):
#     text = re.sub(r'[ ]{2,}', ' ', text)
#     lines = text.strip().splitlines()

#     def extract(pattern, group=1, default="", source=None):
#         src = source if source is not None else text
#         match = re.search(pattern, src, re.IGNORECASE)
#         return match.group(group).strip() if match and match.lastindex and match.lastindex >= group else default

#     def extract_amount(field, source_text):
#         pattern = rf"{re.escape(field)}\s*A?\$([\d.,]+)"
#         match = re.search(pattern, source_text, re.IGNORECASE)
#         return f"A${match.group(1)}" if match else "A$0.00"

#     # Extract Name from first line
#     name = lines[0].strip() if lines else ""

#     # Extract Address between Name and ABN
#     abn_match = re.search(r"(?:ABN|Australian Business Number \(ABN\))\s*:\s*(\d+)", text, re.IGNORECASE)
#     abn = abn_match.group(1) if abn_match else ""

#     address = ""
#     if abn_match:
#         abn_index = text.find(abn_match.group(0))
#         name_index = text.find(name)
#         address_section = text[name_index + len(name):abn_index]
#         address = re.sub(r'\s+', ' ', address_section).strip()

#     # Tax Period line comes after "Update tax information"
#     tax_period = ""
#     for idx, line in enumerate(lines):
#         if "Update tax information" in line:
#             if idx + 1 < len(lines):
#                 period_match = re.search(r"(\d{2}/\d{4})", lines[idx + 1])
#                 if period_match:
#                     tax_period = period_match.group(1)
#             break

#     # On Trip Mileage: line above the one containing "On Trip Mileage"
#     on_trip_mileage = ""
#     for idx, line in enumerate(lines):
#         if "On Trip Mileage" in line:
#             if idx > 0:
#                 on_trip_mileage = lines[idx - 1].strip()
#             break

#     # Trips: line above the one containing "Trips"
#     trips = ""
#     for idx, line in enumerate(lines):
#         if re.match(r"^\s*Trips\s*:?", line, re.IGNORECASE):
#             if idx > 0:
#                 trips_line = lines[idx - 1].strip()
#                 trips_match = re.search(r"(\d+)", trips_line)
#                 if trips_match:
#                     trips = trips_match.group(1)
#             break

#     # Gross Transportation Fare: line below the one containing the label
#     gross_transport_fare = "A$0.00"
#     for idx, line in enumerate(lines):
#         if "Gross Transportation Fare" in line:
#             if idx + 1 < len(lines):
#                 amount_match = re.search(r"A\$([\d,]+\.\d{2})", lines[idx + 1])
#                 if amount_match:
#                     gross_transport_fare = f"A${amount_match.group(1)}"
#             break

#     data = {
#         "Name": name,
#         "Address": address,
#         "Postal Code": extract(r"POSTAL\s*CODE:\s*(\d+)"),
#         "Country": extract(r"COUNTRY:\s*(.*)"),
#         "ABN": abn,
#         "Tax Period": tax_period,

#         "Transportation Income": extract_amount("Transportation Income", text),
#         "Delivery Income": extract_amount("Delivery Income", text),
#         "Other Payments": extract_amount("Other Payments", text),
#         "Total Payments": extract_amount("Total Payments", text),
#         "On Trip Mileage": on_trip_mileage,
#         "Trips": trips,
#         "Tips": extract_amount("Tips", text),

#         "Gross Transportation Fare": gross_transport_fare,
#         "Split Fare": extract_amount("Split Fare", text),
#         "Safe Rides Fee": extract_amount("Safe Rides Fee", text),
#         "Tolls Reimbursement (Transport)": extract_amount(r"Tolls Reimbursement \(Transport\)", text),
#         "Miscellaneous (Transport)": extract_amount(r"Miscellaneous \(Transport\)", text),
#         "City Fee": extract_amount("City Fee", text),
#         "Airport Fee": extract_amount("Airport Fee", text),
#         "Booking Fee": extract_amount("Booking Fee", text),
#         "Total Transportation Income": extract_amount("Total Transportation Income", text),

#         "Delivery Fee": extract_amount("Delivery Fee", text),
#         "Delivery Incentives": extract_amount("Delivery Incentives", text),
#         "Tolls Reimbursement (Delivery)": extract_amount(r"Tolls Reimbursement \(Delivery\)", text),
#         "Total Delivery Income": extract_amount("Total Delivery Income", text),

#         "Miscellaneous (Other Payments)": extract_amount(r"Miscellaneous \(Other Payments\)", text),
#         "Referral / Incentives": extract_amount("Referral / Incentives", text),
#         "Tips (Other Payments)": extract_amount(r"Tips \(Other Payments\)", text),
#         "Total Other Payments": extract_amount("Total Other Payments", text),

#         "Uber Service Fee (Transportation Leads)": extract_amount(r"Uber Service Fee \(Transportation Leads\)", text),
#         "Other Charges from Uber": extract_amount("Other Charges from Uber", text),
#         "Charges from 3rd Parties": extract_amount("Charges from 3rd Parties", text),
#         "Total Potential Tax Deductions": extract_amount("Total Potential Tax Deductions", text),

#         "Tax Summary URL": extract(r"Tax Summary URL:\s*(\S+)"),
#         "Payout Details URL": extract(r"Payout Details URL:\s*(\S+)")
#     }

#     return {
#         "message": "File uploaded and processed successfully",
#         "status": "success",
#         "status_code": 200,
#         "data": [[data]]
#     }


import re

def parse_tax_summary(text: str, request_id: str):
    text = re.sub(r'[ ]{2,}', ' ', text)
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    def extract(pattern, group=1, default="", source=None):
        src = source if source is not None else text
        match = re.search(pattern, src, re.IGNORECASE)
        return match.group(group).strip() if match and match.lastindex and match.lastindex >= group else default

    def extract_amount_after(label):
        for i, line in enumerate(lines):
            if label.lower() in line.lower():
                if i + 1 < len(lines):
                    amt_match = re.search(r"A\$([\d,.]+)", lines[i + 1])
                    if amt_match:
                        return f"A${amt_match.group(1)}"
        return "A$0.00"

    def extract_above(keyword):
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower() and i > 0:
                return lines[i - 1]
        return ""

    def extract_tax_period():
        for i, line in enumerate(lines):
            if "update tax information" in line.lower():
                for j in range(i+1, min(i+4, len(lines))):
                    if re.search(r"\d{2}-\d{2} \w+ \d{4}", lines[j]):
                        return lines[j]
        return extract(r"Tax summary\s*-\s*(\d{2}-\d{2} \w+ \d{4})")
    
    def extract_trips():
        for i, line in enumerate(lines):
            if "trips" in line.lower():
                if i > 0:
                    trips_line = lines[i - 1]
                    trips_match = re.search(r"\b(\d+)\b", trips_line)
                    if trips_match:
                        return trips_match.group(1)
        return ""


    # Extract base info
    name = lines[0]
    abn = extract(r"(?:ABN|Australian Business Number \(ABN\))\s*:\s*(\d+)")
    address_block = []
    for i in range(len(lines)):
        if name in lines[i]:
            for j in range(i+1, i+4):
                if 'ABN' in lines[j] or 'Australian Business Number' in lines[j]:
                    break
                address_block.append(lines[j])
            break
    address = ' '.join(address_block).strip()
    postal_match = re.search(r"\b(\d{4})\b", address)
    postal_code = postal_match.group(1) if postal_match else ""
    country = "Australia" if "Australia" in address else ""

    tax_period = extract_tax_period()

    # Extract values from context
    on_trip_mileage = extract_above("on trip mileage")
    # trips = extract_above("trips")
    trips = extract_trips()
    tips = extract_amount_after("Tips")

    # Extract money fields
    gross_transport_fare = extract_amount_after("Gross transportation fare")
    transportation_income = extract_amount_after("Transportation Income")
    delivery_income = extract_amount_after("Delivery Income")
    other_payments = extract_amount_after("Other Payments")
    total_payments = extract_amount_after("Total Payments")

    split_fare = extract_amount_after("Split fare")
    safe_rides_fee = extract_amount_after("Safe Rides Fee")
    tolls_transport = extract_amount_after("Tolls Reimbursement")
    misc_transport = extract_amount_after("Miscellaneous")
    city_fee = extract_amount_after("City fee")
    airport_fee = extract_amount_after("Airport fee")
    booking_fee = extract_amount_after("Booking fee")
    total_transport_income = extract_amount_after("Total Transportation Income")

    delivery_fee = extract_amount_after("Delivery Fee")
    delivery_incentives = extract_amount_after("Delivery Incentives")
    tolls_delivery = extract_amount_after("Tolls Reimbursement")
    total_delivery_income = extract_amount_after("Total Delivery Income")

    misc_other = extract_amount_after("Miscellaneous")
    referral = extract_amount_after("Referral / Incentives")
    tips_other = extract_amount_after("Tips")
    total_other_payments = extract_amount_after("Total Other Payments")

    uber_service_fee = extract_amount_after("Uber service fee")
    other_charges = extract_amount_after("Other charges from Uber")
    charges_3rd = extract_amount_after("Charges from 3rd parties")
    total_deductions = extract_amount_after("Total Potential Tax Deductions")

    tax_summary_url = extract(r"(https:\/\/drivers\.uber\.com\/p3\/tax-compliance\/profile)")
    payout_details_url = extract(r"(https:\/\/drivers\.uber\.com\/p3\/payments\/statements)")

    data = {
        "Name": name,
        "Address": address,
        "Postal Code": postal_code,
        "Country": country,
        "ABN": abn,
        "Tax Period": tax_period,

        "Transportation Income": transportation_income,
        "Delivery Income": delivery_income,
        "Other Payments": other_payments,
        "Total Payments": total_payments,
        "On Trip Mileage": on_trip_mileage,
        "Trips": trips,
        "Tips": tips,

        "Gross Transportation Fare": gross_transport_fare,
        "Split Fare": split_fare,
        "Safe Rides Fee": safe_rides_fee,
        "Tolls Reimbursement (Transport)": tolls_transport,
        "Miscellaneous (Transport)": misc_transport,
        "City Fee": city_fee,
        "Airport Fee": airport_fee,
        "Booking Fee": booking_fee,
        "Total Transportation Income": total_transport_income,

        "Delivery Fee": delivery_fee,
        "Delivery Incentives": delivery_incentives,
        "Tolls Reimbursement (Delivery)": tolls_delivery,
        "Total Delivery Income": total_delivery_income,

        "Miscellaneous (Other Payments)": misc_other,
        "Referral / Incentives": referral,
        "Tips (Other Payments)": tips_other,
        "Total Other Payments": total_other_payments,

        "Uber Service Fee (Transportation Leads)": uber_service_fee,
        "Other Charges from Uber": other_charges,
        "Charges from 3rd Parties": charges_3rd,
        "Total Potential Tax Deductions": total_deductions,

        "Tax Summary URL": tax_summary_url,
        "Payout Details URL": payout_details_url
    }

    return {
        "message": "File uploaded and processed successfully",
        "status": "success",
        "status_code": 200,
        "data": [[data]]
    }

# Example test block    

def process_pdfs(files):
    """Process uploaded PDF files."""
    file_paths = save_uploaded_files(files)
    structured_data = []


    for pdf_path in file_paths:

        # append the pdf file name contaning the request ID 
        # file_name = os.path.splitext(pdf_path)[0]
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Extract file name without extension

        request_id = file_name.split('_')[0]

        # images = convert_pdf_to_images(pdf_path)
        # extracted_text = convert_images_to_text(images)
        extracted_text = extract_text_from_pdf(pdf_path)
        json_data = result = parse_tax_summary(extracted_text, request_id="DiDi Tax Summary 202307")
        print(json.dumps(result, indent=4)) #extract_structured_data(extracted_text)

        # appending the request ID in json_data
         # Check if json_data is a list and update each dictionary
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    item["request_id"] = request_id
        elif isinstance(json_data, dict):  # If it's a single dictionary, just add request_id
            json_data["request_id"] = request_id
        
        structured_data.append(json_data)



    return structured_data

