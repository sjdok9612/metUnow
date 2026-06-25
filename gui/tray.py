from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt6.QtCore import Qt


class TrayIcon(QSystemTrayIcon):
    def __init__(self, window):
        super().__init__(self._make_icon(), window)
        self._window = window
        self._build_menu()
        self.activated.connect(self._on_activated)

    def _make_icon(self, badge: bool = False) -> QIcon:
        px = QPixmap(64, 64)
        px.fill(Qt.GlobalColor.transparent)
        p = QPainter(px)
        p.setBrush(QColor(0, 102, 204))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(8, 8, 48, 48)
        if badge:
            p.setBrush(QColor(220, 50, 50))
            p.drawEllipse(40, 4, 20, 20)
        p.end()
        return QIcon(px)

    def set_badge(self, on: bool):
        self.setIcon(self._make_icon(badge=on))

    def _build_menu(self):
        menu = QMenu()
        menu.addAction("창 열기", self._show_window)
        menu.addSeparator()
        menu.addAction("종료", QApplication.instance().quit)
        self.setContextMenu(menu)

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._show_history_menu()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_window()

    def _show_history_menu(self):
        self.set_badge(False)
        history = self._window.get_notif_history()
        menu = QMenu()
        menu.setStyleSheet(
            "QMenu { background:#1a1a1a; color:#ccc; border:1px solid #333; padding:4px; }"
            "QMenu::item { padding:5px 16px; font-size:12px; }"
            "QMenu::item:disabled { color:#666; }"
            "QMenu::separator { background:#333; height:1px; margin:3px 0; }"
        )
        if history:
            for entry in history:
                action = menu.addAction(entry)
                action.setEnabled(False)
        else:
            action = menu.addAction("최근 알림 없음")
            action.setEnabled(False)
        menu.addSeparator()
        menu.addAction("창 열기", self._show_window)
        menu.addAction("종료", QApplication.instance().quit)
        menu.exec(self.geometry().topLeft())

    def _show_window(self):
        self._window.show()
        self._window.raise_()
        self._window.activateWindow()
