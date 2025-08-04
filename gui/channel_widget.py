import tkinter as tk
import webbrowser

class ChannelStatusWidget(tk.Frame):
    def __init__(self, master, streamer, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(bg="#3b3b3b")

        # 스트리머 정보 저장
        self._setup_streamer_data(streamer)

        # 폰트 설정
        self._setup_fonts()

        # 라벨 생성 및 배치
        self._create_widgets()
        self._layout_widgets()

        # 이벤트 바인딩
        self._bind_events()

    def _setup_streamer_data(self, streamer):
        self.key= streamer.key
        self.name = f"{streamer.name}{streamer.get_extra_field('oshi_mark', '')}"
        self.uid = streamer.uid  # 대소문자 주의
        self.live_url = streamer.live_url
        
    def _setup_fonts(self):
        self.font_bold = ("Segoe UI", 13, "bold")
        self.font_normal = ("Segoe UI", 13, "normal")

    def _create_widgets(self):
        self.label_name = tk.Entry(self, bg="#3b3b3b", fg="white", font=self.font_normal,
                               borderwidth=0, highlightthickness=0, relief='flat', readonlybackground="#3b3b3b")
        self.label_name.insert(0, self.name)
        self.label_name.config(state="readonly", cursor="hand2")
        self.label_live_url = tk.Label(self, text=self.name, bg="#3b3b3b", fg="white", cursor="hand2", font=self.font_normal)

    def _layout_widgets(self):
        self.label_name.grid(row=0, column=1, padx=5, pady=2, sticky='w')
        self.grid_columnconfigure(1, minsize=105)

    def _bind_events(self):
        self.label_name.bind("<Double-Button-1>", self.on_name_click)

    # 이벤트 핸들러
    def on_name_click(self, event):
        if self.live_url:
            webbrowser.open(self.live_url)
        else:
            print("팬카페 URL이 없습니다.")
    # def on_fan_cafe_click(self, event):
    #     if self.fan_cafe_url:
    #         webbrowser.open(self.fan_cafe_url)
    #     else:
    #         print("팬카페 URL이 없습니다.")

    # def on_youtube_click(self, event):
    #     if self.youtube_url:
    #         webbrowser.open(self.youtube_url)
    #     else:
    #         print("유튜브 URL이 없습니다.")

    # def on_twitter_click(self, event):
    #     if self.twitter_url:
    #         webbrowser.open(self.twitter_url)
    #     else:
    #         print("트위터 URL이 없습니다.")
    
    def update_status(self, is_live: bool):
        if is_live:
            self.label_name.config(fg="blue", font=self.font_bold)
        else:
            self.label_name.config(fg="#242424", font=self.font_normal)  # 연한 회색
