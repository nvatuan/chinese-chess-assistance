# Xiangpi AI with board recognition via Raspberry Camera Module

## dev-boardPreprocess
Đây là nhánh chịu trách nhiệm chuẩn hóa một bức ảnh chứa bàn cờ và crop ra được 90 vị trí của bàn cờ.

### Chuẩn hóa một bức ảnh chứa bàn cờ
Bàn cờ là một hình chữ nhật, nhưng có thể vì góc chụp mà nó thành một hình bình hành.
Bước này sẽ tìm ra được 4 góc của bàn cờ, sau đó warp khu vực bàn cờ thành một hình chữ nhật như là đang nhìn từ top-down.

### Crop ra 90 vị trí của bàn cờ
Sau khi có được bức view top-down, ta sẽ crop hình đó thành 90 bức ảnh nhỏ, tương ứng với 90 vị trí trên bàn cờ.
Sau đó 90 bức ảnh đó sẽ được chuyển sang cho `dev-pieceRecognition`