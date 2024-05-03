# 脚本程序——火箭飞行高度可视化

## 功能

- 兼容 *ESP* 与 *STM* 上的高度数据存储格式
- *ESP* 通过`html`方式读取数据，*STM* 通过`serial`方式读取数据
- 支持自动将高度数据及高度图保存到`data`目录下
- 支持通过修改`config/config.ini`配置改变程序行为
- 支持本地高度数据直接绘图
- 支持数据存储位置、文件名字自定义

## 使用

这里提供了两种方式，可以从[源码](#源码)解释执行，也可以直接下载[二进制文件](#二进制文件)。

### 源码

首先拉取[仓库代码](https://github.com/sephony/Rocket_Plot)

```shell
git clone https://github.com/sephony/Rocket_Plot.git
```

#### 环境搭建

##### venv

如果你直接在本地下载了 `python` 包(*version<3.12*)，请执行下面的语句以创建 `venv` 环境
并安装依赖

```shell
python -m venv rocket
rocket\Scripts\activate
pip install -r requirements.txt
```

这样便在当前路径下搭建了环境。

##### conda

鉴于 `venv` 创建的虚拟环境是特定于创建它的项目，项目多了之后空间占用较大，我们这里更推荐 `conda` 安装。这样可以使多个项目共用一个虚拟环境。

conda 的安装网上资料很多，可以在***anaconda***、***miniconda***、***miniforge***中选择其中一个进行下载。

安装好 conda 之后，执行下面的语句以创建环境并安装依赖。

```shell
conda create -n rocket
conda activate rocket
conda install python=3.11
conda install matplotlib numpy pyserial requests
```

#### 解释执行

这个方法就更多了，你可以使用 *vscode*、*PyCharm* 调试，也可以在当前文件夹下激活虚拟环境后直接运行即可。

```shell
python main.py
```

具体的脚本操作[请看这里](#脚本运行)

### 二进制文件

在[这里](https://github.com/sephony/Rocket_Plot/releases)下载可执行程序 `main.exe`

以下是脚本组成

```shell
|--Rocket_Plot/
    |--config/
        |--config.ini
    |--data/
    |--main.exe
```

- `config/`: 存放配置文件
- `data/`: 存放数据的默认文件夹，运行程序自动生成
- `main.exe`：主程序

#### 脚本运行

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

第一次运行时，会默认生成一个配置文件`config/config.ini`，之后根据你的需求配置好后再次运行即可。

> ***Note***
>
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

ESP通过串口读取的功能暂未开发，等待后续更改ESP主程序。也就是说，现在 `ESP` 对应 `html` 模式，`STM` 对应 `serial` 模式

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
