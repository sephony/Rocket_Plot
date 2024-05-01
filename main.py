import os
import time
import configparser
import shutil

from src.rocket_serial import SerialData
from src.rocket_html import HtmlData
from src.rocket_plot import Rocket_Height


def main():
    # 检测是否存在配置文件，不存在则创建
    if not os.path.exists("config/config.ini"):
        create_config()

    # 获取配置文件中的参数
    (
        chip_type,
        read_method,
        data_path,
        height_data_name,
        height_pic_name,
        height_data_url,
        local_data_path,
    ) = get_config()

    while True:
        # 是否通过本地文件获取数据
        print("-----------------------------------------------------------------")
        print("请选择高度数据来源", flush=True)
        print("1. 串口或者网页数据")
        print("2. 本地文件")
        print("3. 退出")

        choice = input("请输入选项: ")
        if choice == "1":
            # 获取存储路径
            data_folder, height_data_path, height_pic_path = get_this_save_paths(
                data_path, height_data_name, height_pic_name
            )

            # 创建存放这次数据的文件夹
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            print("正在生成 data.txt...", flush=True)
            if read_method == "html":
                rocket = HtmlData()
                rocket.download_file(url=height_data_url, save_path=height_data_path)

            elif read_method == "serial":
                rocket = SerialData()
                rocket.connect()
                rocket.read_data(read_time=10, save_path=height_data_path)

            else:
                print("Error: Wrong read method, Please reconfigure.", flush=True)
                exit(1)

            height = Rocket_Height(chip_type)
            height.read_file(file_path=height_data_path, split_str=" ")

        elif choice == "2":
            # 获取存储路径
            data_folder, height_data_path, height_pic_path = get_this_save_paths(
                data_path, height_data_name, height_pic_name
            )

            # 创建存放这次数据的文件夹
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            # 将本地数据复制到文件夹
            shutil.copy(local_data_path, height_data_path)

            print("正在读取本地文件...\n", flush=True)
            height = Rocket_Height(chip_type)
            height.read_file(file_path=local_data_path, split_str=" ")

        elif choice == "3":
            exit(0)
        else:
            print("Error: 请输入正确的选项\n", flush=True)
            continue

        height.plot(height_pic_path)


def create_config():
    # 创建配置文件
    print("未找到配置文件，正在创建...", flush=True)
    config = configparser.ConfigParser()

    # 配置文件内容
    config["CHIP"] = {"type": "STM"}
    config["READ_METHOD"] = {"method": "serial"}
    config["PATH"] = {"data": "data/", "local_data": "test/data.txt"}
    config["NAME"] = {"height_data": "data", "height_picture": "picture"}
    config["URL"] = {"height_data": "http://192.168.4.1/data/2023_10_05__23_45.txt"}

    # 写入配置文件
    with open("config/config.ini", "w") as configfile:
        config.write(configfile)

    print("配置文件创建成功，请修改配置后重新运行程序", flush=True)
    # 按下任意键退出
    input("按下任意键退出...")
    exit(0)


def get_config():
    # 获取配置文件中的参数
    print("正在读取配置...", flush=True)
    config = configparser.ConfigParser()
    config.read("config/config.ini", encoding="utf-8")

    chip_type = config.get("CHIP", "type")
    read_method = config.get("READ_METHOD", "method")
    data_path = config.get("PATH", "data")
    height_data_name = config.get("NAME", "height_data")
    height_pic_name = config.get("NAME", "height_picture")
    height_data_url = config.get("URL", "height_data")
    local_data_path = config.get("PATH", "local_data")

    # 路径规范化（规范化路径分隔符使其符合对应系统）
    data_path = os.path.normpath(data_path)
    local_data_path = os.path.normpath(local_data_path)

    # 获取程序运行路径
    current_path = os.getcwd()

    # 打印配置信息
    print("读取到的配置如下:\n")
    print("芯片类型:\t\t| ", chip_type)
    print("数据读取方式:\t\t| ", read_method)
    print("所有数据存储路径:\t| ", os.path.join(current_path, data_path))
    print("高度数据文件名:\t\t| ", height_data_name)
    print("高度图文件名:\t\t| ", height_pic_name)
    print("高度数据文件URL:\t| ", height_data_url)
    print("本地高度数据存储路径:\t| ", os.path.join(current_path, local_data_path))
    print("\n", flush=True)

    return (
        chip_type,
        read_method,
        data_path,
        height_data_name,
        height_pic_name,
        height_data_url,
        local_data_path,
    )


def get_this_save_paths(data_path, height_data_name, height_pic_name):
    # 获取当前时间
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))

    # 获取实际路径
    data_folder = os.path.join(data_path, current_time)
    height_data_path = os.path.join(data_folder, height_data_name + ".txt")
    height_pic_path = os.path.join(data_folder, height_pic_name + ".png")

    # 打印此次运行路径
    current_path = os.getcwd()
    print("\n此次存储文件夹路径:\t| ", os.path.join(current_path, data_folder))
    print("此次高度数据存储路径:\t| ", os.path.join(current_path, height_data_path))
    print("此次高度图存储路径:\t| ", os.path.join(current_path, height_pic_path))
    print("\n", flush=True)
    return data_folder, height_data_path, height_pic_path


if __name__ == "__main__":
    main()
