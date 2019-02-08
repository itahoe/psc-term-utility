import matplotlib.pyplot as plt

plt.ion()

class DynamicUpdate():
    #Suppose we know the x range
    min_x = 0
    max_x = 1000
    min_y = 0
    max_y = 25000


    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots( facecolor=('xkcd:gray') )
        self.figure.canvas.set_window_title('PMI Systems')
        plt.title('O2 CONCENTRATION')
        plt.ylabel('PPM')
        self.lines, = self.ax.plot([],[], color=('xkcd:light yellow'), linestyle='-')

        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on( False )
        self.ax.set_xlim( self.min_x, self.max_x )
        self.ax.set_ylim( self.min_y, self.max_y )

        #Other stuff
        #plt.nipy_spectral()
        #plt.prism()
        self.ax.set_facecolor('xkcd:gray')
        self.ax.grid( color='xkcd:light blue', linestyle='dotted', linewidth=1 )

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
        master = modbus_rtu.RtuMaster(serial.Serial(port="COM4", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))

        #for x in np.arange(0,100,1):
        for x in np.arange(0,1000,1):

            master.set_timeout( 2.0 )
            master.set_verbose( False )
            m = master.execute( 13, cst.READ_INPUT_REGISTERS, 1, 4 )
            #print( m[0] )
            xdata.append(x)
            ydata.append( m[0] )

            self.on_running(xdata, ydata)
            time.sleep(1)
        return xdata, ydata

d = DynamicUpdate()
d()
