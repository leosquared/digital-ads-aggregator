## Auth
from facebookads import FacebookSession
from facebookads import FacebookAdsApi
from facebookads.objects import (
    AdUser,
    Campaign,
    AdAccount,
)
from FB_CREDENTIALS import *

# operations
import json, os, pprint, time, dateutil.parser, dateutil.relativedelta
from datetime import datetime, timedelta

def init_ad_user():
    """ return an aduser object to access accounts & campaigns """

    ## Setup session and api objects
    session = FacebookSession(APP_ID, APP_SECRET, APP_TOKEN)
    api = FacebookAdsApi(session)
    FacebookAdsApi.set_default_api(api)
    me = AdUser(fbid='me')
    
    return me

def campaign_stats(my_account):
    """ for a given account, generate states associated with all campaigns in that account """

    report = {}

    params = {
        'date_preset': DATE_PRESET
    }

    for campaign in my_account.get_campaigns(fields=[Campaign.Field.name, Campaign.Field.stop_time]):
        campaign_name = campaign[campaign.Field.name]
        
        ## filter campaigns by date
        campaign_end_date = campaign.get(campaign.Field.stop_time) or '1901-01-01' # sometimes "stop_time" arg is empty, wtf
        campaign_end_date = dateutil.parser.parse(campaign_end_date).date()

        if campaign_end_date >= datetime.today().date() + dateutil.relativedelta.relativedelta(days=-30):
            stat_grp = campaign.get_insights(fields=REPORT_FIELDS, params=params)
            report[campaign_name] = {}
            if stat_grp:
                for stats in stat_grp:
                    for stat in stats:
                        if stat=='actions':
                            for action in stats[stat]:
                                report[campaign_name][stat+'-'+action['action_type']] = action['value']
                        else: 
                            report[campaign_name][stat] = stats[stat]

    return report


pp = pprint.PrettyPrinter(indent=4)


if __name__ == '__main__':
    
    me = init_ad_user()

    # ## Read user permissions
    # print('>>> Reading permissions field of user:')
    # pp.pprint(me.remote_read(fields=[AdUser.Field.permissions]))

    my_accounts = me.get_ad_accounts(fields=[AdAccount.Field.name])
    # print(my_accounts[6].get_campaigns(fields=[Campaign.Field.name]))
    campaign_stats(my_accounts[6])

    # for acc in my_accounts:
    #     print('\n\n\n\n')
    #     pp.pprint(acc)
    #     print('\n\n\n\n')
    #     try:
    #         pp.pprint(campaign_stats(acc))
    #     except Exception as e:
    #         print(e)
            

    
