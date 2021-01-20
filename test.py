from fastapi import FastAPI
import json
from urllib.request import urlopen
# from bs4 import BeautifulSoup
#
# # for page in range(0, 50):
# #     url = "https://twitter.com/FCBarcelona".format(page)
# #     html = urlopen(url)
# #     soup = BeautifulSoup(html, "html.parser")
# #     tweets = soup.find_all("li", attrs={"class": "js-stream-item"})
# #
# # for tweet in tweets:
# #     try:
# #         if tweet.find('p',{"class":'tweet-text'}):
# #             tweet_text = tweet.find('p', {"class": 'tweet-text'}).text.encode('utf8').strip()
# #             retweets = tweet.find('span', {"class": "ProfileTweet-action--retweet"}).text.strip()
# #             print(retweets)
# #     except: AttributeError
# #
# #
# #     for
# #         print()
import requests

token_response = requests.post(url='http://ds-management-app-uat.uat.awsinternal/api/v1.0/users/token', json={
                               'username': 'automation', 'password': 'AutoBot7'}, headers={'Content-Type': 'application/json'})
graph = facebook.GraphAPI(access_token=environment.ACCESS_TOKEN)
acc_token = "139033756598933|GREeGVe5-IEFLnVALH0MnRaXNbY"
post_id = '147398588635445_4802642903110967'
fields = 'shares.summary(1).limit(1),comments.summary(true),reactions.summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),reactions.type(CARE).limit(0).summary(1).as(care)'
url = "https://graph.facebook.com/v8.0/{}/?fields={}&access_token={}".format(
    post_id, fields, acc_token)
print('url', url)
result = requests.get(url).json()
# https://graph.facebook.com/v8.0/147398588635445_4802642903110967/?fields=shares.summary(1).limit(1),comments.summary(true),reactions.summary(1),reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry),reactions.type(CARE).limit(0).summary(1).as(care)&access_token=139033756598933|GREeGVe5-IEFLnVALH0MnRaXNbY
print(result)
token_response = requests.post(url='http://ds-management-app-uat.uat.awsinternal/api/v1.0/users/token', json={
                               "username": 'uat_admin', "password": 'uat9d@as'}, headers={'Content-Type': 'application/json'})
print(json.loads(token_response.text))

access_token = json.loads(token_response.text)['token']

channel_response = requests.get(url='http://ds-management-app-uat.uat.awsinternal/api/v1.0/channels/?type=2&hash_num=0&hash_total=1',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': 'Token {}'.format(
                                        access_token)})
print("hello", json.loads(channel_response.text)['results'])
channel_json = json.loads(channel_response.text)
print("channel_json['next']", channel_json['next'])
# vowels = ['a', 'e', 'i', 'o', 'i', 'u']

# for i in vowels:
# print(vowels.index(i))
# if vowels.index(i) == -1:
#     print(i)
