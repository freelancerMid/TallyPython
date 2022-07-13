# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from google.oauth2 import service_account


def sheetCall():
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	SERVICE_ACCOUNT_FILE = 'key.json'

	creds = None

	creds = service_account.Credentials.from_service_account_file(
		SERVICE_ACCOUNT_FILE, scopes=SCOPES)

	# If modifying these scopes, delete the file token.json.

	# The ID and range of a sample spreadsheet.
	SAMPLE_SPREADSHEET_ID = '1roT3nDDXr20Qhca1FaSnxE40WhTBUvdxvvsUqFubArg'


	service = build('sheets', 'v4', credentials=creds)
	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="A1:C5").execute()

	values = result.get('values', [])
	print(values)
