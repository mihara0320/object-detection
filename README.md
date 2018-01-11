# object-detection

This is final project for Advanced Python (I720) <br />
This module makes use of the 
[Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) for detecting object within the input video data, as well as [OpenCV](https://pypi.python.org/pypi/opencv-python) for handing video data input.
> NB: Works only with Python3, since Tensorflow does not support Python2 

## Install dependencies

All the necessary files coming from Tensorflow Object Detection API are already compiled in this project.
Therefore, simply run: 
```
	pip install -r requirements.txt 
```

## Running project
To run the project:
```
	python main.py [options]
```
### options

 - --w ... "when this flag is set it will use your webcam as data input"
 - --f [path to video file] ... "it will use this data as video input" 

> By default, if no method of data input declared, it will use sample video within the project as data input.

## Running Test
```
	python -m unittest test_processor.py
```
