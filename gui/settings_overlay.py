from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

try:
    from version import BUILD_TIME
except ImportError:
    BUILD_TIME = "dev"


class SettingsOverlay(QWidget):
    test_notification_requested = pyqtSignal()
    image_refresh_requested = pyqtSignal()
    force_check_requested = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #111111;")
        self.setGeometry(parent.rect())

        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(6)

        title = QLabel("설정")
        title.setStyleSheet("color:#ffffff; font-size:14px; font-weight:bold;")
        outer.addWidget(title)

        ver = QLabel(f"빌드: {BUILD_TIME}")
        ver.setStyleSheet("color:#444; font-size:10px;")
        outer.addWidget(ver)

        actions = [
            ("테스트 알람",        self.test_notification_requested),
            ("이미지 새로고침",     self.image_refresh_requested),
            ("전체 방송 상태 확인", self.force_check_requested),
        ]
        for label, sig in actions:
            btn = QPushButton(label)
            btn.setStyleSheet(
                "color:#ffffff; background-color:#2a2a2a; border:none;"
                "padding:10px; font-size:13px; text-align:left;"
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(sig.emit)
            btn.clicked.connect(self._close)
            outer.addWidget(btn)

        outer.addStretch()

        bottom = QHBoxLayout()
        back = QPushButton("← 뒤로")
        back.setStyleSheet(
            "color:#aaaaaa; background:transparent; border:none;"
            "font-size:12px; text-align:left; padding:2px 0;"
        )
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self._close)
        bottom.addWidget(back)
        bottom.addStretch()
        outer.addLayout(bottom)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._close()
        else:
            super().keyPressEvent(event)

    def _close(self):
        self.deleteLater()
