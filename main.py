import time
import typing

from light_controller import LightManager
from serial.tools import list_ports


class LightControllerSearcher:
    def __init__(self, baudrate_list: typing.Union[None, typing.List[int]] = None):
        """
        The aim of this class is to detect right COM PORT and baud rate to communicate with light controller.
        :param baudrate_list: list of communication speeds tested to communicate with light controller.
                              if this parameter is None -> try all standard baud rates.
        """
        # detect available com ports
        self.ports = list_ports.comports()

        self.baudrate_list = baudrate_list
        if self.baudrate_list is None:
            self.baudrate_list = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200]

        self.port, self.baudrate = self.find_controller()

    def find_controller(self) -> [typing.Union[str, None], typing.Union[int, None]]:
        """
        This function iterates over all COM ports and all baud rates. During these iterations, it tries to communicate
        with the light controller thanks to Serial communication. When the communication is established, the script
        launches an initialization writing by UART. If the decoded output is "$" or "" -> the communication worked.
        If there was not any decoded output like "$" or "" -> no light controller like "FG-PDV400W-24" model was found.
        :return: port com, baud rate
        - port com : like "COM3" if a right communication was found else None.
        - baud rate : baud rate if a right communication was found else None.


        """
        for port, _, _ in self.ports:
            for baudrate in self.baudrate_list:
                try:
                    light_manager = LightManager(port=port, baudrate=baudrate, list_channels=[1])
                    light_manager.timeout = 0

                    if light_manager.read() != b'':
                        decoded_output = light_manager.read().decode('windows-1252')
                        if (decoded_output == "$") or (decoded_output == ""):
                            return port, baudrate

                    light_manager.close()

                except Exception as e:
                    print(str(e))

        print("We didn't find any COM PORT which is managing lights.")
        return None, None


if __name__ == '__main__':
    start = time.time()
    lc = LightControllerSearcher(baudrate_list=[9600])

    try:
        lm = LightManager(port=lc.port, baudrate=lc.baudrate, list_channels=[1, 2, 3])
        lm.switch_on([0, 255, 0])
        lm.switch_off()

    except Exception as e:
        print(str(e))
