import numpy as np
from scipy.integrate import odeint
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
import main 
matplotlib.rcParams['animation.writer'] = 'ffmpeg'

Us, t = main.openfile()
nbodies = int(Us.shape[1]/4)

import seaborn as sns
#https://jckantor.github.io/CBE30338/A.03-Animation-in-Jupyter-Notebooks.html
# create a figure and axes
fig = plt.figure(figsize=(12,5))
ax2 = plt.subplot(1,1,1)

# set up the subplots as needed
bound=np.max(np.abs(Us[:,:nbodies*2])) * 1.10
ax2.set_xlim(-bound,bound)
ax2.set_ylim(-bound,bound)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('Position in time')

# create objects that will change in the animation. These are
# initially empty, and will be given new values for each frame
# in the animation.
#txt_title = ax1.set_title('')


yi = []
linei = []
pti = []
for i in range(nbodies):
    color=next(ax2._get_lines.prop_cycler)['color']
    linei.append(ax2.plot([],[],    color = color, lw=2) )
    yi.append(Us[:,2*i])
    yi.append(Us[:,2*i+1])
    pti.append(ax2.plot(  [],[],'.',color = color,ms=20))
#y1 = Us[:,0]


# animation function. This is called sequentially
def drawframe(n):
    n = 1 if n < 2 else n

    print("Animated " + str(n) +"/"+str(len(t))) if n%100 == 0 else 0
    #line1.set_data(t, y1)
    #line2.set_data(t, y2)
    trail_size = 50
    a = n-trail_size if n > trail_size+1 else 0 
    for i in range(nbodies):
        linei[i][0].set_data(yi[2*i][a:n], yi[2*i+1][a:n])
        pti[i][0].set_data(yi[2*i][n],yi[2*i+1][n])
    #line3.set_data(y1[a:n],y2[a:n])    
    # pt1.set_data(y1[n],y2[n])

   # txt_title.set_text('Frame = {0:4d}'.format(n))
    return tuple(linei[i][0] for i in range(nbodies))


from matplotlib import animation

# blit=True re-draws only the parts that have changed.
anim = animation.FuncAnimation(fig, drawframe, frames=len(t), interval=0.1, blit=True)
#interval, time between frames, frames : number of call to drawframe

#from IPython.display import HTML
#HTML(anim.to_html5_video())
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=100, metadata=dict(artist='Me'), bitrate=1500)
anim.save('animation.mp4', writer=writer)





