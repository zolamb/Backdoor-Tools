import cv2
import tempfile

def execute():
	webcam = cv2.VideoCapture(0)
	frame = webcam.read()[1]
	cv2.imwrite(tempfile.gettempdir()+"\webcam.jpg",frame)
	webcam.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	execute()
