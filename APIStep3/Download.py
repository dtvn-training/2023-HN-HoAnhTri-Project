import os
from boxsdk import OAuth2, Client
import re

auth = OAuth2(
    client_id='7e3dsw60msaf5toffs1lr00177dhnvtd',
    client_secret='m9CWsjKytc4rthVonboveo9JuWzgrFk9',
    access_token='NQzoNy8tgLsMOpdpeDpKUdV6LllG2774',
)
client = Client(auth)

user = client.user().get()
print(f'The current user ID is {user.id}')

# Lấy đường dẫn tới thư mục chứa file Python đang thực thi
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tìm đường dẫn tới thư mục PentahoTest dựa trên vị trí hiện tại của file Python
pentaho_test_dir = os.path.join(current_dir, '..', '..', 'PentahoTest')

folder_id='237094077403'
destination_directory = os.path.join(pentaho_test_dir, 'Output')
items = client.folder(folder_id).get_items()
file_pattern = re.compile(r'^Output_adgp_add_result_(\d{4})(\d{2})(\d{2})\.csv$')
# Lặp qua các file trong thư mục và di chuyển các file thỏa mãn định dạng vào thư mục mong muốn
for item in items:
    if item.type == 'file':
        match = file_pattern.match(item.name)
        if match:
            year, month, day = match.groups()
            destination_file_path = os.path.join(destination_directory, item.name)

            # Tải file và di chuyển vào thư mục đích
            with open(destination_file_path, 'wb') as output_file:
                client.file(item.id).download_to(output_file)