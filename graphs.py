import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def blink_graph():
	ani = animation.FuncAnimation(fig, animate, interval=1000)
	plt.show()

def animate(i):
	# pullData = open("sampleText.txt","r").read()
	# dataArray = pullData.split('\n')
	# xar = []
	# yar = []
	# for eachLine in dataArray:
	#     if len(eachLine)>1:
	#         x,y = eachLine.split(',')
	#         xar.append(int(x))
	#         yar.append(int(y))
	df = pd.read_excel('attentiondata.xls', sheet_name=0) # can also index sheet by name or fetch all sheets
	# print(df)
	time = df['Time'].tolist()
	blink = df['Blink count'].tolist()
	blink2 = list(blink)
	# for i in range(1,len(blink)):
	#     blink2[i] -= blink[i-1]
	ax1.clear()
	ax1.plot(time,blink2)
	plt.title('Blink rate')
	plt.xlabel('Time (s)')
	plt.ylabel('Blinks')


blink_graph()