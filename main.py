import sys
import glob
import serial

from light_controller import LightManager


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class LightControllerSearcher():
    def __init__(self):
        self.ports = serial.tools.list_ports.comports()
        self.baudrate_list = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]

        self.port, self.baudrate = self.find_controller()

    def find_controller(self):
        for port, _, _ in self.ports:
            print(port)
            light_manager = LightManager(port=port, baudrate=self.baudrate_list[0], list_channels=[1])
            light_manager.timeout = 0

            for baudrate in self.baudrate_list:

                print(light_manager.baudrate)
                print(light_manager.readable())

                light_manager.switch_on([1])
                print(light_manager.read().decode('windows-1252'))
                if light_manager.read().decode('windows-1252') == "$":
                    return port, baudrate

                light_manager.baudrate = baudrate

            light_manager.close()
        return None, None


if __name__ == '__main__':
    import serial.tools.list_ports

    lc = LightControllerSearcher()
    print(lc.port, lc.baudrate)



    # lm = LightManager(port='COM4', baudrate=9600, list_channels=[1, 2, 3])
    # lm.switch_on([0, 255, 0])

