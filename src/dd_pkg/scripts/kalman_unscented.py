#!/usr/bin/env python3
import rospy
import numpy as np
import matplotlib.pyplot as plt
import math
from std_msgs.msg import Float64MultiArray
#import scipy.linealg
from scipy.linalg import sqrtm

global axr, ayr, tt_imu, tt_gps, pub, yaw, xkh, ykh, vxkh, vykh, x, y, P, tt, w, yawkh
tt_imu=[]
tt_gps=[]
tt=[]
yaw=[]
axr=[]
ayr=[]
xkh=[]
ykh=[]
vxkh=[]
vykh=[]
w=[]
yawkh=[]
xkh.append(0)
vxkh.append(0)
ykh.append(0)
vykh.append(0)
yawkh.append(0)
x=[]
y=[]
P=np.array([
[1,0,0,0,0],
[0,1,0,0,0],
[0,0,1,0,0],
[0,0,0,1,0],
[0,0,0,0,0.1]
])

def funzionef(x,u,Tc):
	#u=[w,ax,ay]
	w=u[0]
	axr=u[1]
	ayr=u[2]	
	vxkh=x[1]+Tc*axr
	vykh=x[3]+Tc*ayr
	v=np.sqrt(pow(vxkh,2)+pow(vykh,2))
	if w<0.0005:
		xkh=x[0]+v*Tc*np.cos(x[4])
		ykh=x[2]+v*Tc*np.sin(x[4])
	else :
		xkh=x[0]+v*(np.sin(x[4]+w*Tc)-np.sin(x[4]))/w
		ykh=x[2]+v*(np.cos(x[4]+w*Tc)-np.cos(x[4]))/w
	yawkh=x[4]+w*Tc
	#print("yaw ",yawkh)
	return np.array([xkh,vxkh,ykh,vykh,yawkh])
	

def read_callback(msg):
	global yaw, axr, ayr, pub, xkh, ykh, vxkh, vykh, P, tt_imu, tt, w, yawkh
	temp=msg.data 
	axr.append(temp[0])
	ayr.append(temp[1])
	tt_imu.append(temp[3])
	tt.append(tt_imu[-1])
	w.append(temp[4])
	print(tt_imu[-1])
	V1=np.array([
	[1,0,0,0,0],
	[0,1,0,0,0],
	[0,0,1,0,0],
	[0,0,0,1,0],
	[0,0,0,0,0.1],
	])
	n=5
	#Xi={}
	if len(tt_imu)>1:
		XK=[xkh[-1],vxkh[-1],ykh[-1],vykh[-1],yawkh[-1]]
		SP=[]
		for i in range(2*n):
			SP.append(XK)
		Q=n*P
		Xi=sqrtm(Q)
		Xi=np.transpose(Xi)
		print("inizio")
		for i in range(n):
			a=Xi[i-1]
			if math.isnan(a[0]) or math.isnan(a[1]) or math.isnan(a[2]) or math.isnan(a[3]) or math.isnan(a[4]):
				print("oddio")
			SP[i]=SP[i]#+a
			SP[i+n]=SP[n+i]#-a		
			#print("size SP[i] ",np.shape(SP[i]))
			#print("punto ", i)
		#print("sigma points ", SP)
		Tc=tt_imu[-1]-tt_imu[-2]
		SPC=SP		
		u=[w[-1],axr[-1],ayr[-1]]
		temp3=[0,0,0,0,0]
		print("temp3 prima ",np.shape(temp3))
		for i in range(len(SPC)):		
			#temp3=funzionef([xkh[-1],vxkh[-1],ykh[-1],vykh[-1],yawkh[-1]],[w[-1],axr[-1],ayr[-1]],Tc)
			SPC[i]=funzionef(SPC[i],u,Tc)
			print("Dinamica ",np.shape(SPC[i]))
			#SPC[i]=SPC[i]
			for j in range(len(temp3)):
				temp3[j]=temp3[j]+SPC[i][j]
			print("temp3 dentro ",np.shape(temp3))
		for j in range(len(temp3)):
			temp3[j]=temp3[j]*(1/(2*n))
		print("temp3 dopo ",np.shape(temp3))
		#print("media ",temp3)
		xkh.append(temp3[0])
		vxkh.append(temp3[1])
		ykh.append(temp3[2])
		vykh.append(temp3[3])
		yawkh.append(temp3[4])
		print("yaw ",temp3[4])
		
	else :
		Tc=0
		xkh.append(0)
		vxkh.append(0)
		ykh.append(0)
		vykh.append(0)
		yawkh.append(0)
	temp5=0*P
	for i in range (2*n):
		temp4=SPC[i]-[xkh[-1],vxkh[-1],ykh[-1],vykh[-1],yawkh[-1]]	
		#print("temp4 ", temp4)
		temp6=0*P
		for j in range(n):
			for k in range(n):
				temp6[j][k]=temp4[j]*temp4[k]
		#print("temp6 ", temp6)
		temp5=temp5+temp6
	P=temp5*(1/(2*n))+V1
	UK_message=Float64MultiArray()
	UK_message.data=[xkh[-1],ykh[-1],tt[-1]]
	pub.publish(UK_message)

	
def read_callback2(msg):
	global x,y, P, xkh, ykh, vxkh, vykh, tt_gps, tt
	temp=msg.data 
	x.append(temp[0])
	y.append(temp[1])
	tt_gps.append(temp[2])
	tt.append(tt_gps[-1])
	#print(tt[-1])
	V2=[
	[1,0],
	[0,1]
	]
	H=[
	[1, 0, 0, 0, 0],
	[0, 0, 1, 0, 0]
	]
	cov=np.dot(np.dot(H,P),np.transpose(H))+V2
	print("cov")
	print(cov)
	K=np.dot(np.dot(P,np.transpose(H)),np.linalg.inv(cov))
	print("K")
	print(K)
	e=[0,0]
	e[0]=-xkh[-1]+temp[0]
	e[1]=-ykh[-1]+temp[1]
	print("e")
	print(e)
	temp2=np.dot(K,e)
	print("Ke")
	print(temp2)
	xkh.append(xkh[-1]+temp2[0])
	vxkh.append(vxkh[-1]+temp2[1])
	ykh.append(ykh[-1]+temp2[2])
	vykh.append(vykh[-1]+temp2[3])
	yawkh.append(yawkh[-1]+temp2[4])
	P=P-np.dot(np.dot(K,H),P)
	print("P")
	print(P)
	EK_message=Float64MultiArray()
	EK_message.data=[xkh[-1],ykh[-1],tt[-1]]
	pub.publish(EK_message)


	
rospy.init_node('kalman_uns')
pub = rospy.Publisher('data_ukf', Float64MultiArray)
sub = rospy.Subscriber('data_imu', Float64MultiArray, read_callback)
sub2= rospy.Subscriber('data_gps', Float64MultiArray, read_callback2)
rospy.spin()
file_uno = open("C:\\file_imu.txt", "w")
contenuto=str(axr)+str(ayr)+str(tt_imu)
file_uno.write(contenuto)
file_uno.close() 

file_due = open("C:\\file_gps.txt", "w")
contenuto=str(x)+str(y)+str(tt_gps)
file_due.write(contenuto)
file_due.close() 

plt.figure()
plt.plot(xkh,ykh)
plt.ylabel('Kalman')
plt.show()

