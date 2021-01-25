import boto3
from pprint import pprint
from fastapi import FastAPI
import requests
import facebook
import json
import os
from decouple import config
from utils.enviornment import Environment
import re
app = FastAPI()
environment = Environment()

# fc_post_id = '197394889304_10159954783384305'
# post_id = '147398588635445_4802642903110967'
# page_id = 197394889304_1296107324101971
# video_id_sample = 197394889304_4202125126468246
'''
post_id example to get request API's below  :

post?_id ='page_id_post_id'

'''

dynamodb = None
if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name=environment.region, aws_access_key_id=environment.aws_access_key_id,
                              aws_secret_access_key=environment.aws_secret_access_key)


@app.get("/facebook/post_id={post_id}")
def Fb_Reaction_DataFetch(post_id):

    table = dynamodb.Table('fb_engagements')
    fields = 'shares.summary(1).limit(1),comments.summary(true),reactions.summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),reactions.type(CARE).limit(0).summary(1).as(care)'
    url = f"https://graph.facebook.com/v9.0/{post_id}/?fields={fields}&access_token={environment.access_token}"
    result = requests.get(url).json()
    shares = result['shares']['count']
    comments = result['comments']['summary']['total_count']
    reactions_count = result['reactions']['summary']['total_count']
    likes = result['like']['summary']['total_count']
    love = result['love']['summary']['total_count']
    wow = result['wow']['summary']['total_count']
    care = result['care']['summary']['total_count']
    angry = result['angry']['summary']['total_count']
    laugh = result['haha']['summary']['total_count']
    sad = result['sad']['summary']['total_count']

    reactions_dict = {'Like': likes, 'Love': love,
                      'Care': care, 'Angry': angry, 'Laugh': laugh, 'Sad': sad, 'Wow': wow}
    dict_ = {'Reactions': reactions_dict, 'Total Shares ': shares, 'Total Comments ': comments,
             'Total Reaction Counts ': reactions_count}

    response = json.dumps(dict_, indent=2)
    response = response.replace('\"', '').replace('\n', '')

    item = {'post_id': post_id, 'response': response}

    data_insert = table.put_item(Item=item)
    return response


@app.get("/facebook/video_id={video_id}")
def Fb_VideoData_to_Dynamodb(video_id):

    table = dynamodb.Table('Fb_Video_Data')
    api_version = "v9.0"
    fields = 'shares.summary(1).limit(1),comments.summary(true),reactions.summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),reactions.type(CARE).limit(0).summary(1).as(care)'

    url = f"https://graph.facebook.com/{api_version}/{video_id}?fields={fields}&access_token={environment.access_token}"
    response = requests.get(url).json()
    item = {video_id: response}
    comments = response['comments']['summary']['total_count']
    love = response['love']['summary']['total_count']
    wow = response['wow']['summary']['total_count']
    care = response['care']['summary']['total_count']
    likes = response['like']['summary']['total_count']
    sad = response['sad']['summary']['total_count']
    laugh = response['haha']['summary']['total_count']
    angry = response['angry']['summary']['total_count']
    reactions_count = response['reactions']['summary']['total_count']
    shares = response['shares']['count']
    reactions_dict = {'Like': likes, 'Love': love,
                      'Care': care, 'Angry': angry, 'Laugh': laugh, 'Sad': sad, 'Wow': wow}
    dict_ = {'Reactions': reactions_dict, 'Total Shares ': shares, 'Total Comments ': comments,
             'Total Reaction Counts ': reactions_count}

    response = json.dumps(dict_, indent=2)
    response = response.replace('\"', '').replace('\n', '')
    item = {'video_id': video_id, 'response': response}
    print('item', item)
    data_insert = table.put_item(Item=item)
    return response


@app.get("/twitter/tweet={tweet_id}")
def Get_Twitter_data_engagement(tweet_id):
    table = dynamodb.Table('Twitter_Data')
    auth_key = environment.twitter_Bearer
    twitter_url = environment.twitter_url
    headers = environment.twitter_Bearer
    url = environment.twitter_url.format(tweet_id)
    response = requests.get(url, headers=headers).json()
    tweet_id = response['data'][0]['id']
    tweeted_text = response['data'][0]['text']
    retweet_count = response['data'][0]['public_metrics']['retweet_count']
    reply_count = response['data'][0]['public_metrics']['reply_count']
    like_count = response['data'][0]['public_metrics']['like_count']
    quote_count = response['data'][0]['public_metrics']['quote_count']

    dict_ = {'Tweet_ID :': tweet_id, 'Tweet :': tweeted_text, 'Retweet_count :': retweet_count,
             'Replies count :': reply_count, 'Likes_count :': like_count, 'Quote_count :': quote_count}

    response = json.dumps(dict_, indent=2).encode('utf-8')
    response = str(json.loads(response)).replace('\"', '').replace('\n', '')
    item = {'Tweet_id': tweet_id, 'response': response}
    print('item', item)
    table.put_item(Item=item)

    return response
