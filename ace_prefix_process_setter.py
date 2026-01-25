import psutil
import ctypes
import ctypes.wintypes
from threading import Event
import sys

# -------------------------- 全局配置 --------------------------
CHECK_INTERVAL = 30  # 检测间隔（秒）
CPU_AFFINITY_MASK = 0xF00000  # 十六进制F00000，对应CPU核心20-23
PROCESS_ALL_ACCESS = 0x1F0FFF
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
IO_PRIORITY_LOW = 0x00000001
GPU_PRIORITY_BELOW_NORMAL = 0x00000001
PROCESS_POWER_THROTTLING_EFFICIENCY_MODE = 0x00000002

# -------------------------- 单例模式（防止重复启动） --------------------------
def is_single_instance():
    try:
        mutex_name = "Global\\AcePrefixProcessSetter_Singleton_Mutex"
        ctypes.windll.kernel32.CreateMutexW(None, ctypes.c_bool(True), mutex_name)
        return ctypes.windll.kernel32.GetLastError() != 0x000000B7  # ERROR_ALREADY_EXISTS
    except:
        return False

# -------------------------- 进程属性设置 --------------------------
def set_process_all_attributes(pid):
    """统一设置单个进程的所有目标属性，静默执行"""
    try:
        # 1. 获取进程句柄
        h_process = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if h_process == 0:
            return

        # 2. 设置CPU优先级（低于正常）
        psutil.Process(pid).nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

        # 3. 设置CPU亲和性（转换位掩码为核心列表）
        cpu_cores = []
        mask, core_idx = CPU_AFFINITY_MASK, 0
        while mask > 0:
            if mask & 1:
                cpu_cores.append(core_idx)
            mask >>= 1
            core_idx += 1
        if cpu_cores:
            psutil.Process(pid).cpu_affinity(cpu_cores)

        # 4. 设置I/O优先级（低）
        ctypes.windll.kernel32.SetProcessInformation(
            h_process, 0x00000002, ctypes.byref(ctypes.c_ulong(IO_PRIORITY_LOW)), ctypes.sizeof(ctypes.c_ulong)
        )

        # 5. 设置GPU优先级（低于正常）
        ctypes.windll.kernel32.SetProcessInformation(
            h_process, 0x00000007, ctypes.byref(ctypes.c_ulong(GPU_PRIORITY_BELOW_NORMAL)), ctypes.sizeof(ctypes.c_ulong)
        )

        # 6. 开启效能模式
        class PROCESS_POWER_THROTTLING_STATE(ctypes.Structure):
            _fields_ = [("Version", ctypes.wintypes.DWORD), ("ControlMask", ctypes.wintypes.DWORD), ("StateMask", ctypes.wintypes.DWORD)]

        throttling = PROCESS_POWER_THROTTLING_STATE()
        throttling.Version = 1
        throttling.ControlMask = throttling.StateMask = PROCESS_POWER_THROTTLING_EFFICIENCY_MODE
        ctypes.windll.kernel32.SetProcessInformation(
            h_process, 0x00000008, ctypes.byref(throttling), ctypes.sizeof(throttling)
        )

        # 7. 释放进程句柄
        ctypes.windll.kernel32.CloseHandle(h_process)
    except:
        pass  # 静默忽略所有错误，不生成日志

# -------------------------- 核心检测逻辑（前缀模糊匹配） --------------------------
def monitor_and_set_processes():
    """每30秒检测所有Ace开头进程，设置属性"""
    stop_event = Event()
    while not stop_event.is_set():
        try:
            # 遍历所有进程，匹配以Ace开头（不分大小写）的进程
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name']
                    if proc_name and proc_name.lower().startswith("ace"):  # 不分大小写前缀匹配
                        set_process_all_attributes(proc.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            stop_event.wait(CHECK_INTERVAL)  # 无阻塞延时，比time.sleep更优雅
        except:
            stop_event.wait(CHECK_INTERVAL)
            continue

# -------------------------- 程序入口 --------------------------
if __name__ == "__main__":
    if not is_single_instance():
        sys.exit(0)
    monitor_and_set_processes()
