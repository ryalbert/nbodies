import numpy as np
from scipy.integrate import odeint
import matplotlib 


NBODIES = 3
TESTCASE = "Default"


def openfile():
    Us = np.loadtxt('outputs/Us.dat')
    t = np.loadtxt('outputs/t.dat')
    return Us, t


def accelG(d1, d2, m1, m2):
    # Returns the acceleration acting on one body
    G = 1  # 6.67 * 10**(-11)
    d = d2 - d1
    Acceleration = G * m1 * m2 / np.linalg.norm(d) ** 3 * d
    return(np.array(Acceleration))


def get_Masses(nbodies=3, testcase="Default"):
    # Returns all the system masses
    if testcase == "Default" and nbodies == 3:
        return([1, 1, 1])
    else:
        return([1]*nbodies)


def InitialConditions(nbodies=3, testcase="Default"):
    if testcase == "Default" and nbodies == 3:  # from https://arxiv.org/abs/math/0011268
        initU = [0.97000436, -0.24308753,
               -0.97000436,  0.24308753,
                         0,  0          ]
        initV = [0.93240737*0.5, 0.86473146*0.5,
                 0.93240737*0.5, 0.86473146*0.5, 
                -0.93240737    ,-0.86473146     ]
    else:
        seed = 100 * np.random.randint(10000)
        print("Seed chosen, in case ya like the setup :" + str(seed))
        initU  = list( np.random.RandomState(seed).rand(nbodies*2)  * 5 - 2.5 )
        initV = list( np.random.RandomState(seed+1).rand(nbodies*2)* 5 - 2.5 )
    U0 =np.array( initU + initV )
    # U0 = [initx,inity, initvx, initvy]
    return (U0)


def dudt2D(U,t):
    # Differential equation for two bodies
    # U = X,Y, ... ,Vx,Vy, ...
    Position = np.array(U[:int(len(U)/2)])
    NBodies = int(len(Position)/2)

    Masses = get_Masses(nbodies=NBodies, testcase=TESTCASE)
    RawAccel = []
    PositionPair = np.split(Position, NBodies)

    for Body, i  in zip(PositionPair, range(NBodies)):
        # could replace with postuplecopy = np.delete(postuple,i) to shorten ?
        PositionPair_copy = list(PositionPair)
        Masses_copy = list(Masses)

        PositionPair_copy.pop(i)
        Masses_copy.pop(i)
        
        for OtherBody, j in zip(PositionPair_copy, range(NBodies-1)) :
            # could divide execution time by two here by computing only once
            # each acceleration
            RawAccel.append(
                accelG(Body, OtherBody, Masses[i], Masses_copy[j])
                )

    SummedAccel = [sum(RawAccel[i:i+NBodies-1]) 
                    for i in range(0,len(RawAccel),NBodies-1)]
    Accels = list(np.array(SummedAccel).ravel())

    Speeds = U[int(len(U)/2):]
    return(np.concatenate([Speeds, Accels]))

 
#U0 = [initx,inity, initvx, initvy]
U0 = InitialConditions(nbodies=NBODIES,testcase=TESTCASE)
t = np.linspace(0,10,500)

Us = odeint(dudt2D, U0, t)



#Save the data
np.savetxt('outputs/Us.dat', Us)
np.savetxt('outputs/t.dat',t)