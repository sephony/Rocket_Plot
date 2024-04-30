import serial
import serial.tools.list_ports
import time
import os


class SerialData:
    def __init__(
        self,
        exclude_port="COM3",
    ):
        self.exclude_port = exclude_port
        self.serial = None

    # 获得serial对象的端口和波特率
    def getImformation(self):
        return self.serial.port, self.serial.baudrate

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

        # 创建一个串口对象
        if self.serial is None:
            self.serial = serial.Serial(port, baud_rate, timeout=5)
            print("Connecting to", port)
        else:
            print("Reconnecting to", port)

        # 关闭串口
        self.serial.close()

        return self.serial

    # 读取串口数据
    def read_data(self, read_time=10, save_path="data.txt", save_to_file=True):

        # 打开串口
        self.serial.open()
        start_time = time.time()

        with open(save_path, "a") as f:
            while True:
                # 读取串口数据
                data = self.serial.readline()
                if data:
                    if save_to_file:
                        f.write(data.decode("utf-8").rstrip("\n"))
                        f.flush()
                        os.fsync(f.fileno())
                    else:
                        print(data.decode("utf-8"), end="")
                # 如果时间超过了规定的时间，结束读取
                if time.time() - start_time > read_time:
                    break

        # 关闭串口
        self.serial.close()

    # 向串口发送数据
    def send_data(self, data, ifkeyboard=False):
        # 打开串口
        self.serial.open()

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
        # 关闭串口
        self.serial.close()

    # 向串口发送文件
    def sendFile(self, filename):
        # 打开串口
        self.serial.open()
        with open(filename, "r") as f:
            for line in f:
                self.serial.write(line.encode())
        # 关闭串口
        self.serial.close()
