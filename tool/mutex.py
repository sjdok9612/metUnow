import ctypes

mutex_handle = None  # 전역 선언

def check_mutex(mutex_name="Global\\MeechuNow"):
    global mutex_handle
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    mutex_handle = kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.get_last_error()

    ERROR_ALREADY_EXISTS = 183
    if last_error == ERROR_ALREADY_EXISTS:
        print("이미 실행 중입니다.")
        return False
    return True

def release_mutex():
    global mutex_handle
    if mutex_handle:  # 체크할 수 있도록
        ctypes.windll.kernel32.CloseHandle(mutex_handle)
        mutex_handle = None