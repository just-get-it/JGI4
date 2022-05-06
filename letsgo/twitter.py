import webbrowser
from requests_oauthlib import OAuth1Session
resource_owner_key=''
resource_owner_secret=''
consumer_key='jcsIBC2MB25FpRcWJO5tcXDtt'
consumer_secret='mV2Gv2bW6SSg4hXrLMV1ieXDS7Md8rlJqkqzo70oDEB6xtKpAT'
oauth_callback='oob'
def get_resource_token():
    request_token=OAuth1Session(client_key=consumer_key,client_secret=consumer_secret,callback_uri=oauth_callback)
    print(request_token)
    url='https://api.twitter.com/oauth/request_token'
    data=request_token.get(url)

    
    data_token = str.split(data.text, '&')
    print(data_token)
    
    ro_key=str.split(data_token[0],'=')
    ro_secret=str.split(data_token[1],'=')
    resource_owner_key=ro_key[1]
    resource_owner_secret=ro_secret[1]
   
    url2='https://api.twitter.com/oauth/authenticate?oauth_token={}'.format(resource_owner_key)
    webbrowser.open(url2)
    
    
    resource=[resource_owner_key,resource_owner_secret]

    return resource

def twitter_get_access_token(verifier,ro_key,ro_secret):
    
    oauth_token=OAuth1Session(client_key=consumer_key,
                                client_secret=consumer_secret,
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret)
    url='https://api.twitter.com/oauth/access_token'
    data={"oauth_verifier":verifier}
    access_token_data=oauth_token.post(url,data=data)
    print(access_token_data.text)
    access_token_list=str.split(access_token_data.text,'&')
    
    
    access_token_key = str.split(access_token_list[0], '=')
    access_token_secret = str.split(access_token_list[1], '=')
    access_token_name = str.split(access_token_list[3], '=')
    access_token_id = str.split(access_token_list[2], '=')
    key=access_token_key[1]
    secret=access_token_secret[1]
    name=access_token_name[1]
    id=access_token_id[1]
    access_token_array=[key,secret]
    return access_token_array                           

