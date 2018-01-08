import argparse
import os
import tarfile
import six.moves.urllib as urllib
import cv2
import numpy as np
import tensorflow as tf

from utils import visualization_utils as vis_util
from utils import label_map_util

MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90


def pre_process():
    opener = urllib.request.URLopener()
    opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
    tar_file = tarfile.open(MODEL_FILE)
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.getcwd())


def process(cap):
    pre_process()
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            while True:
                ret, image_np = cap.read()
                image_np_expanded = np.expand_dims(image_np, axis=0)
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

                cv2.imshow('object detection',
                           cv2.resize(image_np, (800, 600)))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break


def main(args):
    cap = None
    if(args.f == '' and args.w is False):
        cap = cv2.VideoCapture("sample.mp4")
    elif(args.f == '' and args.w is True):
        cap = cv2.VideoCapture(0)
    elif(args.f != '' and args.w is False):
        try:
            cap = cv2.VideoCapture(args.f)
        except:
            return print('Invalid video file')  
    else:
        return print('Something went wrong!')

    return process(cap)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', action="store_true",
                        help='Set this flag if you want to feed video from your webcam')
    parser.add_argument('-f', type=str, default='', help='Path to the video')
    args = parser.parse_args()
    main(args)
