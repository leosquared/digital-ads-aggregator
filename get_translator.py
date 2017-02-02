## Auth
import argparse
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

## must have CREDENTIALS.py in the same directory
from CREDENTIALS.URLTOOL_ARGS import *

## script operations
from csv import writer, reader
from pprint import pprint
import json

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

def get_sheet_data(sheets_service, spreadsheet_id, arg_name, sheet_name_dict, data_dict):
  """ retrieves data from a tab in a google spreadsheet """
  sheet_name = sheet_name_dict['sheet_name']
  range_name = f'\'{sheet_name}\'!A:Z'
  data = sheets_service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name).execute().get('values')

  data_dict[arg_name] = {'delim_position': sheet_name_dict['delim_position'], 'values':{}}

  for row in data[1:]:
    try:
      data_dict[arg_name]['values'][row[sheet_name_dict['col_num']]] = row[0]
    except:
      continue

  return data_dict

def output_translator(json_path, data):
  """ output data in a json format to use in the report script """

  with open(json_path, 'w') as ofile:
    ofile.write(json.dumps(data))

  return f'{OUTPUT_FILE_NAME} generated'

def main():

  service = initialize_sheets()
  data_dict = {}
  for arg_name in SHEET_NAMES:
    get_sheet_data(
      sheets_service=service
      , spreadsheet_id=SHEET_ID
      , arg_name=arg_name
      , sheet_name_dict=SHEET_NAMES[arg_name]
      , data_dict=data_dict
      )

  print(output_translator(OUTPUT_FILE_NAME, data_dict))



if __name__ == '__main__':
  main()