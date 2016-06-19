import wave,pyaudio,base64,urllib.request,urllib.parse,json,io

CHUNK=2000
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=8000
RECORD_SECONDS=3

p=pyaudio.PyAudio()
stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
print('recording')

frames=[]

for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
    data=stream.read(CHUNK)
    frames.append(data)

print('done recording')

stream.stop_stream()
stream.close()
p.terminate()

s=io.BytesIO()
wf=wave.open(s,'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

data=s.getvalue()
length=len(data)
data=base64.b64encode(data)
data=data.decode()
s.close()

urlGetToken='https://openapi.baidu.com/oauth/2.0/token'
tokenData={
    'grant_type':'client_credentials',
    'client_id':'2dESgKFxrD7fedEHrivLwfEQ',
    'client_secret':'61b019bec13fdfefa2631eacd8231dc1'
    }
tokenData=urllib.parse.urlencode(tokenData)
tokenData=tokenData.encode()
req=urllib.request.Request(urlGetToken)
resp=urllib.request.urlopen(req,data=tokenData)
content=resp.read().decode()
d=json.loads(content)
accessToken=d['access_token']

postData={
    'format':'wav',
    'rate':8000,
    'channel':1,
    'token':accessToken,
    'cuid':'test',
    'len':length,
    'speech':data,
}
postData=json.dumps(postData)
postData=postData.encode()

headers={
    'Content-Type':'application/json',
    'Content-Length':len(postData),
}

recognitionRequest=urllib.request.Request('http://vop.baidu.com/server_api',headers=headers)
recognitionResponse=urllib.request.urlopen(recognitionRequest,data=postData)
recognitionContent=recognitionResponse.read().decode()
resultDict=json.loads(recognitionContent)
if resultDict['err_no']!=0:
    print(resultDict['err_msg'])
else:
    print(''.join(resultDict['result']))
