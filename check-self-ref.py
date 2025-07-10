import csv
import sys

def find_self_dependencies(csv_file_path):
    """
    Scans a CSV file for rows where the 'source' and 'target' columns
    have the same value.

    Args:
        csv_file_path (str): The path to the CSV file to check.
    """
    print(f"--- Scanning '{csv_file_path}' for self-referencing dependencies ---")
    
    found_issues = False
    
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            # Using DictReader to access columns by name
            csv_reader = csv.DictReader(csv_file)
            
            # Check if required columns exist
            if not all(field in csv_reader.fieldnames for field in ['source', 'target']):
                print("Error: CSV file must contain 'source' and 'target' columns.", file=sys.stderr)
                return

            for i, row in enumerate(csv_reader):
                line_number = i + 2  # +1 for header, +1 for 0-based index
                source_id = row.get('source', '').strip()
                target_id = row.get('target', '').strip()

                if source_id and target_id and source_id == target_id:
                    print(f"  [!] Issue found on line {line_number}: Source and Target are the same.")
                    print(f"      - ID: {source_id}")
                    found_issues = True

    except FileNotFoundError:
        print(f"Error: The file was not found at '{csv_file_path}'", file=sys.stderr)
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}", file=sys.stderr)
        return

    if not found_issues:
        print("--- Scan complete. No self-referencing dependencies found. ---")
    else:
        print("--- Scan complete. ---")


# --- Main execution ---
if __name__ == '__main__':
    # IMPORTANT: Replace this with the actual path to your CSV file.
    # It assumes the CSV is in the same directory as this script.
    dependencies_csv_path = 'ccss_dependencies.csv' 
    
    find_self_dependencies(dependencies_csv_path)


