import argparse
import cv2
import random
import time
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow_copy import VideoShow
from multiprocessing import Queue, Process, Manager

class Worker(Process):
    def __init__(self, in_queue, out_queue):
        super(Worker, self).__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue
    def run(self):
        """
        Add iterations per second text to lower-left corner of a frame.
        """
        print("in worker before while in_queue: ", self.in_queue.empty())
        while True:
            
            if not self.in_queue.empty():
                frame = self.in_queue.get()
                x = random.randint(10,100)
                y = random.randint(10,100)
                cv2.putText(frame, "TESTING QUEUES",
                    (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255))
                self.out_queue.put(frame)

def test(source=0):
    """Grab and show video frames without multithreading."""

    cap = cv2.VideoCapture(source)

    manager = Manager()
    in_queue = manager.Queue()
    out_queue = manager.Queue()

    worker1 = Worker(in_queue, out_queue)
    worker2 = VideoGet(in_queue)
    #(grabbed, frame) = cap.read()
    # cv2.imshow("Video", frame)
    worker2.start()
    time.sleep(0.2)
    print("OUTSIDE no threading loop", in_queue.qsize())

    while True:
        
        # (grabbed, frame) = cap.read()
        #in_queue.put(frame)
        #if not grabbed or cv2.waitKey(1) == ord("q"):
        #    break
        if not in_queue.empty():
            print("inside no threading loop", in_queue.qsize())
            frame2 = in_queue.get()
            if frame2 is not None:
                cv2.imshow("Video", frame2)

    # worker2.join()


def main():
    test(0)

if __name__ == "__main__":
    main()