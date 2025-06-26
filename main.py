from connections.gsheets import GSheetsClient, GsheetsWorksheets
from pprint import pprint

client = GSheetsClient('14KXydCTaBwpB4un6iEQSj9XTzKOQ0nLfHe_yxmPd43s')
client.connect()

if client.is_connected:
    test_worksheet = GsheetsWorksheets(
        client,
        sheet_name='test'
    )
    x = test_worksheet.get_data(include_row_numbers=True)
    print(x)
