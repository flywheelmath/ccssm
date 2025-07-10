import json
import csv
import sys
import argparse

def convert_json_to_csv(json_path, csv_path, root_key="standards"):
    """
    Reads a JSON file containing a list of objects and converts it to a CSV file.
    It dynamically determines the headers from the keys of the first object.

    Args:
        json_path (str): The path to the input JSON file.
        csv_path (str): The path for the output CSV file.
        root_key (str): The top-level key in the JSON file that contains the list.
    """
    print(f"Attempting to read data from '{json_path}'...")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        records = data.get(root_key)
        if not records:
            print(f"Error: The JSON file does not contain a '{root_key}' list or the list is empty.", file=sys.stderr)
            return False

    except FileNotFoundError:
        print(f"Error: The file was not found at '{json_path}'", file=sys.stderr)
        return False
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file. Please check its format.", file=sys.stderr)
        return False

    print(f"Successfully loaded {len(records)} records. Now writing to '{csv_path}'...")

    try:
        headers = list(records[0].keys())

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(records)

        print(f"Successfully created CSV file at: {csv_path}")
        return True

    except Exception as e:
        print(f"An error occurred while writing the CSV file: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A generic script to convert a JSON file (containing a list of objects) to a CSV file."
    )
    parser.add_argument(
        "json_input", 
        help="The path to the input JSON file."
    )
    parser.add_argument(
        "csv_output", 
        help="The path for the output CSV file."
    )
    parser.add_argument(
        "--key", 
        default="standards", 
        help="The root key in the JSON file that holds the list of records (default: 'standards')."
    )

    args = parser.parse_args()

    convert_json_to_csv(args.json_input, args.csv_output, args.key)
