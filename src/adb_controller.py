# src/adb_controller.py
from ppadb.client import Client as AdbClient
from loguru import logger
import time
import random

class ADBController:
    def __init__(self, device_serial=None):
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = self._connect_device(device_serial)
        self.screen_width, self.screen_height = self.get_screen_size()

    def _connect_device(self, device_serial):
        """连接到设备"""
        devices = self.client.devices()
        if not devices:
            raise Exception("No devices connected")
        
        if device_serial:
            device = next((d for d in devices if d.serial == device_serial), None)
            if not device:
                raise Exception(f"Device with serial {device_serial} not found")
        else:
            device = devices[0]

        logger.info(f"Connected to device: {device.serial}")
        return device

    def tap(self, x, y, random_offset=10):
        """点击指定坐标，带随机偏移"""
        actual_x = x + random.randint(-random_offset, random_offset)
        actual_y = y + random.randint(-random_offset, random_offset)
        # 确保坐标不超出屏幕范围
        actual_x = max(0, min(actual_x, self.screen_width))
        actual_y = max(0, min(actual_y, self.screen_height))
        self.device.shell(f'input tap {actual_x} {actual_y}')
        time.sleep(random.uniform(0.5, 1.5))

    def swipe(self, start_x, start_y, end_x, end_y, duration=300):
        """滑动操作，可控制持续时间"""
        self.device.shell(f'input swipe {start_x} {start_y} {end_x} {end_y} {duration}')
        time.sleep(random.uniform(0.5, 1.5))

    def input_text(self, text):
        """输入文本"""
        # 替换特殊字符，因为 adb shell input text 命令对特殊字符敏感
        safe_text = text.replace(' ', '%s').replace('&', '\\&').replace('<', '\\<').replace('>', '\\>')
        self.device.shell(f'input text "{safe_text}"')
        time.sleep(random.uniform(0.5, 1.0))

    def press_keycode(self, keycode):
        """按下特定按键"""
        self.device.shell(f'input keyevent {keycode}')
        time.sleep(0.5)

    def get_screen_size(self):
        """获取屏幕分辨率"""
        output = self.device.shell('wm size')
        if 'Physical size:' in output:
            size = output.split(':')[1].strip()
            width, height = map(int, size.split('x'))
            return width, height
        return None, None

    def launch_app(self, package_name):
        """启动应用"""
        self.device.shell(f'monkey -p {package_name} 1')
        time.sleep(3)  # 等待应用启动

    def force_stop_app(self, package_name):
        """强制停止应用"""
        self.device.shell(f'am force-stop {package_name}')
        time.sleep(1)

    def check_if_app_installed(self, package_name):
        """检查应用是否已安装"""
        result = self.device.shell(f'pm list packages {package_name}')
        return package_name in result

    def get_current_activity(self):
        """获取当前活动的应用和Activity"""
        result = self.device.shell('dumpsys window windows | grep -E "mCurrentFocus|mFocusedApp"')
        return result

    def screen_on(self):
        """打开屏幕"""
        self.device.shell('input keyevent 224')
        time.sleep(1)

    def screen_off(self):
        """关闭屏幕"""
        self.device.shell('input keyevent 26')
        time.sleep(1)

    def go_home(self):
        """按下Home键"""
        self.press_keycode(3)

    def go_back(self):
        """按下返回键"""
        self.press_keycode(4)