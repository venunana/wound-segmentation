# wound-segmentation

This project presents an automated wound image segmentation system designed to assist in medical diagnostics by accurately identifying and measuring wound areas from digital images. Manual wound assessment methods are often error-prone, time-consuming, and lack consistency due to variations in lighting, angle, and human judgment. To overcome these issues, this project uses classical image processing techniques to provide a fast, objective, and standardized method for wound analysis.

## Features
 - Automatic wound segmentation using grayscale conversion, Gaussian blurring, thresholding, and contour detection.
  
 - Graphical User Interface (GUI) built with Tkinter for user interaction.
  
 - Image preview and result display with side-by-side comparison of original and processed images.
   
 - Wound area in pixels(though it cannot be used to measure the actual area can be used to see whether it is healing(and decreasing) or getting worse(and increasing))
  
 - Export functionality to save processed images with marked wound boundaries.

## Technologies Used

- Python: Core programming language.

- OpenCV: Image processing (blurring, thresholding, erosion, contour detection).

- Tkinter: GUI development.

- Pillow (PIL): Image format conversion and display in GUI.

## Methodology
1. Load wound image.
2. Convert to grayscale and blur.
3. Apply thresholding and contour detection.
4. Calculate detected area in pixels
5. Display and optionally save results.




![image](https://github.com/user-attachments/assets/1d2e2c82-599f-483c-ba48-37839f6a242e)
