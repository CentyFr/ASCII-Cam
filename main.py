import cv2
import numpy as np

ASCII_CHARS = "@%#*+=-:. "

def resize_frame(frame, new_width=120):
    height, width = frame.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return cv2.resize(frame, (new_width, new_height))

def frame_to_ascii_img(frame, scale=10):
    rows, cols = frame.shape
    img_height = rows * scale
    img_width = cols * scale
    ascii_img = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255

    for i in range(rows):
        for j in range(cols):
            pixel = frame[i, j]
            index = pixel * len(ASCII_CHARS) // 256
            char = ASCII_CHARS[index]
            cv2.putText(
                ascii_img,
                char,
                (j * scale, (i + 1) * scale),
                cv2.FONT_HERSHEY_PLAIN,
                0.6,
                (128, 0, 128),  # text color
                1,
                cv2.LINE_AA,
            )
    return ascii_img

def draw_overlay(frame, ascii_mode, paused):
    text = "ASCII MODE" if ascii_mode else "NORMAL MODE"
    if paused:
        text += " - PAUSED"
    cv2.putText(
        frame, text, (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
        (0, 0, 255), 2, cv2.LINE_AA
    )
    return frame

def main():
    cap = cv2.VideoCapture(0)

    cv2.namedWindow("ASCII Webcam", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("ASCII Webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    ascii_mode = True
    paused = False
    last_frame = None

    try:
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break
                last_frame = frame.copy()
            else:
                frame = last_frame

            if ascii_mode:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray_resized = resize_frame(gray, new_width=120)
                display_frame = frame_to_ascii_img(gray_resized, scale=8)
            else:
                display_frame = cv2.resize(frame, (960, 540))

            display_frame = draw_overlay(display_frame, ascii_mode, paused)
            cv2.imshow("ASCII Webcam", display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # quit
                break
            elif key == ord('a'):  # Pause
                paused = not paused
            elif key == ord('n'):  # Toggle 
                ascii_mode = not ascii_mode

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
