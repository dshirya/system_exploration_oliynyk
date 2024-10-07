import re


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
