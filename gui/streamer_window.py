import tkinter as tk
import webbrowser

class StreamerLinkRow(tk.Frame):
    def __init__(self, master, streamer, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(bg="#3b3b3b")

        # 스트리머 정보 저장
        self.streamer = streamer
        self.key= streamer.key
        self.name = f"{streamer.name}{streamer.get_extra_field('oshi_mark', '')}"
        self.uid = streamer.uid  # 대소문자 주의
        self.live_url = streamer.live_url
        # 폰트 설정
        self.font_bold = ("Segoe UI", 13, "bold")
        self.font_normal = ("Segoe UI", 13, "normal")
        
        # 라벨 생성
        self.label_name = tk.Entry(self, bg="#3b3b3b", fg="white", font=self.font_normal,
                               borderwidth=0, highlightthickness=0, relief='flat', readonlybackground="#3b3b3b",width=12)
        self.label_name.insert(0, self.name)
        self.label_name.config(state="readonly", cursor="hand2")
        # extra_fields 기반으로 링크 버튼 생성
        LINK_LABELS = {
            "youtube_url": "유튜브",
            "official_community_url": "팬공간",
            "twitter_url": "X",
            "soop_url": "숲",
            "chzzk_url": "Chzzk",
            "youtube_contents_url": "ch.콘텐츠",
            "youtube_music_url": "ch.뮤직",
        }
        self.link_buttons = []
        for key, label in LINK_LABELS.items():
            url = self.streamer.get_extra_field(key)
            if url:
                btn = tk.Label(self, text=label, fg="white", bg="#1D1D1D", cursor="hand2", font=self.font_normal)
                btn.bind("<Button-1>", lambda e, link=url: webbrowser.open(link))
                self.link_buttons.append(btn)
        #라벨그리드
        self.label_name.grid(row=0, column=0, padx=2, pady=4, sticky='w')
        for idx, btn in enumerate(self.link_buttons):
            btn.grid(row=0, column=idx + 1, padx=4, pady=4,sticky='w')
        #self.grid_columnconfigure(1, minsize=105)
        #버튼 바인드
        self.label_name.bind("<Double-Button-1>", self.on_name_click)

    # 이벤트 핸들러
    def on_name_click(self, event):
        if self.live_url:
            webbrowser.open(self.live_url)
        else:
            print("live_URL실행 실패")
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
            self.label_name.config(fg="#F3F3F3", font=self.font_normal)
        else:
            self.label_name.config(fg="#747474", font=self.font_normal)  # 연한 회색
