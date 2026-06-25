from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSignal
from tool.paths import ASSETS_DIR

COLUMNS = 5
EMPTY_ROWS = 2  # always keep this many extra rows of empty slots


def _fmt_since(since: str) -> str:
    try:
        if "T" in since:
            from datetime import datetime
            dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            return dt.astimezone().strftime("%m/%d %H:%M")
        return since[5:16].replace("-", "/")
    except Exception:
        return since


def _fmt_range(since: str, end: str) -> str:
    if not end:
        return _fmt_since(since)
    try:
        from datetime import datetime
        fmt = "%Y-%m-%d %H:%M:%S"
        dt_s = datetime.strptime(since, fmt)
        dt_e = datetime.strptime(end, fmt)
        mins = int((dt_e - dt_s).total_seconds()) // 60
        h, m = divmod(mins, 60)
        duration = f"{h}시간 {m}분" if h else f"{m}분"
        s_str = since[5:16].replace("-", "/")
        e_str = end[11:16]
        return f"{s_str} ~ {e_str}  ({duration})"
    except Exception:
        return _fmt_since(since)


class StreamerCell(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, streamer):
        super().__init__()
        self._streamer = streamer
        self.key = streamer.key
        self.oshi = streamer.oshi_mark or streamer.name[0]
        self.is_live = streamer.is_live

        self._color_px = self._load_pixmap()
        self._gray_px = self._to_grayscale(self._color_px) if self._color_px else None

        self._label = QLabel(self)
        self._label.setFixedSize(80, 80)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_status()
        self._update_tooltip()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(self._label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _load_pixmap(self) -> QPixmap | None:
        for ext in ("png", "webp", "jpg"):
            path = ASSETS_DIR / f"{self.key}.{ext}"
            if path.exists():
                break
        else:
            return None
        px = QPixmap(str(path)).scaled(
            80, 80,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        return px if not px.isNull() else None

    def _to_grayscale(self, px: QPixmap) -> QPixmap:
        img = px.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
        return QPixmap.fromImage(img)

    def _apply_status(self):
        if self._color_px:
            self._label.setPixmap(self._color_px if self.is_live else self._gray_px)
            self._label.setText("")
        else:
            self._label.setPixmap(QPixmap())
            self._label.setStyleSheet("color: #FFFFFF; font-size: 18px;")
            self._label.setText(self.oshi)

        effect = QGraphicsOpacityEffect(self._label)
        effect.setOpacity(1.0 if self.is_live else 0.3)
        self._label.setGraphicsEffect(effect)

    def update_status(self, is_live: bool):
        self.is_live = is_live
        self._apply_status()
        self._update_tooltip()

    def _update_tooltip(self):
        s = self._streamer
        if not s.live_title and not s.live_since:
            self.setToolTip("")
            return
        parts = []
        if not self.is_live:
            parts.append("마지막 방송")
        if s.live_title:
            parts.append(s.live_title)
        if s.live_category:
            parts.append(s.live_category)
        if s.live_since:
            parts.append(_fmt_range(s.live_since, s.live_end if not self.is_live else ""))
        self.setToolTip("\n".join(parts))

    def mousePressEvent(self, event):
        self.clicked.emit(self.key)
        super().mousePressEvent(event)


class EmptyCell(QWidget):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedSize(88, 88)
        self.setStyleSheet(
            "background-color: #1e1e1e;"
            "border: 1px dashed #3a3a3a;"
            "border-radius: 4px;"
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class HomeView(QWidget):
    streamer_clicked = pyqtSignal(str)
    add_requested = pyqtSignal()

    def __init__(self, streamer_dict):
        super().__init__()
        self.setStyleSheet("background-color: #080808;")
        self._grid = QGridLayout(self)
        self._grid.setSpacing(4)
        self._cells: dict[str, StreamerCell] = {}
        self._empty_cells: list[EmptyCell] = []

        for streamer in streamer_dict.values():
            cell = StreamerCell(streamer)
            cell.clicked.connect(self.streamer_clicked)
            self._cells[streamer.key] = cell

        self.refresh_order()

    def refresh_tooltips(self):
        for cell in self._cells.values():
            cell._update_tooltip()

    def update_status(self, key: str, is_live: bool):
        if key not in self._cells:
            return
        if self._cells[key].is_live == is_live:
            return
        self._cells[key].update_status(is_live)
        self.refresh_order()

    def _sync_empty_pool(self, count: int):
        while len(self._empty_cells) < count:
            empty = EmptyCell()
            empty.clicked.connect(self.add_requested)
            self._empty_cells.append(empty)
        for empty in self._empty_cells[count:]:
            self._grid.removeWidget(empty)
            empty.setParent(None)
        del self._empty_cells[count:]

    def refresh_order(self):
        for cell in self._cells.values():
            self._grid.removeWidget(cell)
        for empty in self._empty_cells:
            self._grid.removeWidget(empty)

        sorted_cells = sorted(
            self._cells.values(),
            key=lambda cell: (not cell.is_live, cell.key)
        )

        occupied = len(sorted_cells)
        col_remainder = occupied % COLUMNS
        padding = (COLUMNS - col_remainder) % COLUMNS
        empty_count = padding + EMPTY_ROWS * COLUMNS
        self._sync_empty_pool(empty_count)

        for idx, cell in enumerate(sorted_cells):
            row, col = divmod(idx, COLUMNS)
            self._grid.addWidget(cell, row, col)

        for i, empty in enumerate(self._empty_cells):
            row, col = divmod(occupied + i, COLUMNS)
            self._grid.addWidget(empty, row, col)
