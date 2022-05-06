import requests
import json
from .models import User_details
page_id=''
aid=2883115551953125
asecret='352a87e92cb615c2173895e10b69f1c4'
def get_atoken(usertoken):
    print(type(usertoken),usertoken)
    ll_usertoken='https://graph.facebook.com/v6.0/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'.format(aid,asecret,usertoken)
    
    r=requests.get(ll_usertoken)
    print(r.text)
    print(type(r))
    r=r.json()
    ll_accesstoken=r["access_token"]
    print(ll_accesstoken)
    userid='https://graph.facebook.com/v6.0/me?access_token={}'.format(ll_accesstoken)
    r1=requests.get(userid)
    r1=r1.json()
    user_id=r1["id"]
    ll_pagetoken='https://graph.facebook.com/{}/accounts?access_token={}'.format(user_id,ll_accesstoken)
    r2=requests.get(ll_pagetoken)
    r2=r2.json()
    atoken=r2['data'][0]['access_token']
    global page_id
    page_id=r2['data'][0]['id']
    user_name=r2['data'][0]['name']
    insta='https://graph.facebook.com/v10.0/{}?fields=instagram_business_account&access_token={}'.format(page_id,ll_accesstoken)
    i1=requests.get(insta)
    print(i1.text)  
    i1=i1.json()
    insta_id=i1["instagram_business_account"]["id"]
    print(insta_id)
    order=User_details(user_name=user_name,page_id=page_id,access_token=atoken,insta_id=insta_id,iaccess_token=ll_accesstoken)
    order.save()
    
def update_twitter(key,secret):
    User_details.objects.filter(page_id=page_id).update(tweet_access_token=key,access_token_secret=secret)
# get_atoken() 
# print(atoken)   