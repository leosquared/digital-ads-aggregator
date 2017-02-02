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
        }]
      }
  ).execute().get('reports')[0]

  return report

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

def output_report(report, ofile_name, account_name):
  """ takes a google analytics report object and loop through the json to get report into a spreadsheet format, reporting base file """

  report_data = report.get('data').get('rows')
  ofile = writer(open(ofile_name, 'a'))
  ga_metrics = [x.get('name') for x in report.get('columnHeader').get('metricHeader').get('metricHeaderEntries')]
  ga_dimensions = report.get('columnHeader').get('dimensions')
  with open(TRANSLATOR_FILE, 'r') as f:
    translator_json = json.loads(f.read())

  if report_data:
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

def update_sheet(sheets_service, spreadsheet_id, sheet_name, data):
  """ take a list of values then write it to the specified sheet """

  range_name = f'\'{sheet_name}\'!A:Z'
  values = data
  body = { 'values': values }

  result = sheets_service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name
    , valueInputOption='USER_ENTERED', body=body).execute()

  return result


def main():

  ga_views = get_views(initialize_management())

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
  for view_id in ga_views:
    print('Running Report for {} ...'.format(ga_views[view_id]))
    report = get_report_obj(analytics, view_id=view_id
            , metrics=METRICS, dimensions=DIMENSIONS)
    output_report(report, OUTPUT_FILE_NAME, account_name=ga_views[view_id])
    print('Report output generated!\n')

  ## Update in google sheets
  with open(OUTPUT_FILE_NAME, 'r') as f:
    r = reader(f)
    data = list(r)
  for row in data:
    row[1] = '{}/{}/{}'.format(row[1][4:6], row[1][6:], row[1][:4])
  update_obj = update_sheet(initialize_sheets(), SHEET_ID, SHEET_NAME, data)

  print('{} Rows Updated in https://docs.google.com/spreadsheets/d/{}/edit'.format(update_obj.get('updatedRows'), SHEET_ID))


if __name__ == '__main__':
  main()

