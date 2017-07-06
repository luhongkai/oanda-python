import os
import oandapy


client = oandapy.API(environment="practice", access_token=os.environ.get('OANDA_API_ACCESS_TOKEN'))
