from facebookads.objects import Campaign

# APP_ID = '373872976314910'
# APP_SECRET = 'f16f5402f7ea9aca226a521417ddf35b'
# APP_TOKEN = 'EAAFUCRXxwh4BAL0CaTFCMyfzYdqABNXDUm9nZBiS95oQ5ruZBXeJrfZAedF8beHAnqtdfZBwvD3UuZBctbZCozUFbh5GBL2siwlM3UoXBjqdE2mh8ZCVgLEgXWuOpXJ6dZA077cNw2hFLfMicPnZBkE0B'
APP_ID = '1222989657750439'
APP_SECRET = '5e106ae4af144603b509b1c60f984a67'
# APP_TOKEN = 'EAARYTXgdO6cBAKRqYE2GZBkyBZCe0YbQaToWmwoOtSLlRw1x7EFeovJoNm3FgpdU3EAHeZBCD216mNrHhhIkKbdAzwCydcH6JoLxS4GZAzzQtYHRRQEQEgtZCZA3HOrdSXVaBdlU5Y8ild6CLCOJUYyJ6WkzFvjw8ZD'
APP_TOKEN = 'EAARYTXgdO6cBAGjOrpZAT7txfpHpqXjOjpNZBfGNEJIp04tjNvbzTgvlyRJtVZCdQhZAyWFfSJc8qGSLZAdgOZCRwDcqXBI83dF1Id3Ob2nZCWgIbZBLcXHWf7ZC4yhvZAV1wKnZCWgSpyu3NtCgV86TTalI1HceirvJ7EZD'
REPORT_FIELDS = [
	'impressions'
	, 'clicks'
	, 'spend'
	, 'website_clicks'
	, 'video_complete_watched_actions'
	, 'actions'
	, 'date_start'
	, 'date_stop'
]
DATE_PRESET = Campaign.DatePreset.last_7_days