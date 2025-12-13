# result_collector.py
import pytest
import time

class ResultCollector:
    def __init__(self):
        self.test_results = {
            "tests": [],
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "pass_rate": "0.00%"
            }
        }
    
    def pytest_runtest_makereport(self, item, call):
        """收集每个测试的结果"""
        if call.when == "call":
            existing_test = None
            for test in self.test_results["tests"]:
                if test["full_name"] == item.nodeid:
                    existing_test = test
                    break

            if existing_test is None:
                test_info = {
                    "name": item.name,
                    "full_name": item.nodeid,
                    "status": "passed" if call.excinfo is None else "failed",
                    "duration": call.stop - call.start if call.stop and call.start else 0,
                    "start_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(call.start)) if call.start else "",
                    "steps": [],
                    "error_message": ""
                }

                if call.excinfo:
                    test_info["error_message"] = str(call.excinfo.exconly())

                self.test_results["tests"].append(test_info)
            else:
                if call.excinfo:
                    existing_test["status"] = "failed"
                    existing_test["error_message"] = str(call.excinfo.exconly())
    
    def pytest_terminal_summary(self, terminalreporter):
        """在测试结束后统计汇总信息"""
        stats = terminalreporter.stats

        passed = len(stats.get('passed', []))
        failed = len(stats.get('failed', []))
        skipped = len(stats.get('skipped', []))
        total = passed + failed + skipped

        self.test_results["summary"]["passed"] = passed
        self.test_results["summary"]["failed"] = failed
        self.test_results["summary"]["skipped"] = skipped
        self.test_results["summary"]["total_tests"] = total

        if total > 0:
            pass_rate = (passed / total) * 100
            self.test_results["summary"]["pass_rate"] = f"{pass_rate:.2f}%"
        else:
            self.test_results["summary"]["pass_rate"] = "0.00%"
    
    def get_results(self):
        return self.test_results

# 创建全局实例
test_collector = ResultCollector()