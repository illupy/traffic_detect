import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

# --- Cấu hình ---
MODEL_PATH = "traffic_sign_classifier.h5"
IMG_SIZE = (64, 64)
class_name = ['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '4', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '5', '50', '51', '6', '7', '8', '9']
# --- Tải mô hình ---
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Mô hình đã được tải thành công.")
except Exception as e:
    print(f"❌ Lỗi khi tải mô hình: {e}")
    model = None

# --- Hàm xử lý ảnh và dự đoán ---
def predict_image(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize(IMG_SIZE)
        img_array = np.array(img).astype("float32")
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_index = int(np.argmax(predictions[0]))
        predicted_class = class_name[predicted_index]
        confidence = float(predictions[0][predicted_index])

        return f"Dự đoán: Class {predicted_class} (Xác suất: {confidence:.2f})"
    except Exception as e:
        return f"Lỗi dự đoán: {e}"

# --- Hàm chọn ảnh ---
def select_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    img = Image.open(file_path).resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    image_label.configure(image=img_tk)
    image_label.image = img_tk

    result = predict_image(file_path)
    result_label.config(text=result)

# --- Giao diện Tkinter ---
root = tk.Tk()
root.title("Nhận diện biển báo giao thông")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

button = tk.Button(frame, text="Chọn ảnh", command=select_image, font=("Arial", 12))
button.pack()

image_label = tk.Label(frame)
image_label.pack(pady=10)

result_label = tk.Label(frame, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
