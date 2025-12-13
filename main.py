# -*- coding: utf-8 -*-
import pytest
import sys
import os
import io
import locale
import xml.etree.ElementTree as ET
from typing import Dict, Any, List

# 设置标准输入输出编码
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'


from aw.Utils import ConfigUtils
from report import ResultCollector,generate_html_report, generate_json_report, generate_xml_report

# 创建TestResultCollector实例
test_collector = ResultCollector()

def load_config():
    """
    加载配置文件
    """
    config_path = "config/user_config.xml"
    if os.path.exists(config_path):
        try:
            config = ConfigUtils.load_xml_config(config_path)
            print(f"配置文件加载成功: {config_path}")
            return config
        except Exception as e:
            print(f"错误: 无法加载配置文件: {str(e)}")
            return None
    else:
        print(f"警告: 配置文件不存在: {config_path}")
        return None

def run_tests():
    """
    运行测试的主要函数
    """

    # 加载配置
    config = load_config()

    # 获取命令行参数
    args = sys.argv[1:]
    
    # 构建pytest命令
    pytest_args = [
        "--tb=short",  # 简洁的错误追踪
        "-v",          # 详细输出
        "testcases/"
    ]    
    
    # 从配置文件获取测试套件
    test_suite = ConfigUtils.get_test_suite_from_config(config)
    
    if test_suite:
        print(f"从配置文件加载了 {len(test_suite)} 个测试用例:")
        for i, case in enumerate(test_suite, 1):
            print(f"  {i}. {case}")
        # 添加测试用例到参数
        pytest_args.extend(test_suite)
    else:
        # 如果配置文件中没有测试套件，则默认执行testcases目录
        print("配置文件中未找到测试套件，执行默认测试目录")
        pytest_args.append("testcases/")

    # 添加额外参数
    if "--device-id" in args:
        device_id = args[args.index("--device-id") + 1]
        pytest_args.extend(["--device-id", device_id])
    
    if "--app-package" in args:
        app_package = args[args.index("--app-package") + 1]
        pytest_args.extend(["--app-package", app_package])
    
    # 运行pytest并获取结果
    try:
        exit_code = pytest.main(pytest_args,plugins=[test_collector])
    except UnicodeDecodeError as e:
        print(f"pytest运行时遇到编码错误: {e}")
        print("尝试使用UTF-8环境变量重新运行...")
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        exit_code = pytest.main(pytest_args)
    
    # 无论测试结果如何都生成报告
    # 获取真实的测试结果
    test_results = test_collector.get_results()
    print(f"收集到的测试结果: {test_results}")  # 调试信息

    # 添加调试信息
    print(f"测试用例数量: {len(test_results['tests'])}")
    for test in test_results['tests']:
        print(f"测试用例: {test['full_name']}, 状态: {test['status']}")

    # 生成不同格式的报告
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
    
    return exit_code

        
if __name__ == "__main__":
    # 设置默认编码环境
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except locale.Error:
            pass  # 使用系统默认
    
    # 加载配置
    #load_config()
    
    # 运行测试
    exit_code = run_tests()
    
    # 退出程序
    sys.exit(exit_code)