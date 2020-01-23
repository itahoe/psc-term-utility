import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time
import csv
import ctypes


#
# CONFIGURATION
#
SER_PORT    = "COM4"
SER_BAUD    = 19200
MDBS_ADDR   = 128


#
# START EXECUTION
#
flog_name   = time.strftime("%Y%m%d.%H%M%S.csv")
flog        = open( flog_name, 'w', newline='' )
writer      = csv.writer( flog )
fieldnames  = [ 'datestamp', 'timestamp', 'concentration', 'temperature' ]
writer      = csv.DictWriter( flog, fieldnames=fieldnames )

master      = modbus_rtu.RtuMaster( serial.Serial(port=SER_PORT, baudrate=SER_BAUD, bytesize=8, parity='N', stopbits=1, xonxoff=0) )
master.set_timeout( 2.0 )
master.set_verbose( False )


while True:
    try:
        time.sleep(1)

        #connect to the modbus slave
        m               = master.execute( MDBS_ADDR, cst.READ_HOLDING_REGISTERS, 0, 32 )

        #convert array to variables
        #concentration   = (m[17] << 16) | m[16]
        concentration   = ctypes.c_int32( (m[17] << 16) | m[16] ).value
        temperature     = ctypes.c_int32( m[18] ).value
        instability     = m[19]
        datestamp       = time.strftime( '%d/%m/%Y' )
        timestamp       = time.strftime( '%H:%M:%S' )

        print( "%8i PPM @ %2d\xB0C\t%4d" % (concentration, temperature, instability) )

        writer.writerow( {  'datestamp':      datestamp,
                            'timestamp':      timestamp,
                            'concentration':  concentration,
                            'temperature':    temperature } )

    except KeyboardInterrupt:
        raise SystemExit(0)
