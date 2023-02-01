import cv2

def frame_height():
	cap = cv2.VideoCapture("test.mp4")
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	cap.release()
	return int(height)
 
def frame_width():
	cap = cv2.VideoCapture("test.mp4")
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	cap.release()
	return int(width)

def versionTst():
	print(cv2.getBuildInformation())