import matplotlib.pyplot as plt
import numpy as np


SER_PORT    = "COM4"
SER_BAUD    = 9600


plt.ion()
#plt.ioff()



class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('X2=%1.2f, y=%1.2f' % (x, y))
        plt.draw()

class Display():
    #Suppose we know the x range
    min_x = 0
    max_x = 1000
    min_y = 0
    max_y = 25000


    #def __init__(self, ax):
    #def __init__(self):
        #self.ax = ax
        # text location in axes coords
        #self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    '''
    def __init__(self, ax):
        self.ax = ax
        #self.lx = ax.axhline(color='k')  # the horiz line
        #self.ly = ax.axvline(color='k')  # the vert line
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
    '''

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots( facecolor=('xkcd:gray') )
        self.figure.canvas.set_window_title('PMI Systems')
        #plt.title( 'O2 CONCENTRATION' )
        plt.ylabel('PPM')
        self.lines, = self.ax.plot([],[], color=('xkcd:light green'), linestyle='-')

        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on( False )
        self.ax.set_xlim( self.min_x, self.max_x )
        self.ax.set_ylim( self.min_y, self.max_y )

        #Other stuff
        #plt.nipy_spectral()
        #plt.prism()
        self.ax.set_facecolor( 'xkcd:gray' )
        self.ax.grid( color='xkcd:light blue', linestyle='dotted', linewidth=1 )
        #self.txt = self.ax.text(0.7, 0.9, '', transform=self.ax.transAxes)

        self.txt = self.ax.text(    0.3, 0.7,
                                    '',
                                    color       = ( 'xkcd:yellow'),
                                    #fontsize    = ( 'xx-large'),
                                    fontsize    = ( 40 ),
                                    weight      = ( 'bold' ),
                                    ha          = ( 'left' ),
                                    transform   = self.ax.transAxes )

    def on_running(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata( xdata )
        self.lines.set_ydata( ydata )

        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()

        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Usage
    def __call__(self):
        import numpy as np
        import time
        import serial
        import modbus_tk.defines as cst
        import modbus_tk.modbus_rtu as modbus_rtu
        self.on_launch()
        xdata = []
        ydata = []
        master = modbus_rtu.RtuMaster(serial.Serial(port=SER_PORT, baudrate=SER_BAUD, bytesize=8, parity='N', stopbits=1, xonxoff=0))

        for x in np.arange(0,1000,1):

            master.set_timeout( 2.0 )
            master.set_verbose( False )
            #y = master.execute( 13, cst.READ_INPUT_REGISTERS, 1, 4 )
            y = master.execute( 13, cst.READ_HOLDING_REGISTERS, 1, 32 )
            #print( y[0] )
            #x = m[0]
            #t = 25.5
            xdata.append(x)
            ydata.append( y[16] )
            self.on_running(xdata, ydata)
            #plt.text( 900, 20000, "O2: %m[0]\nt: ", size=18, va="baseline", ha="right", multialignment="left", bbox=dict(fc="none"))
            #plt.text( 900, 20000, 'O2: %d\nt: ' %m[0], size=18, va="baseline", ha="right", multialignment="left", bbox=dict(fc="none"))
            #plt.title( "O2: %d PPM\nt: 25 C" %c[0] %t )
            #plt.title( "O2: %d PPM\nt: %d C" % (y[0], y[0]) )

            self.txt.set_text( '%5d PPM\n   %5d C' % (y[16], y[17]) )
            #plt.draw()

            time.sleep(1)
        return xdata, ydata


#fig, ax = plt.subplots()
#cursor = Cursor(ax)

d = Display()
d()
