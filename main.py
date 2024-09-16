import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import os
import matplotlib.patches as patches

# Import both coordinate variants
import tables.table_long as table1
import tables.table_short as table2

def generate_unique_filename(base_filename, extension=".png"):
    """Generate a unique filename by appending numbers if a file with the same name exists."""
    counter = 1
    filename = f"{base_filename}{extension}"
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}{extension}"
        counter += 1
    return filename

def main():
    # Ask the user to select an Excel file from the current directory
    print("Available Excel files in the current directory:")
    files = [f for f in os.listdir() if f.endswith('.xlsx')]
    
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")
    
    file_choice = input(f"Choose the file you want to work with by entering the corresponding number (1-{len(files)}): ").strip()
    
    if not file_choice.isdigit() or int(file_choice) < 1 or int(file_choice) > len(files):
        print("Invalid choice. Exiting program...")
        return 0

    file_path = files[int(file_choice) - 1]

    # Prompt the user to choose the table variant
    table_choice = input("Choose the periodic table to draw (1 for long, 2 for short): ")

    if table_choice == "1":
        elements_data = table1.elements_long
        table_type = "long"
    elif table_choice == "2":
        elements_data = table2.elements
        table_type = "short"
    else:
        print("Invalid choice. Exiting program...")
        return 0

    # Ask the user if they want to process a binary or ternary compound
    compound_type = input("Is this a binary or ternary compound? (Enter 'binary' or 'ternary'): ").strip().lower()

    # If ternary, ask for the third element
    third_element = None
    if compound_type == "ternary":
        third_element = input("Enter the symbol of the third element that should be highlighted: ").strip()

    # Load the Excel file
    sheet_names = pd.ExcelFile(file_path).sheet_names
    print(f'Sheets currently in {file_path}: ')
    for index, sheet in enumerate(sheet_names, start=1):
        print(f'{index}. {sheet}')

    user_response = input('Enter the numbers of the sheets you want to visualize, separated by commas (e.g. "1,2,'
                          '3") or type "exit" to quit: ').strip()

    if user_response.lower() == 'exit':
        print('\nExiting Program...')
        return 0
    else:
        sheet_numbers = [int(s.strip()) - 1 for s in user_response.split(',')]

    compounds = []
    output_filename_base = None

    class Compound:
        def __init__(self, formula, structure):
            self.formula = formula
            self.elements = self.parse_formula(formula)
            self.structure = structure

        def parse_formula(self, formula):
            pattern = r'([A-Z][a-z]*)(\d*\.?\d*)'
            matches = re.findall(pattern, formula)
            elements = {}
            for element, count in matches:
                if count:
                    elements[element] = float(count)
                else:
                    elements[element] = 1
            return elements

        def calculate_weighted_coordinates(self):
            counts = []
            coordinates = []
            element_dict = {symbol: (x, y) for x, y, symbol in elements_data}
            for element, count in self.elements.items():
                if element in element_dict:
                    x, y = element_dict[element]
                    counts.append(count)
                    coordinates.append((x, y))
            weight = np.array(counts)
            coord_array = np.array(coordinates)
            weighted_average = np.average(coord_array, weights=weight, axis=0)
            return weighted_average, coord_array

    for sheet_number in sheet_numbers:
        df = pd.read_excel(file_path, sheet_name=sheet_names[sheet_number])

        # Retrieve the first row's entry prototype to use in the filename
        if output_filename_base is None:
            entry_prototype = df['Entry prototype'].iloc[0].split(',')[0].strip()
            output_filename_base = f"{entry_prototype}_{table_type}_table"

        for _, row in df.iterrows():
            formula = row['Formula']
            structure = row['Entry prototype']
            structure = structure.split(',')[0].strip()
            compound = Compound(formula, structure)
            compounds.append(compound)

    structures = set(compound.structure for compound in compounds)
    colors = list(mcolors.TABLEAU_COLORS.values())
    structure_colors = {structure: colors[i % len(colors)] for i, structure in enumerate(structures)}

    added_labels = set()

    fig, ax = plt.subplots(figsize=(36, 10) if table_choice == "1" else (22, 13))

    for x, y, symbol in elements_data:
        ax.add_patch(plt.Rectangle((x-0.5, y-0.5), 1, 1, fill=None, edgecolor='black', lw=2))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=24, weight='bold', zorder=2)

    # Dictionary to track how many rectangles are drawn for each (x, y)
    rectangle_counts = {}
    # Dictionary to track which colors have already been applied to each (x, y)
    applied_colors = {}
    
    # Define a list of 5 marker types
    marker_types = ['o', 's', '^', 'v', 'D']  # Circle, Square, Triangle Up, Triangle Down, Diamond

    # Dictionary to store the marker assigned to each structure
    structure_markers = {}

    # Counter to iterate through marker types
    marker_index = 0

    for compound in compounds:
        structure = compound.structure  # Get the structure of the compound
        center, original_coordinates = compound.calculate_weighted_coordinates()
        center_x, center_y = center

        color = structure_colors.get(structure)

        # If the structure does not have a marker yet, assign the next available marker
        if structure not in structure_markers:
        # Cycle through marker types (wrap around if more than 5 structures)
            structure_markers[structure] = marker_types[marker_index % len(marker_types)]
            marker_index += 1  # Move to the next marker

        # Get the marker for the current structure
        marker = structure_markers[structure]

        # Plot the center point for the compound using the marker
        if structure not in added_labels:
            ax.scatter(center_x, center_y, color=color, label=f'{structure}', zorder=4, s=100, marker=marker)
            added_labels.add(structure)
        else:
            ax.scatter(center_x, center_y, color=color, zorder=4, s=100, marker=marker, alpha=0.2)

        # Loop through each element in the compound
        for idx, (x, y) in enumerate(original_coordinates):
            element_symbol = [symbol for ex, ey, symbol in elements_data if (x, y) == (ex, ey)][0]
            
            # For other elements, draw rectangles and connecting lines as usual
            if (x, y) not in rectangle_counts:
                rectangle_counts[(x, y)] = 0
            if (x, y) not in applied_colors:
                applied_colors[(x, y)] = set()

            # Skip if this color has already been applied to this (x, y)
            if color in applied_colors[(x, y)]:
                continue

            # Get the current count for this element (how many rectangles drawn)
            count = rectangle_counts[(x, y)]

            # Calculate size and offset for the new rectangle (progressively smaller)
            shrink_factor = 0.15 * count  # Smaller shrink for each additional color
            size = 0.92 - shrink_factor  # Start with 0.92 and decrease with each rectangle
            offset = 0.46 - shrink_factor / 2  # Adjust the offset to keep it centered

            # Draw the rectangle with the current size and offset
            ax.add_patch(plt.Rectangle((x - offset, y - offset), size, size, fill=False, edgecolor=color, zorder=4, linewidth=5, alpha=0.8))

            # Mark this color as applied to this (x, y)
            applied_colors[(x, y)].add(color)

            # Increment the count for this element
            rectangle_counts[(x, y)] += 1

        # Draw lines connecting the center to each element (except for the third element)
        for idx, (x, y) in enumerate(original_coordinates):
            element_symbol = [symbol for ex, ey, symbol in elements_data if (x, y) == (ex, ey)][0]

            # Handle the third element in ternary compounds
            if compound_type == "ternary" and element_symbol == third_element:
                ax.add_patch(patches.Rectangle((x - 0.45, y - 0.45), 0.90, 0.90, fill=color, edgecolor=color, zorder=1, linewidth=3, alpha=0.1))
                continue  # Skip drawing lines for the third element

            ax.plot([center_x, x], [center_y, y], color=color, linestyle='-', zorder=2, alpha=0.1)
            

    ax.set_aspect('equal')
    x_margin = 3
    y_margin = 1
    ax.set_xlim(0.5 - x_margin, 32.5 + x_margin if table_choice == "1" else 18.5 + x_margin)
    ax.set_ylim(0.5 - y_margin, 7.5 + y_margin if table_choice == "1" else 10 + y_margin)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.legend(
        title='Structures',
        loc='upper right',      # Change legend position
        fontsize=18,           # Increase font size for labels
        title_fontsize=20,     # Increase font size for title
        frameon=True,          # Show legend frame
        framealpha=1,        # Set transparency of the frame
        edgecolor='black',     # Set edge color of the frame
        markerscale=1.5        # Increase the size of markers in the legend
    )

    # Generate a unique filename if a file already exists
    output_filename = generate_unique_filename(output_filename_base)
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Periodic table saved as {output_filename}")

    #plt.show()

    return 0


if __name__ == '__main__':
    main()