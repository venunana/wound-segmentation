import cv2
import numpy as np
from tkinter import Tk, Button, Label, messagebox, filedialog, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk

def process_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image file")
        
        original_img = img.copy()
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        eroded = cv2.erode(thresh, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(eroded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        inner_black_parts = np.zeros_like(eroded)

        for i, contour in enumerate(contours):
            if hierarchy[0][i][3] != -1:
                cv2.drawContours(inner_black_parts, [contour], -1, 255, thickness=cv2.FILLED)

        inner_contours, _ = cv2.findContours(inner_black_parts, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_contour_area = 500
        total_wound_area = 0

        for contour in inner_contours:
            contour_area = cv2.contourArea(contour)
            if contour_area > min_contour_area:
                cv2.drawContours(img, [contour], -1, (0, 255, 0), thickness=2)
                total_wound_area += contour_area

        return original_img, image_gray, blurred, thresh, eroded, img, total_wound_area

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process image: {str(e)}")
        return None, None, None, None, None, None, None

def resize_image(image, max_size):
    h, w = image.shape[:2]
    scaling_factor = min(max_size / h, max_size / w)
    new_size = (int(w * scaling_factor), int(h * scaling_factor))
    return cv2.resize(image, new_size)

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        original_img, gray_img, blurred_img, thresh_img, eroded_img, processed_img, wound_area = process_image(file_path)
        
        if original_img is not None:
            max_display_size = 200
            images_resized = [
                resize_image(original_img, max_display_size),
                resize_image(gray_img, max_display_size),
                resize_image(blurred_img, max_display_size),
                resize_image(thresh_img, max_display_size),
                resize_image(eroded_img, max_display_size),
                resize_image(processed_img, max_display_size)
            ]

            img_labels = []
            for img in images_resized:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape) == 3 else cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(img_pil)
                img_labels.append(img_tk)

            label_original_img.config(image=img_labels[0])
            label_original_img.image = img_labels[0]
            
            label_gray_img.config(image=img_labels[1])
            label_gray_img.image = img_labels[1]

            label_blurred_img.config(image=img_labels[2])
            label_blurred_img.image = img_labels[2]

            label_thresh_img.config(image=img_labels[3])
            label_thresh_img.image = img_labels[3]

            label_eroded_img.config(image=img_labels[4])
            label_eroded_img.image = img_labels[4]

            label_processed_img.config(image=img_labels[5])
            label_processed_img.image = img_labels[5]

            label_area.config(text=f"Total Wound Area: {wound_area:.2f} pixels")

            btn_save.config(state='normal')
        else:
            label_original_img.config(image='')
            label_gray_img.config(image='')
            label_blurred_img.config(image='')
            label_thresh_img.config(image='')
            label_eroded_img.config(image='')
            label_processed_img.config(image='')
            label_area.config(text="Total Wound Area: N/A")
            btn_save.config(state='disabled')

def save_image():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if save_path:
        processed_img = label_processed_img.image._PhotoImage__photo 
        processed_img.save(save_path)
        messagebox.showinfo("Success", f"Image saved to {save_path}")

root = Tk()
root.title("Wound Image Segmentation")
root.geometry("1200x800")

canvas = Canvas(root)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

btn_open = Button(scrollable_frame, text="Open Image", command=open_image)
btn_open.pack()

frame_images = Frame(scrollable_frame)
frame_images.pack()

label_original_txt = Label(frame_images, text="Original Image")
label_original_txt.pack(side="top")
label_original_img = Label(frame_images)
label_original_img.pack(side="top")

label_gray_txt = Label(frame_images, text="Grayscale Image")
label_gray_txt.pack(side="top")
label_gray_img = Label(frame_images)
label_gray_img.pack(side="top")

label_blurred_txt = Label(frame_images, text="Blurred Image")
label_blurred_txt.pack(side="top")
label_blurred_img = Label(frame_images)
label_blurred_img.pack(side="top")

label_thresh_txt = Label(frame_images, text="Thresholded Image")
label_thresh_txt.pack(side="top")
label_thresh_img = Label(frame_images)
label_thresh_img.pack(side="top")

label_eroded_txt = Label(frame_images, text="Eroded Image")
label_eroded_txt.pack(side="top")
label_eroded_img = Label(frame_images)
label_eroded_img.pack(side="top")

label_processed_txt = Label(frame_images, text="Processed Image with Wound Contours")
label_processed_txt.pack(side="top")
label_processed_img = Label(frame_images)
label_processed_img.pack(side="top")

label_area = Label(scrollable_frame, text="Total Wound Area: N/A")
label_area.pack()

btn_save = Button(scrollable_frame, text="Save Processed Image", command=save_image, state='disabled')
btn_save.pack()

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
root.mainloop()
