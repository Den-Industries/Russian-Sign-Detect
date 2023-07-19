import cv2
import mediapipe as mp
import numpy as np
import pathlib
import pickle

print("sl2")

mpDraw = mp.solutions.drawing_utils

Hu_moments_of_letters = []

wasletters = []

slovar = {
        224: f"а",
        225: f"б",
        226: f"в",
        227: f"г",
        228: f"д",
        229: f"е",
        230: f"ж",
        231: f"з",
        232: f"и",
        233: f"й",
        234: f"к",
        235: f"л",
        236: f"м",
        237: f"н",
        238: f"о",
        239: f"п",
        240: f"р",
        241: f"с",
        242: f"т",
        243: f"у",
        244: f"ф",
        245: f"х",
        246: f"ц",
        247: f"ч",
        248: f"ш",
        249: f"щ",
        251: f"ы",
        252: f"ь",
        253: f"э",
        254: f"ю",
        255: f"я" }

my_file = pathlib.Path("HuMoments.bin")
if my_file.is_file():
    f = open("HuMoments.bin", "rb")
    binstuff = f.read()
    f.close()
    cords = pickle.loads(binstuff)
    Hu_moments_of_letters = pickle.loads(binstuff)

def get_count_of_hu_moments():
    letters = [0] * 32
    for moment in Hu_moments_of_letters:
        letters[moment[1] - 224] += 1

def sign_detecting(landmark, image = None):
    W, H = 640, 480
    huimage = np.zeros((H, W, 3), np.uint8)
    mpDraw.draw_landmarks(huimage, landmark,
                          mp.solutions.hands.HAND_CONNECTIONS,
                          mpDraw.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                          mpDraw.DrawingSpec(color=(255, 255, 255), thickness=30, circle_radius=30))
    huimage = cv2.cvtColor(huimage, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(huimage, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    M = cv2.moments(cnt)
    Hm = cv2.HuMoments(M)
    hm_norm = np.linalg.norm(Hm)
    Hm = Hm / hm_norm
    if image:
        cv2.drawContours(image, [cnt], -1, (0, 255, 255), 3)
    magic = 8
    nearests = [[-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0], [-1, 0]]
    for humoment in Hu_moments_of_letters:
        d2 = np.linalg.norm(humoment[0] - Hm)
        for i in range(0, magic):
            if nearests[i][0] == -1:
                nearests[i][0] = humoment[1]
                nearests[i][1] = d2
                break
            else:
                if nearests[i][1] > d2:
                    for u in range(4, i, -1):
                        nearests[u][0] = nearests[u - 1][0]
                        nearests[u][1] = nearests[u - 1][1]
                    nearests[i][0] = humoment[1]
                    nearests[i][1] = d2
                    break
    lettershere = [0] * 32
    for letter in nearests:
        lettershere[nearests[0][0] - 224] += 1
    biggest = [0, 0]
    for i in range(0, 32):
        if lettershere[i] > biggest[0]:
            biggest[0] = lettershere[i]
            biggest[1] = i + 224
    wasletters.append(biggest[1])
    whatlettershown = [0] * 32
    for letter in wasletters:
        whatlettershown[letter - 224] += 1
    biggest1 = [0, 0]
    for i in range(0, 32):
        if whatlettershown[i] > biggest1[0]:
            biggest1[0] = whatlettershown[i]
            biggest1[1] = i + 224
    wasletters.clear()
    if biggest1[0] > len(wasletters) * 0.75:
        return slovar[biggest1[1]]