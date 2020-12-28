import numpy as np
from scipy.integrate import odeint
import matplotlib
from matplotlib import animation, rc
from IPython.display import HTML
matplotlib.rcParams['animation.writer'] = 'ffmpeg'

NBODIES = 3


def openfile():
	Us = np.loadtxt('outputs/Us.dat')
	t = np.loadtxt('outputs/t.dat') 
	return Us, t


#The acceleration acting on one body is returned by this function
def accelG(pos1,pos2,m1,m2):
    G =1 # 6.67 * 10**(-11)
    d = pos2 - pos1
    Acceleration= G * m1 * m2 /np.linalg.norm(d)**3* d
    return(Acceleration)

#Returns all the system masses
def massesf(nbodies=3, testcase="Stable"):
    if testcase == "Stable" and nbodies == 3:
        return([1,1,1])
    else: 
        return(list(np.random.rand(nbodies) ) )

def InitialConditions(nbodies = 3, testcase = "Stable"):
    if testcase == "Stable" and nbodies == 3:
        #x1=−x2=0.97000436−0.24308753i,x3=0;~V=  ̇x3=−2  ̇x1=−2  ̇x2=−0.93240737−0.86473146i
        init = [0.97000436, -0.24308753,
               -0.97000436, 0.24308753,
                         0, 0] 
        initV = [  0.93240737*0.5, 0.86473146*0.5, 
                0.93240737*0.5, 0.86473146*0.5, 
                -0.93240737, -0.86473146,]
    else:
        init  = list(np.random.rand(nbodies*2)*5 )
        initV = list(np.random.rand(nbodies*2)*5 )
    U0 =np.array( init + initV )
    #U0 = [initx,inity, initvx, initvy]
    return (U0)

#Differential equation for two bodies
def dudt2D(U,t):
	#U = X,Y, ... ,Vx,Vy, ...
    pos = np.array(U[:int(len(U)/2)])
    nbodies = int(len(pos)/2)

    masses = massesf()
    accelout = []
    postuple = np.split(pos,len(pos)/2)

    for planet,i  in zip(postuple,range(len(postuple))):
        #could replace with postuplecopy = np.delete(postuple,i) ? index error
        postuplecopy = list(postuple)
        massescopy = list(masses)
        postuplecopy.pop(i)
        massescopy.pop(i)

        for otherplanet,j in zip(postuplecopy,range(len(postuplecopy))) :
            accel = accelG(planet, otherplanet, masses[i], massescopy[j])
            accelout.append(accel[0])
            accelout.append(accel[1])

    acceleration_vectors = np.split(np.array(accelout),nbodies)
    artifsplit = [np.split(k,2) for k in acceleration_vectors]
    summedaccel = [sum(k) for k in artifsplit]
    outputaccel = list(np.array(summedaccel).ravel()) 

    Speeds = U[int(len(U)/2):]
    return(np.concatenate([Speeds, outputaccel] ) )


    
#U0 = [initx,inity, initvx, initvy]
U0 = InitialConditions()
t = np.linspace(0,10,1000)

Us = odeint(dudt2D, U0, t)



#Save the data
np.savetxt('outputs/Us.dat', Us)
np.savetxt('outputs/t.dat',t)