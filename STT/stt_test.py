import sys
import requests

client_id = "y1fzqckpmp"
client_secret = "98jvrHj4ZtGFB95eqO3Y5ndAjrP5JOo48fn2SD73"
lang = "Kor" # 언어 코드 ( Kor, Jpn, Eng, Chn )
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
data = open('C:\\Users\\hb240\\Desktop\\졸업작품\\practice1\\현빈욕1.mp3', 'rb')
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/octet-stream"
}

response = requests.post(url,  data=data, headers=headers)
rescode = response.status_code

if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)

# import os
# os.getcwd()