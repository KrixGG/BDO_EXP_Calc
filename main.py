import pytesseract
import time
import cv2
import pyautogui
import re
import keyboard


def get_numbers_from_screen_section(x1, y1, x2, y2):
    # Capture the user-defined section of the screen
    screenshot = pyautogui.screenshot(region=(x1, y1, x2, y2))

    # Save the screenshot as an image
    screenshot.save("screenshot.png")

    # Read the image
    image = cv2.imread("screenshot.png")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Pass the image to tesseract to get the recognized text
    text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 11')
    return text

def check_screen_section(x1, y1, x2, y2):
    # Get the current numbers in the screen section
    current_numbers = get_numbers_from_screen_section(x1, y1, x2, y2)
    current_numbers = re.findall(r'\d+', current_numbers)
    current_numbers = int("".join(map(str, current_numbers))) if current_numbers else 0

    while True:
        # Get the numbers in the screen section again
        new_numbers = get_numbers_from_screen_section(x1, y1, x2, y2)
        print(f"new_numbers = {new_numbers}")

        # Convert string to list and remove non numbers
        new_numbers = re.findall(r'\d+', new_numbers)

        # Convert list to int
        new_numbers = int("".join(map(str, new_numbers))) if new_numbers else 0
        print(f"new_numbers alterado = {new_numbers}")

        # Check if the numbers have changed
        if new_numbers != current_numbers:
            start_time = time.time()  # Start the timer

            # Calculate the difference in numbers
            diff = new_numbers - current_numbers

            current_numbers = new_numbers

            end_time = time.time()  # Stop the timer
            elapsed_time = end_time - start_time  # Calculate the elapsed time

            print(f"Numbers changed by {diff}. Time taken: {elapsed_time} seconds.")
            
        else:
            time.sleep(1)  # Sleep for 1 second before checking again


# Call the function with the coordinates of the screen section

x1 = "0"
x2 = "300"
y1 = "0"
y2 = "100"

check_screen_section(x1, y1, x2, y2)
