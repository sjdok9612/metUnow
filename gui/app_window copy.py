#app_window.py
import logging
import threading
import sys
import tkinter as tk
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

class AppWindow:
    def __init__(self, channels_status, update_event):
        self.root = tk.Tk()
        self.root.title("Met U Now")
        self.root.configure(bg="#9E9E9E")
        self.channels_status = channels_status
        self.update_event = update_event
        self.widgets = []

        # ... (위젯 생성 코드)

        self.check_for_update()

        # 트레이 아이콘 생성
        self.icon = pystray.Icon(
            "meechu_now",
            self.create_image(),
            "Met U Now",
            menu=self.create_menu()
        )

        # 스레드에서 실행
        threading.Thread(target=self.icon.run, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        # pystray가 직접 지원하지 않는 좌클릭 처리를 위해
        # 아래처럼 별도 모니터링 스레드를 만들거나
        # 혹은 pywin32 직접 사용 고려 (복잡)

    def create_image(self):
        image = Image.new("RGB", (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill=(0, 102, 204))
        return image

    def create_menu(self):
        return pystray.Menu(
            item("창 열기", lambda: self.root.after(0, self.show_window)),
            item("종료", lambda: self.root.after(0, self.exit_app))
        )

    def show_window(self):
        if self.root.state() == 'iconic' or not self.root.winfo_viewable():
            self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_window(self):
        self.root.withdraw()

    def exit_app(self):
        try:
            self.icon.stop()
        except Exception as e:
            logging.error(f"아이콘 정지 중 에러: {e}")
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


