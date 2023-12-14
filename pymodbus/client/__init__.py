"""Client."""

__all__ = [
    "AsyncModbusSerialClient",
    "AsyncModbusTcpClient",
    "AsyncModbusTlsClient",
    "AsyncModbusUdpClient",
    "ModbusSerialClient",
    "ModbusTcpClient",
    "ModbusTlsClient",
    "ModbusUdpClient",
]

from pymodbus.client.serial import AsyncModbusSerialClient, ModbusSerialClient  #导入异步（async）和同步的串口客户端类(RS-485)
from pymodbus.client.tcp import AsyncModbusTcpClient, ModbusTcpClient           #导入了异步和同步的 Modbus TCP 客户端类
from pymodbus.client.tls import AsyncModbusTlsClient, ModbusTlsClient           #导入了异步和同步的 Modbus TLS 客户端类
from pymodbus.client.udp import AsyncModbusUdpClient, ModbusUdpClient           #导入了异步和同步的 Modbus UDP 客户端类
