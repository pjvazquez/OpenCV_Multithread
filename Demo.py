import argparse
import cv2
from CountsPerSec import CountsPerSec
from VideoGet_copy import VideoGet
from VideoShow_copy import VideoShow
import StateManager
from StateManager import Smile
from transitions import Machine
import numpy as np

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def putState(frame, state):
    """
    Add State info in frame.
    """

    cv2.putText(frame, str(state), 
                (10, 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def runThreads(source=0, FiniteStateMachine = None):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    bg_images = {}
    for i, state in enumerate(StateManager.states):
        bg = cv2.imread(f'img/Diapositiva{i%5+1}.png')
        bg_images[state] = cv2.resize(bg,(3840,2160))

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break
        
        if FiniteStateMachine is not None:
            FiniteStateMachine.next()

            bg = bg_images[FiniteStateMachine.state]


        
        frame = video_getter.frame
        frame = overlay_transparent(bg, frame,0,0)
        frame = putState(frame, FiniteStateMachine.state)
        video_shower.frame = frame
        cps.increment()

def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background

def main():
    smile = Smile()
    fsm = Machine(smile, 
                states = StateManager.states, 
                transitions = StateManager.transitions,
                initial="start")
                
    runThreads(source=0,FiniteStateMachine=smile )

if __name__ == "__main__":
    main()