# -*- coding: utf-8 -*-
import uiautomator2 as u2
import xml.etree.ElementTree as ET
import json
import time
from typing import Dict, Any, Optional, List

class DeviceUtils:
    """
    设备操作工具类
    """
    
    @staticmethod
    def connect_device(device_id: str = None) -> u2.Device:
        """
        连接设备
        
        Args:
            device_id: 设备ID
            
        Returns:
            uiautomator2设备实例
        """
        try:
            if device_id:
                return u2.connect(device_id)
            else:
                return u2.connect()
        except Exception as e:
            raise ConnectionError(f"无法连接到设备 {device_id}: {str(e)}")
    
    @staticmethod
    def get_device_info(device: u2.Device) -> Dict[str, Any]:
        """获取设备信息"""
        info = device.info
        return {
            "deviceName": info.get("deviceName", ""),
            "brand": info.get("brand", ""),
            "model": info.get("model", ""),
            "sdkVersion": info.get("sdkVersion", ""),
            "platformVersion": info.get("platformVersion", "")
        }
    
    @staticmethod
    def screenshot(device: u2.Device, filename: str = None) -> Any:
        """截图"""
        return device.screenshot(filename)
    
    @staticmethod
    def press_key(device: u2.Device, key: str):
        """按下按键"""
        device.press(key)
    
    @staticmethod
    def wait_for_element(device: u2.Device, locator: Dict[str, Any], timeout: int = 10) -> bool:
        """等待元素出现"""
        try:
            element = device(**locator)
            return element.wait(timeout=timeout)
        except Exception:
            return False

class ConfigUtils:
    """
    配置文件处理工具类
    """
    
    @staticmethod
    def load_xml_config(config_path: str) -> Dict[str, Any]:
        """加载多层嵌套XML配置文件"""
        try:
            tree = ET.parse(config_path)
            root = tree.getroot()
            
            def parse_element(element):
                """递归解析XML元素"""
                result = {}
                
                # 处理元素属性
                if element.attrib:
                    result['@attributes'] = element.attrib
                
                # 处理子元素
                children = list(element)
                if children:
                    child_dict = {}
                    for child in children:
                        child_data = parse_element(child)
                        if child.tag in child_dict:
                            # 如果标签已存在，转换为列表
                            if not isinstance(child_dict[child.tag], list):
                                child_dict[child.tag] = [child_dict[child.tag]]
                            child_dict[child.tag].append(child_data)
                        else:
                            child_dict[child.tag] = child_data
                    result.update(child_dict)
                
                # 处理文本内容
                if element.text and element.text.strip():
                    if result:
                        result['#text'] = element.text.strip()
                    else:
                        return element.text.strip()
                
                return result
            
            return {root.tag: parse_element(root)}
            
        except Exception as e:
            raise ValueError(f"无法解析配置文件 {config_path}: {str(e)}")
    

    @staticmethod
    def load_json_config(config_path: str) -> Dict[str, Any]:
        """加载JSON配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"无法解析配置文件 {config_path}: {str(e)}")
        
    @staticmethod
    def get_test_suite_from_config(config_dict) -> List[str]:
        """
        从字典格式的配置中获取测试套件列表
        """
        if config_dict is not None:
            # 获取根标签名
            root_tag = list(config_dict.keys())[0] if config_dict.keys() else None
            
            if root_tag and root_tag in config_dict:
                # 检查 testsuite 是否存在
                if 'testsuite' in config_dict[root_tag]:
                    test_suite_data = config_dict[root_tag]['testsuite']
                    
                    # 如果是字符串，直接处理
                    if isinstance(test_suite_data, str):
                        return [case.strip() for case in test_suite_data.split(',') if case.strip()]
                    # 如果是字典且包含#text键
                    elif isinstance(test_suite_data, dict) and '#text' in test_suite_data:
                        return [case.strip() for case in test_suite_data['#text'].split(',') if case.strip()]
                    # 如果是字典但不包含#text键，检查是否有文本内容
                    elif isinstance(test_suite_data, dict):
                        # 尝试获取文本内容的不同方式
                        text_content = test_suite_data.get('#text', '')
                        
                        if not text_content and len(test_suite_data) == 1:
                            # 如果字典只有一个键值对，且值是字符串，可能是文本内容
                            for key, value in test_suite_data.items():
                                if isinstance(value, str) and key != '@attributes':
                                    text_content = value
                                    break
                        
                        if text_content:
                            return [case.strip() for case in text_content.split(',') if case.strip()]
        return []

class TestUtils:
    """
    测试工具类
    """
    
    @staticmethod
    def assert_equal(actual: Any, expected: Any, message: str = ""):
        """断言相等"""
        assert actual == expected, message or f"期望值: {expected}, 实际值: {actual}"
    
    @staticmethod
    def assert_not_equal(actual: Any, expected: Any, message: str = ""):
        """断言不相等"""
        assert actual != expected, message or f"期望值不等于: {expected}, 但实际值为: {actual}"
    
    @staticmethod
    def assert_true(condition: bool, message: str = ""):
        """断言为真"""
        assert condition, message or "断言条件为假"
    
    @staticmethod
    def assert_false(condition: bool, message: str = ""):
        """断言为假"""
        assert not condition, message or "断言条件为真"