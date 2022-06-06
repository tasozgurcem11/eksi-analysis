import pandas as pd
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def connect_to_google(sheet=None):
    """
    Connect to Google Sheets by using service_account.
    :param sheet:
    :return:
    """
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)

    # authorize the client-sheet
    gc = gspread.authorize(creds)

    if not sheet:
        return "No Target Sheet defined"
    else:
        sh = gc.open_by_key(sheet)
        return sh