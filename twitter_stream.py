#!/usr/bin/python3
# Python code here

#importing the necessary packages
from TwitterAPI import TwitterAPI
import json
import boto3
#import twitterCreds


#Reading in twitter credentials
consumer_key = ''
consumer_secret =''
access_token_key = ''
access_token_secret = ''

#creating the kinesis stream
try:
    client = boto3.client('kinesis')
    response = client.create_stream(
       StreamName='twitter-data-stream', #your streamname here
       ShardCount=1
    )
except:
    pass



#accessing the API
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

kinesis = boto3.client('kinesis')

#r = api.request('statuses/filter', {'follow':'629747990'})
list_terms = ['covid','virus', 'pandemic','pandemia','lockdown','coronavirus']
#for locations
r = api.request('statuses/filter', {'track': list_terms})
#for userids @abcdef:
#r = api.request('statuses/filter', {'follow':'123456'})
#for general text searches
#r = api.request('statuses/filter', {'track':'iphone'})



for item in r:
    tweet = json.loads(json.dumps(item))
    if 'text' in tweet and tweet['lang'] == "en":
        print(str(tweet['text']))
        kinesis.put_record(StreamName="twitter-data-stream", Data=str(tweet['text']), PartitionKey="filler")
