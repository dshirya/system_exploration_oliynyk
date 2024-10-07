import argparse
from data_handler import *
from data_maker import *
from visualize_data import *


def main():
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
    sheet_numbers, table_type = user_input(file_path)

    if args.binary is True:
        print()
    elif args.ternary is True:
        print()
    else:
        compounds = make_psuedobinary_data(file_path, sheet_numbers)
        display_pseudobinary_data_type(compounds, table_type)

if __name__ == '__main__':
    main()
