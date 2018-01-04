from tkinter import *
from pygame import mixer
from time import time
from copy import deepcopy


class Timer:
    COUNT = 180
    count = deepcopy(COUNT)
    isCoundown = False

    def __init__(self):
        self.root = Tk()
        self.root.title("ラーメンタイマー")
        self.root.geometry('500x200')

        self.canvas = Canvas(self.root, width=500, height=200)
        self.canvas.place(x=0, y=0)

        self.image = PhotoImage(file="ramen.gif")

        Button(self.root, text="スタート", command=self.timer_start)\
            .place(relx=0.65, rely=0.35, anchor="c")
        Button(self.root, text="ストップ", command=self.timer_stop)\
            .place(relx=0.65, rely=0.5, anchor="c")
        Button(self.root, text="リセット", command=self.timer_reset)\
            .place(relx=0.65, rely=0.65, anchor="c")
        Button(self.root, text="＋", command=self.timer_up)\
            .place(relx=0.8, rely=0.425, anchor="c")
        Button(self.root, text="ー", command=self.timer_down)\
            .place(relx=0.8, rely=0.575, anchor="c")
        Button(self.root, text="＋10", command=self.timer_up_10)\
            .place(relx=0.9, rely=0.425, anchor="c")
        Button(self.root, text="ー10", command=self.timer_down_10)\
            .place(relx=0.9, rely=0.575, anchor="c")

        mixer.init()
        self.timer_show()

    def update(self):
        start_time = time()
        if self.count == 0 or not self.isCoundown:
            if self.count == 0:
                self.isCoundown = False
                self.timer_end()
            return
        elif self.count == 1:
            mixer.music.fadeout(1000)
        self.count -= 1
        self.timer_show()
        lag = int(1000 - (time() - start_time) * 1000)
        self.root.after(lag, self.update)

    def timer_show(self):
        self.canvas.delete("all")
        mm = "%02d" % int(self.count / 60)
        ss = "%02d" % int(self.count % 60)
        self.canvas.create_image(400, 170, image=self.image)
        self.canvas.create_rectangle(30, 50, 270, 150, fill="white", width=3)
        self.canvas.create_text(250, 20, text="ラーメンタイマー",
                                font=("Hiragino Maru Gothic Pro", 25))
        self.canvas.create_text(150, 100, text=mm + ":" + ss, font=("", 80))
        self.canvas.update()

    def timer_start(self):
        if not self.isCoundown:
            self.isCoundown = True
            self.root.after(1000, self.update)
            mixer.music.load("kyupi.ogg")
            mixer.music.play(-1)

    def timer_stop(self):
        if self.isCoundown:
            self.isCoundown = False
        try:
            mixer.music.stop()
        except Exception as e:
            raise

    def timer_reset(self):
        self.count = deepcopy(self.COUNT)
        self.timer_show()
        try:
            mixer.music.stop()
        except Exception as e:
            raise

    def timer_end(self):
        mixer.music.load("alarm.ogg")
        mixer.music.play(1)

    def timer_up(self):
        self.count += 1
        if not self.isCoundown:
            self.COUNT = self.count
        self.timer_show()

    def timer_down(self):
        if self.count > 0:
            self.count -= 1
            if not self.isCoundown:
                self.COUNT = self.count
            self.timer_show()

    def timer_up_10(self):
        self.count += 10
        if not self.isCoundown:
            self.COUNT = self.count
        self.timer_show()

    def timer_down_10(self):
        if self.count > 9:
            self.count -= 10
            if not self.isCoundown:
                self.COUNT = self.count
            self.timer_show()


if __name__ == '__main__':
    timer = Timer()
    timer.root.mainloop()
