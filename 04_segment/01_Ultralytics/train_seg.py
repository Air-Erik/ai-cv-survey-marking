from clearml import Task
from ultralytics import YOLO
import torch


def main():
    # Проверка работы CUDA и вычисления на GPU
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    print(torch.cuda.current_device())
    print(torch.cuda.device(0))
    print(torch.cuda.get_device_name(0))

    # ClearML; Создание объекта задачи для clearml, описывает проект и
    # название текущей сессии
    task = Task.init(
        project_name="AutoCAD_segment",
        task_name="TEST 3.v2"
        )

    # ClearML; Определение модели на которой будет происходить обучение
    model_variant = "yolov8l"
    task.set_parameter("model_variant", model_variant)

    model = YOLO('yolov8l-seg.pt')

    args = dict(data='datasets/TEST 3.v2/data.yaml',
                epochs=120,
                imgsz=640,
                freeze=10,
                patience=30,
                overlap_mask=False
                )
    task.connect(args)

    model.train(**args)


if __name__ == '__main__':
    main()
