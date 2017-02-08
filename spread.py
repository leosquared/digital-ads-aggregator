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

## script
from csv import writer, reader

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

  result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name
    , valueInputOption='RAW', body=body).execute()

  return result

def delete_sheet_data(service, spreadsheet_id, sheet_name):
  """ deletes all data from a sheet """

  range_name = f'\'{sheet_name}\'!A:Z'
  body = {
    'ranges': [range_name]
  }
  response = service.spreadsheets().values().batchClear(spreadsheetId=spreadsheet_id,
                                               body=body).execute()
  return response

def main():

  spreadsheet_id = '1rEpy_9rsPecX9pSQmsrJkCDJHxcjkx6u9WY-jp5bwZQ'
  # range_name = 'raw!A1:Z100'
  service = initialize_sheets()
  
  # csvfile = reader(open('sample_report.csv', 'r'))
  # data = list(csvfile)
  
  # print(update_sheet(service, spreadsheet_id, 'raw', data))

  print(delete_sheet_data(service, spreadsheet_id, 'raw'))

if __name__ == '__main__':
  main()