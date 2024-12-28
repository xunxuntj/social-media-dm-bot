# src/test_adb.py
import os
import sys
import time
from loguru import logger

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from adb_controller import ADBController

def test_basic_operations():
    try:
        # 创建 ADB 控制器实例
        controller = ADBController(device_serial="cae466d9")
        
        # 1. 基本信息测试
        logger.info("Testing basic device information...")
        width, height = controller.get_screen_size()
        logger.info(f"Screen size: {width}x{height}")
        
        # 2. 屏幕控制测试
        logger.info("Testing screen control...")
        controller.screen_on()
        time.sleep(1)
        logger.info("Screen should be ON now")
        
        # 3. 导航操作测试
        logger.info("Testing navigation operations...")
        controller.go_home()
        time.sleep(1)
        logger.info("Should be at home screen now")
        
        # 4. 滑动测试
        logger.info("Testing swipe operation...")
        # 从屏幕中下部向上滑动
        start_y = int(height * 0.7)
        end_y = int(height * 0.3)
        controller.swipe(width//2, start_y, width//2, end_y, 300)
        logger.info("Swipe completed")
        
        # 5. 应用检查测试
        logger.info("Testing app checks...")
        test_package = "com.android.settings"  # 测试系统设置应用
        is_installed = controller.check_if_app_installed(test_package)
        logger.info(f"Settings app installed: {is_installed}")
        
        # 6. 获取当前活动测试
        logger.info("Testing current activity...")
        current_activity = controller.get_current_activity()
        logger.info(f"Current activity: {current_activity}")
        
        # 7. 文本输入测试（可选）
        response = input("Would you like to test text input? (yes/no): ")
        if response.lower() == 'yes':
            controller.go_home()
            time.sleep(1)
            logger.info("Please open a text input field manually...")
            time.sleep(3)
            controller.input_text("Hello from ADB!")
            
        logger.info("All basic operations completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting ADB controller test...")
    test_basic_operations()