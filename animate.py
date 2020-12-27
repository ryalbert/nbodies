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
#ax1 = plt.subplot(1,2,1)   
ax2 = plt.subplot(1,2,2)

# set up the subplots as needed
#ax1.set_xlim(( 0, 2))            
#ax1.set_ylim((-2, 2))
#ax1.set_xlabel('Time')
#ax1.set_ylabel('Magnitude')

ax2.set_xlim((-2.5,2.5))
ax2.set_ylim((-2.5,2.5))
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('Position in time')

# create objects that will change in the animation. These are
# initially empty, and will be given new values for each frame
# in the animation.
#txt_title = ax1.set_title('')
#line1, = ax1.plot([], [], 'b', lw=2)     # ax.plot returns a list of 2D line objects
#line2, = ax1.plot([], [], 'r', lw=2)
pt1, = ax2.plot([], [], 'g.', ms=20)
pt2, = ax2.plot([], [], 'b.', ms=20)
pt3, = ax2.plot([], [], 'r.', ms=20)
line3, = ax2.plot([], [], 'g', lw=2)
line4, = ax2.plot([], [], 'b', lw=2)
line5, = ax2.plot([], [], 'r', lw=2)

y1 = Us[:,0]
y2 = Us[:,1]
y3 = Us[:,2]
y4 = Us[:,3]
y5 = Us[:,4]
y6 = Us[:,5]

# animation function. This is called sequentially
def drawframe(n):
    n = 1 if n < 2 else n
    #line1.set_data(t, y1)
    #line2.set_data(t, y2)
    a = n-500 if n > 501 else 0 
    line3.set_data(y1[a:n],y2[a:n])
    line4.set_data(y3[a:n],y4[a:n])
    line5.set_data(y5[a:n],y6[a:n])
	
    pt1.set_data(y1[n],y2[n])
    pt2.set_data(y3[n],y4[n])
    pt3.set_data(y5[n],y6[n])
   # txt_title.set_text('Frame = {0:4d}'.format(n))
    return (line3,line4,line5)


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





