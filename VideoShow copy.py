from threading import Thread
import numpy as np
import cv2

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Video",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        toShow = np.zeros((4096,3112))
        while not self.stopped:
            toShow += frame
            cv2.imshow("Video", toShow)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True