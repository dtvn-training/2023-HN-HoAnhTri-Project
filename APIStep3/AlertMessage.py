import csv
import requests
import json
import os
from datetime import datetime

# Lấy đường dẫn tới thư mục chứa file Python đang thực thi
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tìm đường dẫn tới thư mục PentahoTest dựa trên vị trí hiện tại của file Python
pentaho_test_dir = os.path.join(current_dir, '..', '..', 'PentahoTest')

# Tạo tên file theo đúng định dạng mong muốn "Input adgp_yyyymmdd.csv"
formatted_date = datetime.now().strftime('%Y%m%d')
file_name = f'Output_adgp_add_result_{formatted_date}.csv'
# Đường dẫn tới file cần tải lên (tương đối)
file_result = os.path.join(pentaho_test_dir, 'Output', file_name)
file_PIC=os.path.join(pentaho_test_dir,'PICInformation','PIC_Information.csv')

slack_ids = {}
# Đọc dữ liệu từ file CSV và tạo từ điển slack_ids
with open(file_PIC, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        account_id = row['Account_id'].strip()
        slack_id = row['Slack_id']

        if slack_id:  # Kiểm tra xem có giá trị không
            slack_ids[account_id] = slack_id.strip()  # Chỉ sử dụng strip() nếu giá trị không phải None

# Tiếp tục với việc đếm số lượng adgroup thành công và thất bại
success_counts = {}
fail_counts = {}

with open(file_result, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        account_id = row['account_id'].strip()
        add_result = row['add_result'].strip().lower()

        if account_id not in success_counts:
            success_counts[account_id] = 0
            fail_counts[account_id] = 0

        if add_result == 'success':
            success_counts[account_id] += 1
        elif add_result == 'fail':
            fail_counts[account_id] += 1

# In ra thông điệp theo đúng định dạng mong muốn
for account_id in success_counts:
    slack_info = slack_ids.get(account_id)
    if slack_info:
        message = f"<@{slack_info}> Số lượng adgroup thêm thành công: {success_counts[account_id]}\nSố lượng adgroup thêm thất bại: {fail_counts[account_id]}"
    else:
        message = f"<@{account_id}> Số lượng adgroup thêm thành công: {success_counts[account_id]}\nSố lượng adgroup thêm thất bại: {fail_counts[account_id]} (Không có thông tin Slack)"

    payload = {
        "text": message
    }
    print(message)
    
    webhook_url="https://hooks.slack.com/services/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"
    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
           print(f"Thông điệp đã được gửi thành công cho account_id {account_id} đến Slack!")
    else:
          print(f"Gửi thông điệp cho account_id {account_id} đến Slack thất bại. Mã lỗi: {response.status_code}")