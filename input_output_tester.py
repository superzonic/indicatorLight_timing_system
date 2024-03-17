import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()


serialInst.baudrate = 9600
serialInst.port = "COM6"
serialInst.open()

def arduino_read():
    while True:
     if serialInst.in_waiting:
      packet = serialInst.readline()
      return str(packet.decode('utf').rstrip())
