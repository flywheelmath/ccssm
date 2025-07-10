import csv
import os

def validate_and_clean_dependency_file(input_filename="dependencies.csv", output_filename="dependencies_cleaned.csv"):
    """
    Validates a CSV file of dependencies for duplicates and logical consistency,
    and writes a cleaned version to a new file.

    Args:
        input_filename (str): The name of the CSV file to validate.
        output_filename (str): The name for the cleaned output CSV file.

    Returns:
        tuple: A tuple containing (list of errors, number of rows written).
    """
    # Dictionaries to store the relationship and the line number it was first seen on.
    dependencies = {}  # Stores (source, target) -> line_num
    related_pairs = {} # Stores canonical tuple(sorted(source, target)) -> line_num
    errors = []
    cleaned_rows = []
    header = []

    try:
        with open(input_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            try:
                header = next(reader)
                cleaned_rows.append(header)
            except StopIteration:
                return (["Error: CSV file is empty or has no header."], 0)
            
            for line_num, row in enumerate(reader, 2): # Start line count at 2
                if len(row) != 3:
                    errors.append(f"Line {line_num}: Invalid row format. Expected 3 columns, found {len(row)}. Skipping.")
                    continue

                source, target, relationship_type = [col.strip() for col in row]
                
                # Basic validation: ensure no empty cells
                if not all([source, target, relationship_type]):
                    errors.append(f"Line {line_num}: Row contains empty cells. Skipping.")
                    continue
                
                relationship_type_lower = relationship_type.lower()
                is_valid_row = True

                if relationship_type_lower == "dependency":
                    pair = (source, target)
                    reverse_pair = (target, source)

                    if pair in dependencies:
                        first_occurrence = dependencies[pair]
                        errors.append(f"Line {line_num}: Duplicate 'Dependency' row for ({source} -> {target}). First seen on line {first_occurrence}. Skipping.")
                        is_valid_row = False
                    
                    elif reverse_pair in dependencies:
                        first_occurrence = dependencies[reverse_pair]
                        errors.append(f"Line {line_num}: Asymmetry violation for 'Dependency'. Reverse relationship ({target} -> {source}) defined on line {first_occurrence}. Skipping.")
                        is_valid_row = False
                    
                    else:
                        dependencies[pair] = line_num

                elif relationship_type_lower == "related":
                    canonical_pair = tuple(sorted((source, target)))
                    
                    if canonical_pair in related_pairs:
                        first_occurrence = related_pairs[canonical_pair]
                        errors.append(f"Line {line_num}: Duplicate 'Related' relationship between '{source}' and '{target}'. First seen on line {first_occurrence}. Skipping.")
                        is_valid_row = False
                    else:
                        related_pairs[canonical_pair] = line_num

                else:
                    errors.append(f"Line {line_num}: Unknown relationship type '{relationship_type}'. Skipping.")
                    is_valid_row = False
                
                if is_valid_row:
                    cleaned_rows.append(row)

    except FileNotFoundError:
        return ([f"Error: The file '{input_filename}' was not found."], 0)
    except Exception as e:
        return ([f"An unexpected error occurred: {e}"], 0)

    # Post-check for conflicts between dependency and related types
    final_cleaned_rows_with_header = [header]
    final_cleaned_rows_no_header = []
    
    # We need to re-evaluate the cleaned rows for cross-type conflicts
    temp_dependencies = {tuple(row[:2]) for row in cleaned_rows[1:] if row[2].lower() == 'dependency'}
    temp_related = {tuple(sorted(row[:2])) for row in cleaned_rows[1:] if row[2].lower() == 'related'}

    for row in cleaned_rows[1:]:
        source, target, rel_type = row
        is_conflict = False
        if rel_type.lower() == 'dependency':
            if tuple(sorted((source, target))) in temp_related:
                errors.append(f"Conflict: A 'Dependency' and 'Related' relationship exist between '{source}' and '{target}'. Removing dependency.")
                is_conflict = True
        
        if not is_conflict:
            final_cleaned_rows_no_header.append(row)

    final_cleaned_rows_with_header.extend(final_cleaned_rows_no_header)


    # Write the cleaned data to the output file
    try:
        with open(output_filename, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(final_cleaned_rows_with_header)
    except IOError as e:
        errors.append(f"Error writing to output file '{output_filename}': {e}")
        return (errors, 0)
        
    return (errors, len(final_cleaned_rows_with_header) - 1)

if __name__ == "__main__":
    input_file = "dependencies.csv"
    output_file = "dependencies_cleaned.csv"
    
    validation_errors, written_count = validate_and_clean_dependency_file(input_file, output_file)

    if validation_errors:
        print(f"Validation found {len(validation_errors)} error(s):")
        for error in sorted(validation_errors):
            print(f"- {error}")
    else:
        print("Validation complete. No errors found.")
    
    if os.path.exists(output_file):
        print(f"\nSuccessfully wrote {written_count} cleaned rows to '{output_file}'.")


