import numpy as np
import cv2



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

# creates a named window to reuse
cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
# set properties as full screen
cv2.setWindowProperty("Video",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
# moves window longer than primary monitor position so fix it in second monitor
cv2.moveWindow("Video",3000,0)
# gets background image
image = cv2.imread('img/Diapositiva1.png')
image = cv2.resize(image,(3840,2160))
# gets other image to overlay with
image2 = cv2.imread('img/happy.jpg')
# function to overlay images of different sizes at x,y position
toShow = overlay_transparent(image, image2,0,0)
stopped = False

while not stopped:
    cv2.imshow("Video", toShow)
    if cv2.waitKey(1) == ord("q"):
        stopped = True