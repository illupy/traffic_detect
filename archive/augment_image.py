import os
import shutil
import cv2
from filter import processing_image
from class_statistic import get_classes_to_augment

def augment_images(cropped_dir, output_dir, val=10):
    os.makedirs(output_dir, exist_ok=True)
    class_targets = get_classes_to_augment(cropped_dir)

    for class_id, augment_num in class_targets.items():
        class_input_dir = os.path.join(cropped_dir, class_id)
        class_output_dir = os.path.join(output_dir, class_id)
        os.makedirs(class_output_dir, exist_ok=True)

        image_files = [f for f in os.listdir(class_input_dir) if f.endswith(".jpg")]

        # Cần augment thêm ảnh đến khi đủ
        count = 0
        for image_file in image_files:
            src = os.path.join(class_input_dir, image_file)
            dst = os.path.join(class_output_dir, image_file)
            shutil.copy(src, dst)
            if count >= augment_num: break
            image_path = os.path.join(class_input_dir, image_file)
            image = cv2.imread(image_path)

            # Gọi hàm xử lý augmentation
            aug_sets = processing_image(image, val)

            for aug_list in aug_sets:
                for aug_image in aug_list:
                    save_name = f"{image_file.replace('.jpg', '')}_aug{count}.jpg"
                    cv2.imwrite(os.path.join(class_output_dir, save_name), aug_image)
                    count += 1
                    if count >= augment_num:
                        break
                if count >= augment_num:
                    break



cropped_dir="cropped"
output_dir="cropped_and_augment"
augment_images(cropped_dir, output_dir)
