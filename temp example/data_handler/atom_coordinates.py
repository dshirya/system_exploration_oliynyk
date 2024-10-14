import tables.table_long as long_table
import tables.table_short as short_table
import numpy as np


def get_atom_dict(table_type):
    if table_type == 'long':
        elements_data = long_table.elements_long
    elif table_type == 'short':
        elements_data = short_table.elements_short
    element_dict = {symbol: (x, y) for x, y, symbol in elements_data}
    return element_dict


def get_weighted_coordinates(compound, table_type):
    counts = []
    coordinates = []
    atom_coordinates = get_atom_dict(table_type)
    for index, (element, count) in enumerate(compound.elements.items(),start=1):
        if index == compound.fixed_element_number and len(compound.elements) == 3:
            continue
        else:
            x, y = atom_coordinates[element]
            counts.append(count)
            coordinates.append((x, y))

    weight = np.array(counts)
    original_coord_array = np.array(coordinates)
    weighted_average = np.average(original_coord_array, weights=weight, axis=0)
    return weighted_average, original_coord_array
