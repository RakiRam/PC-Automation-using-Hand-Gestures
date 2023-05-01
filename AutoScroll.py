import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Define the scaling factor for scroll speed
scroll_speed = 200
# scroll_pause_duration = 0.5
# scrolling = False
cap = cv2.VideoCapture(0)
# Define the current and previous hand positions
hand_pos = (0, 0)
prev_hand_pos = (0, 0)
velocity = 0


with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        # Capture the current frame from the video stream
        ret, frame = cap.read()

        # Convert the frame to RGB color space
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image with the Hand Tracking module of Mediapipe
        results = hands.process(image)

        # Check if a hand was detected in the image
        if results.multi_hand_landmarks:
            # Get the first detected hand
            hand_landmarks = results.multi_hand_landmarks[0]

            # Find the center of the hand by calculating the average position of all hand landmarks
            x = [lm.x for lm in hand_landmarks.landmark]
            y = [lm.y for lm in hand_landmarks.landmark]
            hand_pos = (int(sum(x) / len(x) * frame.shape[1]), int(sum(y) / len(y) * frame.shape[0]))

            # Calculate the velocity of the hand movement
            velocity = hand_pos[1] - prev_hand_pos[1]

            # Scroll up or down based on the velocity and scaling factor
            if velocity > 0:
                # if not scrolling:
                #     pyautogui.scroll(scroll_speed)
                #     scrolling = True
                #     pyautogui.PAUSE = scroll_pause_duration
                # else:
                #     pyautogui.PAUSE = 0
                pyautogui.scroll(scroll_speed)
                pyautogui.sleep(1)
            elif velocity < 0:
                pyautogui.scroll(-scroll_speed)
                pyautogui.sleep(1)

            # Set the previous hand position to the current hand position
            prev_hand_pos = hand_pos

            # Draw the hand landmarks on the image
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the video stream with the hand position and scroll direction
        cv2.putText(frame, f"Hand Position: {hand_pos}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Scroll Direction: {'Up' if velocity < 0 else 'Down'}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Virtual Mouse', frame)

        # Exit the program if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
