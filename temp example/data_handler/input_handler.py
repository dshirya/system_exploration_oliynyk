import pandas as pd
import sys


def user_input(file_path):
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
        table_type = 'long'
    elif table_choice == '2':
        table_type = 'short'
    else:
        print('Invalid choice. Exiting program...')
        sys.exit()
    return sheet_numbers, table_type
