import unittest
import os
import cv2
import processor


class TestProcessor(unittest.TestCase):
    cap = cv2.VideoCapture("sample.mp4")
    processor = processor.Processor(cap)

    def test_pre_process(self):
        self.processor.pre_process()  # assertTrue
        self.assertTrue(os.path.isfile(processor.PATH_TO_CKPT))

def run():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
