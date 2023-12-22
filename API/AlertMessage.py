import csv
import requests
import json
import pymysql
import os
from datetime import datetime

# Lấy đường dẫn tới thư mục chứa file Python đang thực thi
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tìm đường dẫn tới thư mục PentahoTest dựa trên vị trí hiện tại của file Python
pentaho_test_dir = os.path.join(current_dir, '..', '..', 'PentahoTest')

# Tạo tên file theo đúng định dạng mong muốn "Input adgp_yyyymmdd.csv"
formatted_date = datetime.now().strftime('%Y%m%d')
file_name = f'Input adgp_{formatted_date}.csv'
# Đường dẫn tới file cần tải lên (tương đối)
file_path = os.path.join(pentaho_test_dir, 'Output', file_name)


webhook_url = "https://hooks.slack.com/services/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"

headers = {
    "Content-type": "application/json"
}

payload = {
    "text": ""  # Chuỗi text sẽ được cập nhật với thông tin từ database
}

# Đường dẫn đến file CSV
csv_file_path = file_path

# Danh sách để lưu các account_id tương ứng với fail_reason=null
account_ids_with_null_fail_reason = []

# Mở file CSV và đọc dữ liệu từ nó
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  # Sử dụng dấu chấm phẩy làm delimiter
    for row in reader:
        if row['fail_reason'] is not None and row['fail_reason'].strip() == '':
            account_ids_with_null_fail_reason.append(row['account_id'])

# Kết nối đến cơ sở dữ liệu
db = pymysql.connect(host='localhost', user='root', password='12345678', database='demo')
cursor = db.cursor()
# Khởi tạo payload['text'] với giá trị None hoặc chuỗi rỗng
payload['text'] = None

# Thực hiện truy vấn SQL với các account_id từ file CSV đã lọc
for account_id in account_ids_with_null_fail_reason:
    clean_account_id = account_id.strip()  # Loại bỏ khoảng trắng không mong muốn
    query = f"SELECT Slack_id FROM User INNER JOIN Account ON User.User_id=Account.user_id WHERE Account_id = '{clean_account_id}' "
    cursor.execute(query)
    result = cursor.fetchone()
    print(result)  # Kiểm tra dữ liệu trả về từ cơ sở dữ liệu
    if result:
        slack_id = result[0]
        if payload['text'] is None:
            payload['text'] = f" <@{slack_id}> Upload file successed\n"  # Gán giá trị nếu payload['text'] là None
        else:
            payload['text'] += f" <@{slack_id}> Upload file successed\n"  # Cộng thêm thông tin từ database vào payload['text']
        print(payload['text'])  # Kiểm tra payload['text']


# Đóng kết nối đến cơ sở dữ liệu
db.close()

# Gửi tin nhắn có chứa thông tin từ database lên Slack
response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

print(account_ids_with_null_fail_reason)
print(response.status_code)  # Kiểm tra mã trạng thái của response
print(response.text)  # Hiển thị phản hồi từ Slack
