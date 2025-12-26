1、功能：基于pytest改进的测试框架，支持控制任意用例组合</br>
2、各目录内容：</br>
    aw:方法库</br>
    config:测试用例执行控制，支持灵活选择任意用例</br>
    allure-results:测试报告输出目标</br>
    resource:测试资源</br>
        注：可以通过sdk/tools/bin/uiautomatorviewer.bat查看页面布局</br>
    testcases:测试用例</br>
    
3、执行方法：</br>
    1）python D:\TESTPROJECT\main.py（按config中配置的用例列表执行）</br>
    2）python D:\TESTPROJECT\main.py -m(按pytest mark分类执行)</br>

4、实时查看报告</br>
    allure serve ./allure-results</br>