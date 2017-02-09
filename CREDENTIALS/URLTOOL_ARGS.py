# Args for getting data from the URL Builder tool
JSON_FILE = 'CREDENTIALS/Search Reporting-534a8b279706.json'
SERVICE_ACCOUNT_EMAIL = 'br-googleanalytics@search-reporting-144823.iam.gserviceaccount.com'
DISCOVERY_URI_SHEETS = ('https://sheets.googleapis.com/$discovery/rest?')
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
MASTER_SHEET_ID = '1f7r_6x1XyutqZib7n-o5eQ6Iklzx-sRkkrKE1tovSfY'
SHEET_NAMES = {
		'utm_campaign': {'sheet_name': 'audience', 'col_num': 1, 'delim_position': 0}
		, 'utm_source': {'sheet_name': 'platform', 'col_num': 1, 'delim_position': 0}
		, 'utm_medium': {'sheet_name': 'platform', 'col_num': 2, 'delim_position': 0}
		, 'utm_content': {'sheet_name': 'creative', 'col_num': 3, 'delim_position': 0}
	}
TRANSLATOR_FILE = 'outputs/translator.json'
SHEETS_FILE = 'outputs/report_sheets.json'
REPORT_SHEET_NAME = 'spreadsheets'