from fastapi import FastAPI
import requests
import facebook
import json
# from social_data import Social_data_fetch
app = FastAPI()

# fc_post_id = '197394889304_10159954783384305'
#post_id = '147398588635445_4802642903110967'


@app.get("/ facebook/post_id={post_id}")
def Social_data_fetch(post_id):
    acc_token = "139033756598933|GREeGVe5-IEFLnVALH0MnRaXNbY"
    fields = 'shares.summary(1).limit(1),comments.summary(true),reactions.summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),reactions.type(CARE).limit(0).summary(1).as(care)'
    url = f"https://graph.facebook.com/v8.0/{post_id}/?fields={fields}&access_token={acc_token}"
    result = requests.get(url).json()
    shares = result['shares']['count']
    comments = result['comments']['summary']['total_count']
    reactions_count = result['reactions']['summary']['total_count']
    likes = result['like']['summary']['total_count']
    love = result['love']['summary']['total_count']
    care = result['care']['summary']['total_count']
    angry = result['angry']['summary']['total_count']
    laugh = result['haha']['summary']['total_count']
    sad = result['sad']['summary']['total_count']

    reactions_dict = {'Like': likes, 'Love': love,
                      'Care': care, 'Angry': angry, 'Laugh': laugh, 'Sad': sad}
    dict_ = {'Reactions': reactions_dict, 'Total Shares ': shares, 'Total Comments ': comments,
             'Total Reaction Counts ': reactions_count}

    response = json.dumps(dict_, indent=2)

    response = response.replace('\"', ' ').replace('\n', ' ')

    return response


# @app.get("/ facebook/post_id={post_id}")
# def social_data(post_id):
#     output = Social_data_fetch(post_id)
#     return output
