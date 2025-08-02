import threading
import sys
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

class TrayIcon:
    def __init__(self, show_callback, exit_callback):
        """
        :param show_callback: 트레이 메뉴에서 '창 열기' 선택 시 호출할 함수
        :param exit_callback: 트레이 메뉴에서 '종료' 선택 시 호출할 함수
        """
        self.icon = pystray.Icon(
            "meechu_now",
            self.create_image(),
            "Met U Now",
            menu=self.create_menu()
        )
        self.show_callback = show_callback
        self.exit_callback = exit_callback

    def create_image(self):
        image = Image.new("RGB", (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill=(0, 102, 204))
        return image

    def create_menu(self):
        return pystray.Menu(
            item("창 열기", lambda _: self.show_callback()),
            item("종료", lambda _: self.exit_app())
        )

    def run(self):
        threading.Thread(target=self.icon.run, daemon=True).start()

    def stop(self):
        self.icon.stop()

    def exit_app(self):
        self.stop()
        self.exit_callback()
        sys.exit(0)