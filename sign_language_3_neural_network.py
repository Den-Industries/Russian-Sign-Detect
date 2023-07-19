import tensorflow as tf
import numpy as np

print("sl3")

model_save_path = 'mymodel_all-34.hdf5'

model = tf.keras.models.load_model(model_save_path)

def sign_detecting(landmark):
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
        bufcord.append(((sublandmark.x - landmark.landmark[0].x) / magicx) * 0.5 + 0.5)
        bufcord.append(((sublandmark.y - landmark.landmark[0].y) / magicy) * 0.5 + 0.5)
    prediction_result = model.predict(np.array([bufcord]), verbose = 0)
    answer = [np.argmax(np.squeeze(prediction_result)), max(prediction_result[0])]
    return answer