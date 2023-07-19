import math
from time import time
import cv2
import mediapipe as mp
import numpy as np
import beautiful_draw
import sign_language_1_ifs
import sign_language_2_hu_moments
import sign_language_3_neural_network
import load_save_landmarks_cords

cap = cv2.VideoCapture(0)
W, H = 640, 480
hand_detection = mp.solutions.hands
detector = hand_detection.Hands(max_num_hands=4)
text = u""
cooldown = time()

print('statring')

cords = load_save_landmarks_cords.Load()
load_save_landmarks_cords.get_count_of_cords(cords)

nums = list(range(0, 34))

letters = []

for letter in ''.join([chr(i) for i in range(ord('а'), ord('а') + 32)]):
    letters.append(letter)

letters.append('~')

letters.append('-')

id_letter_dict = dict(zip(nums, letters))

#print(id_letter_dict)


def itwasnot(a):
    return (len(text) == 0 or (len(text) > 0 and text[len(text) - 1] != a))


work = 1

glow = 0

iterations_of_detecting = 0

sign_detecting_tryes = [0] * 34

while cap.isOpened() and work == 1:
    okay, frame = cap.read()
    glow = (glow + 5) % 510
    if okay:
        image = cv2.resize(frame, (W, H))  # BGR~RGB?
        image.flags.writeable = False
        result = detector.process(image)
        currenttime = time()
        if result.multi_hand_landmarks:
            for landmark in result.multi_hand_landmarks:
                if (currenttime - cooldown > 0.05):
                    cooldown = currenttime
                    iterations_of_detecting += 1
                    if iterations_of_detecting >= 0:
                        resultsign = sign_language_3_neural_network.sign_detecting(landmark)
                        if resultsign[1] > 0.5:
                            sign_detecting_tryes[resultsign[0]] += 1
                    if iterations_of_detecting == 4:
                        #print(sign_detecting_tryes)
                        iterations_of_detecting = -2
                        letter = id_letter_dict[np.argmax(sign_detecting_tryes)]
                        if letter == '~':
                            if len(text) > 0:
                                text = text[:-1]
                                print(text, ' *')
                                iterations_of_detecting = -4
                        elif letter == '-':
                            if itwasnot(" "):
                                text += " "
                                print(text, ' *')
                        elif itwasnot(letter):
                            text += letter
                            print(text, ' *')
                        sign_detecting_tryes = [0] * 34

                # mpDraw.draw_landmarks(image, landmark, mp.solutions.hands.HAND_CONNECTIONS, mpDraw.DrawingSpec(thickness=3, circle_radius=3))

                beautiful_draw.rainbow_draw(image, landmark, glow, W, H)

                fingers_stuff = sign_language_1_ifs.fingers_up(landmark)

                cv2.putText(image, str(fingers_stuff[1]),
                            (int(landmark.landmark[0].x * W), int(landmark.landmark[0].y * H)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                cv2.putText(image, str(fingers_stuff[1]),
                            (int(landmark.landmark[0].x * W), int(landmark.landmark[0].y * H)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                if (currenttime - cooldown > 1.2 and False):
                    cooldown = currenttime
                    detect_buf = sign_language_1_ifs.sign_detecting(landmark)
                    if detect_buf == u"/b":
                        text = text[:-1]
                    else:
                        text += detect_buf

                #print(text, end=' ')
                #print(fingers_stuff[0])

        cv2.imshow("program", image)

        buf = cv2.waitKey(2)
        '''
        if buf == 8:
            #letters[cords[-1][1] - 224] -= 1
            #del cords[-1]
            print(letters)
            #text = text[:-1]
            print(text, ' *')
        if buf == 32:
            #text = text + u" "
            print(text, ' *')
            '''
        if result.multi_hand_landmarks and False:
            if (buf >= 224 and buf <= 255) or buf == 8 or buf == 32:
                if buf == 8:
                    buf = 256
                if buf == 32:
                    buf = 257
                print('!! ', buf)
                load_save_landmarks_cords.Append_Cord(cords, result.multi_hand_landmarks[0], buf)
                load_save_landmarks_cords.get_count_of_cords(cords)
                load_save_landmarks_cords.SaveToBin(cords)
                load_save_landmarks_cords.SaveToCSV(cords)

cap.release()
cv2.destroyAllWindows()