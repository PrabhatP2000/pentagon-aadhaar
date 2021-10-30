import requests

def sendSms(msg,mob_no):
    url = "https://www.fast2sms.com/dev/bulkV2"
    api_key="Yxi1RWNsqBuXohyZ603JECLeIwGgmavc9UpVDMSnAOKQbkzTFHs2bQ547C8h6tnpN1waUJ9FKMARHzxL"
    message=msg
    querystring = {"authorization":api_key,"sender_id":"TXTIND","message":message,"route":"v3","numbers":f"{mob_no}"}
    headers = {
    'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)