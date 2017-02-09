from datetime import date, timedelta

JSON_FILE = 'CREDENTIALS/Search Reporting-534a8b279706.json'
SERVICE_ACCOUNT_EMAIL = 'br-googleanalytics@search-reporting-144823.iam.gserviceaccount.com'
DISCOVERY_URI_SHEETS = ('https://sheets.googleapis.com/$discovery/rest?')
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
MASTER_SHEET_ID = '1f7r_6x1XyutqZib7n-o5eQ6Iklzx-sRkkrKE1tovSfY'
MASTER_SHEET_NAME = 'fb_accounts'
FIELDS = [
	'campaign_id'
	, 'campaign_name'
	, 'account_name'
	, 'impressions'
	, 'objective'
	, 'reach'
	, 'spend'
	, 'actions'
	, 'action_values'
]
DIMENSIONS = [
	'account_name'
	, 'campaign_name'
	, 'date_start'
	, 'date_stop'
	, 'objective'
]
METRICS = [
	'impressions'
	, 'reach'
	, 'spend'
]
DATE_PRESET = 'last_7_days'
# TIME_RANGE = "{'since': '2017-01-01', 'until': '2017-02-07'}"
TIME_RANGES = [{
	'since': (date.today()-timedelta(days=7)).strftime('%Y-%m-%d')
	, 'until': (date.today()-timedelta(days=1)).strftime('%Y-%m-%d')
}
, {
	'since': (date.today()-timedelta(days=14)).strftime('%Y-%m-%d')
	, 'until': (date.today()-timedelta(days=8)).strftime('%Y-%m-%d')
}]
REPORT_SHEET_NAME = 'fb_raw'