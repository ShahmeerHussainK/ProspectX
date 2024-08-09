import base64
import os
import requests
import json


url1 = "https://login-api-test.idicore.com/apiclient"
clientid = "api-client@acesolutionstest"
clientsecret = "U9fXWXBjX!e8yqL8ixRDSg&gFbN8zbk!kU4L4XyGhfCzm6Umz&YLJX7LBaVT26jd"

payload = "{\"glba\":\"otheruse\",\"dppa\":\"none\"}"
a = clientid + ":" + clientsecret
print("a is: ", a)
d = base64.b64encode(b'api-client@acesolutionstest:U9fXWXBjX!e8yqL8ixRDSg&gFbN8zbk!kU4L4XyGhfCzm6Umz&YLJX7LBaVT26jd')
print("d is: ", d)
abc = "Basic " + str(d.decode("utf-8"))
print("abc is: ", abc)
headers = {
    'authorization': abc,
    'content-type': "application/json"
    }

response = requests.request("POST", url1, data=payload, headers=headers)
myToken = response.text #token expires in 15 mins
print("token is: ", myToken)

url2 = "https://api-test.idicore.com/search"

inputDict = {"lastName":"BIGGERSTAFF","firstName":"Ronald","address":"1157 BOLENS CREEK RD","city":"BURNSVILLE","state":"NC","zip":"28714","referenceId":"ABC-xyz1","fields":["name","phone","address","email"]}

headers2 = {
    'authorization': myToken,
    'content-type': "application/json",
	#'content-type': "application/x-www-form-urlencoded",
	'accept': "application/json" #json
    }

json_body = json.dumps(inputDict)
response = requests.request("POST", url2, data=json_body, headers=headers2)
print((response.text))

print((response.status_code))


