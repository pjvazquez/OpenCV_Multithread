from multiprocessing import Process, Queue
import argparse
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow
import StateManager
from StateManager import Smile
from transitions import Machine

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame


def runProceses(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    # videoget = VideoGet(source)
    # videoshow = VideoShow(frame)

    frame_queue = Queue()

    videoget_proc = Process(target=VideoGet, args=(source,frame_queue))
    videoshow_proc = Process(target=VideoShow, args=(frame_queue,))
    
    # cps = CountsPerSec().start()

    videoget_proc.start()
    videoshow_proc.start()

    videoget_proc.join()
    videoshow_proc.join()


def main():
    runProceses(source=0)

if __name__ == "__main__":
    main()