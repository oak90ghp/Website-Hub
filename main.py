#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cilent Website - 本地网站托管程序
提供两个端口：
- 网站端口（默认8000）：用于托管网站内容
- 下载端口（默认7000）：用于提供文件下载
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import http.server
import socketserver
import threading
import os
import sys
import json
from datetime import datetime
from urllib.parse import unquote
import mimetypes
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AccessLogger:
    """访问日志记录器"""
    def __init__(self):
        self.logs = []
    
    def add_log(self, ip, method, path, status_code, user_agent='', timestamp=None):
        """添加访问记录"""
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = {
            'timestamp': timestamp,
            'ip': ip,
            'method': method,
            'path': path,
            'status_code': status_code,
            'user_agent': user_agent
        }
        self.logs.append(log_entry)
    
    def get_logs(self):
        """获取所有访问日志"""
        return self.logs
    
    def clear_logs(self):
        """清空日志"""
        self.logs = []


class WebsiteRequestHandler(http.server.SimpleHTTPRequestHandler):
    """网站请求处理器"""
    
    # 类变量，指向访问日志记录器
    access_logger = None
    index_dir = None
    
    def do_GET(self):
        """处理GET请求"""
        client_ip = self.client_address[0]
        path = unquote(self.path)
        
        # 记录访问
        if self.access_logger:
            user_agent = self.headers.get('User-Agent', '')
            self.access_logger.add_log(client_ip, 'GET', path, 0, user_agent)
        
        # 移除查询字符串
        if '?' in path:
            path = path.split('?')[0]
        
        # 移除前导斜杠
        if path.startswith('/'):
            path = path[1:]
        
        # 构建文件系统路径
        full_path = os.path.join(self.index_dir, path)
        
        # 安全检查：防止路径遍历
        try:
            full_path = os.path.normpath(os.path.abspath(full_path))
            if not full_path.startswith(os.path.abspath(self.index_dir)):
                self.send_error(403, "Forbidden")
                if self.access_logger:
                    self.access_logger.logs[-1]['status_code'] = 403
                return
        except Exception as e:
            self.send_error(400, "Bad Request")
            if self.access_logger:
                self.access_logger.logs[-1]['status_code'] = 400
            return
        
        # 检查路径是否存在
        if not os.path.exists(full_path):
            self.send_error(404, "Not Found")
            if self.access_logger:
                self.access_logger.logs[-1]['status_code'] = 404
            return
        
        # 如果是目录
        if os.path.isdir(full_path):
            # 检查是否存在index.html
            index_path = os.path.join(full_path, 'index.html')
            if os.path.isfile(index_path):
                # 发送index.html
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(index_path, 'rb') as f:
                    self.wfile.write(f.read())
                if self.access_logger:
                    self.access_logger.logs[-1]['status_code'] = 200
                return
            else:
                # 列出目录内容
                self.list_directory(full_path)
                if self.access_logger:
                    self.access_logger.logs[-1]['status_code'] = 200
                return
        
        # 如果是文件
        if os.path.isfile(full_path):
            try:
                # 确定MIME类型
                mime_type, _ = mimetypes.guess_type(full_path)
                if mime_type is None:
                    mime_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.send_header('Content-Length', os.path.getsize(full_path))
                self.end_headers()
                
                with open(full_path, 'rb') as f:
                    self.wfile.write(f.read())
                
                if self.access_logger:
                    self.access_logger.logs[-1]['status_code'] = 200
            except Exception as e:
                self.send_error(500, "Internal Server Error")
                if self.access_logger:
                    self.access_logger.logs[-1]['status_code'] = 500
    
    def list_directory(self, path):
        """列出目录内容"""
        try:
            list_html = '<html><head><title>目录列表</title></head><body>'
            list_html += f'<h1>目录列表: /{self.path}</h1><ul>'
            
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    list_html += f'<li><a href="/{self.path.lstrip("/")}/{item}/">{item}/</a></li>'
                else:
                    list_html += f'<li><a href="/{self.path.lstrip("/")}/{item}">{item}</a></li>'
            
            list_html += '</ul></body></html>'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(list_html.encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """重写日志输出"""
        pass  # 禁用默认日志


class DownloadRequestHandler(http.server.SimpleHTTPRequestHandler):
    """下载服务请求处理器"""
    
    access_logger = None
    download_dir = None
    
    def do_GET(self):
        """处理GET请求"""
        client_ip = self.client_address[0]
        path = unquote(self.path)
        
        # 记录访问
        if self.access_logger:
            user_agent = self.headers.get('User-Agent', '')
            self.access_logger.add_log(client_ip, 'GET (Download)', path, 0, user_agent)
        
        # 移除查询字符串
        if '?' in path:
            path = path.split('?')[0]
        
        # 移除前导斜杠
        if path.startswith('/'):
            path = path[1:]
        
        # 构建文件系统路径
        full_path = os.path.join(self.download_dir, path)
        
        # 安全检查
        try:
            full_path = os.path.normpath(os.path.abspath(full_path))
            if not full_path.startswith(os.path.abspath(self.download_dir)):
                self.send_error(403, "Forbidden")
                if self.access_logger:
                    self.access_logger.logs[-1]['status_code'] = 403
                return
        except Exception as e:
            self.send_error(400, "Bad Request")
            if self.access_logger:
                self.access_logger.logs[-1]['status_code'] = 400
            return
        
        # 检查文件是否存在
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            self.send_error(404, "Not Found")
            if self.access_logger:
                self.access_logger.logs[-1]['status_code'] = 404
            return
        
        # 发送文件
        try:
            mime_type, _ = mimetypes.guess_type(full_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.send_header('Content-Length', os.path.getsize(full_path))
            self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(full_path)}"')
            self.end_headers()
            
            with open(full_path, 'rb') as f:
                self.wfile.write(f.read())
            
            if self.access_logger:
                self.access_logger.logs[-1]['status_code'] = 200
        except Exception as e:
            self.send_error(500, "Internal Server Error")
            if self.access_logger:
                self.access_logger.logs[-1]['status_code'] = 500
    
    def log_message(self, format, *args):
        """重写日志输出"""
        pass


class ClientWebsiteApp:
    """主应用程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Cilent Website - 本地网站托管")
        self.root.geometry("800x600")
        
        # 获取程序根目录
        if getattr(sys, 'frozen', False):
            self.app_dir = os.path.dirname(sys.executable)
        else:
            self.app_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.index_dir = os.path.join(self.app_dir, 'index')
        self.download_dir = os.path.join(self.app_dir, 'request', 'download')
        
        # 确保目录存在
        os.makedirs(self.index_dir, exist_ok=True)
        os.makedirs(self.download_dir, exist_ok=True)
        
        # 初始化访问日志
        self.access_logger = AccessLogger()
        
        # 服务器变量
        self.website_server = None
        self.download_server = None
        self.website_thread = None
        self.download_thread = None
        self.website_running = False
        self.download_running = False
        
        # 默认端口
        self.website_port = 8000
        self.download_port = 7000
        
        # 创建UI
        self.create_ui()
    
    def create_ui(self):
        """创建用户界面"""
        # 标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="Cilent Website - 本地网站托管程序", 
                               font=('Arial', 14, 'bold'))
        title_label.pack()
        
        # 配置部分
        config_frame = ttk.LabelFrame(self.root, text="服务器配置", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 网站端口
        ttk.Label(config_frame, text="网站端口:").grid(row=0, column=0, sticky=tk.W)
        self.website_port_var = tk.StringVar(value="8000")
        self.website_port_entry = ttk.Entry(config_frame, textvariable=self.website_port_var, width=10)
        self.website_port_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 下载端口
        ttk.Label(config_frame, text="下载端口:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.download_port_var = tk.StringVar(value="7000")
        self.download_port_entry = ttk.Entry(config_frame, textvariable=self.download_port_var, width=10)
        self.download_port_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # 目录信息
        info_frame = ttk.LabelFrame(self.root, text="目录信息", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"程序根目录: {self.app_dir}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"网站文件夹: index/").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"下载文件夹: request/download/").pack(anchor=tk.W)
        
        # 控制按钮
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_button = ttk.Button(control_frame, text="启动服务", command=self.start_servers)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="停止服务", command=self.stop_servers, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.restart_button = ttk.Button(control_frame, text="重启服务", command=self.restart_servers, state=tk.DISABLED)
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        self.logs_button = ttk.Button(control_frame, text="访问记录", command=self.show_logs)
        self.logs_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        self.status_frame = ttk.LabelFrame(self.root, text="服务状态", padding=10)
        self.status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.status_text = scrolledtext.ScrolledText(self.status_frame, height=10, width=80)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_status("系统就绪。请配置端口并启动服务。")
    
    def log_status(self, message):
        """在状态窗口记录消息"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def start_servers(self):
        """启动服务器"""
        try:
            # 获取端口
            self.website_port = int(self.website_port_var.get())
            self.download_port = int(self.download_port_var.get())
            
            if self.website_port == self.download_port:
                messagebox.showerror("错误", "网站端口和下载端口不能相同！")
                return
            
            # 启动网站服务器
            WebsiteRequestHandler.access_logger = self.access_logger
            WebsiteRequestHandler.index_dir = self.index_dir
            
            self.website_server = socketserver.TCPServer(("localhost", self.website_port), WebsiteRequestHandler)
            self.website_thread = threading.Thread(target=self.website_server.serve_forever, daemon=True)
            self.website_thread.start()
            self.website_running = True
            self.log_status(f"✓ 网站服务已启动 (localhost:{self.website_port})")
            
            # 启动下载服务器
            DownloadRequestHandler.access_logger = self.access_logger
            DownloadRequestHandler.download_dir = self.download_dir
            
            self.download_server = socketserver.TCPServer(("localhost", self.download_port), DownloadRequestHandler)
            self.download_thread = threading.Thread(target=self.download_server.serve_forever, daemon=True)
            self.download_thread.start()
            self.download_running = True
            self.log_status(f"✓ 下载服务已启动 (localhost:{self.download_port})")
            
            # 更新按钮和输入框状态
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.restart_button.config(state=tk.NORMAL)
            self.website_port_entry.config(state=tk.DISABLED)
            self.download_port_entry.config(state=tk.DISABLED)
            
            self.log_status("✓ 所有服务启动成功！")
            self.log_status(f"网站访问地址: http://localhost:{self.website_port}")
            self.log_status(f"文件下载地址: http://localhost:{self.download_port}")
            
        except Exception as e:
            self.log_status(f"✗ 启动失败: {str(e)}")
            messagebox.showerror("启动失败", f"无法启动服务器:\n{str(e)}")
    
    def stop_servers(self):
        """停止服务器"""
        try:
            if self.website_server:
                self.website_server.shutdown()
                self.website_server = None
                self.website_running = False
                self.log_status("✓ 网站服务已停止")
            
            if self.download_server:
                self.download_server.shutdown()
                self.download_server = None
                self.download_running = False
                self.log_status("✓ 下载服务已停止")
            
            # 更新按钮和输入框状态
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.restart_button.config(state=tk.DISABLED)
            self.website_port_entry.config(state=tk.NORMAL)
            self.download_port_entry.config(state=tk.NORMAL)
            
            self.log_status("✓ 所有服务已停止")
        except Exception as e:
            self.log_status(f"✗ 停止失败: {str(e)}")
    
    def restart_servers(self):
        """重启服务器"""
        self.stop_servers()
        self.root.after(500, self.start_servers)
    
    def show_logs(self):
        """显示访问日志"""
        logs = self.access_logger.get_logs()
        
        if not logs:
            messagebox.showinfo("访问记录", "暂无访问记录")
            return
        
        # 创建新窗口
        log_window = tk.Toplevel(self.root)
        log_window.title("Cilent Website - 访问记录")
        log_window.geometry("1000x600")
        
        # 创建表格
        frame = ttk.Frame(log_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        log_text = scrolledtext.ScrolledText(frame, height=30, width=120, yscrollcommand=scrollbar.set)
        log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=log_text.yview)
        
        # 写入日志
        log_text.insert(tk.END, f"{'时间':<20} {'IP地址':<15} {'请求方法':<15} {'请求路径':<40} {'状态码':<8} {'User-Agent':<30}\n")
        log_text.insert(tk.END, "=" * 130 + "\n")
        
        for log in logs:
            user_agent = log.get('user_agent', '')[:25] if log.get('user_agent') else ''
            line = f"{log['timestamp']:<20} {log['ip']:<15} {log['method']:<15} {log['path']:<40} {log['status_code']:<8} {user_agent:<30}\n"
            log_text.insert(tk.END, line)
        
        log_text.config(state=tk.DISABLED)
        
        # 添加清空按钮
        button_frame = ttk.Frame(log_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def clear_logs():
            self.access_logger.clear_logs()
            log_text.config(state=tk.NORMAL)
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, f"{'时间':<20} {'IP地址':<15} {'请求方法':<15} {'请求路径':<40} {'状态码':<8} {'User-Agent':<30}\n")
            log_text.insert(tk.END, "=" * 130 + "\n")
            log_text.config(state=tk.DISABLED)
            messagebox.showinfo("成功", "访问记录已清空")
        
        ttk.Button(button_frame, text="清空记录", command=clear_logs).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="关闭", command=log_window.destroy).pack(side=tk.LEFT, padx=5)


def main():
    """主函数"""
    root = tk.Tk()
    app = ClientWebsiteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()