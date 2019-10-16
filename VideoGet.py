import multiprocessing
import cv2

class VideoGet(multiprocessing.Process):
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """
    def __init__(self, in_queue):
        # super(VideoGet, self).__init__()
        # multiprocessing.set_start_method('spawn')
        multiprocessing.Process.__init__(self)
        self.queue = in_queue
        # (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def run(self):
        print("running camera get")
        self.stream = cv2.VideoCapture(0)
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
            print("new frame in queue")
            self.queue.put(self.frame)

    def stop(self):
        self.stopped = True

    if __name__ == "__main__":
        print("init videoget")
        self.run()