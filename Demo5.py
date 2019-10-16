import argparse
import cv2
import random
import time
import ray
import numpy as np
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow_copy import VideoShow
from multiprocessing import Queue, Process, Manager

@ray.remote
class Worker():
    def __init__(self):
        self.status = True
    def run(self, frame):
        """
        Add iterations per second text to lower-left corner of a frame.
        """
        print("Processing frame")

        x = random.randint(10,100)
        y = random.randint(10,100)
        cv2.putText(frame, "TESTING QUEUES",
            (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255))
        return frame

def test(source=0):
    """Grab and show video frames without multithreading."""

    frame_process = Worker.remote()

    cap = cv2.VideoCapture(source)

    print("OUTSIDE no threading loop")

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break
        frame2 = ray.put(frame)
        frame2 = frame_process.run.remote(frame2)
        frame3 = np.asarray(ray.get(frame2))
        print(frame3)
        cv2.imshow("Video", frame3)


def main():
    test(0)

if __name__ == "__main__":
    ray.init()
    print("Ray initialized: ", ray.is_initialized())
    main()