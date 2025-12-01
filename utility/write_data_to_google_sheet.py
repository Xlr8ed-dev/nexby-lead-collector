import os
import sys
from typing import List, Tuple, Optional

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from gspread_formatting import format_cell_range, CellFormat, TextFormat
from openpyxl.utils import get_column_letter

load_dotenv(override=True, dotenv_path=".env")


def get_credentials():
    scopes = os.environ.get("SCOPES", "").split(" ")
    credential_path_env = os.environ.get("CREDENTIAL_PATH", "")

    if not scopes or scopes == [""]:
        raise ValueError("Scopes are missing from environment. Please set SCOPES in env.")

    if not credential_path_env:
        raise ValueError("CREDENTIAL_PATH is missing from environment.")

    credentials_path = os.path.join(os.getcwd(), credential_path_env)

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found: {credentials_path}")

    # MODERN WAY — FIXED
    return Credentials.from_service_account_file(
        credentials_path,
        scopes=scopes
    )


def initialize_sheet(sheet, header):
    sheet.clear()
    sheet.append_row(header)

    num_columns = len(header)
    bold_header_range = f"A1:{get_column_letter(num_columns)}1"

    format_cell_range(
        sheet,
        bold_header_range,
        cell_format=CellFormat(textFormat=TextFormat(bold=True)),
    )


def write_data_to_google_sheet(
    data: List[str],
    sheet_name: str,
    spreadsheet_name: str,
    header: List[str],
    credentials_path: Optional[str] = None,
) -> Tuple[bool, str]:
    try:
        creds = get_credentials()

        # ✔️ Correct gspread authorization
        client = gspread.authorize(creds)

        workbook = client.open(spreadsheet_name)
        sheet = workbook.worksheet(sheet_name)

        sheet_values = sheet.get_all_values()

        # Initialize header if missing
        if not sheet_values or sheet_values[0] != header:
            initialize_sheet(sheet, header)

        # Append rows
        if isinstance(data[0], list):
            sheet.append_rows(data)
        else:
            sheet.append_row(data)

        return True, "Data was written successfully to the Google Sheet."

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_message = (
            f"An error of type {exc_type.__name__} occurred in file {fname} at line number {exc_tb.tb_lineno}: {exc_obj}"
        )
        return False, error_message
