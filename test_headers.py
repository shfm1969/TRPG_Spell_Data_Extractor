import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from app import get_credentials, get_target_sheet_id

load_dotenv()
creds = get_credentials()
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

sheet_id = get_target_sheet_id(drive_service)

sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
actual_sheet_name = sheet_metadata.get('sheets', [{}])[0].get('properties', {}).get('title', 'Sheet1')

header_range = f"'{actual_sheet_name}'!1:1"
header_result = sheets_service.spreadsheets().values().get(
    spreadsheetId=sheet_id, range=header_range).execute()
headers = header_result.get('values', [[]])[0]

print("--- HEADERS ---")
for i, h in enumerate(headers):
    print(f"Index {i}: '{h}'")
