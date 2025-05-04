from dataclasses import dataclass
import json
import gspread
from google.oauth2.service_account import Credentials
from prompt_toolkit import print_formatted_text


from expense import Expense
from utils.date import get_current_month




credentials_file = "credentials.json"



scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    # "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
client = gspread.Client(credentials)



def get_first_empty_transaction_row(worksheet):
    try:
        server_data_section: str = worksheet.cell("2D").value
        server_data = json.loads(server_data_section)
        transactions_row_upto = server_data["next empty transaction row"]
    except:
        transactions_start_row = 5
        transactions_row_upto = transactions_start_row


    empty_found = False
    while not empty_found:
        row_values = worksheet.row_values(transactions_row_upto)
        if row_values == []:
            empty_found = True
            break
        
        transactions_row_upto += 1
    return transactions_row_upto










categories = [
    "Food",
    "Gifts",
    "Health/medical",
    "Home",
    "Transportation",
    "Personal",
    "Pets",
    "Utilities",
    "Travel",
    "Debt",
    "Other"
]





month_map = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


def create_row_in_sheets(expense: Expense, sheet_id):
    sheet = client.open_by_key(sheet_id)
    month_as_string: str = month_map[get_current_month()]
    worksheet = sheet.worksheet(month_as_string)
    first_empty_transaction_row = get_first_empty_transaction_row(worksheet)
    worksheet.update(f"B{first_empty_transaction_row}:E{first_empty_transaction_row}", [[expense.date, expense.amount, expense.description, expense.category]])
    SERVER_DATA_SECTION = json.dumps({"next empty transaction row": first_empty_transaction_row + 1 })
    worksheet.update_cell(2, 4, SERVER_DATA_SECTION)



