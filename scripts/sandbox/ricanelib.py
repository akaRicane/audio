import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import time
from threading import Thread 
from tkinter import TclError
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import audioplot_qt as qt_plot # noqa E402
from modules import audiofiltering_rt as rt_filtering # noqa E402
from modules import player as Player  # noqa E402
from lib import tool, config  # noqa E402


LAB_DEFAULT_CONFIG_DICT = {
    "MAX_INTEGER": 32768.0,
    "BUFFER_SIZE": 1024,
    "SAMPLING_RATE": 44100
}


class Spectrum_visualizer():
    def __init__(self, buffer_size, memory_size):
        self.fig, (self.ax, self.ax2) = plt.subplots(2, figsize=(15, 8))
        self.memory_size = memory_size
        self.buffer_size = buffer_size
        self.x2_max = self.buffer_size * self.memory_size
        self.x = np.arange(0, self.buffer_size)
        self.x2 = np.arange(0, self.x2_max)

        self.init_lines()
        self.init_axes()

    def init_lines(self):
        self.line, = self.ax.plot(self.x, np.random.rand(self.buffer_size), '-', lw=2)
        self.line2, = self.ax2.plot(self.x2, np.random.rand(self.x2_max), '-', lw=2)

    def init_axes(self):
        self.ax.set_title("AUDIO WAVEFORM")
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Magnitude")
        self.ax.set_xlim(0, self.buffer_size)
        self.ax.set_ylim(-1, 1)
        plt.setp(self.ax,
                 xticks=[0, int(self.buffer_size / 2), self.buffer_size],
                 yticks=[-1, 1])

        self.ax2.set_title("MEMORY")
        self.ax2.set_xlabel("Full signal memory")
        self.ax2.set_ylabel("Magnitude")
        self.ax2.set_xlim(0, self.x2_max)
        self.ax2.set_ylim(-1, 1)
        plt.setp(self.ax2,
                 xticks=[0, int(self.x2_max / 2), self.x2_max],
                 yticks=[-1, 1])
        plt.show(block=False)

    def populate_plot(self, data_line, data_line2):
        self.line.set_ydata(data_line)
        self.line2.set_ydata(data_line2)
        self.update_plot_content()

    def update_plot_content(self):
        try:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        except:
            print("Stream is stopped")
            raise TclError



