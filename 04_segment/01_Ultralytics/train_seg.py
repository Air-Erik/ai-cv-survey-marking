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

    # ClearML; Определение модели на которой будет происходить обучение
    model_name = "yolov8l"
    dataset_name = 'png_pipe_4cls.v5'

    args = dict(data=f'datasets/{dataset_name}/data.yaml',
                epochs=120,
                imgsz=640,
                freeze=10,
                patience=30,
                overlap_mask=True
                )

    # ClearML; Создание объекта задачи для clearml, описывает проект и
    # название текущей сессии
    task = Task.init(
        project_name="AutoCAD_segment",
        task_name=dataset_name,
        tags=['png',
              model_name,
              f"epoch={args['epochs']}",
              f"freeze={args['freeze']}",
              f"patience={args['patience']}"
              ]
        )
    task.set_parameter("model_variant", model_name)

    model = YOLO(f'{model_name}-seg.pt')

    task.connect(args)

    model.train(**args)


if __name__ == '__main__':
    main()
