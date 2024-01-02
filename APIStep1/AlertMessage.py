import csv
import requests
import json
import os
from datetime import datetime

# Lấy đường dẫn tới thư mục chứa file Python đang thực thi
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tìm đường dẫn tới thư mục PentahoTest dựa trên vị trí hiện tại của file Python
pentaho_test_dir = os.path.join(current_dir, '..', '..', 'PentahoTest')

# Tạo tên file theo đúng định dạng mong muốn "Output adgp_yyyymmdd.csv"
formatted_date = datetime.now().strftime('%Y%m%d')
file_name = f'Output adgp_{formatted_date}.csv'
# Đường dẫn tới file cần tải lên (tương đối)
file_adgp = os.path.join(pentaho_test_dir, 'Output', file_name)
file_PIC=os.path.join(pentaho_test_dir,'PICInformation','PIC_Information.csv')


webhook_url = "https://hooks.slack.com/services/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"

headers = {
    "Content-type": "application/json"
}

payload = {
    "text": ""  
}



# Danh sách để lưu các account_id tương ứng với fail_reason=null
account_ids_with_null_fail_reason = set()

# Mở file CSV và đọc dữ liệu từ nó
with open(file_adgp, newline='') as adgroup_file:
    adgroup_reader = csv.DictReader(adgroup_file, delimiter=';')
    for row in adgroup_reader:
        if row.get('fail_reason', '').strip() == "":
            account_ids_with_null_fail_reason.add(row.get('account_id', '').strip())

# Khởi tạo payload['text'] với giá trị None hoặc chuỗi rỗng
payload['text'] = None
#Danh sách lưu các SlackId có adgroup được xử lý thành công
slack_ids = {}
#Đọc file thông tin PIC để tag
with open(file_PIC, newline='') as user_file:
    user_reader = csv.DictReader(user_file, delimiter=';')
    for row in user_reader:
        if row.get('Account_id', '').strip() in account_ids_with_null_fail_reason:
            slack_ids[row.get('Account_id', '').strip()] = row.get('Slack_id', '').strip()

# Gửi tin nhắn có chứa thông tin từ file Information lên Slack
for account_id, slack_id in slack_ids.items():
    message = f"<@{slack_id}> Upload file successed"
    payload = {
        "text": message
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

print(slack_ids)
print(account_ids_with_null_fail_reason)
print(response.status_code)  # Kiểm tra mã trạng thái của response
print(response.text)  # Hiển thị phản hồi từ Slack
