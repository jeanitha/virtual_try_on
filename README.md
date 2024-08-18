# Real-time-virtual-glasses-try-on

This Python script uses OpenCV to detect faces and eyes in real-time video from a webcam, and overlays a pair of sunglasses on the detected face. The sunglasses are automatically scaled and positioned based on the distance between the detected eyes, allowing users to virtually try on glasses.

## Requirements

- Python 3.x
- OpenCV (cv2) library
- Haar cascade classifiers for face and eye detection (`haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`)
- Sunglasses image with an alpha channel (`glasses.png`)

## Usage

1. Install the required libraries (OpenCV) if not already installed.
2. Place the sunglasses image (`glasses.png`) in the same directory as the script.
3. Ensure that the Haar cascade classifiers (`haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`) are also in the same directory or update the file paths accordingly.
4. Connect a webcam to your computer.
5. Run the script.
6. The script will open a window displaying the webcam feed with the overlaid sunglasses on the detected face.
7. Press 'q' to quit the application.

## How it Works

1. The script loads the Haar cascade classifiers for face and eye detection.
2. It reads the sunglasses image (`glasses.png`) with an alpha channel and ensures that it has an alpha channel.
3. The webcam is opened using OpenCV's `VideoCapture` function.
4. In a loop, the script reads frames from the webcam.
5. For each frame:
  - The face detection algorithm is applied to the frame.
  - For each detected face:
    - The face region is extracted from the grayscale and color images.
    - Eye detection is performed within the face region.
    - The centers of the detected eyes are calculated and stored.
  - If two eyes are detected, the script calculates the average position of the eyes and determines the dimensions of a rectangle around the eyes.
  - The sunglasses image is scaled based on the dimensions of the rectangle, while maintaining the aspect ratio. The scaling factor is limited to a range of 0.5 to 2.
  - The scaled sunglasses image is positioned between the detected eyes, centered horizontally and vertically.
  - If the sunglasses dimensions are larger than the face region, the sunglasses are resized to fit the face region.
  - The sunglasses image is blended onto the frame using alpha blending, preserving the transparency of the sunglasses image.
6. The frame with the overlaid sunglasses is displayed using OpenCV.
7. The loop continues until the user presses 'q' to quit the application.
8. The webcam is released, and all windows are closed.

## Note

The script assumes that the sunglasses image (`glasses.png`) is present in the same directory as the script. If the file path or name is different, update it accordingly in the script.
