# Cilent Website

## 项目概述

Cilent Website 是一个用 Python 开发的本地网站托管程序，提供图形化界面，支持在 localhost 上快速搭建和管理网站。本程序使用双端口模式，允许客户端使用互不干扰的端口浏览网页或下载文件。

## 主要功能

- ✅ **双端口**
  - 网站服务器（默认 8000 端口）：托管网站文件，允许用户在浏览器中免下载浏览网页
  - 下载服务器（默认 7000 端口）：提供文件下载，允许用户使用直链西在服务器中的文件

- ✅ **图形化管理界面**
  - 使用 tkinter 构建 GUI
  - 自定义网站和下载端口
  - 一键启动/停止/重启服务
  - 实时状态日志显示
  - 轻松上手，无需复杂命令

- ✅ **智能访问记录**
  - 完整的访问信息（时间、IP、请求方法、路径、状态码、User-Agent）
  - 支持查看和清空日志

- ✅ **灵活的路由规则**
  - 自动处理 `index.html` 映射
  - 支持目录和文件访问
  - 完整的路径访问支持

- ✅ **安全机制**
  - 路径遍历防护
  - MIME 类型自动识别
  - HTTP 状态码完整支持

## 文件结构
- 本条目是再刚刚完成下载后，Cilent Website 所提供的原始包，如果使用的是经过第三方修改的包，可能与此结构不匹配。请参考由修改方提供的```Readme.md```文件
```bash
Cilent Website/
├── main.py
├── index/
│   └── index.html
├── request/                
│   └── download/
└── README.md
```
  - ```Cilent Website```: 程序的根目录
  - ```Cilent Website\main.py```: 未经封装的主程序文件
  - ```Cilent Website\index\```: 网站文件夹，所有用户会请求的网页都会在此处
  - ```Cilent Website\index\index.html```: 实例HTML，可以删除此文件
  - ```Cilent Website\request\```: 所有客户端可能会请求的文件都在```request```文件夹的子文件夹中，目前只有```download```，我们可能会在之后的更新中添加其他子文件夹，具体参考对应版本的更新日志(```update.md```)
  - ```Cilent Website\request\download\```: 客户端所有会请求的文件都会存储在此文件夹中，此文件夹中的文件共客户端下载使用
  - ```Cilent Website\README.md```: 本文件，所有版本的Cilent Website中，```README.md```文件均为用户指南

## 使用步骤
从更新进度来看，正式版 落后 Preview版 落后 调试版。
- Releases版: Cilent Website 最稳定的版本，所有功能经过测试，但更新速度最慢，一般是经过测试的Preview版本。
- Preview版: Cilent Website的测试版，经过一定的测试，但可能存在一些问题，通常是预发布版本，但正在进行测试。此版本是新功能已经完全完整且未出现大规模错误的调试版，在Preview版本中再次进行几轮测试后，我们会将最终的Preview版作为Releases版发布。
- 调试版: 还没有封装的源代码文件，这个版本的功能是最新的，但可能有一些问题需要修复。使用此版本时，需要自行配置Python以及使用命令```python cilent_website.py```运行。

### 方案一：使用Releases/Preview版(推荐)
#### 1.下载并运行封装后的版本
您可以在我们的Github仓库(*https://github.com/oak90ghp/Cilent-Website/*)中，下载我们的Releases或Preview版本。下载完成后，请使用**管理员权限**运行主程序。
#### 2.按照提示操作
按照带有图形版本的提示操作本产品，并按照后文的**开始配置**进行配置。

### 方案二：使用调试版本
#### 1.下载Python
请确保您的电脑中已经安装了Python 3及更高版本的Python，您可以在```cmd.exe```中使用```python --version```命令检查是否已安装Python并查看Python版本。
#### 2.下载源代码
完成Python的安装或更新后，请可以在我们的Github仓库(*https://github.com/oak90ghp/Cilent-Website/*)中，下载我们的源代码文件```main.py```和启动文件```start.bat```。
### 3.启动调试版程序
完成如上文件的下载后，请问```main.py```和```start.bat```创建一个新的文件夹，并确保此文件夹的路径中没有任何中文字符。完成后，请使用管理员身份运行```start.bat```。如果您更改了```main.py```的文件名，请编辑```start.bat```并同步中的```python main.py```语句；您也可以在不下载```start.py```的情况下运行```main.py```，在确保Python已经安装后，在```main.py```所存在的根目录中打开```cmd.exe```，并输入```python main.py```。如果您的Python版本符合要求，调试版窗口就会启动。

## 访问规则详解

### 规则 1：index.html 自动映射
当访问的文件夹中有一个 `index.html` 文件时且要请求此页面时，可以省略```index.html```，但如果要请求的不是```index.html```，则必须加上对应的文件名。

**示例：**
- 文件路径：`index/hosting/help/index.html`
- 访问地址：`http://localhost:8000/hosting/help`

### 规则 2：具体文件访问
当需要访问具体的 HTML 文件时，需要在地址栏中指定文件名。

**示例：**
- 文件路径：`index/hosting/help/pageone.html`
- 访问地址：`http://localhost:8000/hosting/help/pageone.html`

### 规则 3：目录列表
如果文件夹中没有 `index.html`，将显示文件夹内容列表。

### 规则 4：下载文件路径映射
下载服务器将 `request/download` 文件夹映射到下载端口的根目录。

**示例：**
- 文件位置：`request/download/main.exe`
- 下载地址：`http://localhost:7000/main.exe`

## 🎮 管理界面按钮说明

| 按钮 | 功能 | 备注 |
|------|------|------|
| 启动服务 | 启动网站和下载服务 | 启动后按钮变灰，端口配置项锁定 |
| 停止服务 | 停止所有服务 | 仅在服务运行时可用 |
| 重启服务 | 快速重启服务 | 仅在服务运行时可用 |
| 访问记录 | 查看完整的访问日志 | 显示时间、IP、请求信息等 |

## 📊 访问日志信息

访问记录包含以下信息：

| 字段 | 说明 |
|------|------|
| 时间 | 请求时间（YYYY-MM-DD HH:MM:SS） |
| IP地址 | 访问者的 IP 地址 |
| 请求方法 | GET、POST 等 HTTP 方法 |
| 请求路径 | 访问的相对路径 |
| 状态码 | HTTP 状态码（200、404、500 等） |
| User-Agent | 访问者的浏览器信息 |

## 开始配置
恭喜！您已经完成了所有准备工作，马上就能开始使用Cilent Website 了。
### 准备网页
本程序支持各类网页形式，我们最推荐的格式是HTML格式。请将您编写好的HTML文件存储到```Cilent Website\index```中。由于本程序支持自动映射index.html，所以如果您的文件夹中中只有一个文件，请将唯一的文件命名为```index.html```，本产品就会自动减少地址栏输入。
```bash
Cilent Website/
├── main.py
├── index/
│   └── demo/
|       └──index.html
├── request/                
│   └── download/
└── README.md
```
例如此文件格式，当demo中只有一个文件时，只需要在浏览器中输入```localhost:8000\index\demo```，此程序就会自动向浏览器发送```Cilent Website/index/demo/index.html```。
```bash
Cilent Website/
├── main.py
├── index/
│   └── demo/
|       └──page_one.html
|       └──page_two.html
├── request/                
│   └── download/
└── README.md
```
请在看此文件格式，由于```Cilent Website/index/demo```中有两个文件，所以您需要在浏览器中输入完整地址。例如当您想访问```Cilent Website/index/demo/page_one.html```时，您就必须在浏览器中输入```localhost:8000\index\demo\page_one.html```，程序才会向浏览器发送```page_one.html```; 同理，当您想访问```Cilent Website/index/demo/page_two.html```时，您就需要输入```localhost:8000\index\demo\page_two.html```。
### 下载文件
此程序支持下载文件，只需要跳转到您所指定的下载端口即可完成下载。请参考如下文件格式:
```bash
Cilent Website/
├── main.py
├── index/
│   └── demo/
|       └──index.html
├── request/                
│   └── download/
│       └── cilent_proxy
|           └── main.py
|           └── main.exe
|           └── README.md
│       └── cilent_website
|           └── main.py
|           └── main.exe
|           └── README.md
│       └── help.md
└── README.md
```
例如，当您请求```Cilent Website/request/download/cilent_website/README.md```时，只需要让网页跳转至```localhost:7000/cilent_website/README.md```即可下载；同理，当您请求```Cilent Website/request/download/help.md```时，只需要让浏览器跳转至```localhost:7000/help.md```即可。对于HTML，您可以参考此语句：
```html
<a href="http://localhost:7000/filename.ext">下载文件</a>
```

## 🔧 常见问题

### Q: 如何修改默认端口？
A: 在管理界面中修改"网站端口"和"下载端口"的值，然后点击"启动服务"。

### Q: 端口已被占用如何处理？
A: 在管理界面中修改为未被占用的端口号即可。

### Q: 如何暂停服务但保留配置？
A: 点击"停止服务"按钮，配置会被保留。再次点击"启动服务"可恢复。

### Q: 程序能否处理中文文件名？
A: 支持，但建议使用英文文件名以获得最佳兼容性。

## 安全性说明

- 程序实现了路径遍历防护，防止访问指定文件夹外的文件
- 建议在内网或本地环境使用
- 不建议在互联网上直接暴露此服务

---

**Cilent Website** - Designed by oak90ghp.
