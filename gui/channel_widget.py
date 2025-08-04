import tkinter as tk
import webbrowser

class ChannelStatusWidget(tk.Frame):
    def __init__(self, master, Streamer, *args, **kwargs):
        super().__init__()
        self.config(bg="#000000")

        self.font_bold = ("Segoe UI", 13, "normal")
        self.font_normal = ("Segoe UI", 13, "normal")

        self.index = Streamer.index
        self.name = Streamer.name
        self.oshi_makr = Streamer.oshi_mark
        self.UID = Streamer.UID
        self.main_platform = Streamer.main_platform
        self.name = Streamer.oshi_mark
        self.chzzk_url = Streamer.chzzk_url
        self.soop_url = Streamer.soop_url
        self.fan_cafe_url = Streamer.fan_cafe
        self.youtube_url = Streamer.youtube
        self.twitter_url = Streamer.twitter_url

        self.label_name = tk.Label(self, text=self.name, bg="#000000", fg="black", cursor="hand2", font=self.font_normal)
        #self.label_platform = tk.Label(self, text=self.platform, bg="#000000", fg="black", cursor="hand2", font=self.font_normal)
        self.label_fan_cafe = tk.Label(self, text="팬카페", bg="#000000", fg="black", cursor="hand2", font=self.font_normal)
        self.label_youtube = tk.Label(self, text="유튜브", bg="#000000", fg="black", cursor="hand2", font=self.font_normal)
        self.label_twitter = tk.Label(self, text="트위터", bg="#000000", fg="black", cursor="hand2", font=self.font_normal)
        #self.label_twitter = tk.Label(self, text="트위터", bg="#000000", fg="blue", cursor="hand2", underline=True)#하이퍼링크처럼보이게하기

        self.label_name.grid(row=0, column=1, padx=5, pady=2, sticky='w')
        #self.label_platform.grid(row=0, column=2, padx=5, pady=2, sticky='w')
        self.label_fan_cafe.grid(row=0, column=3, padx=5, pady=2, sticky='w')
        self.label_youtube.grid(row=0, column=4, padx=5, pady=2, sticky='w')
        self.label_twitter.grid(row=0, column=5, padx=5, pady=2, sticky='w')



        self.grid_columnconfigure(1, minsize=105)
        self.grid_columnconfigure(2, minsize=80)
        self.grid_columnconfigure(3, minsize=50)
        self.grid_columnconfigure(4, minsize=50)
        self.grid_columnconfigure(5, minsize=50)

        # self.label_platform.bind("<Button-1>", self.on_platform_click)
        # self.label_fan_cafe.bind("<Button-1>", self.on_fan_cafe_click)
        # self.label_youtube.bind("<Button-1>", self.on_youtube_click)
        # self.label_twitter.bind("<Button-1>", self.on_twitter_click)
    # def on_platform_click(self, event):
    #     platform = self.platform.lower()
    #     if platform == "chzzk" and self.chzzk_url:
    #         webbrowser.open(self.chzzk_url)
    #     elif platform == "soop" and self.soop_url:
    #         webbrowser.open(self.soop_url)
    #     elif platform == "youtube" and self.youtube_url:
    #         webbrowser.open(self.youtube_url)
    #     else:
    #         print(f"플랫폼: {self.platform} 클릭됨, 열 URL 없음 또는 지원 안함")

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

    # def update_status(self, is_live: bool):
    #     if is_live:
    #         self.label_name.config(fg="blue", font=self.font_bold)
    #     else:
    #         self.label_name.config(fg="#d3d3d3", font=self.font_normal)  # 연한 회색

