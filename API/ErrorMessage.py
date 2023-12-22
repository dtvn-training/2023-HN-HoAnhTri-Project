import requests
import json

webhook_url = "https://hooks.slack.com/services/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"

headers = {
    "Content-type": "application/json"
}

payload = {
    "text": "<@U063ADBHVTR> File doesn't exist in Box"
}

response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

print(response.status_code)  # Kiểm tra mã trạng thái của response
print(response.text)  # Hiển thị phản hồi từ Slack
