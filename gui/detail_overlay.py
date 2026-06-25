import webbrowser
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from gui.streamer_editor import StreamerEditorDialog


def _fmt_since(since: str) -> str:
    try:
        if "T" in since:
            dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            return dt.astimezone().strftime("%m/%d %H:%M")
        return since[5:16].replace("-", "/")
    except Exception:
        return since


def _fmt_range(since: str, end: str) -> str:
    if not end:
        return _fmt_since(since)
    try:
        fmt = "%Y-%m-%d %H:%M:%S"
        from datetime import datetime as _dt
        dt_s = _dt.strptime(since, fmt)
        dt_e = _dt.strptime(end, fmt)
        mins = int((dt_e - dt_s).total_seconds()) // 60
        h, m = divmod(mins, 60)
        duration = f"{h}시간 {m}분" if h else f"{m}분"
        return f"{since[5:16].replace('-','/')} ~ {end[11:16]}  ({duration})"
    except Exception:
        return _fmt_since(since)



class DetailOverlay(QWidget):
    closed = pyqtSignal()
    edit_requested = pyqtSignal(str)   # key 전달

    def __init__(self, streamer, parent):
        super().__init__(parent)
        self._streamer = streamer
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #111111;")
        self.setGeometry(parent.rect())

        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(6)

        name = f"{streamer.name}{streamer.oshi_mark}"
        title = QLabel(name)
        title.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        title.setWordWrap(True)
        outer.addWidget(title)

        if streamer.live_title or streamer.live_since:
            outer.addWidget(self._live_info(streamer))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        btn_layout = QVBoxLayout(content)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(6)
        self._add_buttons(btn_layout, streamer)
        btn_layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

        bottom = QHBoxLayout()
        back = QPushButton("← 뒤로")
        back.setStyleSheet(
            "color: #aaaaaa; background: transparent; border: none;"
            "font-size: 12px; text-align: left; padding: 2px 0;"
        )
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self._close)
        bottom.addWidget(back)

        bottom.addStretch()

        edit = QPushButton("편집")
        edit.setStyleSheet(
            "color: #aaaaaa; background: transparent; border: none;"
            "font-size: 12px; padding: 2px 0;"
        )
        edit.setCursor(Qt.CursorShape.PointingHandCursor)
        edit.clicked.connect(self._on_edit_clicked)
        bottom.addWidget(edit)
        outer.addLayout(bottom)

    def _live_info(self, streamer) -> QWidget:
        box = QWidget()
        box.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        box.setStyleSheet("background:#1a1a1a; border-radius:4px;")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(3)

        header = QLabel("방송 중" if streamer.is_live else "마지막 방송")
        header.setStyleSheet(
            f"color:{'#4a9' if streamer.is_live else '#666'}; font-size:10px;"
        )
        layout.addWidget(header)

        if streamer.live_title:
            lbl = QLabel(streamer.live_title)
            lbl.setStyleSheet("color:#ddd; font-size:12px;")
            lbl.setWordWrap(True)
            layout.addWidget(lbl)

        meta_parts = []
        if streamer.live_category:
            meta_parts.append(streamer.live_category)
        if streamer.live_since:
            end = streamer.live_end if not streamer.is_live else ""
            meta_parts.append(_fmt_range(streamer.live_since, end))
        if meta_parts:
            meta = QLabel("  ·  ".join(meta_parts))
            meta.setStyleSheet("color:#666; font-size:11px;")
            layout.addWidget(meta)

        return box

    def _add_buttons(self, layout, streamer):
        # 플랫폼 방송 버튼 — URL 자동 구성
        if url := streamer.chzzk_live_url():
            self._make_btn(layout, "Chzzk 방송", url)
        if url := streamer.cime_live_url():
            self._make_btn(layout, "씨미 방송", url)

        # 외부 링크 버튼
        for item in streamer.links:
            label = item.get("label", "")
            url = item.get("url", "")
            if label and url:
                self._make_btn(layout, label, url)

    def _make_btn(self, layout, label: str, url: str):
        btn = QPushButton(label)
        btn.setStyleSheet(
            "color: #ffffff; background-color: #2a2a2a;"
            "border: none; padding: 8px; font-size: 13px;"
        )
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
        layout.addWidget(btn)

    def _on_edit_clicked(self):
        key = self._streamer.key
        self._close()
        self.edit_requested.emit(key)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._close()
        else:
            super().keyPressEvent(event)

    def _close(self):
        self.closed.emit()
        self.deleteLater()
