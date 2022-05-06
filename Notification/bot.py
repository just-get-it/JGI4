





import requests,time,json

BASE_URL="http://raymondinstitutional.justgetit.in"

URL="https://api.telegram.org/bot1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A"



def getOffset():
    URL=BASE_URL+"/api/getOffset"
    r=requests.get(url=URL)
    offset=json.loads(r.content)['offset']
    return offset


def updateOffset(offset):
    URL=BASE_URL+"/api/setOffset"
    data={
        "apikey":"1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A",
        "offset":offset
    }
    r=requests.get(url=URL,params=data)
    return True


def checkLoggedIn(chat_id):
    URL=BASE_URL+"/api/checkLoggedIn"
    data={
        "apikey":"1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A",
        "chat_id":chat_id
    }
    r=requests.get(url=URL,params=data)
    # print(r.content)
    r=json.loads(r.content)
    if r['ok']:
        return True
    else:
        return False


def checkUser(email,password,chat_id):
    URL=BASE_URL+"/api/checkUser"
    data={
        "apikey":"1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A",
        "chat_id":chat_id,
        "email":email,
        "password":password
    }
    r=requests.get(url=URL,params=data)
    r=json.loads(r.content)
    if r['ok']:
        return True
    else:
        return False

def sendMessage(chat_id,message):
    check=checkLoggedIn(chat_id)
    URL = "https://api.telegram.org/bot1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A"
    options={"send":"/sendMessage"}
    if check:
        resp_message="You are already Logged In !!"
        r=requests.get(url=URL+options["send"],params={"text":resp_message,"chat_id":chat_id})
    else:
        if 'Username' in message:
            email=message.strip().split(",")
            if len(email)<=1:
                resp_message="Sorry Login Failed !"
                r=requests.get(url=URL+options["send"],params={"text":resp_message,"chat_id":chat_id})
            else:
                # print(email)
                username=email[0][9:]
                password=email[1][9:]
                # print(username,password)
                out=checkUser(username,password,chat_id)
                if out:
                    resp_message="Hurrah !! You are Logged In"
                    r=requests.get(url=URL+options["send"],params={"text":resp_message,"chat_id":chat_id})
                else:
                    resp_message="Sorry Login Failed !"
                    r=requests.get(url=URL+options["send"],params={"text":resp_message,"chat_id":chat_id})
        else:
            resp_message="Okay ! Lets intiate the Login Process"
            resp_message1="Please send your Username.\nAs in following format 'Username-default@gmail.com,Password-demo'"
            r=requests.get(url=URL+options["send"],params={"text":resp_message,"chat_id":chat_id})
            r=requests.get(url=URL+options["send"],params={"text":resp_message1,"chat_id":chat_id})
    return True


# Offset=923587544

URL = "https://api.telegram.org/bot1039956033:AAH494Vb3W3CrvKpEx_G3OxwFscGzQAuW4A"
options={
    "me":"/getMe",
    "send":"/sendMessage",
    "update":"/getUpdates"
}



while True:
    Offset=getOffset()
    r=requests.get(url=URL+options['update'],params={"offset":Offset})
    r=json.loads(r.content)
    # print(r)
    if r['ok'] and len(r['result']):
        last_offset=r['result'][-1]['update_id']
        # print(last_offset)
        updateOffset(last_offset)
        for i in r['result']:
            chat_id=i['message']['from']['id']
            # print(i['message']['text'])
            # print(i)
            message=i['message']['text']
            sendMessage(chat_id,message)
    # time.sleep(0)

