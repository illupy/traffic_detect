import os
import cv2

# Đường dẫn thư mục gốc
image_dir = "archive/images"
label_dir = "archive/labels"
output_dir = "cropped"

# Tạo thư mục nếu chưa có
os.makedirs(output_dir, exist_ok=True)

def crop_and_save():
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg"):
            image_path = os.path.join(image_dir, filename)
            label_path = os.path.join(label_dir, filename.replace(".jpg", ".txt"))

            if not os.path.exists(label_path):
                continue

            image = cv2.imread(image_path)
            h, w, _ = image.shape

            with open(label_path, 'r') as f:
                for i, line in enumerate(f):
                    parts = line.strip().split()
                    class_id = parts[0]
                    x, y, bw, bh = map(float, parts[1:])

                    # Tính tọa độ bounding box (từ normalized về pixel)
                    x1 = int((x - bw / 2) * w)
                    y1 = int((y - bh / 2) * h)
                    x2 = int((x + bw / 2) * w)
                    y2 = int((y + bh / 2) * h)

                    # Cắt ảnh và lưu vào thư mục theo class
                    crop = image[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]

                    class_dir = os.path.join(output_dir, class_id)
                    os.makedirs(class_dir, exist_ok=True)

                    crop_filename = f"{filename[:-4]}_{i}.jpg"  # ví dụ: 0001_0.jpg
                    cv2.imwrite(os.path.join(class_dir, crop_filename), crop)

    print("Đã cắt và lưu xong tất cả ảnh theo nhãn.")

crop_and_save()
