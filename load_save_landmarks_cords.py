import pathlib
import pickle

print("lslc")

def Load():
    my_file = pathlib.Path("cords.bin")
    if my_file.is_file():
        f = open("cords.bin", "rb")
        binstuff = f.read()
        f.close()
        cords = pickle.loads(binstuff)
        return cords
    return None

def get_count_of_cords(cords):
    letters = [0] * 34
    for cord in cords:
        letters[cord[1] - 224] += 1
    alphabet = ''.join([chr(i) for i in range(ord('а'), ord('а') + 32)])
    alphabet += "~-"
    for i in range(0, 34):
        print(alphabet[i], ':', letters[i], end = ' ', sep = '')
    print('')

def Append_Cord(cords, landmark, letter):
    xList = []
    yList = []
    for id, lm in enumerate(landmark.landmark):
        px, py = lm.x, lm.y
        xList.append(px)
        yList.append(py)
    xmin, xmax = min(xList), max(xList)
    ymin, ymax = min(yList), max(yList)
    magicx = max(landmark.landmark[0].x - xmin, xmax - landmark.landmark[0].x)
    magicy = max(landmark.landmark[0].y - ymin, ymax - landmark.landmark[0].y)
    bufcord = []
    for sublandmark in landmark.landmark:
        bufcord.append((
            (sublandmark.x - landmark.landmark[0].x) / magicx,
            (sublandmark.y - landmark.landmark[0].y) / magicy))
    cords.append((bufcord, letter))

def SaveToBin(cords):
    obj = pickle.dumps(cords)
    f = open("cords.bin", "wb")
    f.write(obj)
    f.close()

def SaveToCSV(cords):
    f = open("all_letters.csv", "w")
    for cord in cords:
        strbuf = str(cord[1] - 224) + ','
        for xy in cord[0]:
            strbuf += str(xy[0] * 0.5 + 0.5) + ',' + str(xy[1] * 0.5 + 0.5) + ','
        strbuf = strbuf[:-1]
        strbuf += '\n'
        f.write(strbuf)
    f.close()