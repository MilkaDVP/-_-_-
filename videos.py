import cv2
import os
import datetime
from ultralytics import YOLO


def detect_objects(video_path):
    # Устанавливаем переменную окружения для избежания ошибок с дублированием библиотеки
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

    # Устанавливаем путь для вывода результатов
    output_path = os.path.join('detected', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(output_path, exist_ok=True)

    # Загружаем модель YOLOv8
    model = YOLO('train/weights/last.pt')

    # Загружаем видео
    cap = cv2.VideoCapture(video_path)

    # Получаем свойства видео
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Создаем видеозаписывающий объект
    out = cv2.VideoWriter(os.path.join(output_path, 'output.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), fps,
                          (width, height))

    ret = True

    # Считываем кадры
    frame_count = 0
    while ret:
        ret, frame = cap.read()

        if ret:
            # Детектируем объекты
            results = model.track(frame, conf=0.5, persist=True)

            # Визуализируем результаты без идентификаторов
            frame_ = results[0].plot()

            # Записываем в видео
            out.write(frame_)

            # Сохраняем каждые 5 секунд
            if frame_count % (fps * 5) == 0:
                cv2.imwrite(os.path.join(output_path, f'frame_{frame_count}.jpg'), frame_)

        frame_count += 1

    # Освобождаем ресурсы
    cap.release()
    out.release()
    cv2.destroyAllWindows()
