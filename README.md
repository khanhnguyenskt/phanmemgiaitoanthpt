Hướng dẫn

1/ Convert code

- Loại bỏ các import của PyQT5
- Loại bỏ hàm main
- Bỏ class, đưa các hàm xử lý ra ngoài
- Bỏ tham số self trong input của các hàm xử lý
- Chuyến các code textbox/combobox trên app thành request.form
- Thêm các thư viện 
```Python
from flask import request, Response, Blueprint

blueprint_dao_ham = Blueprint('dao_ham', __name__)
```
- Thêm routing cho hàm được gọi để xử lý
```Python
@blueprint_dao_ham.route('/', methods=['POST'])
def calculate_derivative():
```

Trong folder server là ví dụ của 1 server chạy bằng framework Flask và 4 bài toán đã được convert thành API:
        
    Đạo hàm: convert từ file dao_ham.py thành /server/dao_ham.py
    Giải phương trình: convert từ file giai_pt.py thành /server/giai_pt.py
    Tính diện tích và thể tích: convert từ file Tinh_Dien_Tich_The_Tich.py thành 2 file /server/tinh_dien_tich_tam_giac.py và tinh_the_tich_tu_dien.py

2/ Chạy project trên local
- Install các thư viện được liệt kê trong file requirements.txt
- Chạy file ./server/server.py bằng IDE (hoặc gõ lệnh python ./server/server.py)
- Ứng dụng được chạy ở port 5000

3/ Chạy project trên Docker

- Tạo Dockerfile

```Dockerfile
FROM python:3.12.7-alpine3.20

WORKDIR /usr/src/app


COPY ./server/ ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

CMD ["python", "./server.py"]
```

- Đi đến thư mục gốc của project
- Chạy lệnh build image
```Terminal
docker build -t app:latest -f Dockerfile .
```
- Chạy lênh run container (thay <port> bằng port mong muốn)
```Terminal
docker run --restart=always -p <port>:5000 --name=app -d app:latest
```