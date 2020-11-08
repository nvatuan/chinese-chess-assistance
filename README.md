# Xiangpi AI assistance
## Raspberry Pi Set-up

Đây là nhánh liên quan đến việc thiết lập, lập trình và triển khai dự án trên Raspberry Pi. 
Nhóm sử dụng `Raspberry Pi 3`

### 1. Setup camera
Sử dụng Camera Module của Rasp Pi (8MP Raspberry Pi Camera v2) để chụp ảnh toàn cảnh của bàn cờ.
Camera được treo phía trên và nhìn xuống bàn cờ ở góc dựng đứng.

#### Status: Đã có setup chân. Không đẹp nhưng đã OK. (TẠM ỔN)

### 2. Webserver
Nhóm có thể sử dụng `apache` hoặc là `SimpleHTTPServer` của `Python`.
Webserver sẽ có nhiệm vụ phục vụ trang web cho các thiết bị kết nối tới, cho biết thông tin về ván cờ đang diễn ra. (Feed của bàn cờ, Chức năng nhận diện quân cờ, Bàn cờ ảo mà AI đang nhìn thấy, Những nước đi mà AI đề xuất)

Điều khó khăn ở đây là: **Thông tin mà webserver phục vụ là ở dạng Video, vì thông tin hình ảnh sẽ thay đổi theo thời gian**.
Điều này có thể đạt được bởi:
- Thay đổi bức ảnh locally và ép trang web phục vụ ảnh refresh mỗi 0.5s.
- Sử dụng `MJPEG`. Phức tạp hơn, nhưng sẽ hoạt động mượt và hiệu quả hơn.

#### Status: Đã có giao diện web. Tuy nhiên các chức năng streaming hay cho thấy feed bàn cờ chưa xong. (KHÔNG ỔN)

### 3. Networking
Raspberry Pi sẽ có IP tĩnh ở một network. Một trong những lựa chọn mà nhóm đang nghĩ tới là cho phép Raspberry Pi phát ra một wifi, các thiết bị kết nối tới nó có thể truy cập vào webserver tại đó.

Hiện tại, Pi của nhóm vẫn sử dụng wi-fi từ router và set IP cố định của nó là `192.168.1.31`. Việc set IP tĩnh như vậy sẽ mâu thuẫn với các hotspot của Android hay Laptop vì các hotspot đó có Network Address là `192.168.4x.0/24`, khác octet thứ 3, và cũng không dễ dàng để thay đổi Network Address của các thiết bị. Nhóm có thể đầu tư một router như là giải pháp.

#### Status: Pi có IP tĩnh của interface `wlan0` là `192.168.1.31`, interface `eth0` là `192.168.1.32`. Pi của nhóm cũng có thể phát wi-fi như một network riêng, nhưng làm việc này đồng nghĩa với không kết nối tới các hotspot khác. Hiện chưa có script để nhanh chóng đổi qua đổi lại. (TẠM ỔN)
