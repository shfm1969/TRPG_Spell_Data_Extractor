import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from app import get_credentials, get_target_sheet_id, fetch_sheet_data, col_idx_to_letter, get_col_idx

load_dotenv()
creds = get_credentials()
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)
sheet_id = get_target_sheet_id(drive_service)

col_map, rows, actual_sheet_name = fetch_sheet_data(sheets_service, sheet_id, 4, 1)

updates = []
for col_name in ["[材料M]", "[器材F]", "[法器DF]", "[豁免說明]", "[施法時間]", "[施法距離]"]:
    idx = get_col_idx(col_map, col_name)
    if idx is not None:
        letter = col_idx_to_letter(idx)
        updates.append({
            'range': f"'{actual_sheet_name}'!{letter}4",
            'values': [['']]
        })

body = {
    'valueInputOption': 'USER_ENTERED',
    'data': updates
}
sheets_service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body=body).execute()
print("Cleared row 4 cells.")
