import numpy as np
from scipy.integrate import odeint
import matplotlib
from matplotlib import animation, rc
from IPython.display import HTML
matplotlib.rcParams['animation.writer'] = 'ffmpeg'

NBODIES = 7


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
        return([1]*nbodies)

def InitialConditions(nbodies = 3, testcase = "Stable"):
    if testcase == "Stable" and nbodies == 3:
        #x1=−x2=0.97000436−0.24308753i,x3=0;~V=  ̇x3=−2  ̇x1=−2  ̇x2=−0.93240737−0.86473146i
        init = [0.97000436, -0.24308753,
               -0.97000436, 0.24308753,
                         0, 0]
        initV = [  0.93240737*0.5, 0.86473146*0.5, 
                0.93240737*0.5, 0.86473146*0.5, 
                -0.93240737, -0.86473146]
    else:
        init  = list(np.random.rand(nbodies*2)*5-2.5 )
        initV = list(np.random.rand(nbodies*2)*5 - 2.5 )
    U0 =np.array( init + initV )
    #U0 = [initx,inity, initvx, initvy]
    return (U0)

#Differential equation for two bodies
def dudt2D(U,t):
	#U = X,Y, ... ,Vx,Vy, ...
    pos = np.array(U[:int(len(U)/2)])
    nbodies = int(len(pos)/2)

    masses = massesf(nbodies = nbodies)
    accelout = []
    posdouble = np.split(pos,nbodies)

    for planet,i  in zip(posdouble,range(nbodies)):
        #could replace with postuplecopy = np.delete(postuple,i) ? index error
        postuplecopy = list(posdouble)
        massescopy = list(masses)
        postuplecopy.pop(i)
        massescopy.pop(i)

        for otherplanet,j in zip(postuplecopy,range(nbodies-1)) :
            accel = accelG(planet, otherplanet, masses[i], massescopy[j])
            accelout.append(np.array(accel))

    summedaccel = [sum(accelout[i:i+nbodies-1]) for i in range(0,len(accelout),nbodies-1)]
    outputaccel = list(np.array(summedaccel).ravel()) 

    Speeds = U[int(len(U)/2):]
    return(np.concatenate([Speeds, outputaccel] ) )


    
#U0 = [initx,inity, initvx, initvy]
U0 = InitialConditions(nbodies=NBODIES)
t = np.linspace(0,300,500)

Us = odeint(dudt2D, U0, t)



#Save the data
np.savetxt('outputs/Us.dat', Us)
np.savetxt('outputs/t.dat',t)