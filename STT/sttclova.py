# import requests

client_id = "hb2407@nvaer.com" #이게 맞는건지 모르겠음!
client_secret = "9a775d9c9e7947d6a25d59aac5772b09"
lang = "Kor"   # 언어 코드 ( Kor, Jpn, Eng, Chn )
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
# CLOVA Speech Invoke URL 뭔지몰라서 일단 긁어놈..
# https://clovaspeech-gw.ncloud.com/external/v1/933/743930e6253db76a3634e3e416513e6e33a79b06e7d32556faa6548df16024fa

data = open('./contents/hi.m4a', 'rb')

headers = {
    "": client_id,
    "9a775d9c9e7947d6a25d59aac5772b09": client_secret,
    "Content-Type": "application/octet-stream"
}

response = requests.post(url, data=data, headers=headers)

rescode = response.status_code

if(rescode == 200):
    print(response.text)
else:
    print("Error : " + response.text)

# 헤더 값에 데이터를, 인증키를설정하고.
# post로 데이터를 날린다.
# endpoint url값은 각각 다르니 상품에 맞게 설정한다.
 값을 설정하고