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

cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Video",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.moveWindow("Video",3000,0)
image = np.asarray(cv2.imread('img/Diapositiva1.png'))
image2 = cv2.resize(image,(3840,2160))
toShow = np.zeros((2160,3840,3))
# toShow[0:image.shape[0],0:image.shape[1]] = image
toShow = overlay_transparent(image2, image,0,0)
stopped = False
while not stopped:
    cv2.imshow("Video", toShow)
    if cv2.waitKey(1) == ord("q"):
        stopped = True