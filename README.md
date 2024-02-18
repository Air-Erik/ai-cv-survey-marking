# ai-cv-survey-marking

Project solving the problem of automatic processing of topographic plans during design. The initial data is a topographic survey in dwg format

The project is based on the idea of converting vector graphics into raster graphics. Working with vector graphics is more accurate, but much more complicated.

After rasterization images are processed by convolutional neural network. I have chosen neural networks of YOLO family. Since they allow to process the whole image. 

The result of neural network work is a set of labels with coordinates (x1, y1, x2, y2). This data is recorded in a PostgeSQL database.
