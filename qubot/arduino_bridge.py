''' 
    arduino_bridge.py
    Para el intercambio de datos mediante protocolo Modbus

    Autor: Claudio Morales Díaz @cmoralesd
    Versión: 1.0 - abril de 2025

    La transacción de datos se realiza mediante protocolo Modbus-RTU
    Requiere la librería pymodbus versión 3.9
    https://pymodbus.readthedocs.io/
    
'''

import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
#-- Seleccionar según comunicacion protocolo serial o TCP
#from pymodbus.client import ModbusTcpClient
from pymodbus.client import ModbusSerialClient

#-- Pueden definirse variables globales para los registros Modbus
REG1 = 4001
REG2 = 4002
COIL1 = 1001
COIL2 = 1002

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')

        #-- Seleccionar según comunicacion protocolo serial o TCP
        #self.client = ModbusTcpClient('localhost', port=502)
        self.client = ModbusSerialClient(
            port="/dev/ttyUSB0", baudrate=115200, timeout=0.5)
        
        self.client.connect()

        # inicializa timer para polling rate de Modbus
        self.polling_period = 0.1  # sec
        self.timer = self.create_timer(
            self.polling_period, self.timer_callback)

        # inicializa publicador y suscriptor
        self.publisher = self.create_publisher(String, '/arduino_info', 1)
        self.cmd_vel = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 1)
        
        # mensaje de inicialización
        self.get_logger().info(f"{self.get_name()} started")

    def timer_callback(self):
        # lee un par de registros Modbus, despliega los datos recibidos
        # y los publica en el tópico '/arduino_info'
        try:
            data = self.client.read_holding_registers(
                address=4001, count=2, slave=1)
            self.get_logger().info(f"arduino registers: {' '.join(str(d) for d in data.registers)}")
            
            msg = String()
            msg.data = " ".join(str(d) for d in data.registers)

            self.publisher.publish(msg)
        except:
            self.get_logger().warning('no communication with arduino...')


    def cmd_vel_callback(self, msg):
        # activa COIL1 por medio segundo cada vez que se recibe un comando de velocidad
        self.client.write_coil(
                address=COIL1, value=True, slave=1)
        time.sleep(0.5)
        self.client.write_coil(
                address=COIL1, value=False, slave=1)
        

def main(args=None):
    try:
        rclpy.init(args=args)
        arduino_bridge = ArduinoBridge()
        rclpy.spin(arduino_bridge)

    except KeyboardInterrupt:
        print(' ... exit node')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()