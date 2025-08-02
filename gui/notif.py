from notifypy import Notify

def send_notification(title: str, message: str = "", duration: int = 3):
    """
    데스크탑 알림을 보냅니다.

    Args:
        title (str): 알림 제목
        message (str): 알림 메시지 (선택)
        duration (int): 알림 지속 시간 (초, 일부 OS만 지원)
    """
    notif = Notify()
    notif.title = title
    notif.message = message
    notif.duration = duration
    notif.send()
    
# def send_notifications_for_changes(channels_status):
#     """
#     channels_status 리스트를 순회하며
#     is_live 상태가 변경된 채널에 대해 알림을 보냅니다.

#     각 ChannelStatus 객체에
#     이전 상태(prev_is_live) 속성을 미리 저장해둬야 하며,
#     상태 변경 시 알림을 보내고 prev_is_live 갱신까지 수행합니다.

#     Args:
#         channels_status (list): ChannelStatus 객체 리스트
#     """
#     for channel in channels_status:
#         # prev_is_live 속성 존재 여부 확인
#         if not hasattr(channel, 'prev_is_live'):
#             channel.prev_is_live = channel.is_live  # 초기값 설정
#             continue

#         if channel.is_live != channel.prev_is_live:
#             notif = Notify()
#             status_text = "방송ON" if channel.is_live else "방송OFF"
#             notif.title = f"{channel.nickname} {status_text}"
#             notif.send()

#             # 상태 갱신
#             channel.prev_is_live = channel.is_live