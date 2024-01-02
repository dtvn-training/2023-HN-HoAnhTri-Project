import os
from datetime import datetime
from boxsdk import OAuth2, Client

# Lấy đường dẫn tới thư mục chứa file Python đang thực thi
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tìm đường dẫn tới thư mục PentahoTest dựa trên vị trí hiện tại của file Python
pentaho_test_dir = os.path.join(current_dir, '..', '..', 'PentahoTest')

if os.path.exists(pentaho_test_dir):
    # Thiết lập thông tin xác thực OAuth2
    auth = OAuth2(
        client_id='7e3dsw60msaf5toffs1lr00177dhnvtd',
        client_secret='m9CWsjKytc4rthVonboveo9JuWzgrFk9',
        access_token='8Pb2bC4SLFUcJG8p1ETTHdxG5i8yba9X',
    )

    # Khởi tạo client
    client = Client(auth)

    # Tạo tên file theo đúng định dạng mong muốn "Input adgp_yyyymmdd.csv"
    formatted_date = datetime.now().strftime('%Y%m%d')
    file_name = f'Output adgp_{formatted_date}.csv'

    # Đường dẫn tới file cần tải lên (tương đối)
    file_path = os.path.join(pentaho_test_dir, 'Output', file_name)

    # Đường dẫn đến thư mục trên Box mà bạn muốn lưu file
    folder_id = '237094077403'

    # Tải file lên Box với tên format mong muốn
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            uploaded_file = client.folder(folder_id).upload_stream(file, file_name)
            print(f"File '{uploaded_file.name}' uploaded to Box with file ID {uploaded_file.id}")
    else:
        print(f"File '{file_path}' does not exist.")
else:
    print("PentahoTest directory does not exist.")
