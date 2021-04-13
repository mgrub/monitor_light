#!/usr/bin/env python3
import tkinter as tk
from tkinter import colorchooser, ttk
import numpy as np

class Gui:
    fullScreen = False
    mode = "temp"

    state = {"red" : [0, 12], "green" : [0, 12], "blue" : [0, 12], "temp" : [2500, 100], "display_info": False}

    def __init__(self):
        self.root = tk.Tk()
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("c", self.set_background_color)
        self.root.bind("r", self.set_mode_red)
        self.root.bind("g", self.set_mode_green)
        self.root.bind("b", self.set_mode_blue)
        self.root.bind("t", self.set_mode_temp)
        self.root.bind("+", self.increase_value)
        self.root.bind("-", self.decrease_value)
        self.root.bind("<ButtonPress>", self.toggle_information)
        self.root.bind("<Escape>", self.deactivateFullscreen)
        self.root.bind("<Control-w>", self.quit)

        self.label = ttk.Label(self.root, text = "")
        self.label.grid(column = 0, row = 0)

        self.root.geometry("500x300")
        self.root.mainloop()
    
    def toggle_information(self, event):
        self.state["display_info"] = not self.state["display_info"]
        self.set_status_display()

    def toggleFullScreen(self, event):
        if self.fullScreen:
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()

    def activateFullscreen(self):
        self.fullScreen = True

        # Store geometry for reset
        self.geometry = self.root.geometry()

        # Hides borders and make truly fullscreen
        self.root.overrideredirect(True)

        # Maximize window (Windows only). Optionally set screen geometry if you have it
        self.root.state("zoomed")

    def deactivateFullscreen(self, event):
        if self.fullScreen:
            self.fullScreen = False
            self.root.state("normal")
            self.root.geometry(self.geometry)
            self.root.overrideredirect(False)

    def quit(self, event=None):
        print("quiting...", event)
        self.root.quit()

    def set_background_color(self, event, rgb=None):
        if rgb is None:
            color = colorchooser.askcolor()
            print(color)
            self.root.configure(bg=color[1])
            self.mode = "custom"
        else:
            self.root.configure(bg=rgb)
    
        self.set_status_display()
    
    def set_status_display(self):
        if self.state["display_info"]:
            self.label.configure(text = str(self.state))
        else:
            self.label.configure(text = "")

    def increase_value(self, event):
        if self.mode in ["red", "green", "blue"]:
            val = self.state[self.mode][0]
            dval = self.state[self.mode][1]
            self.state[self.mode][0] = self.limit_rgb(val + dval)

        elif self.mode == "temp":
            val = self.state[self.mode][0]
            dval = self.state[self.mode][1]
            self.state[self.mode][0] = self.limit_temp(val + dval)
        
            rgb = self.rgb_from_temp(temp=self.state[self.mode][0])
            self.state["red"][0] = self.limit_rgb(rgb[0])
            self.state["green"][0] = self.limit_rgb(rgb[1])
            self.state["blue"][0] = self.limit_rgb(rgb[2])

        self.set_background_color(event, rgb=self.get_current_rgb())

    def decrease_value(self, event):
        if self.mode in ["red", "green", "blue"]:
            val = self.state[self.mode][0]
            dval = self.state[self.mode][1]
            self.state[self.mode][0] = self.limit_rgb(val - dval)
        
        elif self.mode == "temp":
            val = self.state[self.mode][0]
            dval = self.state[self.mode][1]
            self.state[self.mode][0] = self.limit_temp(val - dval)

            rgb = self.rgb_from_temp(temp=self.state[self.mode][0])
            self.state["red"][0] = self.limit_rgb(rgb[0])
            self.state["green"][0] = self.limit_rgb(rgb[1])
            self.state["blue"][0] = self.limit_rgb(rgb[2])
        
        self.set_background_color(event, rgb=self.get_current_rgb())

    def set_mode_red(self, event):
        self.mode = "red"
    
    def set_mode_green(self, event):
        self.mode = "green"
    
    def set_mode_blue(self, event):
        self.mode = "blue"
    
    def set_mode_temp(self, event):
        self.mode = "temp"
    
    def limit_rgb(self, value):
        if value < 0.0:
            return 0
        elif value > 255.0:
            return 255
        else:
            return int(value)

    def limit_temp(self, value):
        if value < 1700.0:
            return 1700
        elif value > 25000.0:
            return 25000
        else:
            return int(value)

    def get_current_rgb(self):
        r = self.state["red"][0]
        g = self.state["green"][0]
        b = self.state["blue"][0]
        hexcolor = f"#{r:02x}{g:02x}{b:02x}"
        return hexcolor

    def rgb_from_temp(self, temp):
        # https://www.color.org/chardata/rgb/srgb.xalter
        S = np.array([
            [3.2406255, -1.537208, -0.4986286],
            [-0.9689307, 1.8757561, 0.0415175],
            [0.0557101, -0.2040211, 1.0569959],
        ])

        xyz = self.xyz_from_temp(temp)
        rgb = np.dot(S, xyz)
        rgb = np.clip(rgb, 0.0, 1.0)
        rgb = rgb / np.max(rgb)

        return np.floor(256*rgb)

    def xyz_from_temp(self, temp):
        # https://en.wikipedia.org/wiki/Planckian_locus
        ti = 1e3 / temp

        if 1667 < temp and temp <= 4000:
            x = -0.2661239 * ti**3 - 0.2343589 * ti**2 + 0.8776956 * ti + 0.179910
        elif 4000 < temp and temp <= 25000:
            x = -3.0258469 * ti**3 + 2.1070379 * ti**2 + 0.2226347 * ti + 0.240390
        else:
            raise ValueError("temp outside range of model-validity")

        if 1667 < temp and temp <= 2222:
            y = -1.1063814 * x**3 - 1.34811020 * x**2 + 2.18555832 * x - 0.20219683
        elif 2222 < temp and temp <= 4000:
            y = -0.9549476 * x**3 - 1.37418593 * x**2 + 2.09137015 * x - 0.16748867
        elif 4000 < temp and temp <= 25000:
            y = +3.0817580 * x**3 - 5.87338670 * x**2 + 3.75112997 * x - 0.37001483
        else:
            raise ValueError("temp outside range of model-validity")

        z = 1 - x - y

        return (x,y,z)

if __name__ == '__main__':
    Gui()