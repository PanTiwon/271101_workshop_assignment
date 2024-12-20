import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
ShowFinger = []

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Initialize the number of raised fingers
    Nfing = 0
    ShowFinger.clear()  # Clear the list for each frame

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Initialize finger states
            Thumb, Index, Middle, Ring, Little = 0, 0, 0, 0, 0

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Get specific finger landmarks
                if id == 4:  # Thumb tip
                    cx4, cy4 = cx, cy
                if id == 3:  # Thumb base
                    cx3, cy3 = cx, cy

                if id == 8:  # Index tip
                    cy8 = cy
                if id == 7:  # Index base
                    cy6 = cy

                if id == 12:  # Middle tip
                    cy12 = cy
                if id == 10:  # Middle base
                    cy10 = cy

                if id == 16:  # Ring tip
                    cy16 = cy
                if id == 14:  # Ring base
                    cy14 = cy

                if id == 20:  # Little tip
                    cy20 = cy
                if id == 18:  # Little base
                    cy18 = cy

            # Thumb raised check
            if cy4 < cy3:  # Thumb is raised if tip is higher than base
                Thumb = 1
                if "Thumb" not in ShowFinger:
                    ShowFinger.append("Thumb")
            else:
                if "Thumb" in ShowFinger:
                    ShowFinger.remove("Thumb")

            # Index raised check
            if cy8 < cy6:  # Index is raised if tip is higher than base
                Index = 1
                if "Index" not in ShowFinger:
                    ShowFinger.append("Index")
            else:
                if "Index" in ShowFinger:
                    ShowFinger.remove("Index")

            # Middle raised check
            if cy12 < cy10:  # Middle is raised if tip is higher than base
                Middle = 1
                if "Middle" not in ShowFinger:
                    ShowFinger.append("Middle")
            else:
                if "Middle" in ShowFinger:
                    ShowFinger.remove("Middle")

            # Ring raised check
            if cy16 < cy14:  # Ring is raised if tip is higher than base
                Ring = 1
                if "Ring" not in ShowFinger:
                    ShowFinger.append("Ring")
            else:
                if "Ring" in ShowFinger:
                    ShowFinger.remove("Ring")

            # Little raised check
            if cy20 < cy18:  # Little is raised if tip is higher than base
                Little = 1
                if "Little" not in ShowFinger:
                    ShowFinger.append("Little")
            else:
                if "Little" in ShowFinger:
                    ShowFinger.remove("Little")

            # Calculate number of raised fingers
            Nfing = Thumb + Index + Middle + Ring + Little
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # Display results
    cv2.putText(img, "raise finger: " + str(Nfing), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    cv2.putText(img, "Fingers: " + str(ShowFinger), (50, 400), cv2.FONT_HERSHEY_PLAIN, 2., (255, 255, 255), 2)
    cv2.putText(img, "Tidtawan Shingkorn 670610760: ", (350, 70), cv2.FONT_HERSHEY_PLAIN, 1., (0, 0, 255), 1)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
