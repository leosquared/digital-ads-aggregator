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
import sys

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
						, 'dateRanges': [{'startDate': '30daysAgo'
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




## -------------------- Script -------------------- ##
analytics = initialize_analytics()
reports = get_report_obj(analytics, view_id='94396389'
						, metrics=METRICS, dimensions=DIMENSIONS)

# pprint(
# 	[len(x.get('data').get('rows')) for x in reports]
# )
for report in reports[:1]:
	for row in report.get('data').get('rows'):
		print(row)