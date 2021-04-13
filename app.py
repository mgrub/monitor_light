#!/usr/bin/env python3
import tkinter as tk
from tkinter import colorchooser

class Gui:
    fullScreen = False
    mode = "temp"

    state = {"red" : [0, 12], "green" : [0, 12], "blue" : [0, 12], "temp" : [2500, 100]}

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
        self.root.bind("<Escape>", self.deactivateFullscreen)
        self.root.bind("<Control-w>", self.quit)
        self.root.mainloop()

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

    def increase_value(self, event):
        if self.mode in ["red", "green", "blue"]:
            val = self.state[self.mode][0]
            dval = self.state[self.mode][1]
            self.state[self.mode][0] = self.limit_rgb(val + dval)

        elif self.mode == "temp":
            val = self.state[self.mode][0]
            dval = self.state[self.mode][1]
            self.state[self.mode][0] = self.limit_temp(val + dval)
        
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
        if value < 1500.0:
            return 0
        elif value > 255.0:
            return 6000.0
        else:
            return int(value)

    def get_current_rgb(self):
        r = self.state["red"][0]
        g = self.state["green"][0]
        b = self.state["blue"][0]
        hexcolor = f"#{r:02x}{g:02x}{b:02x}"

        print(hexcolor)
        return hexcolor

if __name__ == '__main__':
    Gui()