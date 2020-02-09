import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import matplotlib.animation as animation
import xlwt
from xlwt import Workbook

# dist_norm = np.random.normal(loc=0, scale=1, size=1000)
# dist_tdis = np.random.standard_t(df=29, size=1000)
# dist_fdis = np.random.f(dfnum=59, dfden=28, size=1000)
# dist_chsq = np.random.chisquare(df=2, size=1000)

def plotgraphs():

	df = pd.read_excel('attentiondata.xls', sheet_name=0) # can also index sheet by name or fetch all sheets
	# print(df)
	time = df['Time'].tolist()
	blink = df['Blink count'].tolist()
	pixel = df['Pixel Difference'].tolist()
	emotion = df['Emotion'].tolist()
	dist = df['Distraction'].tolist()
	noise = df['Noise level'].tolist()
	att = df['Attention level'].tolist()


	blink2 = list(blink)
	# for i in range(1,len(blink)):
	#      blink2[i] -= blink[i-1]


	# Plot figure with subplots of different sizes
	fig = plt.figure(1)
	# set up subplot grid
	gridspec.GridSpec(3,3)

	# large subplot
	plt.subplot2grid((2,3), (0,0))
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)
	plt.plot(time,blink2)
	plt.title('Blink rate')
	plt.xlabel('Time (s)')
	plt.ylabel('Blinks')

	# small subplot 1
	plt.subplot2grid((2,3), (0,1))
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)
	plt.plot(time,pixel)
	plt.title('Position change')
	plt.xlabel('Time (s)')
	plt.ylabel('Pixel Difference')

	# small subplot 2
	plt.subplot2grid((2,3), (0,2))
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)
	plt.plot(time,emotion)
	plt.title('Emotion')
	plt.xlabel('Time (s)')
	plt.ylabel('Emotion detection')

	# small subplot 3
	plt.subplot2grid((2,3), (1,0))
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)
	plt.plot(time,dist)
	plt.title('Distraction level')
	plt.xlabel('Time (s)')
	plt.ylabel('Distraction')	

	# small subplot 3
	plt.subplot2grid((2,3), (1,1))
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)
	plt.plot(time,noise)
	plt.title('Noise level')
	plt.xlabel('Time (s)')
	plt.ylabel('Noise level')

	# wb = Workbook() 
	# sheet1 = wb.add_sheet('Sheet 1')

	# att= []
	# for i in range(len(time)):
	# 	att.append((1/blink2[i])*0.2 + (pixel[i])*0.2 + (emotion[i])*0.2 + (dist[i])*0.2 + (1/noise[i])*0.2)
	# 	j=i+1
	# 	sheet1.write(j,6,att[i])

	# small subplot 3
	plt.subplot2grid((2,3), (1,2))
	plt.locator_params(axis='x', nbins=5)
	plt.locator_params(axis='y', nbins=5)
	plt.plot(time,att)
	plt.title('Attention level')
	plt.xlabel('Time (s)')
	plt.ylabel('Attention lenvel')

	# fit subplots and save fig
	fig.tight_layout()
	fig.set_size_inches(w=15,h=7)
	fig_name = 'plot.png'
	fig.savefig(fig_name)

	# wb.save('attentiondata.xls')


		

	# plt.show()


if __name__ == '__main__' :
	plotgraphs()