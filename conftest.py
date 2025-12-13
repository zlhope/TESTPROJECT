# conftest.py
import pytest
import os
import xml.etree.ElementTree as ET
from report import ResultCollector
from aw.Utils import ConfigUtils

# 创建全局的test_collector实例
test_collector = None

def pytest_configure(config):
    """pytest配置时注册插件"""
    global test_collector
    test_collector = ResultCollector()
    config.pluginmanager.register(test_collector, "test-result-collector")


def pytest_collection_modifyitems(config, items):
    """
    修改测试项收集过程，如果没有指定测试用例，则从配置文件加载
    """
    # 检查是否通过命令行指定了测试用例
    file_or_dir = config.getoption("file_or_dir", [])
    
    # 如果没有指定测试用例，且没有通过标记(-m)选择，则从配置文件加载
    markexpr = config.getoption("-m", None)
    
    if not file_or_dir and not markexpr:
        # 尝试从配置文件加载测试套件
        config_path = "config/user_config.xml"
        if os.path.exists(config_path):
            try:
                config_root = ConfigUtils.load_xml_config(config_path)
                test_suite = ConfigUtils.get_test_suite_from_config(config_root)
                
                if test_suite:
                    print(f"从配置文件加载了 {len(test_suite)} 个测试用例:")
                    for i, case in enumerate(test_suite, 1):
                        print(f"  {i}. {case}")
                    
                    # 根据test_suite过滤测试项
                    selected_items = []
                    for item in items:
                        for test_case in test_suite:
                            # 精确匹配或前缀匹配
                            if item.nodeid == test_case or item.nodeid.startswith(test_case + "::"):
                                selected_items.append(item)
                                break
                    
                    # 更新items列表
                    items[:] = selected_items
                    print(f"最终选择 {len(items)} 个测试项执行")
                    
            except Exception as e:
                print(f"从配置文件读取测试套件时出错: {e}")   

def pytest_unconfigure(config):
    """pytest结束时生成报告"""
    global test_collector
    if test_collector:
        from report import generate_html_report, generate_json_report, generate_xml_report
        
        # 获取测试结果
        test_results = test_collector.get_results()
        
        # 只有当有测试结果时才生成报告
        if test_results and (test_results['summary']['total_tests'] > 0):
            print(f"\n收集到的测试结果: {test_results}")
            
            try:
                html_path = generate_html_report(test_results)
                json_path = generate_json_report(test_results)
                xml_path = generate_xml_report(test_results)
                    
                print(f"\n报告已生成:")
                print(f"HTML报告: {html_path}")
                print(f"JSON报告: {json_path}")
                print(f"XML报告: {xml_path}")
            except Exception as e:
                print(f"生成报告时出错: {e}")
        else:
            print("\n没有测试结果需要生成报告")