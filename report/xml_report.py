# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Any

def generate_xml_report(test_results: Dict[str, Any], output_dir: str = "reports") -> str:
    """
    生成XML格式的测试报告
    
    Args:
        test_results: 测试结果数据
        output_dir: 输出目录
        
    Returns:
        报告文件路径
    """
    try:
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.xml"
        filepath = os.path.join(output_dir, filename)
        
        # 创建XML根元素
        root = ET.Element("test-report")
        
        # 添加基本信息
        info = ET.SubElement(root, "info")
        ET.SubElement(info, "generated-at").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(info, "framework").text = "Hypium Project Template"
        ET.SubElement(info, "version").text = "1.0"
        
        # 添加测试统计信息
        stats = ET.SubElement(root, "statistics")
        total_tests = len(test_results.get('tests', []))
        passed_tests = sum(1 for test in test_results.get('tests', []) if test.get('status') == 'passed')
        failed_tests = sum(1 for test in test_results.get('tests', []) if test.get('status') == 'failed')
        skipped_tests = sum(1 for test in test_results.get('tests', []) if test.get('status') == 'skipped')
        
        ET.SubElement(stats, "total-tests").text = str(total_tests)
        ET.SubElement(stats, "passed").text = str(passed_tests)
        ET.SubElement(stats, "failed").text = str(failed_tests)
        ET.SubElement(stats, "skipped").text = str(skipped_tests)
        ET.SubElement(stats, "pass-rate").text = f"{(passed_tests/total_tests*100) if total_tests > 0 else 0:.2f}%"
        
        # 添加测试用例
        tests = ET.SubElement(root, "tests")
        for test in test_results.get('tests', []):
            test_element = ET.SubElement(tests, "test")
            # 确保文本内容正确处理编码
            name = str(test.get('name', 'unknown'))
            status = str(test.get('status', 'unknown'))
            duration = str(test.get('duration', 0))
            start_time = str(test.get('start_time', 'unknown'))
            
            ET.SubElement(test_element, "name").text = name
            ET.SubElement(test_element, "status").text = status
            ET.SubElement(test_element, "duration").text = duration
            ET.SubElement(test_element, "start-time").text = start_time
            
            # 添加错误信息（如果有）
            if 'error_message' in test:
                error_msg = str(test.get('error_message', ''))
                ET.SubElement(test_element, "error-message").text = error_msg
            
            # 添加步骤
            steps = ET.SubElement(test_element, "steps")
            for step in test.get('steps', []):
                step_element = ET.SubElement(steps, "step")
                
                description = str(step.get('description', 'unknown'))
                step_status = str(step.get('status', 'unknown'))
                step_duration = str(step.get('duration', 0))
                
                ET.SubElement(step_element, "description").text = description
                ET.SubElement(step_element, "status").text = step_status
                ET.SubElement(step_element, "duration").text = step_duration
                
                # 添加步骤错误信息（如果有）
                if 'error_message' in step:
                    step_error = str(step.get('error_message', ''))
                    ET.SubElement(step_element, "error-message").text = step_error
        
        # 写入XML文件，确保正确编码
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        
        return filepath
        
    except Exception as e:
        print(f"生成XML报告时出错: {e}")
        raise