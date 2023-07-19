import gspread
from google.oauth2.service_account import Credentials

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
    
def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list provided.
    """
    print("updating sales sheet....")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("updated successfully")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)