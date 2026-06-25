from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QScrollArea, QWidget, QLabel
)
from PyQt6.QtCore import pyqtSignal


class LinkRow(QWidget):
    remove_requested = pyqtSignal(object)

    def __init__(self, label="", url=""):
        super().__init__()
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)

        self.label_edit = QLineEdit(label)
        self.label_edit.setPlaceholderText("라벨")
        self.label_edit.setFixedWidth(70)

        self.url_edit = QLineEdit(url)
        self.url_edit.setPlaceholderText("URL")

        rm = QPushButton("✕")
        rm.setFixedWidth(24)
        rm.setStyleSheet("color:#888; background:transparent; border:none;")
        rm.clicked.connect(lambda: self.remove_requested.emit(self))

        row.addWidget(self.label_edit)
        row.addWidget(self.url_edit)
        row.addWidget(rm)

    def data(self) -> dict | None:
        label = self.label_edit.text().strip()
        url = self.url_edit.text().strip()
        return {"label": label, "url": url} if label and url else None


class StreamerEditorDialog(QDialog):
    saved = pyqtSignal(dict)
    deleted = pyqtSignal(str)

    def __init__(self, streamer=None, parent=None):
        super().__init__(parent)
        self.streamer = streamer
        self.setWindowTitle("스트리머 편집" if streamer else "스트리머 추가")
        self.setMinimumWidth(300)
        self.setStyleSheet("""
            QDialog { background-color: #1a1a1a; color: #ffffff; }
            QLineEdit {
                background: #2a2a2a; color: #fff;
                border: 1px solid #333; border-radius: 4px;
                padding: 6px 8px; font-size: 13px;
            }
            QLineEdit:focus { border-color: #555; }
            QLabel { color: #888; font-size: 11px; }
        """)

        outer = QVBoxLayout(self)
        outer.setSpacing(8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        body = QVBoxLayout(content)
        body.setSpacing(10)
        body.setContentsMargins(2, 2, 2, 2)
        scroll.setWidget(content)
        outer.addWidget(scroll)

        self._name  = QLineEdit(streamer.name if streamer else "")
        self._oshi  = QLineEdit(streamer.oshi_mark if streamer else "")
        self._c_uid = QLineEdit(streamer.chzzk.get("uid", "") if streamer else "")
        self._ci_hdl = QLineEdit(streamer.cime.get("handle", "") if streamer else "")

        body.addLayout(self._field("이름 *", self._name))
        body.addLayout(self._field("오시마크", self._oshi))

        body.addWidget(self._section("CHZZK"))
        body.addLayout(self._field("UID", self._c_uid))

        body.addWidget(self._section("CIME"))
        body.addLayout(self._field("Handle  (@없이)", self._ci_hdl))

        body.addWidget(self._section("링크"))
        self._link_container = QVBoxLayout()
        self._link_container.setSpacing(4)
        self._link_rows: list[LinkRow] = []
        for item in (streamer.links if streamer else []):
            self._add_link_row(item.get("label", ""), item.get("url", ""))
        body.addLayout(self._link_container)

        add_link = QPushButton("+ 링크 추가")
        add_link.setStyleSheet(
            "color:#666; background:transparent; border:1px dashed #333;"
            "border-radius:4px; padding:5px; font-size:12px;"
        )
        add_link.clicked.connect(lambda: self._add_link_row())
        body.addWidget(add_link)
        body.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        save_btn = QPushButton("저장")
        save_btn.setStyleSheet(
            "background:#2a7a2a; color:#fff; border:none;"
            "border-radius:4px; padding:7px;"
        )
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)

        if streamer:
            del_btn = QPushButton("삭제")
            del_btn.setStyleSheet(
                "background:#7a2a2a; color:#fff; border:none;"
                "border-radius:4px; padding:7px;"
            )
            del_btn.clicked.connect(self._delete)
            btn_row.addWidget(del_btn)

        cancel_btn = QPushButton("취소")
        cancel_btn.setStyleSheet(
            "background:#2a2a2a; color:#aaa; border:none;"
            "border-radius:4px; padding:7px;"
        )
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        outer.addLayout(btn_row)

    def _field(self, label_text: str, widget) -> QVBoxLayout:
        vbox = QVBoxLayout()
        vbox.setSpacing(3)
        lbl = QLabel(label_text)
        vbox.addWidget(lbl)
        vbox.addWidget(widget)
        return vbox

    def _section(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color:#aaa; font-size:12px; font-weight:bold; letter-spacing:1px;"
            "border-bottom:1px solid #444; padding-bottom:4px; margin-top:8px;"
        )
        return lbl

    def _add_link_row(self, label="", url=""):
        row = LinkRow(label, url)
        row.remove_requested.connect(self._remove_link_row)
        self._link_rows.append(row)
        self._link_container.addWidget(row)

    def _remove_link_row(self, row: LinkRow):
        self._link_rows.remove(row)
        self._link_container.removeWidget(row)
        row.deleteLater()

    def _save(self):
        if not self._name.text().strip():
            return
        d: dict = {
            "key": self.streamer.key if self.streamer
                   else self._name.text().strip().lower().replace(" ", "_"),
            "name": self._name.text().strip(),
            "oshi_mark": self._oshi.text().strip(),
        }
        if self._c_uid.text().strip():
            d["chzzk"] = {"uid": self._c_uid.text().strip()}
        if self._ci_hdl.text().strip():
            d["cime"] = {"handle": self._ci_hdl.text().strip().lstrip("@")}
        d["links"] = [r.data() for r in self._link_rows if r.data()]
        self.saved.emit(d)
        self.accept()

    def _delete(self):
        self.deleted.emit(self.streamer.key)
        self.accept()
