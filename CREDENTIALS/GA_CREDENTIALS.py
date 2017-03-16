# Credentials for berlinrosenca@gmail.com are stored here, for Google Analytics
JSON_FILE = 'CREDENTIALS/Search Reporting-534a8b279706.json'
SCOPES_MANAGEMENT = ['https://www.googleapis.com/auth/analytics.readonly']
SCOPES_ANALYTICS = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI_ANALYTICS = ('https://analyticsreporting.googleapis.com/$discovery/rest')
SERVICE_ACCOUNT_EMAIL = 'br-googleanalytics@search-reporting-144823.iam.gserviceaccount.com'
DISCOVERY_URI_SHEETS = ('https://sheets.googleapis.com/$discovery/rest?')
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
MASTER_SHEET_ID = '1f7r_6x1XyutqZib7n-o5eQ6Iklzx-sRkkrKE1tovSfY'
TRANSLATOR_FILE = 'outputs/translator.json'
SHEET_ID_FILE = 'outputs/report_sheets.json'

SHEET_NAMES = {
	1: 'ga_raw_1'
	, 2: 'ga_raw_2'
	, 3: 'ga_raw_3'
}

METRICS = {
	1: [
		'sessions'
		, 'goalCompletionsAll'
		, 'sessionDuration'
		, 'pageViews'
	]
	, 2: [
		'totalEvents'
	]
	, 3: [
		'impressions'
		, 'adClicks'
		, 'adCost'
	]
}

DIMENSIONS = {
	1: [
		'date'
		, 'source'
		, 'medium'
		, 'campaign'
	]
	, 2: [
		'date'
		, 'eventLabel'
		, 'campaign'
	]
	, 3: [
		'date'
		, 'adGroup'
		, 'adContent'
	]
}
