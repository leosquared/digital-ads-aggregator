## Auth
import argparse
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

## must have CREDENTIALS.py in the same directory
from CREDENTIALS.GA_CREDENTIALS import *

## For Script
from pprint import pprint
from collections import OrderedDict, Iterable
from csv import writer, reader
import re, json

## ******************** Google Analytics & Adwords Report Output ******************** ##

def initialize_management():
  """ get a management API object for a list of accounts, etc """

  credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scopes=SCOPES_MANAGEMENT)
  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build('analytics', 'v3', http=http)

  return service

def get_views(management_service):
  """ get a list of views, using the view IDs to get reports """

  def clean_name(unit_name):
    """ clean up names of web properties in google analytics that have irregular characters """

    return re.sub('[^A-Za-z0-9]+', ' ', unit_name)
  
  ga_views = OrderedDict()
  accounts = management_service.management().accountSummaries().list().execute().get('items')
  for acc in accounts:
    for wp in acc.get('webProperties'):
      for view in wp.get('profiles'):
        ga_views[view.get('id') ] = '{}-{}'.format(clean_name(wp.get('name')), clean_name(view.get('name')))

  return ga_views

def initialize_analytics():
  """ Initializes an analyticsreporting service object. """

  credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scopes=SCOPES_ANALYTICS)
  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI_ANALYTICS)

  return service

def get_report_obj(analytics_service, view_id, dimensions, metrics):
  """ Use the Analytics Service Object to query the Analytics Reporting API V4. """
  
  dimensions_input = []
  for d in dimensions:
    dimensions_input.append({'name': f'ga:{d}'})

  metrics_input = []
  for m in metrics:
    metrics_input.append({'expression': f'ga:{m}'})

  reports = []
  report = {'nextPageToken': '0'}
  while report.get('nextPageToken') is not None:
    report = analytics_service.reports().batchGet(
        body={
          'reportRequests': [
          {
            'viewId': view_id
            , 'dateRanges': [{'startDate': '60daysAgo'
              , 'endDate': '1daysAgo'}]
            , 'metrics': metrics_input
            , 'dimensions': dimensions_input
            , 'includeEmptyRows': False
            , 'pageSize': 10000
            , 'pageToken': report.get('nextPageToken')
          }]
        }
    ).execute().get('reports')[0]
    reports.append(report)

  return reports

def translate_dimension(translator_json, dimension_name, dimension_value):
  """ translates a raw dimension value into human readable ones """

  dim_name = dimension_name.replace('ga:', 'utm_')

  if not translator_json.get(dim_name):
    return dimension_value
  else:
    try:
      return translator_json[dim_name]['values'] \
          .get(dimension_value.split('-')[translator_json[dim_name]['delim_position']]) or dimension_value
    except:
      return 'other'

def output_report(reports, ofile_name, account_name):
  """ takes a google analytics report object and loop through the json to get report into a spreadsheet format, reporting base file """

  first_report = reports[0]
  report_data = first_report.get('data').get('rows') # first report's headers
  ofile = writer(open(ofile_name, 'a'))
  ga_metrics = [x.get('name') for x in first_report.get('columnHeader').get('metricHeader').get('metricHeaderEntries')]
  ga_dimensions = first_report.get('columnHeader').get('dimensions')
  with open(TRANSLATOR_FILE, 'r') as f:
    translator_json = json.loads(f.read())

  if report_data:
    for report in reports:
      for row in report_data:

        translated_dimensions = []
        for i, dim in enumerate(row.get('dimensions')):
          translated_dimensions.append(translate_dimension(translator_json, ga_dimensions[i], dim))

        for i, m in enumerate(ga_metrics):
          values = row.get('metrics')[0].get('values')
          if float(values[i])!=0:
            ofile.writerow([account_name] + translated_dimensions + [m, values[i]])

  return None

## ******************** Uploading to Google Sheet raw data ******************** ##

def initialize_sheets():
  """ creates a service object for uploading data to google sheets """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scopes=SCOPES_SHEETS)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build('sheets', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI_SHEETS)

  return service

def delete_sheet_data(sheets_service, spreadsheet_id, sheet_name):
  """ deletes all data from a sheet """

  range_name = f'\'{sheet_name}\'!A:Z'
  body = {
    'ranges': [range_name]
  }
  response = sheets_service.spreadsheets().values().batchClear(spreadsheetId=spreadsheet_id,
                                               body=body).execute()
  return response


def update_sheet(sheets_service, spreadsheet_id, sheet_name, data):
  """ take a list of values then write it to the specified sheet """

  range_name = f'\'{sheet_name}\'!A:Z'
  values = data
  body = { 'values': values }

  result = sheets_service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name
    , valueInputOption='USER_ENTERED', body=body).execute()

  return result

## ******************** Begin Script ******************** ##

def main():

  analytics = initialize_analytics()

  ## write header row
  with open(OUTPUT_FILE_NAME, 'w') as f:
    writer(f).writerow(['account'] + DIMENSIONS + ['metric'] + ['metric_value'])

  # ## run one off report
  # report = get_report_obj(analytics, view_id=list(ga_views.keys())[0]
  #         , metrics=METRICS, dimensions=DIMENSIONS)
  # output_report(report, 'test.csv', account_name='hello')
  
  import get_translator

  ## Run report for each web property

  with open(SHEET_ID_FILE, 'r') as f:
    ga_views = json.loads(f.read())

  for view_id in ga_views:

    ## write header row
    file_name = f'outputs/report {ga_views[view_id]["report_name"]}.csv'
    with open(file_name, 'w') as f:
      writer(f).writerow(['account'] + DIMENSIONS + ['metric'] + ['metric_value'])

    ## Ping API and run report

    print(f'\n\nRunning Report for {ga_views[view_id]["report_name"]} ...')
    report = get_report_obj(analytics, view_id=view_id
            , metrics=METRICS, dimensions=DIMENSIONS)
    output_report(report, file_name, account_name=ga_views[view_id]['report_name'])
    print('Report output generated!\n')

  ## Update in google sheets
    with open(file_name, 'r') as f:
      r = reader(f)
      data = list(r)
    ## transform date
    for row in data:
      row[1] = '{}/{}/{}'.format(row[1][4:6], row[1][6:], row[1][:4])
    ## delete data first
    service = initialize_sheets()
    delet_obj = delete_sheet_data(service, ga_views[view_id]['sheet_id'], SHEET_NAME)
    update_obj = update_sheet(service, ga_views[view_id]['sheet_id'], SHEET_NAME, data)

    print(f'{update_obj.get("updatedRows")} Rows Updated in https://docs.google.com/spreadsheets/d/{ga_views[view_id]["sheet_id"]}/edit')


if __name__ == '__main__':
  main()

