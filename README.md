# 专为火箭飞行高度数据可视化设计的脚本程序

## 依赖

如果你已经安装了conda, 可以通过以下命令安装依赖：
首先新建一个conda环境，然后激活这个环境，最后安装依赖。

```shell
conda create -n rocket python=3.11
conda activate rocket
conda install matplotlib numpy pyserial requests
```

## 使用

### 脚本构成

- `config/`: 存放配置文件
- `data/`: 存放数据
- `main.exe`：主程序

运行主程序后，会打开一个命令行窗口，按照提示操作即可。可能的界面如下：

```shell
正在读取配置...
读取到的配置如下:

芯片类型:               |  STM
数据读取方式:           |  serial
所有数据存储路径:       |  E:\Code\python\Rocket_Plot\data
高度数据文件名:         |  data
高度图文件名:           |  picture
高度数据文件URL:        |  http://192.168.4.1/data/2023_10_05__23_45.txt
本地高度数据存储路径:   |  E:\Code\python\Rocket_Plot\test\data.txt


-----------------------------------------------------------------
请选择高度数据来源
1. 串口或者网页数据
2. 本地文件
3. 退出
请输入选项: 1

此次存储文件夹路径:     |  E:\Code\python\Rocket_Plot\data\2024-04-30_19-37-46
此次高度数据存储路径:   |  E:\Code\python\Rocket_Plot\data\2024-04-30_19-37-46\data.txt
此次高度图存储路径:     |  E:\Code\python\Rocket_Plot\data\2024-04-30_19-37-46\picture.png


正在生成 data.txt...
Connecting to COM6
图像绘制中...
图像绘制完成
```

> Note
> 运行`main.exe`前，需要先更改`config/config.ini`中的配置（如果需要）。

### 配置文件

配置文件`config/config.ini`中的配置项如下：

```ini
[CHIP]
; 芯片类型
type = STM
[READ_METHOD]
; 读取高度数据的方法，有两种：serial和html
; serial: 通过串口读取数据(STM)
; html: 通过访问URL读取数据(ESP)
method = serial
[PATH]
; 高度数据文件和高度图存储的位置
data = data/
; 本地数据文件
local_data = test/data.txt
[NAME]
; 高度数据文件名
height_data = data
; 高度图文件名
height_picture = picture
[URL]
; 访问ESP flash中高度数据文件的URL（method=html情况下使用）
height_data = http://192.168.4.1/data/2023_10_05__23_45.txt
```

ESP通过串口读取的功能暂未开发，等待后续更改ESP主程序。

## 数据查看

每一次成功读取数据后，都会在`data/`文件夹下生成一个以当前时间命名的文件夹，文件夹中包含了高度数据文件和高度图文件。文件树形式如下：

```shell
|--data/
    |--2024-04-30_19-37-46/
        |--data.txt
        |--picture.png
    |--2024-04-30_19-37-47/
        |--data.txt
        |--picture.png
```

<!-- conda install pyinstaller -->
