# ai-cv-survey-marking

Project solving the problem of automatic processing of topographic plans during design. The initial data is a topographic survey in dwg format

The project is based on the idea of converting vector graphics into raster graphics. Working with vector graphics is more accurate, but much more complicated.

After rasterization images are processed by convolutional neural network. I have chosen neural networks of YOLO family. Since they allow to process the whole image. 

The result of neural network work is a set of labels with coordinates (x1, y1, x2, y2). This data is recorded in a PostgeSQL database.
|Original image|Recognized marks|
|:-:|:-:|
|![image](https://github.com/Air-Erik/ai-cv-survey-marking/assets/99266772/2631a419-bf31-4b0c-a5ca-f9edb7293077)|![image](https://github.com/Air-Erik/ai-cv-survey-marking/assets/99266772/72a1d8f6-1467-4606-a21c-e75c8edf37e2)
|![image](https://github.com/Air-Erik/ai-cv-survey-marking/assets/99266772/21f336cf-eb6a-4e39-a7a1-c98b35a8c4a5)|![image](https://github.com/Air-Erik/ai-cv-survey-marking/assets/99266772/88212fda-fb35-4efc-b78a-33a1fb9bc658)



