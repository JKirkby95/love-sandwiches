import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from user
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be 6 numbers separated by commas.")
        print("Example: 1,2,3,4,5")

        data_str = input("Enter your data here:")
        
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Raises error if strings are not converted to int , or if they are not exactly
     6 values"
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values needed, you provided {len(values)}"
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.')
        return False

    return True
    
# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list provided.
#     """
#     print("updating sales sheet....")
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print("updated successfully")

# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the list provided.
#     """
#     print("updating surplus sheet....")
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)
#     print("updated successfully")

def update_worksheet(data ,worksheet):
    """
    Update surplus worksheet, add new row with the list provided.
    """
    print(f"updating {worksheet} sheet....")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f" {worksheet} updated successfully")

def calculate_surplus_data(sales_row):
    """
    Calculating surplus using subtraction
    """
    print("Calculating surplus data...")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_value = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_value, "surplus")


print("Welcome to Love Sandwiches Data Automation")
main()