# -*- coding: utf-8 -*-
"""
#!!================================================================
#版权 (C) 2025, zltech Co., Ltd. 保留所有权利。
#==================================================================
#文 件 名：                 Jingdong2.py
#文件说明：                 
#作    者：                 zltech
#生成日期：                 2025-10-23
#!!================================================================
"""

import pytest
import allure
import time
import os
import sys
import json
# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
testcases_dir = os.path.dirname(current_file)
project_root = os.path.dirname(testcases_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from aw.Utils import DeviceUtils, ConfigUtils, TestUtils
from resource.locators import LOCATORS
# 加载XML配置文件
config_path = os.path.join(project_root, "config", "user_config.xml")
user_config = ConfigUtils.load_xml_config(config_path)
case_config_path = os.path.join(project_root, "testcases", "test_Jingdong2.json")
case_config = ConfigUtils.load_json_config(case_config_path)

@allure.feature("京东应用测试")
@allure.story("特价功能")
class TestCase:
    """
    测试用例类
    """
    
    @allure.step("初始化测试环境")
    def setup_method(self,method):
        """测试方法前执行"""
        self.device = DeviceUtils.connect_device(user_config['configuration']['device']['id'])
        self.device.implicitly_wait(10)

    @allure.step("清理测试环境")    
    def teardown_method(self,method):
        """测试方法后执行"""
        if hasattr(self, 'device'):
            self.device.app_stop(case_config["config"]["package"])
        
    @allure.title("测试打开特价功能")
    @allure.description("验证用户能够成功打开京东特价功能并进入特价界面")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "tejia")
    def test_open_tejia(self):
        """测试打开特价"""
        with allure.step("启动京东应用"):    
            self.device.app_start(case_config["config"]["package"])
            self.device.implicitly_wait(10)
        
        with allure.step("等待应用首页加载完成"):
            time.sleep(5)
            login_page = self.device(**LOCATORS["firstpage"])        
        
        
        with allure.step("查找并点击特价按钮"):
            time.sleep(5)
            #self.device(**LOCATORS["tejia"]).click_gone(maxretry=3, interval=2.0)
            # 使用ADB命令点击特价按钮
            tejia_element = self.device(**LOCATORS["tejia"])
            if tejia_element.exists:
                # 获取元素中心坐标
                info = tejia_element.info
                x = info['bounds']['left'] + (info['bounds']['right'] - info['bounds']['left']) // 2
                y = info['bounds']['top'] + (info['bounds']['bottom'] - info['bounds']['top']) // 2
                # 使用ADB命令执行点击
                result=self.device.shell(f"input tap {x} {y} && sleep 10") 
                if result:
                    allure.attach("点击执行成功", "点击状态", allure.attachment_type.TEXT)
                    print("点击成功")
                else:
                    allure.attach("点击可能失败", "点击状态", allure.attachment_type.TEXT)
                    print("点击可能失败")

            else:
                allure.attach("特价按钮未找到", "错误信息", allure.attachment_type.TEXT)
                pytest.fail("特价按钮未找到")

            time.sleep(5)
            #判断“9.9包邮”出现”
            baoyou = self.device(**LOCATORS["baoyou"])
            assert baoyou.wait(timeout=10), "未进入特价界面"

