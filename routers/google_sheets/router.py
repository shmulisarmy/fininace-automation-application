

from fastapi import APIRouter, HTTPException, Request
from prompt_toolkit import print_formatted_text
from jwt_utils import get_auth_details
from utils.date import get_current_month
from encryption import decrypt


from .talk_to_sheets import create_row_in_sheets
from expense import Expense
from expense import ExpenseResponse
import json

import inspect
import os

def print_call_info():
    caller_frame = inspect.currentframe().f_back
    filepath = os.path.abspath(caller_frame.f_code.co_filename)
    line_number = caller_frame.f_lineno
    function_name = caller_frame.f_code.co_name
    print(f"{filepath}:{line_number} - In function '{function_name}'")

sheets_router = APIRouter()

def get_sheet_id(request: Request) -> str:
    auth_details = get_auth_details(request)
    print(f'{auth_details = }')



    with open("sheet_ids.json", "r") as f:
        sheets = json.load(f)
    
    sheet_id = sheets.get(auth_details, None)
    print(f'{sheet_id = }')
    if sheet_id is None:
        raise HTTPException(status_code=404, detail="Sheet not found")
    print(f'{sheet_id = }')
    
    return sheet_id






@sheets_router.post("", response_model=ExpenseResponse)
def create_expense(expense: Expense, request: Request):
    print(f'{request = }')
    print(f'{request.cookies = }')
    
    print_call_info()
    print(f'{expense = }')
    
    # Set default date to today if not provided
    sheet_id = get_sheet_id(request)
    create_row_in_sheets(expense, sheet_id)
    print(f'{expense = }')
    
    return {
        "id": 1,
        "date": expense.date,
        "amount": expense.amount,
        "description": expense.description,
        "category": expense.category
    }
