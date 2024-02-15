from ultralytics import YOLO
import torch


def main():
    # Проверка работы CUDA и вычисления на GPU
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    print(torch.cuda.current_device())
    print(torch.cuda.device(0))
    print(torch.cuda.get_device_name(0))

    model = YOLO('yolov8l-seg.pt')

    args = dict(data='datasets/Segment_AI/data.yaml',
                epochs=100,
                imgsz=640,
                freeze=8,
                patience=20,
                )

    model.train(**args)


if __name__ == '__main__':
    main()
