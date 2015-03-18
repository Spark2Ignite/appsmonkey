import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
from apiclient.http import HttpError
from pprint import pprint
from optparse import OptionParser

usage = "usage: %prog [options] DOMAIN"
parser = OptionParser(usage)
parser.add_option("-l", action='store',  help="list customer subscriptions for DOMAIN")
parser.add_option("-p", action='store',  help="print customer details for DOMAIN")
parser.add_option("-r", action='store',  help="set renewal options for DOMAIN")

options, args = parser.parse_args()

# establish the list of scopes.
OAUTH2_SCOPES = [
    'https://www.googleapis.com/auth/apps.order',
    'https://www.googleapis.com/auth/siteverification',
    'https://www.googleapis.com/auth/admin.directory.user'
]

# replace with your own values.
SERVICE_ACCOUNT_EMAIL = '243249193855-v5ahmll4pkrq8sft61ttk1fbc4k7io2c@developer.gserviceaccount.com'
PRIVATE_KEY_FILE = 'key.p12'
RESELLER_ADMINISTRATOR_USER = 'vadim@doit-g.co.il'

# create an HTTP client
http = httplib2.Http()

# read private key.
f = file(PRIVATE_KEY_FILE)
key = f.read()
f.close()

# establish the credentials.
credentials = SignedJwtAssertionCredentials(
    service_account_name=SERVICE_ACCOUNT_EMAIL,
    private_key=key,
    scope=' '.join(OAUTH2_SCOPES),
    sub=RESELLER_ADMINISTRATOR_USER)

# authorize
credentials.authorize(http)

# utilize the same http object constructed earlier.
service = build(serviceName='reseller',
                version='v1',
                http=http)

# default vault of false.
customer_exists = False

# create subscription object for given domain
try:
    subscription_record = service.subscriptions().list(customerId=options.domain).execute()
    subscription_exists = True
except HttpError, ex:
    if int(e.resp['status']) == 404:
        # customer record not found
        customer_exists = False
    else:
        # unknown error!
        raise

# create customer object for given domain
try:
    customer_record = service.customers().get(customerId=options.domain).execute()
    # a customer record was returned, customer exists
    customer_exists = True
except HttpError, ex:
    if int(e.resp['status']) == 404:
        # customer record not found
        customer_exists = False
    else:
        # unknown error!
        raise

pprint(customer_record)

# if options.cmd==
#     print "reading %s..." % options.filename

for subscription in subscription_record["subscriptions"]:
    if subscription["skuId"] == 'Google-Apps-For-Business':
        pprint(subscription)

        # pprint(subscription_record)