import argparse
import cv2
import random
from CountsPerSec import CountsPerSec
from VideoGet_copy import VideoGet
from VideoShow_copy import VideoShow
from multiprocessing import Queue, Process, Manager

class Worker(Process):
    def __init__(self, in_queue, out_queue):
        super(Worker, self).__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue
    def start(self):
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

def noThreading(source=0):
    """Grab and show video frames without multithreading."""

    cap = cv2.VideoCapture(source)

    manager = Manager()
    in_queue = manager.Queue()
    out_queue = manager.Queue()

    workers = Worker(in_queue, out_queue)
    (grabbed, frame) = cap.read()
    cv2.imshow("Video", frame)
    workers.start()
    workers.join()

    while True:
        print("inside no threading loop")
        (grabbed, frame) = cap.read()
        in_queue.put(frame)
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break
        if not out_queue.empty():
            frame2 = out_queue.get()
            cv2.imshow("Video", frame2)

def threadVideoGet(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Main thread shows video frames.
    """
    print("start video getter")
    video_getter = VideoGet(source).start()
    print("creates manager and queues")
    manager = Manager()
    in_queue = manager.Queue()
    out_queue = manager.Queue()
    print("initiate worker")
    workers = Worker(in_queue, out_queue)
    workers.start()    

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            workers.terminate()
            break
        print("get frame")
        frame = video_getter.frame
        print("put frame")
        in_queue.put(frame)
        print("have frame?", out_queue.qsize())
        if not out_queue.empty():
            framein = out_queue.get()
            cv2.imshow("Video", framein)

def threadVideoShow(source=0):
    """
    Dedicated thread for showing video frames with VideoShow object.
    Main thread grabs video frames.
    """

    cap = cv2.VideoCapture(source)
    (grabbed, frame) = cap.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    ap.add_argument("--thread", "-t", default="none",
        help="Threading mode: get (video read in its own thread),"
            + " show (video show in its own thread), both"
            + " (video read and video show in their own threads),"
            + " none (default--no multithreading)")
    args = vars(ap.parse_args())

    if args["thread"] == "both":
        threadBoth(args["source"])
    elif args["thread"] == "get":
        threadVideoGet(args["source"])
    elif args["thread"] == "show":
        threadVideoShow(args["source"])
    else:
        noThreading(args["source"])

if __name__ == "__main__":
    main()