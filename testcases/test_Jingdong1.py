# -*- coding: utf-8 -*-
"""
#!!================================================================
#版权 (C) 2025, zltech Co., Ltd. 保留所有权利。
#==================================================================
#文 件 名：                 Jingdong1.py
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
case_config_path = os.path.join(project_root, "testcases", "test_Jingdong1.json")
case_config = ConfigUtils.load_json_config(case_config_path)

@allure.feature("京东应用测试")
@allure.story("登录功能")
class TestCase:
    """
    测试用例类
    """
    
    @allure.step("初始化测试环境")
    def setup_method(self, method):
        """测试方法前执行"""
        self.device = DeviceUtils.connect_device(user_config['configuration']['device']['id'])
        self.device.implicitly_wait(10)
        
    @allure.step("清理测试环境")
    def teardown_method(self, method):
        """测试方法后执行"""
        if hasattr(self, 'device'):
            self.device.app_stop(case_config["config"]["package"])
    
    @pytest.mark.smoke
    @allure.title("测试登录成功")
    @allure.description("验证用户能够成功启动京东应用并进入首页")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "login")    
    def test_login_success(self):
        """测试登录成功"""
        with allure.step("启动京东应用"):
            self.device.app_start(case_config["config"]["package"])
            self.device.implicitly_wait(10)
        
        with allure.step("等待应用加载"):
            time.sleep(5)

        with allure.step("检查首页是否出现"):    
            # 等待“首页”出现
            login_page = self.device(**LOCATORS["firstpage"])

        with allure.step("验证首页加载成功"):    
            assert login_page.wait(timeout=10), "首页未出现"
        
    
