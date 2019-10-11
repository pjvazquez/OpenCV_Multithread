from multiprocessing import Process
import numpy as np
import cv2

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """
    def __init__(self, frame_queue):
        self.frame = frame_queue
        self.stopped = False

    def show(self):
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("Video",3000,0)
        cv2.setWindowProperty("Video",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

        while not self.stopped:
            if not self.frame.empty():
                cv2.imshow("Video", self.frame.get())

            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True

    if __name__ == "__main__":
        print("init videoshow")
        show()
