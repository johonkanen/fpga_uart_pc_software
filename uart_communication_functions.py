import serial
import struct
import numpy as np
from matplotlib import pyplot

class uart_link:
    def __init__(self, port, baud):
        self.uart_object = serial.Serial()
        self.uart_object.baudrate = baud
        self.uart_object.timeout = 0.1
        self.uart_object.port = port
        self.uart_object.open()
        self.uart_object.set_buffer_size(rx_size=2**20, tx_size=None)
        self.uart_object.reset_input_buffer()
        self.uart_object.reset_output_buffer()

    def get_data_from_uart(self):
        data_from_uart = self.uart_object.read(5)
        return int.from_bytes(data_from_uart[3:5], "big")

    def send_data_request_to_address(self, address):
        uart_message = address | 2 << 16
        self.uart_object.write(uart_message.to_bytes(3, "big"))

    def request_data_from_address(self, address):
        self.send_data_request_to_address(address)
        return self.get_data_from_uart()

    def write_data_to_address(self, address, data):
        uart_message = 4
        self.uart_object.write(uart_message.to_bytes(1, "big"))
        uart_message = address
        self.uart_object.write(uart_message.to_bytes(2, "big"))
        uart_message = data 
        self.uart_object.write(uart_message.to_bytes(2, "big"))

    def get_stream_packet_from_uart(self):
        return int.from_bytes(self.uart_object.read(2), "big")

    def request_data_stream_from_address(self, address, number_of_registers):
        uart_message = 5
        self.uart_object.write(uart_message.to_bytes(1, "big"))
        uart_message = address
        self.uart_object.write(uart_message.to_bytes(2, "big"))
        uart_message = number_of_registers 
        self.uart_object.write(uart_message.to_bytes(3, "big"))

    def request_fpga_controlled_data_stream_from_address(self, address, number_of_registers):
        uart_message = 6
        self.uart_object.write(uart_message.to_bytes(1, "big"))
        uart_message = address
        self.uart_object.write(uart_message.to_bytes(2, "big"))
        uart_message = number_of_registers 
        self.uart_object.write(uart_message.to_bytes(3, "big"))

    def get_streamed_data(self, number_of_registers):
        received_stream = np.arange(1,number_of_registers+1)
        for i in range(number_of_registers):
            received_stream[i] = self.get_stream_packet_from_uart()
        return received_stream
    
    def stream_data_from_address(self, address, number_of_registers):
        self.request_data_stream_from_address(address, number_of_registers)
        return self.get_streamed_data(number_of_registers)

    def plot_data_from_address(self, address, number_of_registers):
        pyplot.plot(self.stream_data_from_address(address, number_of_registers)) 
        pyplot.show()

    def testi(self):
        print("this is from a test")
