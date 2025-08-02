#app_window.py
from gui.channel_widget import ChannelStatusWidget
from gui.tray_icon import TrayIcon

import logging
import tkinter as tk
import sys

class AppWindow:
    def __init__(self, channels_status, update_event): #gui 생성 및 초기화
        self.root = tk.Tk()
        self.root.title("Met U Now")
        self.root.configure(bg="#9E9E9E")
        self.channels_status = channels_status
        self.update_event = update_event
        self.widgets = []

        for creator in channels_status: ##채널정보 나열
            widget = ChannelStatusWidget(self.root, creator) ##채널정보 하나씩 위젯화
            widget.grid(sticky='w', pady=2, padx=4)
            self.widgets.append({
                "widget": widget,
                "creator": creator
            })
        self.root.update_idletasks()  # 위젯 배치 계산 후 호출

        # 현재 윈도우 크기 구하기
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # 최소 크기를 현재 크기로 고정
        self.root.minsize(width, height)
        self.root.maxsize(width, height)
        
        self.check_for_update() #이벤트 핸들러

         # 트레이 아이콘 생성
        self.tray_icon = TrayIcon(self.show_window, self.exit_app)
        self.tray_icon.run()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

    def show_window(self):
        if self.root.state() == 'iconic' or not self.root.winfo_viewable():
            self.root.deiconify()  # 창 보이기
        self.root.lift()  # 최상위로
        self.root.focus_force()

    def hide_window(self):
        self.root.withdraw()  # 창 숨기기

    def exit_app(self):
        self.icon.stop()
        self.root.quit()
        sys.exit(0)

    def check_for_update(self):
        if self.update_event.is_set():
            for item in self.widgets:
                widget = item["widget"]
                creator = item["creator"]
                widget.update_status(creator.is_live)
            logging.debug("GUI 갱신")
            self.update_event.clear()

        self.root.after(1000, self.check_for_update)

    def run(self):
        self.root.mainloop()
