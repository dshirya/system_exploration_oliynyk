import pandas as pd
import argparse
import re
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import matplotlib.patches as patches
# Import both coordinate variants
import tables.table_long as table1
import tables.table_short as table2
import sys


def main():
    # The following code should be only for obtaining the user's input
    parser = argparse.ArgumentParser(
        prog='Data Visualization Tool',
        usage='py data_visualization.py [options] [file_path] || Use -h option for more information.',
        description='Processes Excel file and visualizes binary and ternary compounds via periodic table.'
                    ' Maintained by Brian Hoang & Danila Shiryaev.',
        epilog='This program is currently being developed for the 2024 Oliynyk Research Group.')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('file_path', type=str,
                        help='This is the path to the Excel file. The Excel file should contain two columns: '
                             '"Formula", and "Entry prototype". The excel sheet is assumed to contain a header on the '
                             'first row. For ternary compounds, the formulas are expected to be organized to have '
                             'consistent subscripts for pseudo-binary visualization.')

    group.add_argument('-b', '--binary', action='store_true',
                       help='for visualizations of only binary data.')
    group.add_argument('-t', '--ternary', action='store_true',
                       help='for visualizations of only ternary data.')

    args = parser.parse_args()
    file_path = args.file_path

    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names

    print(f'Sheets currently in {file_path}: ')
    for index, sheet in enumerate(sheet_names, start=1):
        print(f'{index}. {sheet}')

    user_response = input('\nEnter the numbers of the sheets you want to visualize, separated by commas (e.g. "1,2,'
                          '3") or type "exit" to quit: ').strip()

    if user_response.lower() == 'exit':
        print('\nExiting Program...')
        return 0
    else:
        sheet_numbers = [int(s.strip()) - 1 for s in user_response.split(',')]

    table_choice = input('\nPeriodic Table Types \n1. Long \n2. Short \n'
                         'Choose the periodic table type to draw (e.g. "1" or "2"): ')

    if table_choice == '1':
        elements_data = table1.elements_long
        table_type = 'long'
    elif table_choice == '2':
        elements_data = table2.elements
        table_type = 'short'
    else:
        print('Invalid choice. Exiting program...')
        return 0

    element_dict = {symbol: (x, y) for x, y, symbol in elements_data}  # Need this part for verification and calculation purposes
    marker_types = ['o', 's', '^', 'D', 'P', '*', '2', '8', 'X', 'h']
    # circle, square, triangle, diamond, pentagon, star, tri_up, octagon, X, hexagon
    colors = list(mcolors.TABLEAU_COLORS.values())

    def verify_elements(molecule):
        for element in molecule.elements.keys():
            if element not in element_dict:
                print(f'Please check the following formula in the sheet: {molecule.formula}.'
                      f' It may contain a bad element: {element}.')
                sys.exit()

    def periodic_table():
        fig, ax = plt.subplots(figsize=(36, 10) if table_type == 'long' else (22, 13))
        for x, y, symbol in elements_data:
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=None, edgecolor='black', lw=1))
            ax.text(x, y, symbol, ha='center', va='center', fontsize=12 if table_type == 'long' else 18, weight='bold',
                    zorder=2, alpha=0.7)

        ax.set_aspect('equal')
        x_margin = 3
        y_margin = 2
        ax.set_xlim(0.5 - x_margin, 32.5 + x_margin if table_type == 'long' else 18.5 + x_margin)
        ax.set_ylim(0.5 - y_margin, 7.5 + y_margin if table_type == 'long' else 10 + y_margin)
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        return ax

    class Compound:
        def __init__(self, formula, structure, fixed_element_number=None):
            self.formula = formula
            self.elements = self.parse_formula(formula)
            self.structure = structure
            self.fixed_element_number = fixed_element_number

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

    def calculate_coordinates(compound):
        counts = []
        coordinates = []
        for index, (element, count) in enumerate(compound.elements.items(), start=1):
            if index == compound.fixed_element_number and len(compound.elements) == 3:
                continue
            if element in element_dict:
                x, y = element_dict[element]
                counts.append(count)
                coordinates.append((x, y))

        weight = np.array(counts)
        coord_array = np.array(coordinates)
        weighted_average = np.average(coord_array, weights=weight, axis=0)
        return weighted_average, coord_array


# - Beginning of psuedo-ternary logic - #

    def make_psuedobinary_data():
        ternary_detected = False
        fixed_element_number = None
        compounds = []
        for sheet_number in sheet_numbers:
            df = pd.read_excel(excel_file, sheet_name=sheet_names[sheet_number])
            df = df.drop_duplicates(subset=['Formula', 'Entry prototype'])
            for _, row in df.iterrows():
                formula = row['Formula']
                structure = row['Entry prototype']
                structure = structure.split(',')[0].strip()
                compound = Compound(formula, structure, fixed_element_number)
                if ternary_detected is False and len(compound.elements) == 3:
                    fixed_number = int(input(f'Ternary compound detected, {formula}. Please input a number corresponding '
                                             'to the fixed element: e.g. 1, 2, or 3: '))
                    ternary_detected = True
                    compound = Compound(formula, structure, fixed_number)
                    compounds.append(compound)
                elif ternary_detected is True and len(compound.elements) == 3:
                    compound = Compound(formula, structure, fixed_number)
                    compounds.append(compound)
                else:
                    compound = Compound(formula, structure)
                    compounds.append(compound)

        return compounds

    def display_pseudobinary_data_type(ax):
        added_labels = set()
        structure_marker_map = {}  # To keep track of structures used
        color_map = {}  # To keep track of colors used for fixed element
        structure_marker_counter = 0
        color_counter = 0

        for compound in compounds:
            verify_elements(compound)
            jitter = np.random.uniform(-0.10, 0.10  )

            structure = compound.structure
            if structure not in structure_marker_map:
                structure_marker_map[structure] = marker_types[structure_marker_counter]
                structure_marker_counter += 1
            marker = structure_marker_map[structure]
            center, original_coordinates = calculate_coordinates(compound)
            center_x, center_y = center + jitter  # Jitter to prevent overlap
            coords_x, coords_y = zip(*original_coordinates)

            # Logic for jittering the lines drawn
            coords_x = [x + jitter for x in coords_x]
            coords_y = [y + jitter for y in coords_y]

            if len(compound.elements) == 2:
                is_binary = True
            else:
                is_binary = False

            if is_binary:
                if structure not in added_labels:
                    ax.scatter(center_x, center_y, edgecolors='black', facecolors='None', label=f'{structure}',
                               zorder=4, s=50, marker=marker, alpha=0.5)
                    added_labels.add(structure)
                else:
                    ax.scatter(center_x, center_y, edgecolors='black', facecolors='None', zorder=4, s=50, marker=marker,
                               alpha=0.5)

                ax.plot(coords_x, coords_y, color='black', zorder=3, linestyle='-', alpha=0.5)

            if not is_binary:
                elements = compound.elements
                fixed_number = compound.fixed_element_number - 1
                fixed_element = list(elements.keys())[fixed_number]

                if fixed_element not in color_map:
                    color_map[fixed_element] = colors[color_counter]
                    color_counter += 1
                color = color_map[fixed_element]
                x, y = element_dict[fixed_element]
                rectangle = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=color)
                ax.add_patch(rectangle)
                ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', zorder=4, s=50, marker=marker,
                           alpha=0.5)
                ax.plot(coords_x, coords_y, color=color, zorder=3, linestyle='-', alpha=0.5)

        plt.legend(
            loc='upper right',  # Change legend position
            fontsize=15,  # Increase font size for labels
            frameon=True,  # Show legend frame
            framealpha=1,  # Set transparency of the frame
            edgecolor='black',  # Set edge color of the frame
            markerscale=1  # Increases the size of markers in the legend
        )
        plt.show()

# - End of psuedo-ternary logic - #
# - Beginning of binary logic - #

    def make_binary_data():
        compounds = []
        for sheet_number in sheet_numbers:
            df = pd.read_excel(excel_file, sheet_name=sheet_names[sheet_number])
            df = df.drop_duplicates(subset=['Formula', 'Entry prototype'])
            for _, row in df.iterrows():
                formula = row['Formula']
                structure = row['Entry prototype']
                structure = structure.split(',')[0].strip()
                compound = Compound(formula, structure)
                if len(compound.elements) != 2:
                    print(f'Non-binary data detected ({compound.formula}). -b flag is not good for this data type!')
                    sys.exit()
                else:
                    compounds.append(compound)

        return compounds

    def display_binary_data_type(ax):
        # Danila's code here (Edited a bit to work properly).
        structures = set(compound.structure for compound in compounds)
        structure_colors = {structure: colors[i % len(colors)] for i, structure in enumerate(structures)}
        added_labels = set()

        # Dictionary to track how many rectangles are drawn for each (x, y)
        rectangle_counts = {}
        # Dictionary to track which colors have already been applied to each (x, y)
        applied_colors = {}
        structure_markers = {}
        marker_index = 0

        for compound in compounds:
            verify_elements(compound)
            structure = compound.structure

            center, original_coordinates = calculate_coordinates(compound)
            center_x, center_y = center
            coords_x, coords_y = zip(*original_coordinates)
            color = structure_colors.get(structure)

            if structure not in structure_markers:
                structure_markers[structure] = marker_types[marker_index]
                marker_index += 1
            marker = structure_markers[structure]

            # Plot the center point for the compound using the marker
            if structure not in added_labels:
                ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', label=f'{structure}', zorder=4, s=100, marker=marker,alpha=0.5)
                added_labels.add(structure)
            else:
                ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', zorder=4, s=100, marker=marker, alpha=0.5)

            # Loop through each element in the compound
            for x, y in original_coordinates:
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
                ax.add_patch(plt.Rectangle((x - offset, y - offset), size, size, fill=False, edgecolor=color, zorder=4,
                                           linewidth=5, alpha=0.8))

                # Mark this color as applied to this (x, y)
                applied_colors[(x, y)].add(color)

                # Increment the count for this element
                rectangle_counts[(x, y)] += 1

                ax.plot(coords_x, coords_y, color=color, linestyle='-', zorder=2, alpha=0.5)

        plt.legend(
            loc='upper right',  # Change legend position
            fontsize=15,  # Increase font size for labels
            frameon=True,  # Show legend frame
            framealpha=1,  # Set transparency of the frame
            edgecolor='black',  # Set edge color of the frame
            markerscale=1  # Increases the size of markers in the legend
        )
        plt.show()

# - End of binary logic - #
# - Beginning of ternary logic - #

    def make_ternary_data():
        compounds = []
        for sheet_number in sheet_numbers:
            df = pd.read_excel(excel_file, sheet_name=sheet_names[sheet_number])
            df = df.drop_duplicates(subset=['Formula', 'Entry prototype'])
            for _, row in df.iterrows():
                formula = row['Formula']
                structure = row['Entry prototype']
                structure = structure.split(',')[0].strip()
                compound = Compound(formula, structure)
                if len(compound.elements) != 3:
                    print(f'Non-ternary data detected ({compound.formula}). -t flag is not good for this data type!')
                    sys.exit()
                else:
                    compounds.append(compound)
        return compounds

    def display_ternary_data_type(ax):
        # This is reused code from above. Could maybe refactor so they share the same overall logic?
        # A little redundant, but opted to do this in case ternary data needed to be displayed using a different logic
        structures = set(compound.structure for compound in compounds)
        structure_colors = {structure: colors[i % len(colors)] for i, structure in enumerate(structures)}
        added_labels = set()

        # Dictionary to track how many rectangles are drawn for each (x, y)
        rectangle_counts = {}
        # Dictionary to track which colors have already been applied to each (x, y)
        applied_colors = {}
        structure_markers = {}
        marker_index = 0

        for compound in compounds:
            verify_elements(compound)
            structure = compound.structure

            center, original_coordinates = calculate_coordinates(compound)
            center_x, center_y = center
            color = structure_colors.get(structure)

            if structure not in structure_markers:
                structure_markers[structure] = marker_types[marker_index]
                marker_index += 1
            marker = structure_markers[structure]

            # Plot the center point for the compound using the marker
            if structure not in added_labels:
                ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', label=f'{structure}', zorder=4, s=100, marker=marker,alpha=0.5)
                added_labels.add(structure)
            else:
                ax.scatter(center_x, center_y, edgecolors=color, facecolors='None', zorder=4, s=100, marker=marker, alpha=0.5)

            # Loop through each element in the compound
            for x, y in original_coordinates:
                ax.plot([center_x, x], [center_y, y], color=color, linestyle='-', zorder=2, alpha=0.5)
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
                ax.add_patch(plt.Rectangle((x - offset, y - offset), size, size, fill=False, edgecolor=color, zorder=4,
                                           linewidth=5, alpha=0.8))

                # Mark this color as applied to this (x, y)
                applied_colors[(x, y)].add(color)

                # Increment the count for this element
                rectangle_counts[(x, y)] += 1


        plt.legend(
            loc='upper right',  # Change legend position
            fontsize=15,  # Increase font size for labels
            frameon=True,  # Show legend frame
            framealpha=1,  # Set transparency of the frame
            edgecolor='black',  # Set edge color of the frame
            markerscale=1  # Increases the size of markers in the legend
        )
        plt.show()

# - End of ternary logic - #

    # Please keep this part tidy. Try not to do anything complicated down here

    if args.binary:
        compounds = make_binary_data()
        display_binary_data_type(periodic_table())

    elif args.ternary:
        compounds = make_ternary_data()
        display_ternary_data_type(periodic_table())
    else:
        compounds = make_psuedobinary_data()
        display_pseudobinary_data_type(periodic_table())
    return 0


if __name__ == '__main__':
    main()
