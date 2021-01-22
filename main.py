import boto3
from pprint import pprint
from fastapi import FastAPI
import requests
import facebook
import json
app = FastAPI()

fc_post_id = '197394889304_10159954783384305'
# post_id = '147398588635445_4802642903110967'
page_id = 197394889304_1296107324101971

aws_access_key_id = 'AKIA3M4LJ3HMVYHXMMCO'
aws_secret_access_key = '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'
acc_token = "139033756598933|GREeGVe5-IEFLnVALH0MnRaXNbY"


@app.get("/facebook/post_id={post_id}")
def Fb_Reaction_DataFetch(post_id):
    dynamodb = None
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)

    table = dynamodb.Table('fb_engagements')
    # acc_token = "139033756598933|GREeGVe5-IEFLnVALH0MnRaXNbY"
    fields = 'shares.summary(1).limit(1),comments.summary(true),reactions.summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),reactions.type(CARE).limit(0).summary(1).as(care)'
    url = f"https://graph.facebook.com/v9.0/{post_id}/?fields={fields}&access_token={acc_token}"
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


# video_id_sample = 197394889304_4202125126468246


@app.get("/facebook/video_id={video_id}")
def Fb_VideoData_to_Dynamodb(video_id):
    dynamodb = None
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)

    table = dynamodb.Table('Fb_Video_Data')

    access_token = "139033756598933|GREeGVe5-IEFLnVALH0MnRaXNbY"
    api_version = "v9.0"
    fields = 'shares.summary(1).limit(1),comments.summary(true),reactions.summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),reactions.type(CARE).limit(0).summary(1).as(care)'

    url = f"https://graph.facebook.com/{api_version}/{video_id}?fields={fields}&access_token={access_token}"
    # url_ = f"https://graph.facebook.com/{api_version}/{video_id}/insights?&access_token={access_token}"
    response = requests.get(url).json()
    # response_ = requests.get(url_).json()
    item = {video_id: response}
    # print('item', response_)
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

# data_insert = table.put_item(Item=item)
# graph = facebook.GraphAPI(access_token)
# response_1 = graph.get_object(
#     f'https://graph.facebook.com/{api_version}/{video_id}/views')
