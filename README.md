# Chinese chess assistance

## About the Project
Đây là một đồ án "Hệ thống Thông minh" (Smart System) với các yêu cầu như sau:
1. Có ứng dụng Trí tuệ Nhân tạo
2. Có lập trình nhúng
3. Có liên kết giữa nhiều thiết bị (IoT, network,..)
Với mục đích hỗ trợ con người đưa ra quyết định.

## Tóm tắt
### Yêu cầu
"Cung cấp hình ảnh chứa một bàn cờ tướng, hãy đề xuất những nước đi tốt."

Dựa vào mô tả như trên, Project của chúng tôi có thể được tóm gọn bằng hai mô hình:
1. Máy tính hiểu được bàn cờ (sử dụng computer vision và một model tensorflow nhận diện)
2. Máy tính đề xuất nước đi. (sử dụng một [engine cờ tướng](https://github.com/bupticybee/elephantfish) làm backend)

## Bước giải quyết
1. Tiền xử lý:
Từ một hình ảnh có chứa bàn cờ, trích ra được 90 vị trí của nó.
2. Nhận diện:
Sử dụng một model nhận diện (tự tạo, tự train) để dự đoán vị trí của bàn cờ là quân gì.
3. Đề xuất:
Có được trạng thái bàn cờ, gọi đến engine cờ để lấy đề xuất.

Ngoài ra, hệ thống của chúng tôi còn có một webserver để broadcast thông tin của ván cờ hiện tại cho mọi thiết bị kết nối đến.

