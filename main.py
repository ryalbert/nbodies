import numpy as np
from scipy.integrate import odeint
import matplotlib
from matplotlib import animation, rc
from IPython.display import HTML
matplotlib.rcParams['animation.writer'] = 'ffmpeg'


NBODIES = 2

#The force acting on one body is returned by this
def accelG(pos1,pos2,m1,m2):
    G =1 # 6.67 * 10**(-11)
    d = pos2 - pos1
    accel= G * m1 * m2 /np.linalg.norm(d)**3* d
    
    return(accel)

#Differential equation for two bodies
def dudt2D(U,t):
    pos1 = np.array([U[0],U[1]]) 
    pos2 = np.array([U[2],U[3]])
    accelxy1 = accelG(pos1, pos2, 1, 20)
    accelxy2 = accelG(pos2, pos1, 20, 1)
    #return [U[2],U[3], accelxy[0], accelxy[1]]
    return [U[4],U[5],U[6], U[7], accelxy1[0], accelxy1[1], accelxy2[0], accelxy2[1]]
init1 = [0, 1]
init2 = [0, 0]
initv1 = [5, 0]

initv2 = [0, 0]

#U0 = [initx,inity, initvx, initvy]

U0 = [ init1[0],  init1[1],  init2[0],  init2[1],
      initv1[0], initv1[1], initv2[0], initv2[1] ]

t = np.linspace(0,2,500)

Us = odeint(dudt2D, U0, t)



#Save the data
np.savetxt('outputs/Us.dat', Us)
np.savetxt('outputs/t.dat',t)

def openfile():
	Us = np.loadtxt('outputs/Us.dat')
	t = np.loadtxt('outputs/t.dat') 
	return Us, t
