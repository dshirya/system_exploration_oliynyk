from matplotlib import colors as mcolors
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from data_handler.atom_coordinates import *
from visualize_data.make_periodic_table import periodic_table_visual

marker_types = ['o', 's', '^', 'D', 'P', '*', '2', '8', 'X', 'h']
# circle, square, triangle, diamond, pentagon, star, tri_up, octagon, X, hexagon
colors = list(mcolors.TABLEAU_COLORS.values())


def display_pseudobinary_data_type(compounds, table_type):
    added_labels = set()
    structure_marker_map = {}  # To keep track of structures used
    color_map = {}  # To keep track of colors used for fixed element
    structure_marker_counter = 0
    color_counter = 0
    ax = periodic_table_visual(table_type)
    element_dict = get_atom_dict(table_type)

    for compound in compounds:
        jitter = np.random.uniform(-0.10, 0.10)

        structure = compound.structure
        if structure not in structure_marker_map:
            structure_marker_map[structure] = marker_types[structure_marker_counter]
            structure_marker_counter += 1
        marker = structure_marker_map[structure]
        center, original_coordinates = get_weighted_coordinates(compound, table_type)
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
