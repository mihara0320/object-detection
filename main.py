import argparse
import cv2
from processor import Processor


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

    porcessor = Processor(cap)
    porcessor.pre_process()
    porcessor.process()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', action="store_true",
                        help='Set this flag if you want to feed video from your webcam')
    parser.add_argument('-f', type=str, default='', help='Path to the video')
    args = parser.parse_args()
    main(args)
