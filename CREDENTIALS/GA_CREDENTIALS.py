# Credentials for berlinrosenca@gmail.com are stored here, for Google Analytics
JSON_FILE = 'CREDENTIALS/Search Reporting-534a8b279706.json'
SCOPES_MANAGEMENT = ['https://www.googleapis.com/auth/analytics.readonly']
SCOPES_ANALYTICS = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI_ANALYTICS = ('https://analyticsreporting.googleapis.com/$discovery/rest')
SERVICE_ACCOUNT_EMAIL = 'br-googleanalytics@search-reporting-144823.iam.gserviceaccount.com'
DISCOVERY_URI_SHEETS = ('https://sheets.googleapis.com/$discovery/rest?')
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_NAME = 'raw'
MASTER_SHEET_ID = '1f7r_6x1XyutqZib7n-o5eQ6Iklzx-sRkkrKE1tovSfY'
OUTPUT_FILE_NAME = 'outputs/analytics_output.csv'
TRANSLATOR_FILE = 'outputs/translator.json'
SHEET_ID_FILE = 'outputs/report_sheets.json'
METRICS = [
						'sessions'
						, 'impressions'
						, 'adClicks'
						, 'adCost'
						, 'bounces'
						, 'goalCompletionsAll'
						]
DIMENSIONS = [
							'date'
							, 'source'
							, 'medium'
							, 'campaign'
							, 'adContent'
							, 'adGroup'
							, 'keyword'
							]