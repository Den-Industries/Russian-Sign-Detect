import cv2
import mediapipe as mp

print("bc")

def rainbow_draw(draw_image, landmark, glow, W, H):
    for stuff in mp.solutions.hands.HAND_CONNECTIONS:
        cv2.line(draw_image,
                 (int(landmark.landmark[stuff[0]].x * W), int(landmark.landmark[stuff[0]].y * H)),
                 (int(landmark.landmark[stuff[1]].x * W), int(landmark.landmark[stuff[1]].y * H)),
                 (abs((((landmark.landmark[stuff[0]].x + landmark.landmark[stuff[1]].x) / 2) * 1000) % 510 - 255),
                  abs(glow - 250),
                  abs((((landmark.landmark[stuff[0]].y + landmark.landmark[stuff[1]].y) / 2) * 1000) % 510 - 255)), 3)
        # print(stuff[0], ' ', stuff[1], " $")
    for sublandmark in landmark.landmark:
        x, y = sublandmark.x, sublandmark.y
        cv2.circle(draw_image, (int(x * W), int(y * H)), 6,
                   (abs((x * 1000) % 510 - 255),
                    abs(glow - 250),
                    abs((y * 1000) % 510 - 255)),
                   cv2.FILLED)