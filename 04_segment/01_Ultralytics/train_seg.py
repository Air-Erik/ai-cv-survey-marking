from ultralytics import YOLO
import torch


def main():
    # Проверка работы CUDA и вычисления на GPU
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    print(torch.cuda.current_device())
    print(torch.cuda.device(0))
    print(torch.cuda.get_device_name(0))

    model_variant = "yolov8n-seg"
    model = YOLO(f'{model_variant}.pt')

    args = dict(data='datasets/Segment_AI/data.yaml',
                epochs=300,
                imgsz=640,
                freeze=10,
                patience=25
                )

    model.train(**args)
    model.val()


if __name__ == '__main__':
    main()
