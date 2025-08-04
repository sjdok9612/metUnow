# tray_icon.py

import threading
import sys
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import tkinter as tk


class TrayIcon:
    def __init__(self, root: tk.Tk, update_event):
        """
        :param root: tkinter의 루트 창
        :param update_event: 업데이트 이벤트
        """
        self.root = root
        self.update_event = update_event

        self.icon = pystray.Icon(
            "meechu_now",
            self.create_image(),
            "Met U Now",
            menu=self.create_menu()
        )

        # 루트 창 종료 시 트레이에 숨기기
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

    def create_image(self):
        image = Image.new("RGB", (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill=(0, 102, 204))
        return image

    def create_menu(self):
        return pystray.Menu(
            item("창 열기", lambda _: self.show_window()),
            item("종료", lambda _: self.exit_app())
        )

    def run(self):
        threading.Thread(target=self.icon.run, daemon=True).start()

    def stop(self):
        self.icon.stop()

    def show_window(self):
        if self.root.state() == 'iconic' or not self.root.winfo_viewable():
            self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_window(self):
        self.root.withdraw()

    def exit_app(self):
        self.stop()
        self.update_event.set()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
