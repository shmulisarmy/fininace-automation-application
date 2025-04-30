from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from datetime import date


categories = [
    "Food", "Gifts", "Health/medical", "Home", "Transportation", "Personal",
    "Pets", "Utilities", "Travel", "Debt", "Other"
]

category_completer = WordCompleter(categories, ignore_case=True)


default_date = date.today().isoformat()


print("Enter a new transaction:\n")




def get_transaction_row_from_user():
    date_input = prompt(f"Date (default: today): ") or default_date


    while True:
        amount_input = prompt("Amount (e.g. 10.99): $")
        try:
            amount = float(amount_input)
            amount = f"{amount:.2f}"  
            break
        except ValueError:
            print("Please enter a valid number.")

    description = prompt("Description: ")

    category = prompt("Category (tab to autocomplete): ", completer=category_completer)

    print("\nTransaction recorded:")
    print(f"  Date: {date_input}")
    print(f"  Amount: ${amount}")
    print(f"  Description: {description}")
    print(f"  Category: {category}")

    return [date_input, amount, description, category]

