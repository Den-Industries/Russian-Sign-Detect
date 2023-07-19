import tensorflow as tf
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from keras.utils import plot_model
import matplotlib.pyplot as plt
import xlrd, xlwt

def create_train_charts(filename, history):
    """
    Создает графики потерь и точности при обучении и валидации модели, построенной на базе Keras с обучением и валидацией с помощью метода fit.
    Результат сохраняет в файл.

    Предполагается, что:
        1. метрика точности имела название 'accuracy'.

    Параметры:
        history:    атрибут history объекта History, который возвращает метод fit из Keras;
        filename:   путь к файлу, в который нужно сохранить график.
    """

    # Список с данными для построения графиков.
    data = []
    # Данные точности.
    data.append({
        'label': 'Точность при обучении',
        'title': 'Точность',
        'val_label': 'Точность при валидации',
        'val_values': history.get('val_accuracy'),
        'values': history['accuracy'],
    })
    # Данные потерь.
    data.append({
        'label': 'Потери при обучении',
        'title': 'Потери',
        'val_label': 'Потери при валидации',
        'val_values': history.get('val_loss'),
        'values': history['loss'],
    })

    # Определение количества эпох обучения для краткости.
    epochs = range(1, len(data[0]['values'])+1)

    # Создание основной фигуры и нужного количества холстов для графиков.
    figure, axes = plt.subplots(len(data), 1, figsize=(7, 10))
    # Корректировка расстояния между разными графиками.
    plt.subplots_adjust(hspace=.4)

    # Перебор данных для разных графиков.
    for i, axis in enumerate(axes):
        # Сетка под графиком.
        axis.grid(color='lightgray', which='both', zorder=0)
        # График основных данных в виде зеленых точек.
        axis.plot(
            epochs,
            data[i]['values'],
            '.',
            label=data[i]['label'],
            color='g',
            zorder=3
        )
        # Если данные по валидации есть...
        if data[i]['val_values']:
            # ...рисуется их график в виде красной линии.
            axis.plot(
                epochs,
                data[i]['val_values'],
                label=data[i]['val_label'],
                color='r',
                zorder=3
            )
        # Общий заголовок графика.
        axis.set_title(data[i]['title'])
        # Подпись оси Х.
        axis.set_xlabel('Эпохи')
        # Подпись оси Y.
        axis.set_ylabel(data[i]['title'])
        # Отображение легенды.
        axis.legend()

    # Сохранение графика в файл.
    figure.savefig(filename)

    plt.close()

RANDOM_SEED = 17

NUM_CLASSES = 34

dataset = 'all_letters.csv'

model_save_path = 'mymodel_all-34.hdf5'

X_dataset = np.loadtxt(dataset, delimiter = ',', dtype = 'float32', usecols = list(range(1, 42 + 1)))

Y_dataset = np.loadtxt(dataset, delimiter = ',', dtype = 'int', usecols = 0)

#excel_file = xlwt.Workbook(encoding="utf-8")

#excel_file_sheet = excel_file.add_sheet("Sheet 1")

X_train, X_test, Y_train, Y_test = train_test_split(X_dataset, Y_dataset, random_state=RANDOM_SEED, shuffle=True, train_size=0.75)

cp_callback = tf.keras.callbacks.ModelCheckpoint(model_save_path, verbose=1, save_weights_only=False)

es_callback = tf.keras.callbacks.EarlyStopping(verbose=1, patience=40)

'''
for i1 in range(0, 10):
    excel_file_sheet.write(0, i1 + 1, i1 + 1)
for i2 in range(0, 10):
    excel_file_sheet.write(i2 + 1, 0, 180 + i2 * 5)

for i1 in range(0, 5):
    for i2 in range(0, 15):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.InputLayer(42))
        print(i1 + 1, ' ', 180 + i2 * 5, ' ?')
        for i3 in range(0, i1 + 1):
            model.add(tf.keras.layers.Dropout(0.15))
            model.add(tf.keras.layers.Dense(180 + i2 * 5, activation='relu'))
        model.add(tf.keras.layers.Dense(NUM_CLASSES, activation='softmax'))
        model.summary()
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')
        history = model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_test, Y_test),
                            callbacks=[es_callback])
        excel_file_sheet.write(i2 + 1, i1 + 1, max(history.history['val_accuracy']))
        print(i1 + 1, ' ', 180 + i2 * 5, ' !')
        excel_file.save("stat3.xls")
        del model
'''
model = tf.keras.models.Sequential()

model.add(tf.keras.layers.InputLayer(42))
model.add(tf.keras.layers.Dropout(0.15))
model.add(tf.keras.layers.Dense(250, activation='relu'))
model.add(tf.keras.layers.Dropout(0.15))
model.add(tf.keras.layers.Dense(250, activation='relu'))
model.add(tf.keras.layers.Dropout(0.15))
model.add(tf.keras.layers.Dense(250, activation='relu'))
model.add(tf.keras.layers.Dropout(0.15))
model.add(tf.keras.layers.Dense(250, activation='relu'))
model.add(tf.keras.layers.Dense(NUM_CLASSES, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')

history = model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_test, Y_test), callbacks=[cp_callback, es_callback])

create_train_charts("charts/chart.png", history.history)

model = tf.keras.models.load_model(model_save_path)

plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)

prediction_result = model.predict(np.array([X_test[0]]))

print('!! ', max(history.history['val_accuracy']))

'''
print(X_test[0])

print(prediction_result, ' ', Y_test[0])

print(np.argmax(np.squeeze(prediction_result)))
'''