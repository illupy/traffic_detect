import os
import matplotlib.pyplot as plt

# Thư mục chứa ảnh đã crop
cropped_dir = "cropped_and_augment"

def count_images_per_class(cropped_dir):
    '''
    Đếm số ảnh theo từng class (tên thư mục là class_id) 
    '''
    counts = {}
    for class_id in os.listdir(cropped_dir):
        class_dir = os.path.join(cropped_dir, class_id)
        if os.path.isdir(class_dir):
            counts[class_id] = len([f for f in os.listdir(class_dir) if f.endswith(".jpg")])
    return counts

def get_classes_to_augment(cropped_dir):
    '''
    Tìm các class có số lượng ảnh ít hơn class có số lượng ảnh nhiều nhất
    '''
    counts = count_images_per_class(cropped_dir)
    max_count = max(counts.values())
    return {cls: max_count - cnt for cls, cnt in counts.items() if cnt < max_count}


class_counts = count_images_per_class(cropped_dir)
# Sắp xếp theo class_id
sorted_counts = dict(sorted(class_counts.items(), key=lambda x: int(x[0])))

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.bar(sorted_counts.keys(), sorted_counts.values(), color='skyblue')
plt.xlabel("Class ID")
plt.ylabel("Số lượng ảnh")
plt.title("Số lượng ảnh theo từng nhãn")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
