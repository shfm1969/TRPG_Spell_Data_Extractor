import codecs
from dotenv import load_dotenv
from googleapiclient.discovery import build
from app import get_credentials, get_doc_text

load_dotenv()
creds = get_credentials()
docs_service = build('docs', 'v1', credentials=creds)

text = get_doc_text(docs_service, '12gkApfn8nDcJTJlW5zL13UijP8k83UqIZGtRtCRAuBQ')
with codecs.open('doc_output.txt', 'w', 'utf-8') as f:
    f.write(text)
