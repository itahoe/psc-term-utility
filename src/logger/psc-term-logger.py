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
#MDBS_ADDR   = 128
MDBS_ADDR   = 13


#
# START EXECUTION
#
flog_name   = time.strftime("%Y%m%d.%H%M%S.csv")
flog        = open( flog_name, 'w', newline='' )
writer      = csv.writer( flog )
fieldnames  = [ 'datestamp', 'timestamp', 't_cels', 'ppm', 'raw' ]
writer      = csv.DictWriter( flog, fieldnames=fieldnames )

master      = modbus_rtu.RtuMaster( serial.Serial(port=SER_PORT, baudrate=SER_BAUD, bytesize=8, parity='N', stopbits=1, xonxoff=0) )
master.set_timeout( 2.0 )
master.set_verbose( False )


while True:
    try:
        time.sleep(1)

        #connect to the modbus slave
        m               = master.execute( MDBS_ADDR, cst.READ_HOLDING_REGISTERS, 0, 64 )

        #convert array to variables
        #concentration   = (m[17] << 16) | m[16]

        ppm             = ctypes.c_int32( (m[33] << 16) | m[32] ).value
        raw             = ctypes.c_int32( (m[35] << 16) | m[34] ).value
        instability     = m[36]
        t_cels          = ctypes.c_int32( m[38] ).value
        datestamp       = time.strftime( '%d/%m/%Y' )
        timestamp       = time.strftime( '%H:%M:%S' )

        print( "%8i PPM @ %2d\xB0C\t%4d\t%8i" % (ppm, t_cels, instability, raw) )

        writer.writerow( {  'datestamp':    datestamp,
                            'timestamp':    timestamp,
                            't_cels':       t_cels,
                            'ppm':          ppm,
                            'raw':          raw } )

    except KeyboardInterrupt:
        raise SystemExit(0)
