import csv
import json
import sys

def build_k8_lookup_map(k8_json_path):
    """
    Reads the ccss-k8.json file and builds a lookup map from a short ID tuple
    to the full standard object.
    Key: (grade, domain, standard, substandard)
    Value: The full standard dictionary from the JSON
    """
    try:
        with open(k8_json_path, 'r', encoding='utf-8') as f:
            k8_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Could not read or parse the K-8 standards JSON file at '{k8_json_path}'. {e}", file=sys.stderr)
        return None

    lookup_map = {}
    for standard in k8_data.get('standards', []):
        # Create a key based on the components of a short ID
        key = (
            standard.get('grade_level_code'),
            standard.get('domain_code'),
            standard.get('standard_counter'),
            standard.get('substandard_counter')
        )
        lookup_map[key] = standard  # Store the whole object
    return lookup_map

def get_full_id(original_id, k8_lookup_map):
    """
    Takes an ID from the CSV, sanitizes it, and reconstructs the full canonical ID
    if it's a short K-8 ID by looking up the cluster code based on the new logic.
    """
    # First, perform basic sanitization (0 -> K)
    if original_id.startswith('0.'):
        original_id = 'K' + original_id[1:]
    
    parts = original_id.split('.')

    # Handle High School ID sanitization first, as it's a distinct pattern
    if len(parts) > 1 and parts[0] == 'HS' and len(parts[1]) == 1 and parts[1].isalpha():
        grade_part = parts[0] + parts[1]
        return ".".join([grade_part] + parts[2:])

    # Now, handle K-8 standards and check if they are short based on the new, precise logic
    if parts[0] in ['K', '1', '2', '3', '4', '5', '6', '7', '8']:
        is_short = False
        lookup_key = None
        last_part = parts[-1]

        # Case 1: Short substandard ID (e.g., 4.NF.3.a -> 4 components, last is lowercase)
        if len(parts) == 4 and last_part.islower() and len(last_part) == 1:
            is_short = True
            grade, domain, standard, substandard = parts[0], parts[1], parts[2], parts[3]
            lookup_key = (grade, domain, standard, substandard)

        # Case 2: Short standard ID (e.g., 3.NF.1 -> 3 components, last is a digit)
        elif len(parts) == 3 and last_part.isdigit():
            is_short = True
            grade, domain, standard = parts[0], parts[1], parts[2]
            substandard = None
            lookup_key = (grade, domain, standard, substandard)

        if is_short:
            match = k8_lookup_map.get(lookup_key)
            if match:
                # Reconstruct the full ID by inserting the found cluster code
                cluster = match.get('cluster_code')
                full_id_parts = [lookup_key[0], lookup_key[1], cluster, lookup_key[2]]
                if lookup_key[3]: # if substandard exists
                    full_id_parts.append(lookup_key[3])
                return ".".join(filter(None, full_id_parts))
            else:
                # If no match, we can't fix it, so we print a warning and return the original ID
                print(f"Warning: Could not find a match for short ID '{original_id}' in the K-8 lookup map.", file=sys.stderr)
                return original_id

    # If none of the short ID conditions were met, and it's not HS, it's a full ID. Return it as is.
    return original_id

def sanitize_relationship(relationship_str):
    """
    Sanitizes the relationship string to a consistent format.
    """
    if relationship_str.strip().lower() == 'dependency':
        return 'dependency'
    if relationship_str.strip().lower() == 'related':
        return 'conceptual connection'
    return relationship_str

def convert_csv_to_json(csv_file_path, k8_json_path):
    """
    Reads a CSV file of dependencies, sanitizes the data using a K-8 lookup file,
    and returns a JSON formatted string.
    """
    k8_lookup_map = build_k8_lookup_map(k8_json_path)
    if k8_lookup_map is None:
        return None # Stop if the K-8 lookup could not be built

    dependencies_list = []
    
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            if not all(field in csv_reader.fieldnames for field in ['source', 'target', 'relationship']):
                print("Error: CSV file must contain 'source', 'target', and 'relationship' columns.", file=sys.stderr)
                return None
            
            for row in csv_reader:
                # Sanitize source and target using the new lookup method
                sanitized_source = get_full_id(row['source'], k8_lookup_map)
                sanitized_target = get_full_id(row['target'], k8_lookup_map)
                sanitized_relation = sanitize_relationship(row['relationship'])
                
                dependencies_list.append({
                    "source": sanitized_source,
                    "target": sanitized_target,
                    "relationship": sanitized_relation
                })
                
    except FileNotFoundError:
        print(f"Error: The dependencies CSV file was not found at {csv_file_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return None
        
    final_json_structure = {"dependencies": dependencies_list}
    return json.dumps(final_json_structure, indent=2)

# --- Main execution ---
if __name__ == '__main__':
    # Define paths to your input files.
    # IMPORTANT: Replace these with the actual paths to your files.
    dependencies_csv_path = 'ccss-dependencies.csv' 
    k8_standards_path = 'ccss-k8.json'
    output_json_path = 'sanitized_dependencies.json'
    
    json_output = convert_csv_to_json(dependencies_csv_path, k8_standards_path)
    
    if json_output:
        try:
            with open(output_json_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"Successfully created sanitized JSON file at: {output_json_path}")
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)


