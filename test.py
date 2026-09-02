#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cilent Website - 功能测试脚本
测试程序的各项功能是否正常
"""

import sys
import os

def test_imports():
    """测试导入"""
    print("=" * 50)
    print("测试1：导入模块")
    print("=" * 50)
    try:
        from main import WebsiteHubApp, AccessLogger, WebsiteRequestHandler, DownloadRequestHandler, ControlRequestHandler
        print("✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_directory_structure():
    """测试目录结构"""
    print("\n" + "=" * 50)
    print("测试2：目录结构")
    print("=" * 50)

    app_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.path.join(app_dir, 'index')
    download_dir = os.path.join(app_dir, 'request', 'download')
    control_dir = os.path.join(app_dir, 'request', 'control')

    checks = [
        (index_dir, "网站文件夹 (index)"),
        (download_dir, "下载文件夹 (request/download)"),
        (control_dir, "操控文件夹 (request/control)"),
    ]
    
    all_ok = True
    for path, name in checks:
        if os.path.exists(path) and os.path.isdir(path):
            print(f"✓ {name}: 存在")
        else:
            print(f"✗ {name}: 不存在或不是目录")
            all_ok = False
    
    return all_ok

def test_access_logger():
    """测试访问日志记录器"""
    print("\n" + "=" * 50)
    print("测试3：访问日志记录器")
    print("=" * 50)
    
    try:
        from main import AccessLogger
        
        logger = AccessLogger()
        print("✓ AccessLogger 实例创建成功")
        
        # 添加测试日志
        logger.add_log("192.168.1.1", "GET", "/index", 200, "Mozilla/5.0")
        logs = logger.get_logs()
        
        if len(logs) == 1 and logs[0]['ip'] == "192.168.1.1":
            print("✓ 日志记录功能正常")
        else:
            print("✗ 日志记录出错")
            return False
        
        # 测试清空
        logger.clear_logs()
        if len(logger.get_logs()) == 0:
            print("✓ 日志清空功能正常")
            return True
        else:
            print("✗ 日志清空出错")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_file_structure():
    """测试关键文件"""
    print("\n" + "=" * 50)
    print("测试4：关键文件")
    print("=" * 50)
    
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    files = [
        (os.path.join(app_dir, "main.py"), "主程序文件"),
        (os.path.join(app_dir, "README.md"), "说明文档"),
        (os.path.join(app_dir, "index", "index.html"), "示例主页"),
    ]
    
    all_ok = True
    for path, name in files:
        if os.path.exists(path) and os.path.isfile(path):
            size = os.path.getsize(path)
            print(f"✓ {name}: 存在 ({size} 字节)")
        else:
            print(f"✗ {name}: 不存在或不是文件")
            all_ok = False
    
    return all_ok

def test_control_feature():
    """测试远程操控功能"""
    print("\n" + "=" * 50)
    print("测试6：远程操控功能")
    print("=" * 50)

    import tempfile
    from main import find_entry_file, read_need_password, find_control_folder

    all_ok = True

    # 准备临时 control 目录
    tmp = tempfile.mkdtemp()
    try:
        # 场景1：无密码保护
        folder = os.path.join(tmp, 'test.exe')
        os.makedirs(folder)
        with open(os.path.join(folder, 'main.txt'), 'w', encoding='utf-8') as f:
            f.write('test')
        with open(os.path.join(folder, 'WEBSTIEHUB_RUNNING_INFO.ini'), 'w', encoding='utf-8') as f:
            f.write('NEED-PASSWORD=False\n')

        if find_entry_file(folder) and read_need_password(folder) is False:
            print("✓ 无密码配置解析正常")
        else:
            print("✗ 无密码配置解析出错")
            all_ok = False

        located, error = find_control_folder(tmp, 'test.exe')
        if error is None and located == folder:
            print("✓ 文件夹定位正常")
        else:
            print(f"✗ 文件夹定位出错: {error}")
            all_ok = False

        # 场景2：密码保护
        folder2 = os.path.join(tmp, 'calc.exe')
        os.makedirs(folder2)
        with open(os.path.join(folder2, 'main.bat'), 'w', encoding='utf-8') as f:
            f.write('@echo off\n')
        with open(os.path.join(folder2, 'WEBSTIEHUB_RUNNING_INFO.ini'), 'w', encoding='utf-8') as f:
            f.write('NEED-PASSWORD=7891dog.0\n')

        if read_need_password(folder2) == '7891dog.0':
            print("✓ 密码配置解析正常")
        else:
            print("✗ 密码配置解析出错")
            all_ok = False

        # 场景3：文件夹缺少必要文件
        folder3 = os.path.join(tmp, 'bad.exe')
        os.makedirs(folder3)
        with open(os.path.join(folder3, 'main.txt'), 'w', encoding='utf-8') as f:
            f.write('test')

        _, error = find_control_folder(tmp, 'bad.exe')
        if error == 400:
            print("✓ 缺少配置文件时返回 400")
        else:
            print(f"✗ 缺少配置文件时应返回 400，实际: {error}")
            all_ok = False

        # 场景4：不存在的文件夹
        _, error = find_control_folder(tmp, 'none.exe')
        if error == 404:
            print("✓ 不存在的文件夹返回 404")
        else:
            print(f"✗ 不存在的文件夹应返回 404，实际: {error}")
            all_ok = False

        # 场景5：路径遍历防护
        _, error = find_control_folder(tmp, '..%2f..%2fmain.py')
        if error == 403:
            print("✓ 路径遍历防护正常 (403)")
        else:
            print(f"✗ 路径遍历防护异常，实际: {error}")
            all_ok = False

    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    return all_ok

def test_syntax():
    """测试 Python 语法"""
    print("\n" + "=" * 50)
    print("测试5：Python 语法检查")
    print("=" * 50)
    
    import py_compile
    
    try:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        main_py = os.path.join(app_dir, "main.py")
        py_compile.compile(main_py, doraise=True)
        print("✓ main.py 语法正确")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ 语法错误: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "Cilent Website 功能测试" + " " * 13 + "║")
    print("╚" + "=" * 48 + "╝")
    
    tests = [
        test_imports,
        test_directory_structure,
        test_access_logger,
        test_file_structure,
        test_syntax,
        test_control_feature,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ 测试异常: {e}")
            results.append(False)
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n✅ 所有测试通过！程序已准备就绪。")
        print("\n使用方法:")
        print("  python main.py")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查环境。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
