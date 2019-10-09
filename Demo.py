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

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break
        
        if FiniteStateMachine is not None:
            FiniteStateMachine.next()
        
        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        frame = putState(frame, FiniteStateMachine.state)
        video_shower.frame = frame
        cps.increment()

def main():
    smile = Smile()
    fsm = Machine(smile, 
                states = StateManager.states, 
                transitions = StateManager.transitions,
                initial="start")
                
    runThreads(source=0,FiniteStateMachine=smile )

if __name__ == "__main__":
    main()