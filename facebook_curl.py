## Google Sheets Auth
import argparse
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from CREDENTIALS.FB_CREDENTIALS import *

## for curl calls
import json, subprocess, pprint, time

def initialize_sheets():
  """ creates a service object for uploading data to google sheets """
  
  credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scopes=SCOPES_SHEETS)
  http = credentials.authorize(httplib2.Http())
  service = build('sheets', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI_SHEETS)

  return service

def get_sheet_data(sheets_service, spreadsheet_id, sheet_name):
  """ retrieves data from a tab in a google spreadsheet """
  
  range_name = f'\'{sheet_name}\'!A:Z'
  data = sheets_service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name).execute().get('values')
  result = {}
  for row in data[1:]:
  	result[row[0]] = {'ad_account_id': row[1], 'access_token': row[2], 'report_sheet_id': row[3]}
  
  return result


def delete_sheet_data(sheets_service, spreadsheet_id, sheet_name):
  """ deletes all data from a specified sheet, from ranges A-Z """

  range_name = f'\'{sheet_name}\'!A:Z'
  body = {
    'ranges': [range_name]
  }
  response = sheets_service.spreadsheets().values().batchClear(spreadsheetId=spreadsheet_id,
                                               body=body).execute()
  return response


def get_campaign_report(campaign_id, access_token, fields, time_ranges):
	""" obtains dict of an ad campaign with specified fields """
	
	sr = subprocess.run(
		[
			'curl', '-G', '-#'
			, '-d', f"fields={','.join(fields)}"
			, '-d', f"time_ranges={str(time_ranges).replace(' ', '')}"
			, '-d', f"access_token={access_token}"
			, f"https://graph.facebook.com/v2.8/{campaign_id}/insights"
		]
		, stdout=subprocess.PIPE
		, encoding='utf-8'
	)

	js = json.loads(f"{sr.stdout}")
	print(js)

	return js.get('data')

def ls_campaigns(ad_account_id, access_token):
	""" get a list of campaign ids in an account account """

	sr = subprocess.run(
		[
			'curl', '-G', '-#'
			, '-d', "fields=campaign_id"
			, '-d', f"access_token={access_token}"
			, f"https://graph.facebook.com/v2.8/act_{ad_account_id}/campaigns"
		]
		, stdout=subprocess.PIPE
		, encoding='utf-8'
	)
	js = json.loads(f"{sr.stdout}")
	campaigns = [x.get('id') for x in js.get('data')]
	
	return campaigns

def transform_data(report_obj):
	""" takes a report output and transform it into columns and rows with header """

	data = []
	if not report_obj:
		return None
	else:
		header_row = DIMENSIONS + ['metric_name', 'metric_value']
		data.append(header_row)
		for d in report_obj:
			for m in METRICS:
				data_row = []
				data_row.extend([d.get(x) for x in DIMENSIONS])
				data_row.append(m)
				data_row.append(d.get(m))
				data.append(data_row)
			for action in d.get('actions'):
				data_row = []
				data_row.extend([d.get(x) for x in DIMENSIONS])
				data_row.append(action.get('action_type'))
				data_row.append(action.get('value'))
				data.append(data_row)

		return data

def update_sheet(sheets_service, spreadsheet_id, sheet_name, data):
  """ take a list of values then write it to the specified sheet """

  range_name = f'\'{sheet_name}\'!A:Z'
  values = data
  body = { 'values': values }

  result = sheets_service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name
    , valueInputOption='USER_ENTERED', body=body).execute()

  return result




## ******************** Main Script ******************** ##

service = initialize_sheets()
ad_accounts = get_sheet_data(service, MASTER_SHEET_ID, MASTER_SHEET_NAME)

for account_name, ad_account in ad_accounts.items():
	campaigns = ls_campaigns(ad_account_id=ad_account['ad_account_id'], access_token=ad_account['access_token'])
	account_data = []
	for campaign in campaigns:
		r = get_campaign_report(campaign_id=campaign
					, access_token=ad_account['access_token'], fields=FIELDS
					, time_ranges=TIME_RANGES)
		if r:
			account_data.extend(transform_data(r))
	pprint.pprint(
		delete_sheet_data(service, ad_account['report_sheet_id'], REPORT_SHEET_NAME)
	)
	pprint.pprint(
		update_sheet(service, ad_account['report_sheet_id'], REPORT_SHEET_NAME, account_data)
	)


# ## run script
# campaigns = ls_campaigns(ad_account_id='124668274277892', access_token=access_token)
# pprint.pprint(campaigns)

# for campaign in campaigns:
# 	time.sleep(2)
# 	pprint.pprint(
# 		get_campaign_report(campaign_id=campaign
# 		, access_token=access_token, fields=fields
# 		, date_preset=date_preset)
# 	)
