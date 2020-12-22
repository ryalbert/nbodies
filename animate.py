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

import seaborn as sns
#https://jckantor.github.io/CBE30338/A.03-Animation-in-Jupyter-Notebooks.html
# create a figure and axes
fig = plt.figure(figsize=(12,5))
ax1 = plt.subplot(1,2,1)   
ax2 = plt.subplot(1,2,2)

# set up the subplots as needed
ax1.set_xlim(( 0, 2))            
ax1.set_ylim((-2, 2))
ax1.set_xlabel('Time')
ax1.set_ylabel('Magnitude')

ax2.set_xlim((-2,2))
ax2.set_ylim((-2,2))
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('Position in time')

# create objects that will change in the animation. These are
# initially empty, and will be given new values for each frame
# in the animation.
txt_title = ax1.set_title('')
line1, = ax1.plot([], [], 'b', lw=2)     # ax.plot returns a list of 2D line objects
line2, = ax1.plot([], [], 'r', lw=2)
pt1, = ax2.plot([], [], 'g.', ms=20)
pt2, = ax2.plot([], [], 'b.', ms=20)
line3, = ax2.plot([], [], 'y', lw=2)


# animation function. This is called sequentially
def drawframe(n):
    n = 1 if n < 2 else n
    y1 = Us[:,0]
    y2 = Us[:,1]
    line1.set_data(t, y1)
    line2.set_data(t, y2)
    a = n-50 if n > 51 else 0 
    line3.set_data(y1[a:n],y2[a:n])
    #line3.set_data(y1[0:n],y2[0:n])
    pt1.set_data(y1[n],y2[n])
    pt2.set_data(0,0)
   # txt_title.set_text('Frame = {0:4d}'.format(n))
    return (line1,line2)


from matplotlib import animation

# blit=True re-draws only the parts that have changed.
anim = animation.FuncAnimation(fig, drawframe, frames=200, interval=150, blit=True)


#from IPython.display import HTML
#HTML(anim.to_html5_video())
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1500)
anim.save('anim3.mp4', writer=writer)





