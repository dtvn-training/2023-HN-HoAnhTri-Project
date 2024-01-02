import requests
import json
import csv
import os

# Lấy đường dẫn tới thư mục chứa file Python đang thực thi
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tìm đường dẫn tới thư mục PentahoTest dựa trên vị trí hiện tại của file Python
pentaho_test_dir = os.path.join(current_dir, '..', '..', 'PentahoTest')
file_PIC=os.path.join(pentaho_test_dir,'PICInformation','PIC_Information.csv')

slack_id=None
#Đọc file thông tin PIC để tag
with open(file_PIC, newline='') as slack_file:
    slack_reader = csv.DictReader(slack_file, delimiter=';')
    for row in slack_reader:
        if row.get('PIC_name', '').strip() == "Doan Nguyen Duy":
            slack_id = row.get('Slack_id', '').strip()

if slack_id:
    webhook_url = "https://hooks.slack.com/services/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"  # Thay YOUR_WEBHOOK_URL bằng URL webhook của bạn
    message = f"<@{slack_id}> File doesn't exist in BOX"

    payload = {
        "text": message
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print(f"Tin nhắn đã được gửi thành công đến người dùng có Slack ID {slack_id}")
    else:
        print(f"Gửi tin nhắn đến người dùng có Slack ID {slack_id} thất bại. Mã lỗi: {response.status_code}")
else:
    print("Không tìm thấy Slack ID cho người dùng có PIC_name là 'Doan Nguyen Duy'")   
        

