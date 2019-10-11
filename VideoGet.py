from multiprocessing import Process, Queue
import cv2

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src, frame_queue):
        self.queue = frame_queue
        self.stream = cv2.VideoCapture(src)
        # (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                self.queue(self.frame)

    def stop(self):
        self.stopped = True

    if __name__ == "__main__":
        print("init videoget")
        get()