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
        task_name="Pipe_4cls_pixel.v6"
        )

    # ClearML; Определение модели на которой будет происходить обучение
    model_variant = "yolov8l"
    task.set_parameter("model_variant", model_variant)

    model = YOLO('yolov8l-seg.pt')

    args = dict(data='datasets/Pipe_4cls_pixel.v6/data.yaml',
                epochs=250,
                imgsz=640,
                freeze=8,
                patience=30,
                )
    task.connect(args)

    model.train(**args)


if __name__ == '__main__':
    main()
