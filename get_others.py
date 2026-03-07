import os
import os.path
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets',
]

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json not found.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def find_folder_id(drive_service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

def find_file_id(drive_service, file_name, parent_id=None):
    query = f"name='{file_name}' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

def get_target_sheet_id(drive_service):
    target_path = os.getenv("TARGET_FOLDER_NAME", "5團資料_大叔")
    sheet_name = os.getenv("TARGET_SHEET_NAME", "法術詳述列表_大叔")
    current_parent_id = 'root'
    for folder in target_path.split('/'):
        folder_id = find_folder_id(drive_service, folder, current_parent_id)
        if not folder_id: return None
        current_parent_id = folder_id
    return find_file_id(drive_service, sheet_name, current_parent_id)

def main():
    load_dotenv()
    creds = get_credentials()
    if not creds: return

    try:
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        
        sheet_id = get_target_sheet_id(drive_service)
        if not sheet_id:
            print("找不到試算表")
            return

        # Fetch entire sheet data
        # To get the whole sheet, we can just specify the sheet name or a large range
        # Here we get the first sheet metadata to find its title
        sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        actual_sheet_name = sheet_metadata.get('sheets', [{}])[0].get('properties', {}).get('title', 'Sheet1')
        
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"'{actual_sheet_name}'").execute()
        rows = result.get('values', [])
        
        if not rows:
            print("沒有資料")
            return

        headers = rows[0]
        col_map = {name.replace('\n', '').strip(): idx for idx, name in enumerate(headers)}
        
        target_col = "[施法距離]"
        target_col_alt = "施法距離"
        col_idx = col_map.get(target_col)
        if col_idx is None:
            col_idx = col_map.get(target_col_alt)
        
        if col_idx is None:
            print(f"找不到欄位: {target_col}")
            print(f"可用欄位: {list(col_map.keys())}")
            return

        others_rows = []
        for i, row in enumerate(rows):
            row_num = i + 1 # 1-indexed
            if len(row) > col_idx:
                val = str(row[col_idx]).strip()
                if val == "其他":
                    others_rows.append(str(row_num))
        
        outputs = [f"uv run app.py --start-row {rn}" for rn in others_rows]
        
        with open("get_others.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(outputs))
            f.write("\n")
            
        print(f"已找出 {len(others_rows)} 筆 [施法距離]='其他' 的資料，並以命令格式輸出至 get_others.txt")

    except HttpError as error:
        print(f'發生錯誤: {error}')

if __name__ == '__main__':
    main()
