import fcntl
import os

LOCK_PATH = "/tmp/metUnow.lock"
_lock_fd = None


def check_mutex(mutex_name=None) -> bool:
    global _lock_fd
    try:
        _lock_fd = open(LOCK_PATH, "w")
        fcntl.flock(_lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        _lock_fd.write(str(os.getpid()))
        _lock_fd.flush()
        return True
    except IOError:
        print("프로그램이 이미 실행 중입니다.")
        return False


def release_mutex():
    global _lock_fd
    if _lock_fd:
        fcntl.flock(_lock_fd, fcntl.LOCK_UN)
        _lock_fd.close()
        _lock_fd = None
        try:
            os.remove(LOCK_PATH)
        except OSError:
            pass
