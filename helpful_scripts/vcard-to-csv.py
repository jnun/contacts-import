# Note: Portions of this code may have been generated with AI assistance.
#
# Convert a vcaard 3.0 export to a mapped CSV, for importing to a CRM or
# database more easily.

import csv
from tqdm import tqdm

# Field sanitization to remove unnecessary characters
def sanitize_field(value):
    """
    Remove unnecessary backslashes from the value.
    """
    if value and isinstance(value, str):
        return value.replace(r"\,", ",").strip()
    return value

# Address parsing logic
def parse_address_field(line, prefix):
    """
    Parse an address field into its components (po_box, extended, street, city, state, postal_code, country).
    """
    parts = line.split(":", 1)[1].split(";")
    address_field_mapping = ["po_box", "extended", "street", "city", "state", "postal_code", "country"]
    return {
        f"{prefix}_{subfield}": sanitize_field(parts[idx]) if idx < len(parts) else None
        for idx, subfield in enumerate(address_field_mapping)
    }

# Organization parsing logic
def parse_org_field(line):
    """
    Parse the ORG: field into organization components.
    """
    parts = line.split(":", 1)[1].split(";")
    return {
        "org": parts[0].strip() if len(parts) > 0 else None,
        "org_department": parts[1].strip() if len(parts) > 1 else None,
        "org_division": parts[2].strip() if len(parts) > 2 else None,
        "org_team": parts[3].strip() if len(parts) > 3 else None,
    }

# Social media parsing logic
def parse_social_media(line):
    """
    Parse social media fields dynamically based on type.
    """
    social_media_mapping = {
        "type=instagram": "social_instagram",
        "type=telegram": "social_telegram",
        "type=facebook": "social_facebook",
        "type=twitter": "social_x",
        "type=linkedin": "social_linkedin",
    }
    for key, column in social_media_mapping.items():
        if key in line.lower():
            value = line.split(":", 1)[1].strip()
            return {column: value}
    return {}

# Main parsing function for a vCard line
def parse_vcard_line(line):
    """
    Parse a single vCard line and return a dictionary of parsed fields.
    """
    field_data = {}

    # Skip lines without a colon
    if ":" not in line:
        return field_data

    # Parse specific fields
    if "URL" in line:
        if "type=HOME" in line:
            field_data["website_personal"] = sanitize_field(line.split(":", 1)[1])
        elif "type=WORK" in line:
            field_data["website_business"] = sanitize_field(line.split(":", 1)[1])
        else:
            field_data["website_other"] = sanitize_field(line.split(":", 1)[1])

    elif "ADR" in line:
        if "type=HOME" in line:
            field_data.update(parse_address_field(line, "address_personal"))
        elif "type=WORK" in line:
            field_data.update(parse_address_field(line, "address_business"))

    elif "X-SOCIALPROFILE" in line:
        field_data.update(parse_social_media(line))

    elif line.startswith("FN:"):
        field_data["name_full"] = sanitize_field(line.split(":", 1)[1])
    elif line.startswith("N:"):
        parts = line[2:].split(";")
        field_data.update({
            "name_last": sanitize_field(parts[0]) if len(parts) > 0 else None,
            "name_first": sanitize_field(parts[1]) if len(parts) > 1 else None,
            "name_middle": sanitize_field(parts[2]) if len(parts) > 2 else None,
            "name_prefix": sanitize_field(parts[3]) if len(parts) > 3 else None,
            "name_suffix": sanitize_field(parts[4]) if len(parts) > 4 else None,
        })
    elif line.startswith("ORG:"):
        field_data.update(parse_org_field(line))
    elif line.startswith("TITLE:"):
        field_data["title"] = sanitize_field(line.split(":", 1)[1])
    elif line.startswith("NOTE:"):
        field_data["note"] = sanitize_field(line.split(":", 1)[1])
    elif line.startswith("TEL"):
        if "type=WORK" in line:
            field_data["phone_work"] = sanitize_field(line.split(":", 1)[1])
        elif "type=CELL" in line:
            field_data["phone_cell"] = sanitize_field(line.split(":", 1)[1])
    return field_data

# Process the entire vCard file
def process_vcard(file_path):
    """
    Process the vCard file line-by-line and return a list of parsed records.
    """
    records = []
    current_record = {}

    with open(file_path, 'r', encoding='utf-8') as vcard_file:
        with tqdm(desc="Processing vCard", unit="line") as pbar:
            for line in vcard_file:
                line = line.strip()
                pbar.update(1)

                if not line:
                    continue
                if line.startswith("BEGIN:VCARD"):
                    current_record = {}
                elif line.startswith("END:VCARD"):
                    if current_record:
                        records.append(current_record)
                    current_record = {}
                else:
                    current_record.update(parse_vcard_line(line))

    print(f"Total records processed: {len(records)}")
    return records

# Save the parsed records to a CSV file
def save_to_csv(records, output_file):
    """
    Save parsed records to a CSV file.
    """
    if not records:
        print("No records to save.")
        return

    headers = {key for record in records for key in record.keys()}
    headers = sorted(headers)

    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {output_file}")

# Main entry point
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python vcard-to-csv.py input.vcf output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    records = process_vcard(input_file)
    save_to_csv(records, output_file)
