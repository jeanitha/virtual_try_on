import cv2
import numpy as np

# Load the cascade classifiers for face and eye detection
f_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
e_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Load the sunglasses image with alpha channel
sunglasses = cv2.imread("glasses.png", -1)  # Load sunglasses with alpha channel

# Check if the sunglasses image has an alpha channel, if not, add one
if sunglasses.shape[2] == 3:  # If there are only 3 channels (BGR)
    b, g, r = cv2.split(sunglasses)
    alpha = np.ones(b.shape, dtype=b.dtype) * 255  # Create an alpha channel
    sunglasses = cv2.merge((b, g, r, alpha))

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = f_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # Extract the face region from the grayscale and color images
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        # Detect eyes in the face region
        eyes = e_cascade.detectMultiScale(roi_gray)
        eye_centers = []  # List to store the coordinates of the centers of the eyes

        # Calculate the center of each eye and store the coordinates in the list
        for (ex, ey, ew, eh) in eyes:
            eye_center_x = x + ex + (ew // 2)
            eye_center_y = y + ey + (eh // 2)
            eye_centers.append((eye_center_x, eye_center_y))

        # Calculate the average coordinates of the centers of the eyes
        if len(eye_centers) == 2:
            avg_eye_center_x = (eye_centers[0][0] + eye_centers[1][0]) // 2
            avg_eye_center_y = (eye_centers[0][1] + eye_centers[1][1]) // 2

            # Calculate the dimensions of the rectangle around the eyes by adding a constant margin
            rect_width = abs(eye_centers[0][0] - eye_centers[1][0]) + 80
            rect_height = abs(eye_centers[0][1] - eye_centers[1][1]) + 80

            # Calculate scale factors for the sunglasses
            scale_factor_x = rect_width / sunglasses.shape[1]
            scale_factor_y = rect_height / sunglasses.shape[0]

            # Limit the scale factors to the range of 0.5 to 2
            scale_factor_x = max(0.5, min(2, scale_factor_x))
            scale_factor_y = max(0.5, min(2, scale_factor_y))

            # Choose the smallest scale factor
            scale_factor = min(scale_factor_x, scale_factor_y)

            # Resize the sunglasses while maintaining the original aspect ratio
            scaled_sunglasses = cv2.resize(sunglasses, (0, 0), fx=scale_factor, fy=scale_factor)

            # Calculate the top-left coordinates of the sunglasses to be centered between the eyes
            sunglasses_x = avg_eye_center_x - scaled_sunglasses.shape[1] // 2
            sunglasses_y = avg_eye_center_y - scaled_sunglasses.shape[0] // 2

            # If the dimensions of the sunglasses are larger than the face region, adjust the size of the sunglasses to fit the face region
            if scaled_sunglasses.shape[0] > h or scaled_sunglasses.shape[1] > w:
                scaled_sunglasses = cv2.resize(sunglasses, (w, h))
                sunglasses_x = x
                sunglasses_y = y

            for c in range(3):
                img[sunglasses_y:sunglasses_y + scaled_sunglasses.shape[0],
                    sunglasses_x:sunglasses_x + scaled_sunglasses.shape[1], c] = (
                    scaled_sunglasses[:, :, c] * (scaled_sunglasses[:, :, 3] / 255.0) +
                    img[sunglasses_y:sunglasses_y + scaled_sunglasses.shape[0],
                        sunglasses_x:sunglasses_x + scaled_sunglasses.shape[1], c] *
                    (1.0 - scaled_sunglasses[:, :, 3] / 255.0)
                )

    # Display the image
    cv2.imshow('Virtual Glasses Try-On', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
