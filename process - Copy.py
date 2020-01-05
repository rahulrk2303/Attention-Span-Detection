import cv2
import time
import numpy as numpy
from threading import Thread, Lock
import blinkrate_new
from quantify import quant, ret_quant
from Test.face_classification.src.face_expr_test import expr,ret_exp
import xlwt
from xlwt import Workbook
from Test.GazeTracking.gaze_tracking import GazeTracking


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

text = ""

def capture(cap=None):
	# cap = cv2.VideoCapture(0)
	cap = cap.start()
	# fourcc = cv2.VideoWriter_fourcc(*'XVID')
	# out = cv2.VideoWriter('capture.avi',fourcc, 20.0, (640,480))
	x = 0

	gaze = GazeTracking()

	while(True):
		frame = cap.read()
		# out.write(frame)

		# cv2.imshow('capture', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if x%(5*10*2) == 0:
			frame2 = frame
		if (x-50)%(5*10*2) == 0:
			frame1 = frame
			# quant(frame1, frame2)
			if x%2==0:
				quant(frame1, frame2)
			else:
				quant(frame2, frame1)
		x+=1


		global text
		gaze.refresh(frame)
		frame = gaze.annotated_frame()
		if gaze.is_left():
			text = "Left"
		elif gaze.is_right():
			text = "Right"
		elif gaze.is_center():
			text = "Center"
		else:
			text = "None"

		cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

		# left_pupil = gaze.pupil_left_coords()
		# right_pupil = gaze.pupil_right_coords()
		# cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
		# cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
		cv2.imshow("Eye tracking", frame)

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
	t1 = Thread(target = capture, kwargs={'cap': wvs})
	t2 = Thread(target = timer)
	t3 = Thread(target = blinkrate_new.func, kwargs={'vs': wvs})
	t4 = Thread(target = expr, kwargs={'video_capture': wvs})

	t1.start()
	t3.start()
	t4.start()
	t2.start()

	ttt = 0
	ii = 1

	wb = Workbook() 
	  
	# add_sheet is used to create sheet. 
	sheet1 = wb.add_sheet('Sheet 1') 
	sheet1.write(0, 0, 'Time') 
	sheet1.write(0, 1, 'Blink count') 
	sheet1.write(0, 2, 'Manhattan Norm') 
	sheet1.write(0, 3, 'Manhattan Zero') 
	sheet1.write(0, 4, 'Max of Norm') 
	sheet1.write(0, 5, 'Max of Zero') 
	sheet1.write(0, 6, 'Emotion')
	sheet1.write(0, 7, 'Eye position')

	while(True):
		time.sleep(5)
		ttt+=5
		b = blinkrate_new.blink_count()
		x, y, z, z1 = ret_quant()
		exp = ret_exp()
		exp_data=round(exp)
		if(exp_data==1):
			exp_send='happy'
		elif(exp_data==2):
			exp_send='angry'
		elif(exp_data==3):
			exp_send='sad'
		elif(exp_data==4):
			exp_send='surprise'
		else:
			exp_send='None'

		sheet1.write(ii,0,ttt)
		sheet1.write(ii,1,b)
		sheet1.write(ii,2,x)
		sheet1.write(ii,3,y)
		sheet1.write(ii,4,z) 
		sheet1.write(ii,5,z1)
		sheet1.write(ii,6,exp_send)
		sheet1.write(ii,7,text)

		wb.save('attentiondata.xls')
		ii+=1
