# 🚀 Cilent Website - 快速开始指南

## 第一步：启动程序

打开命令行，进入程序目录，运行：

```bash
python main.py
```

会弹出 **Cilent Website** 管理界面。

## 第二步：配置端口（可选）

在管理界面中：
- **网站端口**：默认 8000（可自定义）
- **下载端口**：默认 7000（可自定义）

> 💡 确保两个端口不相同且未被其他程序占用

## 第三步：启动服务

点击 **"启动服务"** 按钮，状态窗口会显示：

```
✓ 网站服务已启动 (localhost:8000)
✓ 下载服务已启动 (localhost:7000)
✓ 所有服务启动成功！
```

## 第四步：上传网站文件

将你的网页文件放在 `index/` 文件夹中：

```
index/
├── index.html          # 主页
├── style.css
├── script.js
└── pages/
    ├── index.html
    └── about.html
```

## 第五步：访问网站

在浏览器中访问：
- **主页**：http://localhost:8000
- **子页面**：http://localhost:8000/pages/about.html

## 第六步：添加下载功能

### 6.1 放置下载文件

将文件放在 `request/download/` 文件夹：

```
request/download/
├── main.exe
├── document.pdf
└── image.zip
```

### 6.2 在 HTML 中添加下载链接

```html
<a href="http://localhost:7000/main.exe">下载程序</a>
<a href="http://localhost:7000/document.pdf">下载文档</a>
<a href="http://localhost:7000/image.zip">下载图片</a>
```

## 📋 访问规则参考

### 规则 1：自动 index.html 映射

| 文件位置 | 访问地址 |
|---------|---------|
| `index/help/index.html` | `localhost:8000/help` |
| `index/docs/faq/index.html` | `localhost:8000/docs/faq` |

### 规则 2：直接访问 HTML 文件

| 文件位置 | 访问地址 |
|---------|---------|
| `index/help/page1.html` | `localhost:8000/help/page1.html` |
| `index/docs/manual.html` | `localhost:8000/docs/manual.html` |

### 规则 3：下载文件

| 文件位置 | 下载地址 |
|---------|---------|
| `request/download/app.exe` | `localhost:7000/app.exe` |
| `request/download/docs/file.pdf` | `localhost:7000/docs/file.pdf` |

## 🎮 管理界面操作

### 启动/停止服务

- ✅ **启动服务**：点击按钮启动两个服务
- ⏹️ **停止服务**：点击按钮停止所有服务
- 🔄 **重启服务**：快速重新启动

### 查看访问记录

点击 **"访问记录"** 按钮查看：

```
时间                 IP地址         请求方法      请求路径            状态码
2024-01-01 10:30:45  192.168.1.100  GET          /                  200
2024-01-01 10:31:12  192.168.1.100  GET          /style.css         200
2024-01-01 10:31:15  192.168.1.100  GET (Download) /main.exe         200
```

支持清空记录。

## 🛠️ 常见问题

### Q: 如何修改端口？
**A:** 在启动服务前，修改界面上的端口号，然后启动即可。

### Q: 如何添加 CSS 和 JavaScript？
**A:** 直接放在 `index/` 目录中，在 HTML 中引用即可：
```html
<link rel="stylesheet" href="/style.css">
<script src="/script.js"></script>
```

### Q: 如何创建多层目录结构？
**A:** 正常创建文件夹即可：
```
index/
└── hosting/
    ├── help/
    │   ├── index.html     (访问: /hosting/help)
    │   └── faq.html       (访问: /hosting/help/faq.html)
    └── docs/
        └── index.html     (访问: /hosting/docs)
```

### Q: 如何让外网访问？
**A:** 修改代码中的 `"localhost"` 为 `"0.0.0.0"` 或你的 IP 地址。不建议直接暴露到互联网。

### Q: 端口被占用怎么办？
**A:** 更改为其他可用端口，如 8001、8080、9000 等。

### Q: 如何编译为 EXE 文件？
**A:** 安装 PyInstaller 后运行：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## 📝 文件清单

```
Cilent Website/
├── main.py              ← 主程序（直接运行）
├── test.py              ← 功能测试脚本
├── README.md            ← 完整说明文档
├── QUICKSTART.md        ← 本文件
├── index/               ← 网站文件夹（你的网页在这里）
│   └── index.html       ← 示例主页
└── request/download/    ← 下载文件夹（需要下载的文件在这里）
```

## 🎯 典型使用流程

```
1. python main.py              启动程序
   ↓
2. 配置端口（可选）
   ↓
3. 点击"启动服务"
   ↓
4. 在 index/ 放置网页文件
   ↓
5. 在浏览器中访问 http://localhost:8000
   ↓
6. 在 request/download/ 放置下载文件
   ↓
7. 在 HTML 中添加下载链接
   ↓
8. 查看"访问记录"了解用户活动
```

## ✨ 功能特性

- ✅ 图形化管理界面（无需命令行）
- ✅ 双端口架构（网站 + 下载分离）
- ✅ 自动 index.html 映射
- ✅ 完整的访问日志
- ✅ 一键启动/停止/重启
- ✅ 自定义端口支持
- ✅ 中文界面和日志
- ✅ 路径安全防护

## 📞 需要帮助？

1. 查看 README.md 获取详细信息
2. 运行 `python test.py` 诊断问题
3. 检查状态窗口的错误消息

---

**现在你可以开始使用 Cilent Website 了！** 🎉
