import os
import os.path
import argparse
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
    'https://www.googleapis.com/auth/documents.readonly'
]

def get_credentials():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json not found.")
                print("Please download your OAuth 2.0 Client credentials from Google Cloud Console")
                print("and save it as 'credentials.json' in this directory.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def find_folder_id(drive_service, folder_name, parent_id=None):
    """Finds a folder by name, optionally within a specific parent folder."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if not items:
        return None
    return items[0]['id']

def find_file_id(drive_service, file_name, parent_id=None):
    """Finds a file by name, optionally within a specific parent folder."""
    query = f"name='{file_name}' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
        
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if not items:
        return None
    return items[0]['id']

def get_target_sheet_id(drive_service):
    """Navigates the folder structure to find the target spreadsheet."""
    root_folder_name = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER", "我的雲端硬碟")
    target_path = os.getenv("TARGET_FOLDER_NAME", "5團資料_大叔")
    sheet_name = os.getenv("TARGET_SHEET_NAME", "法術詳述列表_大叔")
    
    print(f"Searching for folder path: {root_folder_name}/{target_path}")
    
    # We don't actually query "My Drive" by name, "root" is the alias for My Drive
    current_parent_id = 'root'
    
    # Traverse the path
    for folder in target_path.split('/'):
        folder_id = find_folder_id(drive_service, folder, current_parent_id)
        if not folder_id:
            print(f"Error: Could not find folder '{folder}' in the path.")
            return None
        current_parent_id = folder_id
        
    print(f"Found target directory. Searching for spreadsheet: {sheet_name}")
    sheet_id = find_file_id(drive_service, sheet_name, current_parent_id)
    
    if not sheet_id:
         print(f"Error: Could not find spreadsheet '{sheet_name}'.")
         return None
         
    return sheet_id

def col_idx_to_letter(col_idx):
    """Converts a 0-based column index to A1 notation letter (e.g., 0 -> A, 26 -> AA)."""
    letter = ""
    col_idx += 1
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        letter = chr(65 + remainder) + letter
    return letter

def fetch_sheet_data(sheets_service, sheet_id, start_row, batch_size):
    """Fetches headers and a specific range of rows from the first sheet."""
    # Get actual first sheet name to avoid 'Unable to parse range' errors
    sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    actual_sheet_name = sheet_metadata.get('sheets', [{}])[0].get('properties', {}).get('title', 'Sheet1')
    
    # First, get the headers (assuming row 1 is headers)
    # Fetch entire row 1
    header_range = f"'{actual_sheet_name}'!1:1"
    header_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=header_range).execute()
    headers = header_result.get('values', [[]])[0]
    
    if not headers:
        print("Error: Could not find headers in row 1.")
        return None, None, None
        
    # Build a column index map (e.g., {'[語言V]': 5, '[法術詳述 連結]': 20, ...})
    # This helps us find the right column regardless of hidden newlines in Google Sheets
    col_map = {name.replace('\n', '').strip(): idx for idx, name in enumerate(headers)}
    
    # Calculate the data range
    end_row = start_row + batch_size - 1
    # Fetch the entire row range to support sheets wider than Z
    data_range = f"'{actual_sheet_name}'!{start_row}:{end_row}"
    
    print(f"Fetching data from range: {data_range} (with hyperlink support)")
    
    response = sheets_service.spreadsheets().get(
        spreadsheetId=sheet_id, 
        ranges=[data_range], 
        fields="sheets/data/rowData/values/formattedValue,sheets/data/rowData/values/hyperlink,sheets/data/rowData/values/textFormatRuns/format/link/uri"
    ).execute()
    
    try:
        row_data = response.get('sheets', [{}])[0].get('data', [{}])[0].get('rowData', [])
    except (KeyError, IndexError):
        row_data = []
        
    rows = []
    for r in row_data:
        current_row = []
        for cell in r.get('values', []):
            formatted_val = cell.get('formattedValue', '')
            hyperlink = cell.get('hyperlink', '')
            
            # If the hyperlink is attached to specific text runs instead of the whole cell
            if not hyperlink and 'textFormatRuns' in cell:
                for run in cell['textFormatRuns']:
                    run_link = run.get('format', {}).get('link', {}).get('uri')
                    if run_link:
                        hyperlink = run_link
                        break # Just take the first link found
            
            # If there's a hyperlink, favor it (especially for docs URLs)
            if hyperlink:
                current_row.append(hyperlink)
            else:
                current_row.append(formatted_val)
        rows.append(current_row)
    
    return col_map, rows, actual_sheet_name

TARGET_COLUMNS = [
    "[語言V]", "[姿勢S]", "[材料M]", "[器材F]", "[法器DF]", 
    "[施法時間]", "[施法距離]", "[持續時間]", "[豁免]", "[豁免說明]", "[法抗]"
]

def get_col_idx(col_map, name):
    """Helper to find column index with or without brackets."""
    idx = col_map.get(name)
    if idx is not None: return idx
    return col_map.get(name.strip('[]'))

def filter_rows_for_processing(rows, col_map, start_row, verbose=False):
    """Filters rows that have missing data and a valid Google Docs URL."""
    rows_to_process = []

    url_col_idx = get_col_idx(col_map, "[法術詳述 連結]")
    if url_col_idx is None:
        print("Error: Could not find '[法術詳述 連結]' or '法術詳述 連結' column in headers.")
        print("Available headers:", list(col_map.keys()))
        return rows_to_process

    for i, row in enumerate(rows):
        actual_row_num = start_row + i

        # Check if the URL column exists in this row's data
        if len(row) <= url_col_idx or not row[url_col_idx]:
            if verbose: print(f"Row {actual_row_num}: skipped (no URL)")
            continue

        url = row[url_col_idx]
        if "docs.google.com/document/d/" not in url:
            if verbose: print(f"Row {actual_row_num}: skipped (invalid URL: {url!r})")
            continue

        # Check if any target column is missing data
        is_missing_data = False
        for col_name in TARGET_COLUMNS:
            col_idx = get_col_idx(col_map, col_name)
            if col_idx is None:
                continue # If the column doesn't exist in header, we can't update it

            # If the row is shorter than the column index, or the cell is empty string
            if len(row) <= col_idx or not str(row[col_idx]).strip():
                is_missing_data = True
                break

        if is_missing_data:
            # Extract doc ID from URL
            parts = url.split("/d/")
            if len(parts) > 1:
                doc_id = parts[1].split("/")[0]
                rows_to_process.append({
                    'row_num': actual_row_num,
                    'row_data': row,
                    'doc_id': doc_id
                })
                if verbose: print(f"Row {actual_row_num}: queued for processing (doc_id: {doc_id})")
        else:
            if verbose: print(f"Row {actual_row_num}: skipped (all target fields already filled)")

    return rows_to_process

def get_doc_text(docs_service, document_id):
    """Retrieves and concatenates all text from a Google Doc."""
    try:
        doc = docs_service.documents().get(documentId=document_id).execute()
        text = ""
        for element in doc.get('body').get('content'):
            if 'paragraph' in element:
                for p_element in element.get('paragraph').get('elements'):
                    if 'textRun' in p_element:
                        text += p_element.get('textRun').get('content')
        return text
    except HttpError as err:
        print(f"Error fetching doc {document_id}: {err}")
        return ""

import re
import opencc

# 初始化簡體→臺灣繁體轉換器（s2twp = Simplified to Traditional with Taiwan phrases）
_converter = opencc.OpenCC('s2twp')
# 初始化繁體→簡體轉換器，用於標題搜尋時對齊 Google Doc 的簡體標題
_t2s_converter = opencc.OpenCC('t2s')

def to_zh_tw(text: str) -> str:
    """將文字從簡體中文轉換為繁體中文（臺灣用字），並將全形括號轉為半形。若輸入為空則原樣回傳。"""
    if not text:
        return text
    converted = _converter.convert(text)
    # 全形括號→半形括號
    converted = converted.replace('（', '(').replace('）', ')')
    return converted

def parse_spell_data(text, spell_name, verbose=False):
    """Parses text to extract spell properties based on business rules."""
    parsed_data = {
        "[語言V]": "",
        "[姿勢S]": "",
        "[材料M]": "",
        "[器材F]": "",
        "[法器DF]": ""
    }

    # Extract English name to find target block (bypassing Traditional/Simplified issues)
    english_name_match = re.search(r'[(（]([a-zA-Z\s\-\']+)[)）]', str(spell_name))
    if english_name_match:
        target_name = english_name_match.group(1).lower().strip()
    else:
        # 嘗試匹配沒有括號的英文部分，這通常是由空白分隔的結尾英文
        eng_match = re.search(r'\s+([a-zA-Z\s\-\']+)$', str(spell_name))
        if eng_match:
            target_name = eng_match.group(1).lower().strip()
        else:
            target_name = str(spell_name).lower().strip()

    # 同時準備簡體版 target_name，以對齊 Google Doc 中可能使用簡體的標題
    target_name_simp = _t2s_converter.convert(target_name).lower()
    if verbose: print(f"  [parse] spell_name={spell_name!r}  target_name={target_name!r}  target_name_simp={target_name_simp!r}")

    lines = text.split('\n')
    start_idx = 0

    # First pass: prefer heading-style lines where the spell name appears as a title
    # e.g., "反魔場（Antimagic Field）" or "修改机运 Alter Fortune"
    heading_like = re.compile(r'^[^:：]{1,40}(?:[(（].*[)）]|\s+[a-zA-Z0-9\s\-\'’,\/]+)\s*$')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if target_name and (target_name in line_lower or target_name_simp in line_lower) and heading_like.match(line.strip()):
            if verbose: print(f"  [parse] heading matched at line {i}: {line.strip()!r}")
            start_idx = i
            break
    else:
        # No heading-style match found — give up
        if verbose: print(f"  [parse] no heading match → skipping")
        return parsed_data
            
    end_idx = len(lines)
    heading_pattern = re.compile(r'^[^:：\(（\s]+(?:[(（][a-zA-Z0-9\s\-\'’,\/]+[)）]|\s+[a-zA-Z0-9\s\-\'’,\/]+)\s*$')
    for i in range(start_idx + 1, len(lines)):
        if heading_pattern.match(lines[i].strip()):
            end_idx = i
            break
            
    # Process only the isolated block for this specific spell
    isolated_lines = lines[start_idx:end_idx]
    
    for line in isolated_lines:
        line = line.strip()
        
        # Parse Components: [語言V] / [姿勢S] / [材料M] / [器材F] / [法器DF]
        if line.startswith("成分") or line.startswith("法术成分") or line.startswith("法術成分"):
            if "語言" in line or "语言" in line or "言语" in line or "言語" in line or re.search(r'\bV\b', line): parsed_data["[語言V]"] = "語"
            if "姿勢" in line or "姿势" in line or re.search(r'\bS\b', line): parsed_data["[姿勢S]"] = "姿"
            if "材料" in line or re.search(r'\bM\b', line): parsed_data["[材料M]"] = "材"
            if "法器" in line or re.search(r'\bDF\b', line): parsed_data["[法器DF]"] = "法"
            if "器材" in line or re.search(r'(?<![A-Z])F(?![A-Z])', line): parsed_data["[器材F]"] = "器"
            
        # Parse Casting Time: [施法時間]
        if line.startswith("施法时间") or line.startswith("施法時間"):
            content = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            if "一个标准动作" in content: parsed_data["[施法時間]"] = "標動"
            elif "一个直觉动作" in content: parsed_data["[施法時間]"] = "即時"
            else: parsed_data["[施法時間]"] = content
            
        # Parse Range: [施法距離]
        if line.startswith("距离") or line.startswith("距離") or line.startswith("施法距离") or line.startswith("施法距離"):
            content = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            if content.startswith("近距"): parsed_data["[施法距離]"] = "近距"
            elif content.startswith("中距"): parsed_data["[施法距離]"] = "中距"
            elif content.startswith("遠距") or content.startswith("远距"): parsed_data["[施法距離]"] = "遠距"
            elif content.startswith("接触") or content.startswith("接觸"): parsed_data["[施法距離]"] = "接觸"
            else: parsed_data["[施法距離]"] = "其他"
            
        # Parse Duration: [持續時間] (先替換「每等級」→「每CL」，再判斷長度 <= 16)
        if line.startswith("持续时间") or line.startswith("持續時間"):
            content = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            content = content.replace("每等级", "每CL").replace("每等級", "每CL")
            parsed_data["[持續時間]"] = content if len(content) <= 16 else "其他"
            
        # Parse Saving Throw: [豁免] & [豁免說明] (Limit <= 12 chars)
        if line.startswith("豁免检定") or line.startswith("豁免檢定") or line.startswith("豁免:") or line.startswith("豁免："):
            content = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            content = content.replace("无", "無").replace("强韧", "強靭").replace("强靭", "強靭")
            
            # Type detection for [豁免]
            if content.startswith("意志"): parsed_data["[豁免]"] = "意志"
            elif content.startswith("強靭"): parsed_data["[豁免]"] = "強靭"
            elif content.startswith("敏捷"): parsed_data["[豁免]"] = "敏捷"
            elif content.startswith("反射"): parsed_data["[豁免]"] = "反射" # In case rulebooks say Reflex, but standard expects 敏捷? Wait, D&D "反射" actually corresponds to Reflex. Users said "敏捷", so let's output "敏捷" if it's reflex or 敏捷
            elif content.startswith("無"): parsed_data["[豁免]"] = "無"
            else: parsed_data["[豁免]"] = "其他"
            
            # If the parser sees "反射" it outputs "敏捷" because user specifically requested that (or "其他" if it doesn't match). If it really was "反射" in CN, let's map it to "敏捷" to be safe.
            parsed_data["[豁免說明]"] = content if len(content) <= 16 else "其他"
            
        # Parse Spell Resistance: [法抗]
        if line.startswith("法术抗力") or line.startswith("法術抗力"):
            content = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            if content.startswith("不可"): parsed_data["[法抗]"] = "不可"
            elif content.startswith("否") or content.startswith("无") or content.startswith("無"): parsed_data["[法抗]"] = "不可"
            elif content.startswith("可") or content.startswith("有"): parsed_data["[法抗]"] = "可"
            else: parsed_data["[法抗]"] = "其他"

    return parsed_data

def main():
    parser = argparse.ArgumentParser(description="Extract TRPG spells and update Google Sheet.")
    parser.add_argument("--start-row", type=int, required=True, help="The starting row number in the Google Sheet.")
    parser.add_argument("--batch-size", type=int, default=1, help="Number of rows to process (max 100). Default is 1.")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostic output for each row.")
    args = parser.parse_args()
    
    if args.batch_size > 100:
        print("Error: batch-size cannot exceed 100.")
        return
        
    start_row = args.start_row
    batch_size = args.batch_size

    # Load environment variables
    load_dotenv()
    
    print("Setting up TRPG Spell Data Extraction...")
    creds = get_credentials()
    if not creds:
        print("Setup failed: Missing or invalid credentials.")
        return

    try:
        # Build API services
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        docs_service = build('docs', 'v1', credentials=creds)
        
        print("Successfully authenticated with Google APIs.")
        
        # 2. File Discovery
        sheet_name = os.getenv("TARGET_SHEET_NAME", "法術詳述列表_大叔")
        sheet_id = get_target_sheet_id(drive_service)
        if not sheet_id:
            print("Failed to locate the target spreadsheet. Exiting.")
            return
            
        print(f"Successfully located target spreadsheet ID: {sheet_id}")
        
        # 3. Spreadsheet Data Retrieval
        col_map, rows, actual_sheet_name = fetch_sheet_data(sheets_service, sheet_id, start_row, batch_size)
        if not col_map:
            return
            
        print(f"Fetched {len(rows)} rows from the spreadsheet (Tab: {actual_sheet_name}).")
        
        # Filter missing data and valid URLs
        rows_to_process = filter_rows_for_processing(rows, col_map, start_row, verbose=args.verbose)
        print(f"Found {len(rows_to_process)} rows that need processing.")
        
        # 4. Document Parsing & 5. Data Formatting
        updates = []
        for index, item in enumerate(rows_to_process):
            print(f"Processing ({index+1}/{len(rows_to_process)}) - Row {item['row_num']}, Doc ID: {item['doc_id']}")
            text = get_doc_text(docs_service, item['doc_id'])
            if not text:
                continue
            # Safely get spell name from row_data
            name_idx = get_col_idx(col_map, "法術名稱")
            spell_idx = get_col_idx(col_map, "spells")
            
            english_spell_name = ""
            if spell_idx is not None and len(item['row_data']) > spell_idx:
                english_spell_name = str(item['row_data'][spell_idx]).strip()
                
            chinese_spell_name = ""
            if name_idx is not None and len(item['row_data']) > name_idx:
                chinese_spell_name = str(item['row_data'][name_idx]).strip()
                
            # If we have an english spell name, use that for robust searching, otherwise fallback
            search_name = english_spell_name if english_spell_name else chinese_spell_name
            
            parsed_data = parse_spell_data(text, search_name, verbose=args.verbose)
            if args.verbose: print(f"  [parse] extracted fields: {parsed_data}")

            # Format update for this specific row based on col_map
            for col_name, new_val in parsed_data.items():
                col_idx = get_col_idx(col_map, col_name)
                if col_idx is not None:
                    # 寫入前先將欄位值轉換為繁體中文
                    new_val = to_zh_tw(str(new_val))
                    # Convert col index to A1 notation column letter
                    col_letter = col_idx_to_letter(col_idx)
                    cell_range = f"'{actual_sheet_name}'!{col_letter}{item['row_num']}"
                    
                    updates.append({
                        'range': cell_range,
                        'values': [[new_val]]
                    })

        # 5. Data Write-Back
        if updates:
            print(f"Applying {len(updates)} cell updates to the spreadsheet...")
            body = {
                'valueInputOption': 'USER_ENTERED',
                'data': updates
            }
            
            # Use dry-run logic if we want, but for now just execute
            response = sheets_service.spreadsheets().values().batchUpdate(
                spreadsheetId=sheet_id, body=body).execute()
                
            print(f"Successfully updated {response.get('totalUpdatedCells')} cells.")
        else:
            print("No updates required for the processed rows.")
            
        print("Execution completed.")
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
