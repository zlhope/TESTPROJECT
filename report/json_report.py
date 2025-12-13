# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from typing import Dict, Any

def generate_json_report(test_results: Dict[str, Any], output_dir: str = "reports") -> str:
    """
    生成JSON格式的测试报告
    
    Args:
        test_results: 测试结果数据
        output_dir: 输出目录
        
    Returns:
        报告文件路径
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_report_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # 写入JSON文件
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    return filepath