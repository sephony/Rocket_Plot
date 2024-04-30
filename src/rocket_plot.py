from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Rocket_Height:
    def __init__(self, chip_type):
        if chip_type == "ESP":
            self.chip = Rocket_Height_ESP()
        elif chip_type == "STM":
            self.chip = Rocket_Height_STM()
        else:
            raise ValueError("Invalid chip type")

    def read_file(self, file_path, **kwargs):
        return self.chip.read_file(file_path, **kwargs)

    def plot(self, pic_path):
        return self.chip.plot(pic_path)


class Rocket_Height_Base(ABC):
    def __init__(self):
        self.time = []
        self.original_heights = []
        self.filtered_heights = []
        self.fig, self.ax = plt.subplots()
        self.text = self.ax.text(0, 0, "", va="bottom", ha="left", fontsize=10)

    # 从文件中读取并整合数据
    @abstractmethod
    def read_file(self, file_path, **kwargs):
        pass

    # 绘制图表
    def plot(self, pic_path=None):
        print("图像绘制中...")
        # 绘制原始高度折线图
        self.ax.plot(
            self.time,
            self.original_heights,
            label="Original Heights",
            color="b",
            linestyle="-",
            linewidth=0.5,
        )
        # 绘制滤波后高度折线图
        self.ax.plot(
            self.time,
            self.filtered_heights,
            label="Filtered Heights",
            color="r",
            linestyle="-",
            linewidth=0.5,
        )
        # 标记最高点
        max_index = self.filtered_heights.index(max(self.filtered_heights))
        max_value = self.filtered_heights[max_index]
        self.ax.plot(self.time[max_index], max_value, "ro")
        self.ax.annotate(
            f"Max: ({self.time[max_index]}, {max_value:.2f})",
            xy=(self.time[max_index], max_value),
            xytext=(self.time[max_index] + 0.2, max_value + 0.4),
            arrowprops=dict(arrowstyle="->", lw=1, facecolor="black"),
            ha="center",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.5),
        )
        # 标记起始点
        self.ax.plot(self.time[0], self.filtered_heights[0], "ro")
        self.ax.annotate(
            f"Start: ({self.time[0]}, {self.filtered_heights[0]:.2f})",
            xy=(self.time[0], self.filtered_heights[0]),
            xytext=(self.time[0] - 0.3, self.filtered_heights[0] - 0.4),
            arrowprops=dict(arrowstyle="->", lw=1, facecolor="black"),
            ha="center",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.5),
        )
        print("图像绘制完成.\n")
        # 添加图例，并指定位置为右上角（loc='upper right'）
        self.ax.legend(loc="lower right")

        # 添加图表标题和轴标签
        self.ax.set_title("Rocket altitude data")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Height")

        # 连接鼠标事件
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.fig.canvas.mpl_connect("axes_leave_event", self.on_leave)

        # 保存图表
        self.fig.savefig(pic_path)

        # 显示图表
        plt.show()

    def on_motion(self, event):
        if event.inaxes == self.ax:
            x = event.xdata
            index = int(x * 20)
            if 0 <= index <= len(self.filtered_heights):
                y_original = self.original_heights[index]
                y_filtered = self.filtered_heights[index]
                self.text.set_text(
                    f"Time: {x:.2f}\nOriginal Height: {y_original:.2f}\nFiltered Height: {y_filtered:.2f}"
                )
                self.text.set_position((x, y_filtered + 2))
                self.fig.canvas.draw_idle()

    def on_leave(self, event):
        self.text.set_text("")
        self.fig.canvas.draw_idle()


class Rocket_Height_STM(Rocket_Height_Base):

    # 从文件中读取并整合数据
    def read_file(
        self,
        file_path,
        start_identifier="1000 1000",
        end_identifier="1001 1001",
        split_str=" ",
    ):
        # 读取数据,1000到1001之间的数据
        with open(file_path, "r") as f:
            lines = f.readlines()

        data_started = False

        for line in lines:
            line = line.strip()  # 去除行首行尾的空白字符
            if line == start_identifier:
                data_started = True
                print("数据读取中...", flush=True)
            elif line == end_identifier and data_started:
                print("数据读取完成.\n")
                break
            elif data_started:
                values = line.split(split_str)  # 分割行
                self.original_heights.append(float(values[0]))
                self.filtered_heights.append(float(values[1]))
        # print("\n数据读取中...", flush=True)
        # with open(file_path, "r") as f:
        #     for line in f.readlines():
        #         line = line.strip().split(split_str)
        #         self.original_heights.append(float(line[0]))
        #         self.filtered_heights.append(float(line[1]))
        # print("数据读取完成.\n")

        # 采样频率是50Hz 对应的时间序列
        self.time = [i / 20 for i in range(len(self.original_heights))]

        return self.time, self.original_heights, self.filtered_heights


class Rocket_Height_ESP(Rocket_Height_Base):
    # 从文件中读取并整合数据
    def read_file(
        self,
        file_path,
        start_identifier="Detached!",
        end_identifier="Landed!",
        split_str=" ",
    ):
        with open(file_path, "r") as f:
            lines = f.readlines()

        data_started = False

        for line in lines:
            line = line.strip()  # 去除行首行尾的空白字符
            if line == start_identifier:
                data_started = True
                print("\n数据读取中...", flush=True)
            elif line == end_identifier and data_started:
                print("数据读取完成.\n")
                break
            elif data_started:
                values = line.split(split_str)  # 分割行
                try:
                    time_value = float(values[0])
                    original_height = float(values[1])
                    filtered_height = float(values[2])
                except ValueError:
                    continue  # 如果转换失败，跳过这一行
                self.time.append(time_value)
                self.original_heights.append(original_height)
                self.filtered_heights.append(filtered_height)

        return self.time, self.original_heights, self.filtered_heights
