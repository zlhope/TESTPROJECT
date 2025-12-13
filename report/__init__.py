# -*- coding: utf-8 -*-
"""
报告模块初始化文件
"""

from .html_report import generate_html_report
from .json_report import generate_json_report
from .xml_report import generate_xml_report
from .result_collector import ResultCollector

__all__ = [
    'generate_html_report',
    'generate_json_report',
    'generate_xml_report',
    'ResultCollector'

]