## Auth
import argparse
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

## must have CREDENTIALS.py in the same directory
from CREDENTIALS import *

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

def main():

  spreadsheet_id = '17Qf7D6pzR5mK90L2sjzo90JaRBY2OYhA28lOUDrn6rU'
  range_name = 'test2!A1:Z3'
  service = get_credentials()
  
  csvfile = reader(open('sample_report.csv', 'r'))
  data = list(csvfile)
  
  print(update_sheet(service, spreadsheet_id, 'test2', data))

if __name__ == '__main__':
  main()