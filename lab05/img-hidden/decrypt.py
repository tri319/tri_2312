import sys
from PIL import Image

def decode_image(encoded_image_path):
    # Mở ảnh đã được giấu tin
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""
    
    # Bước 1: Trích xuất tất cả các bit cuối cùng (LSB) từ các pixel
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            # Duyệt qua 3 kênh màu R, G, B
            for color_channel in range(3):
                # Lấy bit cuối cùng của giá trị màu (0 hoặc 1)
                binary_message += format(pixel[color_channel], '08b')[-1]

    # Bước 2: Chuyển chuỗi nhị phân thành ký tự văn bản
    message = ""
    for i in range(0, len(binary_message), 8):
        # Lấy từng cụm 8 bit
        char_bin = binary_message[i:i+8]
        if len(char_bin) < 8:
            break
            
        # Chuyển từ nhị phân sang số nguyên rồi sang ký tự ASCII
        char = chr(int(char_bin, 2))
        
        # Bước 3: Kiểm tra dấu kết thúc thông điệp
        # Nếu gặp ký tự Null '\x00' hoặc chuỗi kết thúc đặc biệt thì dừng lại
        if char == '\x00' or message.endswith('\xff\xfe'):
            break
        message += char
        
    # Trả về thông điệp sạch (loại bỏ các ký tự rác nếu có)
    return message.split('\xff')[0]

def main():
    # Kiểm tra xem người dùng có nhập đường dẫn ảnh không
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
    
    encoded_image_path = sys.argv[1]
    
    try:
        decoded_message = decode_image(encoded_image_path)
        print("-" * 30)
        print(f"Decoded message: {decoded_message}")
        print("-" * 30)
    except Exception as e:
        print(f"Lỗi khi giải mã: {e}")

if __name__ == "__main__":
    main()