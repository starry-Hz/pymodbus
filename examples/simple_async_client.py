#!/usr/bin/env python3
"""Pymodbus asynchronous client example.

An example of a single threaded synchronous client.

usage: simple_client_async.py

All options must be adapted in the code
The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import asyncio

import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    Framer,
    ModbusException,
    pymodbus_apply_logging_config,
)

# async 关键字用于定义异步函数
# comm:通信类型，host:主机，port:端口，framer:帧类型

async def run_async_simple_client(comm, host, port, framer=Framer.SOCKET):
    """Run async client."""
    # activate debugging    激活调试模式
    pymodbus_apply_logging_config("DEBUG")

    print("get client")
    if comm == "tcp":
        client = ModbusClient.AsyncModbusTcpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,   #设置通信超时时间
            # retries=3,    #设置在发生错误时重新尝试连接的次数
            # retry_on_empty=False,     #True 在没有收到响应时候重试
            # close_comm_on_error=False,    #True 发生通信错误时关闭通信
            # strict=True,  #True 启用严格的Modbus协议模式
            # source_address=("localhost", 0),  #设置本地地址
        )
    elif comm == "udp":
        client = ModbusClient.AsyncModbusUdpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # source_address=None,
        )
    elif comm == "serial": #    创建一个Modbus串口客户端对象
        client = ModbusClient.AsyncModbusSerialClient(
            port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            baudrate=9600,  #波特率
            bytesize=8,     #每个字节的位数设置为8
            parity="N",     #奇偶校验
            stopbits=1,     #停止位
            # handle_local_echo=False,
        )
    elif comm == "tls":
        client = ModbusClient.AsyncModbusTlsClient(
            host,
            port=port,
            framer=Framer.TLS,  #指定使用 TLS（安全传输层协议）作为帧生成器
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # sslctx=sslctx,    #配置 Modbus TLS 客户端的 SSL 上下文
            certfile="../examples/certificates/pymodbus.crt",   #   指定客户端的证书文件路径
            keyfile="../examples/certificates/pymodbus.key",    #   指定客户端的私钥文件路径
            # password="none",
            server_hostname="localhost",                        #   服务器的主机名
        )
    else:  # pragma no cover
        print(f"Unknown client {comm} selected")
        return

    print("connect to server")
    await client.connect()
    # test client is connected
    assert client.connected     #   验证客户端是否已经成功连接服务器

    print("get and verify data")
    try:
        # See all calls in client_calls.py
        rr = await client.read_coils(1, 1, slave=1)     #   异步调用，尝试读取Modbus服务器的状态
    except ModbusException as exc:  # pragma no cover
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():  # pragma no cover
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):  # pragma no cover    #   检查 rr 对象是否是 ExceptionResponse 类型的实例
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()

    print("close connection")
    client.close()


if __name__ == "__main__":
    asyncio.run(
        run_async_simple_client("tcp", "127.0.0.1", 5020), debug=True
    )  # pragma: no cover
