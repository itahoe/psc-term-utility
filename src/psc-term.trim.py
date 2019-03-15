import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


'''
CONFIG
'''

SER_PORT    = "COM4"
SER_BAUD    = 9600


freqs = np.arange(2, 20, 3)

fig, ax = plt.subplots( facecolor=('xkcd:gray') )
fig.canvas.set_window_title('PSC-TERM-TRIM')

plt.subplots_adjust(bottom=0.2)
t = np.arange(0.0, 1.0, 0.001)
s = np.sin(2*np.pi*freqs[0]*t)
l, = plt.plot(t, s, lw=2)


class Callback(object):
    ind = 0

    def decrement(self, event):
        self.ind += 1
        i = self.ind % len(freqs)
        ydata = np.sin(2*np.pi*freqs[i]*t)
        l.set_ydata(ydata)
        plt.draw()

    def increment(self, event):
        self.ind -= 1
        i = self.ind % len(freqs)
        ydata = np.sin(2*np.pi*freqs[i]*t)
        l.set_ydata(ydata)
        plt.draw()

    def save(self, event):
        self.ind -= 1
        i = self.ind % len(freqs)
        ydata = np.sin(2*np.pi*freqs[i]*t)
        l.set_ydata(ydata)
        plt.draw()

callback = Callback()
ax_dec  = plt.axes( [0.1, 0.05, 0.1, 0.075] )
ax_inc  = plt.axes( [0.2, 0.05, 0.1, 0.075] )
ax_save = plt.axes( [0.8, 0.05, 0.1, 0.075] )

b_dec   = Button( ax_dec, '-' )
b_inc   = Button( ax_inc, '+' )
b_save  = Button( ax_save, 'SAVE' )

b_dec.on_clicked(   callback.decrement  )
b_inc.on_clicked(   callback.increment  )
b_save.on_clicked(  callback.save       )

plt.show()
