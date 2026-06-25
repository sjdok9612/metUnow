import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLabel, QPushButton
from PyQt6.QtCore import Qt
from tool.paths import ASSETS_DIR
from gui.tray import TrayIcon
from gui.home_view import HomeView
from gui.detail_overlay import DetailOverlay
from gui.settings_overlay import SettingsOverlay
from gui.streamer_editor import StreamerEditorDialog
from tool.Streamers import Streamer, save_streamers_to_json
from tool.fetch_images import image_exists, ensure_streamer_image
from api.liveCheck import LiveCheckWorker


class AppWindow(QWidget):
    def __init__(self, streamer_dict):
        super().__init__()
        self.streamer_dict = streamer_dict
        self.setWindowTitle("Met U Now")
        self.setStyleSheet("background-color: #080808;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.home_view = HomeView(streamer_dict)
        self.home_view.streamer_clicked.connect(self._show_overlay)
        self.home_view.add_requested.connect(self._open_add_editor)
        layout.addWidget(self.home_view)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 0, 0, 0)

        self._status_label = QLabel("● 상태 확인 중...")
        self._status_label.setStyleSheet("color:#555; font-size:10px; padding:2px 0;")
        bottom_bar.addWidget(self._status_label)
        bottom_bar.addStretch()

        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(22, 22)
        settings_btn.setStyleSheet(
            "color:#555; background:transparent; border:none; font-size:14px;"
        )
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self._open_settings)
        bottom_bar.addWidget(settings_btn)

        layout.addLayout(bottom_bar)

        self.tray = TrayIcon(self)
        self.tray.show()

        self.adjustSize()
        self.setFixedSize(self.size())

        self._notif_history: list[str] = []

        self._worker = LiveCheckWorker(self.streamer_dict)
        self._worker.status_changed.connect(self._on_status_changed)
        self._worker.first_poll_done.connect(self._on_first_poll_done)
        self._worker.start()
        QApplication.instance().aboutToQuit.connect(self._stop_worker)

    def _open_add_editor(self):
        dlg = StreamerEditorDialog(streamer=None, parent=self)
        dlg.saved.connect(self._on_saved)
        dlg.exec()

    def _show_overlay(self, key: str):
        streamer = self.streamer_dict.get(key)
        if not streamer:
            return
        overlay = DetailOverlay(streamer, self)
        overlay.edit_requested.connect(self._open_editor)
        overlay.show()

    def _open_editor(self, key: str):
        streamer = self.streamer_dict.get(key)
        dlg = StreamerEditorDialog(streamer, self)
        dlg.saved.connect(self._on_saved)
        dlg.deleted.connect(self._on_deleted)
        dlg.exec()

    def _on_saved(self, data: dict):
        key = data["key"]
        self.streamer_dict[key] = Streamer.from_dict(data)
        save_streamers_to_json(self.streamer_dict)
        self._worker.add_streamer(key)
        self._rebuild_home()

    def _on_deleted(self, key: str):
        self.streamer_dict.pop(key, None)
        save_streamers_to_json(self.streamer_dict)
        self._worker.remove_streamer(key)
        self._rebuild_home()

    def _rebuild_home(self):
        self.home_view.deleteLater()
        self.home_view = HomeView(self.streamer_dict)
        self.home_view.streamer_clicked.connect(self._show_overlay)
        self.home_view.add_requested.connect(self._open_add_editor)
        self.layout().addWidget(self.home_view)

    def _open_settings(self):
        overlay = SettingsOverlay(self)
        overlay.test_notification_requested.connect(self._test_notification)
        overlay.image_refresh_requested.connect(self._refresh_images)
        overlay.force_check_requested.connect(self._worker.force_check_all)
        overlay.show()

    def _notify(self, title: str, body: str, icon: str = "dialog-information"):
        subprocess.Popen(
            ["/usr/bin/notify-send", "-i", icon, "-t", "4000", title, body],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def _test_notification(self):
        self._notify("metUnow", "테스트 알람입니다.")

    def _refresh_images(self):
        fetched = [s for s in self.streamer_dict.values() if ensure_streamer_image(s)]
        if fetched:
            self._rebuild_home()

    def _on_first_poll_done(self):
        self._status_label.setText("")
        self.home_view.refresh_tooltips()
        missing = [s for s in self.streamer_dict.values() if not image_exists(s.key)]
        if missing:
            fetched = [s for s in missing if ensure_streamer_image(s)]
            if fetched:
                self._rebuild_home()

    def _on_status_changed(self, key: str, is_live: bool):
        self.home_view.update_status(key, is_live)
        streamer = self.streamer_dict.get(key)
        if not streamer:
            return
        label = f"{streamer.name}{streamer.oshi_mark}"
        if is_live:
            msg = f"방송 ON\n{streamer.live_title}" if streamer.live_title else "방송 ON"
        else:
            msg = "방송 OFF"
        entry = f"{label}  {'방송 ON' if is_live else '방송 OFF'}"
        self._notif_history = ([entry] + self._notif_history)[:5]
        self.tray.set_badge(True)
        icon = next(
            (str(ASSETS_DIR / f"{key}.{ext}") for ext in ("png", "jpg", "webp")
             if (ASSETS_DIR / f"{key}.{ext}").exists()),
            "dialog-information"
        )
        self._notify(label, msg, icon)
        if is_live:
            subprocess.Popen(
                ["/usr/bin/paplay", "/usr/share/sounds/freedesktop/stereo/message-new-instant.oga"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

    def get_notif_history(self) -> list[str]:
        return self._notif_history

    def _stop_worker(self):
        self._worker.stop()
        self._worker.wait()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
