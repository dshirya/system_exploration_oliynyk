import pandas as pd
from data_handler.compound_object import *


def make_psuedobinary_data(file_path, sheet_numbers):
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names
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

