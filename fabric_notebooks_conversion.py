import json

def convert_fabric_py_to_ipynb(input_file_path, output_file_path):
    """
    Converts a Fabric/Synapse exported .py notebook file to a Jupyter .ipynb file.
    """
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Initialize the Jupyter notebook structure
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 2,
        "metadata": {
            "kernelspec": {
                "display_name": "synapse_pyspark",  # Default, adjust if needed
                "language": "python",
                "name": "synapse_pyspark"
            }
        },
        "cells": []
    }

    # Split the content into sections based on METADATA blocks
    sections = content.split('# METADATA ********************\n')
    
    for section in sections[1:]:  # Skip first empty section
        if not section.strip():
            continue
            
        # Split metadata from cell content
        parts = section.split('# CELL ********************\n')
        if len(parts) < 2:
            continue
            
        metadata_part = parts[0]
        cell_content = parts[1].strip()
        
        # Extract language from metadata (simplified parsing)
        cell_type = "code"  # Default to code cell
        language = "python"  # Default language
        
        # Very basic metadata extraction - you may need to enhance this
        if '"language":' in metadata_part:
            # This is a simplified parser - you might need more robust JSON parsing
            pass
        
        # Create cell structure
        cell = {
            "cell_type": cell_type,
            "metadata": {},
            "source": cell_content.splitlines(True)  # Keep as list of lines
        }
        
        notebook["cells"].append(cell)

    # Write the .ipynb file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

# Usage
convert_fabric_py_to_ipynb(
    "../fabric_items2/bronze_nb.Notebook/notebook-content.py", 
    "converted_notebook.ipynb"
)