import numpy as np
from scipy.integrate import odeint
import matplotlib
from matplotlib import animation, rc
from IPython.display import HTML
matplotlib.rcParams['animation.writer'] = 'ffmpeg'


NBODIES = 3

#The force acting on one body is returned by this
def accelG(pos1,pos2,m1,m2):
    G =1 # 6.67 * 10**(-11)
    d = pos2 - pos1
    accel= G * m1 * m2 /np.linalg.norm(d)**3* d
    
    return(accel)
def massesf():
    return([1,1,1])

#Differential equation for two bodies
def dudt2D(U,t):
	#U = X,Y,... ,Vx,Vy, ...
    pos1 = np.array([U[0],U[1]])
    pos2 = np.array([U[2],U[3]])
    pos = np.array(U[:int(len(U)/2)])
    #print(pos)

    postuple = []
    for i in range(int(len(pos)/2)):
        postuple.append( np.array( [pos[2*i], pos[2*(i)+1] ] ) )
    masses = massesf()
    accelout = []
    for planet,i  in zip(postuple,range(len(postuple))):
        postuplecopy = list(postuple)
        massescopy = list(masses)
        postuplecopy.pop(i)
        massescopy.pop(i)

        for otherplanet,j in zip(postuplecopy,range(len(postuplecopy))) :
             accel = accelG(planet, otherplanet, masses[i], massescopy[j])
             accelout.append(accel[0])
             accelout.append(accel[1])

    acceleration_vectors = np.split(np.array(accelout),3)
    artifsplit = [np.split(k,2) for k in acceleration_vectors]
    summedaccel = [sum(k) for k in artifsplit]
    outputaccel = list(np.array(summedaccel).ravel()) 

    Speeds = U[int(len(U)/2):]
    return(np.concatenate([Speeds, outputaccel] ) )
init1 = [0.97000436, -0.24308753]
init2 = [-0.97000436, 0.24308753]
init3 = [0, 0]
init = [init1[0], init1[1], init2[0], init2[1], init3[0], init3[1] ]
initv3 = [-0.93240737, -0.86473146]
initv1 = [0.93240737*0.5, 0.86473146*0.5]
initv2 = [0.93240737*0.5, 0.86473146*0.5]



initV = [initv1[0], initv1[1], initv2[0], initv2[1], initv3[0], initv3[1] ]
#U0 = [initx,inity, initvx, initvy]
U0 =np.array( init + initV )

t = np.linspace(0,2,15000)

Us = odeint(dudt2D, U0, t)



#Save the data
np.savetxt('outputs/Us.dat', Us)
np.savetxt('outputs/t.dat',t)

def openfile():
	Us = np.loadtxt('outputs/Us.dat')
	t = np.loadtxt('outputs/t.dat') 
	return Us, t
