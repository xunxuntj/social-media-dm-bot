from ppadb.client import Client as AdbClient
from loguru import logger
import time
import random

class ADBController:
    def __init__(self, device_serial=None):
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = self._connect_device(device_serial)

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
        """点击指定坐标"""
        actual_x = x + random.randint(-random_offset, random_offset)
        actual_y = y + random.randint(-random_offset, random_offset)
        self.device.shell(f'input tap {actual_x} {actual_y}')
        time.sleep(random.uniform(0.5, 1.5))

    def swipe(self, start_x, start_y, end_x, end_y, duration=300):
        """滑动操作"""
        self.device.shell(f'input swipe {start_x} {start_y} {end_x} {end_y} {duration}')
        time.sleep(random.uniform(0.5, 1.5))

    def input_text(self, text):
        """输入文本"""
        self.device.shell(f'input text "{text}"')
        time.sleep(random.uniform(0.5, 1.0))

    def launch_app(self, package_name):
        """启动应用"""
        self.device.shell(f'monkey -p {package_name} 1')
        time.sleep(3)  # 等待应用启动

    def get_screen_size(self):
        """获取屏幕分辨率"""
        output = self.device.shell('wm size')
        if 'Physical size:' in output:
            size = output.split(':')[1].strip()
            width, height = map(int, size.split('x'))
            return width, height
        return None, None