# Xiangpi AI with board recognition via Raspberry Camera Module

## About the Project
Đây là một dự án 4-người, với chủ đề "Hệ thống Thông minh" (Smart System) với các yêu cầu như sau:
1. Có ứng dụng Trí tuệ Nhân tạo, đưa ra gợi ý, quyết định,..
2. Có lập trình nhúng
3. Có liên kết giữa nhiều thiết bị (network)
4. ...

## Mô tả
Project của chúng tôi bao gồm:
1. Một server chứa các model AI đã train, với các API mà thông qua đó có thể request hỗ trợ từ AI. (tôi sẽ gọi nó là Main Server)
2. Một Raspberry Pi có kết nối với Main Server, có module camera chụp top-down bàn cờ tướng, xử lý hình ảnh này và gửi về Main Server. Sau đó Main Server sẽ gửi những thông tin cần thiết về Raspberry. Raspberry còn là một webserver, là một access point, mọi thiết bị connect vào có thể xem các thông tin thêm về ván cờ đang diễn ra.

## Các chức năng hiện tại:
1. Cho trạng thái bàn cờ hiện tại, đề xuất nước đi tốt nhất.
2. Nhận diện được chính xác trạng thái bàn cờ từ ảnh chụp top-down (điều kiện môi trường tự quyết)
3. Khả năng render một bàn cờ ảo theo yêu cầu
4. Raspberry là một access point và có Webserver tại đó.
5. Main Server có kết nối với Raspberry, có API cho các AI của nó để Rasp yêu cầu.

## Progress
Project được chia ra làm 4 phần lớn:
1. AI - Play
2. AI - Recognition
3. IP - Render board
4. WS - Raspberry Pi Webserver
5. MS - Main Server connections
