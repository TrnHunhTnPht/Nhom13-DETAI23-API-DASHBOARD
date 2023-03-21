import requests
import json

url = "http://cads-api.fpt.vn/fiber-detection/v2/using_json_inf/2022/12"

payload = ""
headers = {
  'Content-Type': 'application/json',
  'Authorization': '07Ok0aIEZSOY2Y946YmSdZRSRPy0QJtA'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

