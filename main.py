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


def accelG(pos1, pos2, m1, m2):
    # Returns the acceleration acting on one body
    G = 1  # 6.67 * 10**(-11)
    d = pos2 - pos1
    Acceleration = G * m1 * m2 / np.linalg.norm(d) ** 3 * d
    return(Acceleration)

def get_Masses(nbodies=3, testcase="Stable"):
    # Returns all the system masses
    if testcase == "Stable" and nbodies == 3:
        return([1, 1, 1])
    else:
        return([1]*nbodies)


def InitialConditions(nbodies = 3, testcase = "Stable"):
    if testcase == "Stable" and nbodies == 3:
        init = [0.97000436, -0.24308753,
               -0.97000436,  0.24308753,
                         0,  0          ]
        initV = [0.93240737*0.5, 0.86473146*0.5,
                 0.93240737*0.5, 0.86473146*0.5, 
                -0.93240737    ,-0.86473146     ]
    else:
        seed = 11
        init  = list( np.random.RandomState(seed).rand(nbodies*2)  * 5 - 2.5 )
        initV = list( np.random.RandomState(seed+1).rand(nbodies*2)* 5 - 2.5 )
    U0 =np.array( init + initV )
    # U0 = [initx,inity, initvx, initvy]
    return (U0)


def dudt2D(U,t):
    # Differential equation for two bodies
    # U = X,Y, ... ,Vx,Vy, ...
    Position = np.array(U[:int(len(U)/2)])
    NBodies = int(len(Position)/2)

    Masses = get_Masses(nbodies=NBodies)
    Accel_Out = []
    Position_Pairs = np.split(Position, NBodies)

    for Planet, i  in zip(Position_Pairs, range(NBodies)):
        # could replace with postuplecopy = np.delete(postuple,i) ? index error
        postuplecopy = list(np.delete(Position_Pairs)
        massescopy = list(Masses)
        postuplecopy.pop(i)
        massescopy.pop(i)

        for OtherPlanet, j in zip(postuplecopy, range(NBodies-1)) :
            # could divide execution time by two here by computing only once
            # each acceleration
            accel = accelG(Planet, OtherPlanet, Masses[i], massescopy[j])
            Accel_Out.append(np.array(accel))

    summedaccel = [sum(Accel_Out[i:i+NBodies-1]) 
                    for i in range(0,len(Accel_Out),NBodies-1)]
    outputaccel = list(np.array(summedaccel).ravel() )

    Speeds = U[int(len(U)/2):]
    return(np.concatenate([Speeds, outputaccel]) )

 
#U0 = [initx,inity, initvx, initvy]
U0 = InitialConditions(nbodies=NBODIES)
t = np.linspace(0,10,500)

Us = odeint(dudt2D, U0, t)



#Save the data
np.savetxt('outputs/Us.dat', Us)
np.savetxt('outputs/t.dat',t)