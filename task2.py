import csv
import json
import multiprocessing as mp

# Masking functions
def mask_name(name):
    parts = name.split()
    masked = []
    for part in parts:
        masked.append(part[0] + '*' * (len(part) - 1))
    return ' '.join(masked)

def mask_email(email):
    local, domain = email.split('@')
    return '*@' + domain

def mask_phone(phone):
    return '--' + phone[-4:]

def mask_ssn(ssn):
    return '--*'

# Function to apply masking rules to each row
def apply_masking(row, rules):
    masked_row = {}
    for key, value in row.items():
        if key == 'Name' and rules[key] == 'partial':
            masked_row[key] = mask_name(value)
        elif key == 'Email' and rules[key] == 'domain':
            masked_row[key] = mask_email(value)
        elif key == 'Phone' and rules[key] == 'last4':
            masked_row[key] = mask_phone(value)
        elif key == 'SSN' and rules[key] == 'full':
            masked_row[key] = mask_ssn(value)
        else:
            masked_row[key] = value
    return masked_row

# Main function
def mask_data(input_csv, rules_json, output_csv):
    with open(rules_json, 'r') as f:
        rules = json.load(f)
    
    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    with mp.Pool(mp.cpu_count()) as pool:
        masked_rows = pool.starmap(apply_masking, [(row, rules) for row in rows])
    
    with open(output_csv, 'w', newline='') as f:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(masked_rows)

mask_data('data.csv', 'rules.json', 'masked_data.csv')