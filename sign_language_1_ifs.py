import math

print("sl1")

def fingers_up(landmark):
    BFs = [0, 0, 0, 0, 0]
    if (landmark.landmark[4].x > landmark.landmark[3].x and landmark.landmark[0].x < landmark.landmark[1].x) or (
            landmark.landmark[4].x < landmark.landmark[3].x and landmark.landmark[0].x > landmark.landmark[1].x):
        BFs[0] = 1
    for i in range(1, 5):
        if (landmark.landmark[(i + 1) * 4].y < landmark.landmark[(i + 1) * 4 - 2].y and landmark.landmark[
            (i + 1) * 4 - 3].y < landmark.landmark[0].y) or (
                landmark.landmark[(i + 1) * 4].y > landmark.landmark[(i + 1) * 4 - 2].y and landmark.landmark[
            (i + 1) * 4 - 3].y > landmark.landmark[0].y):
            BFs[i] = 1
    countoffingersup = 0
    for i in BFs:
        if i == 1:
            countoffingersup += 1
    return (BFs, countoffingersup)

fingersrules = [
    [0, 3, 3, 3, 3, 3],  # 1 а
    [1, 0, 1, 0, 0, 0],  # 2 б
    [4, 0, 3, 3, 3, 3],  # 3 в
    [2, 1, 1, 3, 3, 3],  # 4 г
    [],  # 5 д
    [],  # 6 е
    [],  # 7 ё
    [],  # 8 ж
    [1, 3, 1, 3, 3, 3],  # 9 з
    [2, 3, 3, 3, 1, 1],  # 10 и
    [],  # 11 й
    [2, 3, 1, 1, 3, 3],  # 12 к
    [2, 3, 1, 1, 3, 3],  # 13 л
    [3, 3, 1, 1, 1, 3],  # 14 м
    [3, 3, 1, 1, 3, 1],  # 15 н
    [3, 3, 3, 1, 1, 1],  # 16 о
    [2, 3, 1, 1, 3, 3],  # 17 п
    [3, 3, 1, 3, 1, 1],  # 18 р
    [],  # 19 с
    [3, 3, 1, 1, 1, 3],  # 20 т
    [2, 1, 3, 3, 3, 1],  # 21 у
    [],  # 22 ф
    [],  # 23 х
    [],  # 24 ц
    [],  # 25 ч
    [3, 3, 1, 1, 1, 3],  # 26 ш
    [3, 3, 1, 1, 1, 3],  # 27 щ
    [],  # 28 ъ
    [2, 3, 1, 3, 3, 1],  # 29 ы
    [2, 1, 1, 3, 3, 3],  # 30 ь
    [],  # 31 э
    [1, 3, 3, 3, 3, 1],  # 32 ю
    [5, 3, 3, 3, 3, 3],  # 33 я
]

def dist(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def fingersright(a, countoffingersup, BFs):
    buf = fingersrules[a][0] == countoffingersup
    for i in range(1, 6):
        if fingersrules[a][i] != 3:
            buf = buf and BFs[i - 1] == fingersrules[a][i]
    return buf

def sign_detecting(landmark):
    fingersinfo = fingers_up(landmark)
    BFs = fingersinfo[0]
    countoffingersup = fingersinfo[1]
    if (countoffingersup == 1 and BFs[0] == 1 and landmark.landmark[4].x > landmark.landmark[0].x):
        return u"/b"
    elif (countoffingersup == 1 and BFs[0] == 1 and landmark.landmark[4].x <
          landmark.landmark[0].x):
        return u" "
    elif (fingersright(0, countoffingersup, BFs)):
        return u"а"
    elif (fingersright(1, countoffingersup, BFs) and landmark.landmark[8].y < landmark.landmark[0].y):
        return u"б"
    elif (fingersright(2, countoffingersup, BFs) and landmark.landmark[8].y < landmark.landmark[0].y):
        return u"в"
    elif (fingersright(3, countoffingersup, BFs) and landmark.landmark[8].y > landmark.landmark[0].y):
        return u"г"
    elif (fingersright(8, countoffingersup, BFs) and landmark.landmark[8].y > landmark.landmark[0].y):
        return u"з"
    elif (fingersright(9, countoffingersup, BFs)):
        return u"и"
    elif (fingersright(11, countoffingersup, BFs) and landmark.landmark[8].y < landmark.landmark[0].y):
        return u"к"
    elif (fingersright(12, countoffingersup, BFs) and landmark.landmark[8].y > landmark.landmark[0].y and dist(
            landmark.landmark[8], landmark.landmark[12]) > dist(landmark.landmark[7], landmark.landmark[11])):
        return u"л"
    elif (fingersright(13, countoffingersup, BFs) and landmark.landmark[8].y > landmark.landmark[0].y and dist(
            landmark.landmark[8], landmark.landmark[16]) > dist(landmark.landmark[7], landmark.landmark[15])):
        return u"м"
    elif (fingersright(14, countoffingersup, BFs)):
        return u"н"
    elif (fingersright(15, countoffingersup, BFs)):
        return u"о"
    elif (fingersright(16, countoffingersup) and landmark.landmark[8].y > landmark.landmark[0].y and dist(
            landmark.landmark[8], landmark.landmark[12]) <= dist(landmark.landmark[7], landmark.landmark[11])):
        return u"п"
    elif (fingersright(17, countoffingersup, BFs)):
        return u"р"
    elif (countoffingersup == 3 and BFs[1] == 1 and BFs[2] == 1 and BFs[3] == 1 and
          landmark.landmark[8].y > landmark.landmark[0].y and dist(landmark.landmark[8], landmark.landmark[16]) <= dist(
                    landmark.landmark[7], landmark.landmark[15])):
        return u"т"
    elif (countoffingersup == 4 and BFs[0] == 0 and landmark.landmark[8].y > landmark.landmark[
        0].y and dist(landmark.landmark[8], landmark.landmark[16]) <= dist(landmark.landmark[7],
                                                                           landmark.landmark[15])):
        return u"т"
    elif (fingersright(20, countoffingersup, BFs)):
        return u"у"
    elif (fingersright(25) and landmark.landmark[8].y < landmark.landmark[0].y and dist(
            landmark.landmark[8], landmark.landmark[16]) <= dist(landmark.landmark[7], landmark.landmark[15])):
        return u"ш"
    elif (fingersright(26, countoffingersup, BFs) and landmark.landmark[8].y < landmark.landmark[0].y and dist(
            landmark.landmark[8], landmark.landmark[16]) > dist(landmark.landmark[7], landmark.landmark[15])):
        return u"щ"
    elif (fingersright(28, countoffingersup, BFs)):
        return u"ы"
    elif (fingersright(29, countoffingersup, BFs) and landmark.landmark[8].y < landmark.landmark[0].y):
        return u"ь"
    elif (fingersright(31, countoffingersup, BFs)):
        return u"ю"
    elif (fingersright(32, countoffingersup, BFs) and (
            landmark.landmark[8].x < landmark.landmark[12].x and landmark.landmark[5].x > landmark.landmark[9].x)):
        return u"я"
    elif ((landmark.landmark[8].x > landmark.landmark[5].x and landmark.landmark[5].x > landmark.landmark[0].x) or
          (landmark.landmark[8].x < landmark.landmark[5].x and landmark.landmark[5].x < landmark.landmark[0].x)) and ((landmark.landmark[12].x > landmark.landmark[9].x and landmark.landmark[9].x > landmark.landmark[0].x) or
         (landmark.landmark[12].x < landmark.landmark[9].x and landmark.landmark[9].x <landmark.landmark[0].x)) and ((landmark.landmark[16].x < landmark.landmark[10].x and landmark.landmark[9].x > landmark.landmark[0].x) or
         (landmark.landmark[16].x > landmark.landmark[10].x and landmark.landmark[9].x < landmark.landmark[0].x)) and ((landmark.landmark[20].x < landmark.landmark[10].x and landmark.landmark[9].x > landmark.landmark[0].x) or
         (landmark.landmark[20].x > landmark.landmark[10].x and landmark.landmark[9].x < landmark.landmark[0].x)) and landmark.landmark[16].y > landmark.landmark[12].x and landmark.landmark[20].y > landmark.landmark[12].x and landmark.landmark[0].y > landmark.landmark[8].y:
        return u"д"
    # абвгдзиклмнопртушщьыюя