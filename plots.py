import numpy as np
import matplotlib.pyplot as plt
import main

Us, t = main.openfile()
nbodies = int(Us.shape[1]/4)


##Plots 
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot(Us[:,0] ,Us[:,1],t, label='parametric curve 1')
# ax.plot(Us[:,2] ,Us[:,3],t, label= 'parametric curve 2')
# ax.scatter(Us[0][0], Us[0][1],0,color="darkblue",marker="o",s=100)
# ax.scatter(0,0,0,color="red",marker="o",s=100, label="Point central")
# ax.legend()
# plt.show()

plt.figure()
for i in range(nbodies,2*nbodies):
    plt.plot(t,Us[:,2*i])
# plt.plot(Us[:,0] ,Us[:,1],color="darkblue");
# plt.plot(Us[:,2] ,Us[:,3], color="red");
# ax.scatter(Us[0][0], Us[0][1],0,color="darkblue",marker="o",s=100)
# plt.scatter(0,0,color="red",marker="o",s=100,)
# plt.xlim(-0.1, 3)
# plt.ylim(-0.1, 3)
plt.show()

