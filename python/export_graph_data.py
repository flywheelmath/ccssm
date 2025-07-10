import json
import sys
import argparse

def generate_graph_data(k8_path, hs_path, deps_path, output_path):
    """
    Reads standards and dependencies from JSON files and creates a single
    JSON file formatted for D3.js force-directed graphs.
    This script is a standalone replacement for the Django management command.

    Args:
        k8_path (str): Path to the ccssm-k8.json file.
        hs_path (str): Path to the ccssm-hs.json file.
        deps_path (str): Path to the sanitized_dependencies.json file.
        output_path (str): Path for the output graph_data.json file.
    """
    print("Starting graph data export...")

    try:
        with open(k8_path, 'r', encoding='utf-8') as f:
            k8_standards = json.load(f).get("standards", [])
        print(f"Loaded {len(k8_standards)} K-8 standards from '{k8_path}'.")

        with open(hs_path, 'r', encoding='utf-8') as f:
            hs_standards = json.load(f).get("standards", [])
        print(f"Loaded {len(hs_standards)} High School standards from '{hs_path}'.")

        with open(deps_path, 'r', encoding='utf-8') as f:
            dependencies = json.load(f).get("dependencies", [])
        print(f"Loaded {len(dependencies)} dependencies from '{deps_path}'.")

    except FileNotFoundError as e:
        print(f"Error: Input file not found. {e}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from a file. Please check its format. {e}", file=sys.stderr)
        return False

    nodes = []
    
    category_names = {
        "N": "Number & Quantity", "A": "Algebra", "F": "Functions",
        "G": "Geometry", "S": "Statistics & Probability"
    }

    all_standards = k8_standards + hs_standards
    for std in all_standards:
        grade_part = std.get('grade_level_code')
        if grade_part == 'HS' and std.get('category_code'):
            grade_part += std.get('category_code')
        
        id_parts = [
            grade_part,
            std.get('domain_code'),
            std.get('cluster_code'),
            std.get('standard_counter'),
            std.get('substandard_counter')
        ]

        node_id = ".".join([str(p) for p in id_parts if p is not None])
        group = f"Grade {std.get('grade_level_code')}"
        if std.get('grade_level_code') == 'HS':
            group = category_names.get(std.get('category_code'), "High School")

        nodes.append({
            "id": node_id,
            "description": std.get('description', ''),
            "group": group
        })

    links = []
    for dep in dependencies:
        links.append({
            "source": dep.get("source"),
            "target": dep.get("target"),
            "type": dep.get("relationship", "dependency").replace("_", " ").title()
        })

    graph_data = {
        "nodes": nodes,
        "links": links
    }

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2)
        print(f"\nSuccessfully exported data for {len(nodes)} nodes and {len(links)} links to '{output_path}'")
        return True
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate a D3.js graph JSON file from standards and dependency JSON files."
    )
    parser.add_argument("--k8-file", default="../json/ccssm-k8.json", help="Path to the K-8 standards JSON file.")
    parser.add_argument("--hs-file", default="../json/ccssm-hs.json", help="Path to the High School standards JSON file.")
    parser.add_argument("--deps-file", default="../json/ccssm-dependencies.json", help="Path to the sanitized dependencies JSON file.")
    parser.add_argument("--output", default="../graph_data.json", help="Path for the output graph_data.json file.")

    args = parser.parse_args()
    generate_graph_data(args.k8_file, args.hs_file, args.deps_file, args.output)
