import serial
import serial.tools.list_ports
import time
import os


class SerialData:
    default_port = "COM3"

    def __init__(
        self,
        port=default_port,
        exclude_port=default_port,
        baud_rate=115200,
        read_time=10,
        file_path="data.txt",
    ):
        self.port = port
        self.exclude_port = exclude_port
        self.baud_rate = baud_rate
        self.read_time = read_time
        self.file_path = file_path
        self.serial = None

    # 获取所有可用的串口
    def getAvailablePorts(self, ifPrint=True):
        ports = serial.tools.list_ports.comports()
        if ifPrint:
            print("Available ports:")
            for port in ports:
                print(port)
        return ports

    # 连接串口
    def connect(self, port=None, baud_rate=115200):
        # 如果用户没有提供端口，按照逻辑获取端口
        if port is None:
            ports = self.getAvailablePorts(ifPrint=False)
            # 除去特定的串口
            # TODO exclude_port以后可以改成一个列表，可以排除多个串口
            # TODO 或者自动选择串口
            ports = [port for port in ports if self.exclude_port not in port.device]
            # 选择最后添加的除了特定的串口
            if ports:
                port = ports[-1].device
        # 如果没有可用端口，报错
        if not port:
            raise RuntimeError("No available ports!")

        self.port = port
        self.baud_rate = baud_rate

        # 创建一个串口对象
        if self.serial is None:
            self.serial = serial.Serial(port, baud_rate, timeout=5)

        print("Connecting to", port)
        return self.serial

    # 读取串口数据
    def readData(self, read_time=10, save_path="data.txt", save_to_file=True):
        self.read_time = read_time
        self.file_path = save_path

        start_time = time.time()
        if save_to_file:
            with open(save_path, "a") as f:
                while True:
                    # 读取串口数据
                    data = self.serial.readline()
                    if data:
                        # print(data.decode("utf-8"), end="")
                        f.write(data.decode("utf-8").rstrip("\n"))
                        f.flush()
                        os.fsync(f.fileno())
                    if time.time() - start_time > read_time:
                        break
        else:
            while True:
                # 读取串口数据
                data = self.serial.readline()
                if data:
                    print(data.decode("utf-8"), end="")
                if time.time() - start_time > read_time:
                    break

    # 向串口发送数据
    def sendData(self, data, ifkeyboard=False):
        if ifkeyboard:
            print("Press Ctrl+C to exit")
            try:
                while True:
                    self.serial.write(data.encode())
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Exit")
        else:
            self.serial.write(data.encode())

    # 向串口发送文件
    def sendFile(port, filename):
        # 打开串口
        with serial.Serial(port, 9600, timeout=1) as ser:
            # 打开文件
            with open(filename, "rb") as f:
                while True:
                    # 读取文件内容
                    data = f.read(1024)
                    if not data:
                        break
                    # 将内容写入串口
                    ser.write(data)
