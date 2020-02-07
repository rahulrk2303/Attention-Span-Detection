import cv2
import time
import numpy as np
from threading import Thread, Lock
import blinkrate_new
# from quantify import quant, ret_quant
from Test.face_classification.src.face_expr_test import expr,ret_exp
import xlwt
from xlwt import Workbook
from Test.GazeTracking.gaze_tracking.gaze_tracking import GazeTracking
from skimage.measure import compare_ssim
import imutils
from audio3 import audio
from flask import url_for, jsonify, Flask, render_template, request, jsonify

app = Flask(__name__)

ssim = 0

class WebcamVideoStream :
	def __init__(self, src = 0, width = 640, height = 480) :
		self.stream = cv2.VideoCapture(src)
		self.stream.set( cv2.CAP_PROP_FRAME_WIDTH, width)
		self.stream.set( cv2.CAP_PROP_FRAME_HEIGHT, height)
		(self.grabbed, self.frame) = self.stream.read()
		self.started = False
		self.read_lock = Lock()

	def start(self) :
		if self.started :
			# print ("already started!!")
			return None
		self.started = True
		self.thread = Thread(target=self.update, args=())
		self.thread.start()
		return self

	def update(self) :
		while self.started :
			(grabbed, frame) = self.stream.read()
			self.read_lock.acquire()
			self.grabbed, self.frame = grabbed, frame
			self.read_lock.release()

	def read(self) :
		self.read_lock.acquire()
		frame = self.frame.copy()
		self.read_lock.release()
		return frame

	def stop(self) :
		self.started = False
		self.thread.join()

	def __exit__(self, exc_type, exc_value, traceback) :
		self.stream.release()



subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)

def difference(im1,im2):
	im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
	im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
	(score, diff) = compare_ssim(im1, im2, full=True)
	return score

distract = []

def capture(cap=None):
	# cap = cv2.VideoCapture(0)
	cap = cap.start()
	# fourcc = cv2.VideoWriter_fourcc(*'XVID')
	# out = cv2.VideoWriter('capture.avi',fourcc, 20.0, (640,480))
	x = 0

	gaze = GazeTracking()
	blink_c = 0

	while(True):
		frame = cap.read()
		# out.write(frame)

		# cv2.imshow('capture', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		# frame = subtractor.apply(frame) #Background sub
		# cv2.imshow('capture', frame)
		
		global ssim
		if x%(5*10*2) == 0:
			frame2 = frame
		if (x-50)%(5*10*2) == 0:
			frame1 = frame
			# quant(frame1, frame2)
			if x%2==0:
				# quant(frame1, frame2)
				ssim = difference(frame1,frame2)
			else:
				# quant(frame2, frame1)
				ssim = difference(frame2,frame1)

		x+=1

		# while True:
	    # We get a new frame from the webcam
	    # frame = camm.read()

	    # We send this frame to GazeTracking to analyze it
		gaze.refresh(frame)

		frame = gaze.annotated_frame()
		text = ""

		if gaze.is_blinking():
		    text = "Blinking"
		    # distract.append(0)
		    blink_c += 1
		    if blink_c >=10:
		    	distract.append(0)
			# else:
	  #   		distract.append(0.5)
		    	# print(blink_c)
		elif gaze.is_right():
		    text = "Looking right"
		    distract.append(0.2)
		    blink_c = 0
		elif gaze.is_left():
		    text = "Looking left"
		    distract.append(0.2)
		    blink_c = 0
		elif gaze.is_center():
		    text = "Looking center"
		    distract.append(1)
		    blink_c = 0
		# time.sleep(0.5)

		cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

		left_pupil = gaze.pupil_left_coords()
		right_pupil = gaze.pupil_right_coords()
		cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
		cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

		cv2.imshow("Distraction", frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break


	cap.stop()
	# out.release()
	cv2.destroyAllWindows()


timer_run = True
i = 0


def timer ():
	
	while (timer_run):
		time.sleep(1)
		global i
		i = i+1


if __name__ == '__main__':

	wvs = WebcamVideoStream()
	t4 = Thread(target = expr, kwargs={'video_capture': wvs})
	t1 = Thread(target = capture, kwargs={'cap': wvs})
	t2 = Thread(target = timer)
	t3 = Thread(target = blinkrate_new.func, kwargs={'vs': wvs})
	# t5 = Thread(target = gaze_track, kwargs={'camm': wvs})
	# t6 = Thread(target = audio)


	t4.start()
	t1.start()
	t2.start()
	t3.start()	
	# t5.start()
	# t6.start()

	ttt = 0
	ii = 1

	wb = Workbook() 
	  
	sheet1 = wb.add_sheet('Sheet 1') 
	sheet1.write(0, 0, 'Time') 
	sheet1.write(0, 1, 'Blink count') 
	sheet1.write(0, 2, 'Pixel Difference')
	sheet1.write(0, 3, 'Emotion')
	sheet1.write(0, 4, 'Distraction')

	while(True):
		time.sleep(5)
		ttt+=5
		b = blinkrate_new.blink_count()
		
		exp = int(ret_exp())
		distract_mean = np.mean(distract)

		sheet1.write(ii,0,ttt)
		sheet1.write(ii,1,b)
		sheet1.write(ii,2,ssim)
		sheet1.write(ii,3,exp)
		sheet1.write(ii,4,distract_mean)

		distract.clear()

		wb.save('attentiondata.xls')
		ii+=1
