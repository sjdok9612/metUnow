from gui.streamer_window import StreamerLinkRow
from gui.tray_icon import TrayIcon

import logging
import tkinter as tk
import sys

class AppWindow:
    def __init__(self, Streamers, update_event):
        self.root = tk.Tk()
        self.root.title("Met U Now")
        self.root.configure(bg="#080808")
        self.Streamers = Streamers
        self.update_event = update_event
        self.widgets = []

        for streamer in Streamers.values():
            widget = StreamerLinkRow(self.root, streamer)
            widget.grid(sticky='w', pady=4, padx=4)
            self.widgets.append({
                "widget": widget,
                "streamer": streamer
            })

        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.root.minsize(width, height)
        self.root.maxsize(width, height)
        self.check_for_update()

        # 트레이 아이콘 생성 (콜백 전달)
        self.tray_icon = TrayIcon(self.root, self.update_event)
        self.tray_icon.run()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

    def show_window(self):
        if self.root.state() == 'iconic' or not self.root.winfo_viewable():
            self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_window(self):
        self.root.withdraw()

    def exit_app(self):
        self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

    def check_for_update(self):
        if self.update_event.is_set():
            for item in self.widgets:
                widget = item["widget"]
                streamer = item["streamer"]
                widget.update_status(streamer.is_live)
            logging.debug("GUI 갱신")
            self.update_event.clear()
        self.root.after(1000, self.check_for_update)

    def run(self):
        self.root.mainloop()
