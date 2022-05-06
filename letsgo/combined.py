import requests
import json
import tweepy
import os 
consumer_key='jcsIBC2MB25FpRcWJO5tcXDtt'
consumer_secret='mV2Gv2bW6SSg4hXrLMV1ieXDS7Md8rlJqkqzo70oDEB6xtKpAT'
# tweet_access_token=''
# access_token_secret=''

# page_id=109214341345652
# itoken='EAAoZBLaZASEOUBAPmxBoBtEA3E9zf6PoJ534E6vwxuBbQWm9e9WwS4o4egEMxhdDzL885ZA8jhN7QWRD58pBmaffuvJutMS7VZCaNL4JLGfYiqfTfq8UNfpfQ08oswbE4grQnej3jLmz594ZBwwH70sOJS54OCRdSA4g3mgw00spYMEZBZATgZABlooNpzvCqJlKZB9cOzAZAanRIDpnleZC7ZBORtT9Tbkr3nDJxC0GRboZCtp6ikMmuh06B'
# def set_var(key,secret):
#     global tweet_access_token,access_token_secret
#     tweet_access_token=key
#     access_token_secret=secret
def OAuth(tweet_access_token,access_token_secret):
        auth= tweepy.OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(tweet_access_token,access_token_secret)
        return auth

def post_img(fb_id,img_url,msg,atoken):
    msg=msg
    page_id=fb_id
    image_url='https://graph.facebook.com/{}/photos'.format(page_id)
    image_loc=img_url
    img_payload={
    'message':msg,
    'url':image_loc,
    'access_token':atoken,

    }
    r=requests.post(image_url,data=img_payload)
    print(r.text)
    # insta_post()

def post_status(page_id,msg,token):
    
    atoken=token
    print(atoken)
    
    post_url='https://graph.facebook.com/{}/feed'.format(page_id)
    
    mesg=msg
    payload={
             'message':msg,
             'access_token':atoken,
               }  
    r=requests.post(post_url,data=payload)
    print(r.text)

def insta_post(insta_id,itoken,img_url,msg):
    msg=msg
    ig_user_id=insta_id
    image_location_1=img_url
    post_url='https://graph.facebook.com/v10.0/{}/media'.format(ig_user_id)
    payload = {
          'image_url':image_location_1,
          'caption':msg,
          'access_token':itoken,

             }  
    r=requests.post(post_url,data=payload)
    print(r.text)
    result=json.loads(r.text)
    if 'id' in result:
        creation_id=result['id']
        second_url='https://graph.facebook.com/{}/media_publish'.format(ig_user_id)
        second_payload={
             'message':msg,
             'creation_id':creation_id,
             'access_token':itoken
        }
        r=requests.post(second_url,data=second_payload)
        print(r.text)
    else:
        print("we have problm")

def twitter_status(key,secret,msg):
    oath=OAuth(key,secret)
    api=tweepy.API(oath)
    status=msg
    api.update_status(status)
    print("done")

def twitter_img(key,secret,url,msg):
    
    oath=OAuth(key,secret)
    api=tweepy.API(oath) 
    message=msg
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")
