# your_app/management/commands/export_graph_data.py

import json
from django.core.management.base import BaseCommand
from django.db import transaction
from schemas.models import CCSSStandard, CCSSStandardDependency

class Command(BaseCommand):
    """
    A Django management command to export the CCSS standards and their
    dependencies into a JSON file suitable for D3.js force-directed graphs.
    """
    help = 'Exports standards and dependencies to a graph_data.json file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='The path to the output JSON file.',
            default='graph_data.json'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """
        The main logic of the command.
        """
        output_path = options['output']
        self.stdout.write(self.style.SUCCESS("Starting to export graph data..."))

        # --- Step 1: Fetch all standards for the 'nodes' array ---
        nodes = []
        all_standards = CCSSStandard.objects.select_related('grade_level', 'category_code').all()
        
        for std in all_standards:
            # Determine the grouping for color-coding in the graph
            group = "K-8"
            if std.grade_level.code == 'HS':
                group = std.category_code.name if std.category_code else "High School"

            nodes.append({
                "id": std.ccss_id,
                "description": std.description,
                "group": group
            })

        # --- Step 2: Fetch all dependencies for the 'links' array ---
        links = []
        all_dependencies = CCSSStandardDependency.objects.select_related('source_standard', 'target_standard').all()

        for dep in all_dependencies:
            links.append({
                "source": dep.source_standard.ccss_id,
                "target": dep.target_standard.ccss_id,
                "type": dep.description # e.g., "Dependency" or "Conceptual Connection"
            })
            
        # --- Step 3: Combine into the final structure and write to file ---
        graph_data = {
            "nodes": nodes,
            "links": links
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, indent=2)
            self.stdout.write(self.style.SUCCESS(f"\nSuccessfully exported data for {len(nodes)} nodes and {len(links)} links to {output_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"\nAn error occurred while writing the JSON file: {e}"))


