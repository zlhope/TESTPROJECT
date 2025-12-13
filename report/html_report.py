# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from typing import Dict, List, Any

def generate_html_report(test_results: Dict[str, Any], output_dir: str = "reports") -> str:
    """
    生成HTML格式的测试报告
    
    Args:
        test_results: 测试结果数据
        output_dir: 输出目录
        
    Returns:
        报告文件路径
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 构建HTML内容
    html_content = build_html_content(test_results)
    
    # 生成报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_report_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath

def build_html_content(test_results: Dict[str, Any]) -> str:
    """
    构建HTML报告内容
    
    Args:
        test_results: 测试结果数据
        
    Returns:
        HTML字符串
    """
    # 获取测试统计信息
    total_tests = len(test_results.get('tests', []))
    passed_tests = sum(1 for test in test_results.get('tests', []) if test.get('status') == 'passed')
    failed_tests = sum(1 for test in test_results.get('tests', []) if test.get('status') == 'failed')
    skipped_tests = sum(1 for test in test_results.get('tests', []) if test.get('status') == 'skipped')
    
    # 构建HTML模板
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>移动应用测试报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .summary {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .test-cases {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .test-case {{
            margin-bottom: 15px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .test-name {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .test-status {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            margin-right: 10px;
        }}
        .passed {{ background-color: #d4edda; color: #155724; }}
        .failed {{ background-color: #f8d7da; color: #721c24; }}
        .skipped {{ background-color: #fff3cd; color: #856404; }}
        .test-time {{
            color: #666;
            font-size: 0.9em;
        }}
        .test-details {{
            margin-top: 10px;
            padding-left: 20px;
        }}
        .test-step {{
            margin-bottom: 5px;
        }}
        .step-status {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }}
        .step-passed {{ background-color: #28a745; }}
        .step-failed {{ background-color: #dc3545; }}
        .step-skipped {{ background-color: #ffc107; }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>移动应用测试报告</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="summary">
        <h2>测试概要</h2>
        <table>
            <tr>
                <td><strong>总测试用例数:</strong></td>
                <td>{total_tests}</td>
            </tr>
            <tr>
                <td><strong>通过:</strong></td>
                <td>{passed_tests}</td>
            </tr>
            <tr>
                <td><strong>失败:</strong></td>
                <td>{failed_tests}</td>
            </tr>
            <tr>
                <td><strong>跳过:</strong></td>
                <td>{skipped_tests}</td>
            </tr>
            <tr>
                <td><strong>通过率:</strong></td>
                <td>{(passed_tests/total_tests*100) if total_tests > 0 else 0:.2f}%</td>
            </tr>
        </table>
    </div>

    <div class="test-cases">
        <h2>测试用例详情</h2>
        {build_test_cases_html(test_results)}
    </div>

    <div class="footer">
        <p>测试框架: Hypium Project Template</p>
        <p>基于pytest和uiautomator2</p>
    </div>
</body>
</html>
    """
    
    return html_template

def build_test_cases_html(test_results: Dict[str, Any]) -> str:
    """
    构建测试用例HTML内容
    
    Args:
        test_results: 测试结果数据
        
    Returns:
        HTML字符串
    """
    test_cases_html = ""
    
    for test in test_results.get('tests', []):
        status_class = {
            'passed': 'passed',
            'failed': 'failed',
            'skipped': 'skipped'
        }.get(test.get('status'), 'skipped')
        
        test_cases_html += f"""
        <div class="test-case">
            <div class="test-name">{test.get('name', '未知测试')}</div>
            <div class="test-status {status_class}">{test.get('status').upper()}</div>
            <div class="test-time">执行时间: {test.get('duration', 'N/A')}秒</div>
            
            <div class="test-details">
                <div class="test-step">
                    <span class="step-status step-{test.get('status')}"></span>
                    <span>开始时间: {test.get('start_time', 'N/A')}</span>
                </div>
                
                {build_steps_html(test.get('steps', []))}
                
                {build_error_message(test.get('error_message', ''))}
            </div>
        </div>
        """
    
    return test_cases_html

def build_steps_html(steps: List[Dict[str, Any]]) -> str:
    """
    构建步骤HTML内容
    
    Args:
        steps: 步骤列表
        
    Returns:
        HTML字符串
    """
    steps_html = ""
    
    for step in steps:
        status_class = {
            'passed': 'passed',
            'failed': 'failed',
            'skipped': 'skipped'
        }.get(step.get('status'), 'skipped')
        
        steps_html += f"""
        <div class="test-step">
            <span class="step-status step-{status_class}"></span>
            <span>{step.get('description', '未知步骤')}</span>
            <span class="test-time">耗时: {step.get('duration', 'N/A')}ms</span>
        </div>
        """
    
    return steps_html

def build_error_message(error_message: str) -> str:
    """
    构建错误消息HTML内容
    
    Args:
        error_message: 错误消息
        
    Returns:
        HTML字符串
    """
    if error_message:
        return f"<div style='color: red; margin-top: 10px;'>错误: {error_message}</div>"
    return ""