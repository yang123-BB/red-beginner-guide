# 第04章：计算机网络基础深度解析

**课程难度**：⭐⭐ (初级)  
**预计时间**：60-90分钟  
**课程类型**：理论+实践

---

## 📋 学习目标

完成本章学习后，您将能够：

1. **理解网络分层模型**
   - 掌握OSI七层模型和TCP/IP四层模型的结构
   - 理解各层的功能和协议
   - 能够分析数据包在不同层的封装过程

2. **掌握网络协议分析**
   - 深入理解以太网帧、IP数据包、TCP/UDP段的结构
   - 掌握HTTP/HTTPS协议的工作原理
   - 理解DNS、DHCP、ARP、ICMP等核心协议

3. **熟练使用网络工具**
   - 掌握Wireshark抓包分析技巧
   - 熟练使用常用网络命令进行故障排查
   - 能够分析网络流量和识别异常行为

4. **具备安全防护意识**
   - 了解常见网络攻击原理（ARP欺骗、DNS劫持等）
   - 掌握基本的网络防御措施
   - 能够配置基础的安全策略

---

## 📚 背景知识

### 1. 网络通信的本质

计算机网络是现代信息社会的基石。从最早的ARPANET到今天的互联网，网络通信技术的发展改变了整个世界。对于网络安全从业者来说，理解网络通信原理不仅是基础知识，更是进行安全分析、漏洞挖掘、入侵检测的必备技能。

#### 1.1 为什么需要网络分层？

想象一下，如果没有分层设计，所有的网络通信功能都要写在一个庞大的程序中，任何改动都可能影响整个系统。分层设计带来了以下优势：

- **模块化**：每一层只关心自己的功能，各司其职
- **标准化**：不同厂商的设备可以互相通信
- **简化问题**：将复杂问题分解为多个小问题
- **易于维护**：某一层的变化不会影响其他层

这就像建造一栋大楼，有设计师、结构工程师、电工、管道工等，每个人负责自己的专业领域，通过标准化的接口协作。

### 2. OSI七层模型详解

OSI（Open System Interconnection）参考模型是国际标准化组织（ISO）制定的一个网络互连模型。虽然实际应用中TCP/IP模型更常用，但OSI模型的概念对于理解网络通信至关重要。

#### 2.1 物理层（Layer 1 - Physical）

**功能**：负责在物理介质上传输原始比特流

**关键概念**：
- **传输介质**：双绞线、光纤、无线电波、同轴电缆
- **信号类型**：模拟信号 vs 数字信号
- **编码方式**：曼彻斯特编码、差分曼彻斯特编码
- **传输模式**：单工、半双工、全双工

**物理层设备**：
- 中继器（Repeater）：放大信号，延长传输距离
- 集线器（Hub）：多端口中继器，广播发送数据

**安全视角**：
- 物理层攻击：搭线窃听、电磁泄漏
- 防御措施：加密传输、屏蔽线缆、物理隔离

**实例讲解**：
当你用网线连接电脑和路由器时，网线中的8根铜线负责传输电信号。物理层定义了这些电信号的电压、时序、接口形状等标准。比如，RJ-45接口就是物理层的标准。

#### 2.2 数据链路层（Layer 2 - Data Link）

**功能**：提供可靠的节点到节点数据传输，负责帧的传输

**关键概念**：
- **MAC地址**：48位硬件地址，全球唯一（如：00:1A:2B:3C:4D:5E）
- **以太网帧**：数据链路层的协议数据单元（PDU）
- **交换机**：基于MAC地址转发的智能设备
- **VLAN**：虚拟局域网，逻辑隔离广播域

**以太网帧结构**：
```
┌──────────┬──────────┬──────┬──────┬────────┬─────────┬──────────┐
│前导码(7) │帧起始(1) │目标MAC│源MAC │类型/长度│数据载荷│FCS(4)  │
│ (56位)  │ (1字节)  │(6字节)│(6字节)│(2字节) │(46-1500)│(CRC32) │
└──────────┴──────────┴──────┴──────┴────────┴─────────┴──────────┘
```

**重要字段解析**：
- **目标MAC地址**：接收方的硬件地址
- **源MAC地址**：发送方的硬件地址
- **类型/长度**：标识上层协议（0x0800=IPv4, 0x0806=ARP, 0x86DD=IPv6）
- **FCS（Frame Check Sequence）**：帧校验序列，用于检测传输错误

**数据链路层协议**：
- **以太网（Ethernet）**：最流行的局域网技术
- **Wi-Fi（802.11）**：无线网络标准
- **PPP（Point-to-Point Protocol）**：点对点协议
- **HDLC（High-Level Data Link Control）**：高级数据链路控制

**安全视角**：
- **ARP欺骗**：攻击者发送虚假ARP消息，将目标IP映射到攻击者的MAC地址
- **MAC泛洪**：向交换机发送大量虚假MAC地址，使其进入"失败开放"模式
- **VLAN跳跃**：利用VLAN标签进行跨VLAN攻击

**实战案例**：
假设你的电脑（MAC: AA:AA:AA:AA:AA:AA）要访问服务器（MAC: BB:BB:BB:BB:BB:BB）。数据链路层会将IP数据包封装成以太网帧，添加目标MAC和源MAC，通过物理介质发送。

#### 2.3 网络层（Layer 3 - Network）

**功能**：负责数据包的路由和转发，实现不同网络之间的通信

**关键概念**：
- **IP地址**：32位（IPv4）或128位（IPv6）的逻辑地址
- **路由**：选择数据包从源到目标的最佳路径
- **路由器**：连接不同网络的设备，基于IP地址转发数据包
- **ICMP**：Internet控制消息协议，用于网络诊断

**IP数据包结构（IPv4）**：
```
┌─────────┬──────┬──────┬──────────┬──────┬────────┬──────────┐
│版本(4位)│首部长度│服务类型│ 总长度   │标识   │标志/偏移│ 生存时间 │
│ (4位)   │ (8位) │ (8位)│ (16位)  │(16位)│ (16位) │  (8位)  │
├─────────┼──────┼──────┼──────────┼──────┼────────┼──────────┤
│协议(8位)│首部校验│  源IP地址 (32位)                │          │
│         │ 和(16)│                                   │          │
├─────────┼───────┼──────────────────────────────────┤          │
│  目标IP地址 (32位)                                     │ 可选字段│
├───────────────────────────────────────────────────────┤          │
│                      数据载荷                          │          │
└───────────────────────────────────────────────────────┴──────────┘
```

**重要字段解析**：
- **版本**：4表示IPv4，6表示IPv6
- **TTL（Time To Live）**：防止数据包在网络中无限循环，每经过一个路由器减1
- **协议**：标识上层协议（1=ICMP, 6=TCP, 17=UDP）
- **源IP地址**：发送方的逻辑地址
- **目标IP地址**：接收方的逻辑地址

**IP地址分类（IPv4）**：
- **A类**：1.0.0.0 ~ 126.255.255.255（大型网络）
- **B类**：128.0.0.0 ~ 191.255.255.255（中型网络）
- **C类**：192.0.0.0 ~ 223.255.255.255（小型网络）
- **D类**：224.0.0.0 ~ 239.255.255.255（组播地址）
- **E类**：240.0.0.0 ~ 255.255.255.255（保留地址）

**私有地址范围**：
- 10.0.0.0 ~ 10.255.255.255（10.0.0.0/8）
- 172.16.0.0 ~ 172.31.255.255（172.16.0.0/12）
- 192.168.0.0 ~ 192.168.255.255（192.168.0.0/16）

**子网掩码**：
用于划分网络和主机部分。例如：
- 255.255.255.0（/24）：前24位是网络部分，后8位是主机部分
- 可容纳254台主机（2^8 - 2，减去网络地址和广播地址）

**路由协议**：
- **静态路由**：手动配置路由表
- **动态路由**：
  - RIP（Routing Information Protocol）：距离矢量协议，最大跳数15
  - OSPF（Open Shortest Path First）：链路状态协议，基于Dijkstra算法
  - BGP（Border Gateway Protocol）：自治系统间的路由协议

**安全视角**：
- **IP欺骗**：伪造源IP地址进行攻击
- **路由劫持**：篡改路由表，将流量重定向到恶意节点
- **DDoS攻击**：利用大量僵尸网络发起拒绝服务攻击

**实战案例**：
当你的电脑访问www.baidu.com时，数据包需要经过多个路由器转发。网络层负责选择合适的路径，确保数据包能够到达目标网络。

#### 2.4 传输层（Layer 4 - Transport）

**功能**：提供端到端的通信服务，负责数据的分段和重组

**关键概念**：
- **端口号**：标识应用程序的逻辑端点（0-65535）
- **TCP（Transmission Control Protocol）**：面向连接的可靠传输
- **UDP（User Datagram Protocol）**：无连接的不可靠传输
- **多路复用/多路分解**：通过端口号区分不同应用程序

**TCP段结构**：
```
┌──────────┬──────────┬──────────┬──────────┐
│  源端口   │  目标端口 │   序列号  │          │
│ (16位)   │ (16位)   │  (32位)  │          │
├──────────┼──────────┼──────────┤          │
│确认号     │ 首部长度 │ 标志位    │ 窗口大小 │
│ (32位)   │ (4位)    │ (9位)    │ (16位)  │
├──────────┼──────────┼──────────┼──────────┤
│校验和     │ 紧急指针  │ 选项(可选) │ 填充    │
│ (16位)   │ (16位)   │          │          │
├──────────┴──────────┴──────────┴──────────┤
│              数据载荷                        │
└─────────────────────────────────────────────┘
```

**重要字段解析**：
- **序列号**：标识发送的数据字节流中的每个字节
- **确认号**：期望收到的下一个字节的序列号
- **标志位**：
  - SYN：同步序列号，建立连接
  - ACK：确认号有效
  - FIN：结束连接
  - RST：重置连接
  - PSH：推送数据
  - URG：紧急指针有效

**TCP三次握手**：
```
客户端                    服务器
  |                        |
  |------- SYN ---------->|  (1) 发送SYN=1, seq=x
  |<------ SYN+ACK -------|  (2) 发送SYN=1, ACK=1, seq=y, ack=x+1
  |------- ACK ---------->|  (3) 发送ACK=1, seq=x+1, ack=y+1
  |                        |
```

**TCP四次挥手**：
```
客户端                    服务器
  |                        |
  |------- FIN ---------->|  (1) 客户端请求关闭连接
  |<------ ACK ------------|  (2) 服务器确认
  |<------ FIN ------------|  (3) 服务器请求关闭连接
  |------- ACK ---------->|  (4) 客户端确认
  |                        |
```

**TCP vs UDP 对比**：

| 特性 | TCP | UDP |
|------|-----|-----|
| 连接 | 面向连接 | 无连接 |
| 可靠性 | 可靠（重传机制） | 不可靠（尽最大努力） |
| 顺序 | 保证顺序 | 不保证顺序 |
| 速度 | 较慢（握手、确认） | 快（无额外开销） |
| 开销 | 大（首部20字节） | 小（首部8字节） |
| 应用 | Web、Email、FTP | 视频、DNS、DHCP |

**常见端口号**：
- 20/21：FTP（文件传输协议）
- 22：SSH（安全Shell）
- 23：Telnet（远程登录）
- 25：SMTP（简单邮件传输协议）
- 53：DNS（域名系统）
- 80：HTTP（超文本传输协议）
- 443：HTTPS（安全HTTP）
- 3306：MySQL数据库
- 3389：RDP（远程桌面协议）

**安全视角**：
- **端口扫描**：攻击者扫描开放端口，寻找漏洞
- **SYN Flood**：发送大量SYN请求，耗尽服务器资源
- **会话劫持**：劫持已建立的TCP会话

**实战案例**：
当你浏览网页时，浏览器会通过TCP连接到服务器的80或443端口。传输层负责将数据分段，并确保所有段都能正确到达。

#### 2.5 会话层、表示层、应用层（Layer 5-7）

在实际的TCP/IP模型中，这三层通常合并为应用层。但它们在概念上仍然有重要意义。

**会话层（Layer 5 - Session）**：
- 功能：建立、管理和终止会话
- 协议：NetBIOS、RPC（远程过程调用）
- 实例：当你登录QQ时，会话层负责维护你与QQ服务器的会话

**表示层（Layer 6 - Presentation）**：
- 功能：数据格式转换、加密/解密、压缩/解压缩
- 协议：SSL/TLS、ASCII、JPEG、MPEG
- 实例：当你访问HTTPS网站时，表示层负责TLS加密和解密

**应用层（Layer 7 - Application）**：
- 功能：为用户应用程序提供网络服务
- 协议：HTTP、FTP、SMTP、DNS、DHCP
- 实例：浏览器、邮件客户端、文件传输工具

### 3. TCP/IP四层模型

实际应用中的TCP/IP模型将OSI七层模型简化为四层：

```
┌─────────────────────────────────┐
│  应用层 (Application)           │  ← OSI第5-7层
├─────────────────────────────────┤
│  传输层 (Transport)             │  ← OSI第4层
├─────────────────────────────────┤
│  网络层 (Internet)              │  ← OSI第3层
├─────────────────────────────────┤
│  网络接口层 (Network Interface) │  ← OSI第1-2层
└─────────────────────────────────┘
```

**数据封装过程**：

当你发送一封邮件时，数据会经过以下封装过程：

1. **应用层**：邮件内容 + SMTP头部
2. **传输层**：添加TCP头部（源端口、目标端口等）
3. **网络层**：添加IP头部（源IP、目标IP等）
4. **数据链路层**：添加以太网帧头部和尾部（目标MAC、源MAC、FCS）
5. **物理层**：转换为电信号或光信号发送

接收方则进行相反的解封装过程，逐层去掉头部，最终得到原始数据。

### 4. 核心协议深度解析

#### 4.1 HTTP/HTTPS协议

**HTTP（HyperText Transfer Protocol）**：

HTTP是无状态的请求-响应协议，基于TCP（默认端口80）。

**HTTP请求方法**：
- **GET**：请求获取资源（如：访问网页）
- **POST**：提交数据（如：提交表单）
- **PUT**：上传资源
- **DELETE**：删除资源
- **HEAD**：只获取响应头
- **OPTIONS**：查询服务器支持的方法
- **PATCH**：部分修改资源

**HTTP请求结构**：
```
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
Connection: keep-alive
```

**HTTP响应状态码**：
- **1xx**：信息性状态码（100 Continue）
- **2xx**：成功（200 OK、201 Created）
- **3xx**：重定向（301 Moved Permanently、302 Found）
- **4xx**：客户端错误（400 Bad Request、404 Not Found、403 Forbidden）
- **5xx**：服务器错误（500 Internal Server Error、502 Bad Gateway）

**HTTP头部字段**：
- **通用头部**：Date、Cache-Control、Connection
- **请求头部**：Host、User-Agent、Accept、Authorization
- **响应头部**：Server、Set-Cookie、Content-Type
- **实体头部**：Content-Length、Content-Encoding

**Cookie和Session**：

**Cookie**：
- 服务器发送到浏览器并保存在本地的小数据
- 每次请求时，浏览器会自动携带Cookie
- 用途：会话管理、个性化设置、用户追踪

**Session**：
- 服务器端保存的用户会话信息
- 通过Session ID（通常存储在Cookie中）识别用户
- 更安全，敏感数据不暴露在客户端

**实例讲解**：
当你登录淘宝时：
1. 输入用户名和密码，点击登录
2. 服务器验证通过后，创建一个Session，保存你的登录状态
3. 服务器返回一个Cookie，包含Session ID
4. 之后每次请求，浏览器都会携带这个Cookie
5. 服务器通过Session ID找到对应的Session，识别你的身份

**HTTPS（HTTP Secure）**：

HTTPS = HTTP + SSL/TLS，默认端口443。

**SSL/TLS握手过程**：
```
客户端                    服务器
  |                        |
  |--- Client Hello ------>|  1. 发送支持的加密套件、随机数
  |<-- Server Hello -------|  2. 选择加密套件、发送证书、随机数
  |--- Key Exchange ----->|  3. 验证证书、发送加密的预主密钥
  |<-- Finished ----------|  4. 生成会话密钥
  |--- Finished --------->|  5. 开始加密通信
  |                        |
```

**TLS版本**：
- SSL 3.0（已废弃，不安全）
- TLS 1.0 / 1.1（已废弃）
- TLS 1.2（目前主流）
- TLS 1.3（最新，更快更安全）

**安全视角**：
- **中间人攻击**：攻击者在客户端和服务器之间拦截通信
- **SSL Stripping**：将HTTPS降级为HTTP
- **证书伪造**：伪造服务器证书

**防御措施**：
- 使用最新的TLS版本
- 启用HSTS（HTTP Strict Transport Security）
- 证书锁定（Certificate Pinning）

#### 4.2 DNS协议

**DNS（Domain Name System）**：域名系统，将域名转换为IP地址。

**DNS查询流程**：

假设你要访问 www.baidu.com：

1. **本地hosts文件**：检查 `C:\Windows\System32\drivers\etc\hosts`
2. **本地DNS缓存**：检查浏览器和操作系统的DNS缓存
3. **本地DNS服务器**：向ISP的DNS服务器发起查询
4. **根域名服务器**：返回.com顶级域名服务器的地址
5. **顶级域名服务器**：返回.baidu.com权威域名服务器的地址
6. **权威域名服务器**：返回www.baidu.com的IP地址

**DNS记录类型**：
- **A记录**：域名 → IPv4地址
- **AAAA记录**：域名 → IPv6地址
- **CNAME记录**：域名别名（如：www.baidu.com → www.a.shifen.com）
- **MX记录**：邮件交换记录
- **NS记录**：域名服务器记录
- **TXT记录**：文本记录（常用于SPF、DKIM）
- **PTR记录**：IP → 域名（反向解析）

**DNS查询方式**：
- **递归查询**：DNS服务器代替客户端完成全部查询
- **迭代查询**：DNS服务器返回下一个应该查询的服务器地址

**DNS安全问题**：

**DNS劫持**：
攻击者篡改DNS记录，将目标域名解析到恶意IP。

**DNS隧道**：
利用DNS协议传输非DNS流量，绕过防火墙。

**原理**：
- 客户端将数据包编码到DNS查询中（如：将"secret data"编码为 "c2VjcmV0IGRhdGE=.attacker.com"）
- 攻击者控制的DNS服务器收到查询后，解析出原始数据
- 响应中也包含编码的数据

**防御措施**：
- 使用可信的DNS服务器（如：8.8.8.8、1.1.1.1）
- 启用DNSSEC（DNS安全扩展）
- 监控异常DNS流量

#### 4.3 DHCP协议

**DHCP（Dynamic Host Configuration Protocol）**：动态主机配置协议，自动分配IP地址。

**DHCP租约过程（DORA）**：
```
客户端                    服务器
  |                        |
  |--- DHCP Discover --->|  (1) 广播发现DHCP服务器
  |<-- DHCP Offer --------|  (2) 服务器提供IP地址
  |--- DHCP Request ---->|  (3) 客户端请求使用该IP
  |<-- DHCP Ack ----------|  (4) 服务器确认租约
  |                        |
```

**DHCP报文结构**：
- **op**：操作类型（1=请求，2=响应）
- **htype**：硬件类型（1=以太网）
- **xid**：事务ID，匹配请求和响应
- **chaddr**：客户端MAC地址
- **yiaddr**：分配给客户端的IP地址
- **options**：可选字段（如：子网掩码、网关、DNS）

**DHCP攻击面**：

**DHCP Starvation（DHCP饥饿攻击）**：
- 攻击者发送大量DHCP Discover请求，耗尽IP地址池
- 防御：启用DHCP Snooping（交换机功能）

**恶意DHCP服务器**：
- 攻击者搭建虚假DHCP服务器，分配恶意配置（如：将网关指向攻击者）
- 防御：交换机端口安全、DHCP Snooping

#### 4.4 ARP协议

**ARP（Address Resolution Protocol）**：地址解析协议，将IP地址解析为MAC地址。

**ARP解析流程**：

假设主机A（192.168.1.100）要访问主机B（192.168.1.200）：

1. 主机A检查ARP缓存，看是否有192.168.1.200的MAC地址
2. 如果没有，主机A广播ARP请求："谁是192.168.1.200？请告诉192.168.1.100"
3. 主机B收到广播后，单播ARP响应："我是192.168.1.200，我的MAC地址是XX:XX:XX:XX:XX:XX"
4. 主机A将主机B的IP-MAC映射存入ARP缓存

**ARP缓存表**：
```
C:\> arp -a

接口: 192.168.1.100 --- 0xb
  Internet 地址         物理地址               类型
  192.168.1.1          00-11-22-33-44-55     动态
  192.168.1.200        aa-bb-cc-dd-ee-ff     动态
```

**ARP报文结构**：
- **硬件类型**：1=以太网
- **协议类型**：0x0800=IPv4
- **操作**：1=ARP请求，2=ARP响应
- **发送方MAC/IP**：请求方的地址
- **目标MAC/IP**：要查询的目标地址（请求时目标MAC为00:00:00:00:00:00）

**ARP安全问题**：

**ARP欺骗（ARP Spoofing）**：
攻击者发送虚假ARP消息，将目标IP映射到攻击者的MAC地址。

**攻击场景**：
```
正常情况：
主机A → 网关（192.168.1.1 → MAC: 00:11:22:33:44:55）

攻击情况：
主机A → 攻击者（192.168.1.1 → MAC: 攻击者MAC）
攻击者 → 网关（进行中间人攻击）
```

**防御措施**：
- 静态ARP绑定（在路由器上绑定IP-MAC映射）
- ARP防火墙
- 交换机启用DAI（Dynamic ARP Inspection）

#### 4.5 ICMP协议

**ICMP（Internet Control Message Protocol）**：互联网控制消息协议，用于网络诊断和错误报告。

**ICMP报文类型**：
- **Type 0**：Echo Reply（ping响应）
- **Type 8**：Echo Request（ping请求）
- **Type 3**：Destination Unreachable（目标不可达）
- **Type 11**：Time Exceeded（TTL超时，traceroute使用）

**Ping工作原理**：
```
发送方                    接收方
  |                        |
  |--- ICMP Echo Request ->|  1. Type=8, 包含数据和序列号
  |<-- ICMP Echo Reply -----|  2. Type=0, 回显相同数据
  |                        |
```

**Traceroute工作原理**：
```
发送方                    路由器1 → 路由器2 → 目标
  |                        |         |         |
  |--- TTL=1 ------------>|  1. TTL超时，返回Time Exceeded
  |<-- Time Exceeded ------|     记录路由器1的IP
  |                        |
  |--- TTL=2 ------------>|-->|  2. TTL超时，返回Time Exceeded
  |                        |<--|     记录路由器2的IP
  |                        |
  |--- TTL=3 ------------>|-->|-->|  3. 到达目标，返回Port Unreachable
  |                        |   |<--|     记录目标的IP
```

**ICMP安全问题**：

**Ping Flood**：
发送大量ICMP Echo Request，消耗带宽和处理能力。

**Ping of Death**：
发送超过65535字节的ICMP数据包，导致系统崩溃（已修复）。

**ICMP隧道**：
利用ICMP数据包传输恶意数据，绕过防火墙。

---

## 🔬 实验环境

### 硬件要求
- **处理器**：Intel Core i5或同等性能以上
- **内存**：8GB以上（推荐16GB）
- **硬盘**：50GB可用空间
- **网卡**：支持监控模式的无线网卡（可选，用于无线安全实验）

### 软件要求
1. **虚拟机软件**：VMware Workstation 或 VirtualBox
2. **操作系统**：
   - Kali Linux 2024.x（攻击方）
   - Windows 10/11（受害方）
   - Metasploitable 2/3（故意存在漏洞的目标系统）
3. **网络工具**：
   - Wireshark 4.x
   - Nmap 7.x
   - Netcat
   - TCPDump
   - Scapy（Python库，用于数据包操作）

### 网络拓扑

```
┌─────────────────────────────────────────────────────────┐
│                  虚拟网络 (NAT/Host-Only)                │
│                                                         │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐     │
│  │ Kali     │      │ Windows  │      │ Metasploitable│
│  │ Linux    │<────>│ 10/11   │<────>│            │     │
│  │          │      │          │      │            │     │
│  └──────────┘      └──────────┘      └──────────┘     │
│       │                │                 │             │
│       └────────────────┴─────────────────┘             │
│                     │                                 │
│              ┌──────────────┐                         │
│              │ 虚拟交换机    │                         │
│              └──────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

### 环境搭建步骤

1. **安装虚拟机软件**
   ```bash
   # VMware Workstation Pro 17
   # 或 VirtualBox 7.x（免费）
   ```

2. **下载并导入虚拟机镜像**
   - Kali Linux：https://www.kali.org/downloads/
   - Metasploitable：https://sourceforge.net/projects/metasploitable/

3. **配置虚拟网络**
   - 使用NAT模式或Host-Only模式
   - 确保所有虚拟机在同一网段

4. **安装工具**
   ```bash
   # Kali Linux中
   sudo apt update
   sudo apt install wireshark nmap netcat tcpdump python3-scapy
   ```

---

## 🧪 实验步骤

### 实验1：Wireshark抓包分析

**目标**：掌握Wireshark的基本使用，能够捕获和分析网络数据包

**步骤**：

1. **启动Wireshark**
   ```bash
   sudo wireshark
   ```

2. **选择网络接口**
   - 选择正在使用的网络接口（如：eth0、wlan0）

3. **开始捕获**
   - 点击"开始捕获"按钮
   - 进行网络操作（如：访问网站、ping等）

4. **使用过滤器**
   ```
   # 只显示HTTP流量
   http
   
   # 只显示来自/去往特定IP的流量
   ip.addr == 192.168.1.100
   
   # 只显示特定端口的流量
   tcp.port == 80
   
   # 组合过滤条件
   ip.addr == 192.168.1.100 and tcp.port == 80
   
   # 排除特定流量
   !arp
   ```

5. **分析数据包**
   - 选择感兴趣的数据包
   - 查看各层协议的详细信息
   - 右键"Follow TCP Stream"查看完整会话

6. **统计功能**
   - Statistics → Conversations：查看会话统计
   - Statistics → Endpoints：查看端点统计
   - Statistics → Protocol Hierarchy：查看协议分布

**实验任务**：
- 捕获一次HTTP访问的完整过程
- 分析TCP三次握手和四次挥手
- 提取用户名和密码（如果有）

### 实验2：ARP欺骗攻击与防御

**目标**：理解ARP欺骗原理，掌握防御方法

**攻击步骤**（仅在授权环境中进行）：

1. **查看ARP缓存**
   ```bash
   arp -a
   ```

2. **使用Ettercap进行ARP欺骗**
   ```bash
   sudo ettercap -G  # 启动图形界面
   # 或命令行模式
   sudo ettercap -T -i eth0 -M arp:remote /192.168.1.1/ /192.168.1.100/
   ```

3. **验证攻击效果**
   - 在受害者机器上查看ARP缓存
   - 应该看到网关的IP映射到攻击者的MAC

4. **进行中间人攻击**
   - 攻击者可以拦截、修改、丢弃数据包

**防御步骤**：

1. **静态ARP绑定**
   ```bash
   # Windows
   arp -s 192.168.1.1 00-11-22-33-44-55
   
   # Linux
   sudo arp -s 192.168.1.1 00:11:22:33:44:55
   ```

2. **使用ARP防火墙**
   - Windows：ARP防火墙软件
   - Linux：arpwatch

3. **交换机启用DAI**
   ```bash
   # Cisco交换机
   ip arp inspection vlan 1
   ```

### 实验3：DNS协议分析

**目标**：理解DNS查询流程，识别DNS安全问题

**步骤**：

1. **使用nslookup进行DNS查询**
   ```bash
   nslookup www.baidu.com
   ```

2. **使用dig进行详细查询**
   ```bash
   dig www.baidu.com
   dig @8.8.8.8 www.baidu.com  # 指定DNS服务器
   dig www.baidu.com A  # 查询A记录
   dig www.baidu.com MX  # 查询MX记录
   ```

3. **使用Wireshark捕获DNS流量**
   - 过滤器：`dns`
   - 分析DNS查询和响应的详细字段

4. **修改hosts文件进行DNS劫持演示**
   ```bash
   # Windows: C:\Windows\System32\drivers\etc\hosts
   # Linux: /etc/hosts
   
   # 添加以下行
   127.0.0.1 www.baidu.com
   ```

5. **清除DNS缓存**
   ```bash
   # Windows
   ipconfig /flushdns
   
   # Linux
   sudo systemd-resolve --flush-caches
   ```

### 实验4：常用网络命令实战

**目标**：熟练掌握网络故障排查命令

**命令清单**：

1. **ping**
   ```bash
   ping www.baidu.com  # 基本用法
   ping -c 4 www.baidu.com  # 只发送4个包（Linux）
   ping -n 4 www.baidu.com  # 只发送4个包（Windows）
   ping -t www.baidu.com  # 持续ping（Windows）
   ping -l 1000 www.baidu.com  # 设置包大小（Windows）
   ```

2. **traceroute / tracert**
   ```bash
   # Linux
   traceroute www.baidu.com
   traceroute -I www.baidu.com  # 使用ICMP
   traceroute -T www.baidu.com  # 使用TCP
   
   # Windows
   tracert www.baidu.com
   ```

3. **nslookup**
   ```bash
   nslookup  # 进入交互模式
   nslookup www.baidu.com  # 直接查询
   nslookup -type=MX baidu.com  # 查询MX记录
   ```

4. **netstat**
   ```bash
   # Windows
   netstat -ano  # 显示所有连接和进程ID
   netstat -r  # 显示路由表
   
   # Linux
   netstat -tulnp  # 显示监听端口和进程
   netstat -rn  # 显示路由表
   ```

5. **ss（Linux替代netstat）**
   ```bash
   ss -tuln  # 显示监听端口
   ss -tup  # 显示活动连接和进程
   ```

6. **ipconfig / ifconfig**
   ```bash
   # Windows
   ipconfig  # 显示IP配置
   ipconfig /all  # 显示详细配置
   ipconfig /release  # 释放DHCP租约
   ipconfig /renew  # 续订DHCP租约
   
   # Linux
   ifconfig  # 显示网络接口（已废弃）
   ip addr  # 显示IP地址（推荐）
   ip route  # 显示路由表
   ```

7. **arp**
   ```bash
   arp -a  # 显示ARP缓存
   arp -d 192.168.1.1  # 删除ARP缓存项
   ```

8. **route**
   ```bash
   # Windows
   route print  # 显示路由表
   route add 10.0.0.0 mask 255.0.0.0 192.168.1.1  # 添加路由
   
   # Linux
   route -n  # 显示路由表
   ip route add 10.0.0.0/8 via 192.168.1.1  # 添加路由
   ```

**实验任务**：
- 使用ping和traceroute诊断网络连通性
- 使用netstat/ss查看系统开放端口
- 使用nslookup排查DNS问题
- 使用arp查看和清理ARP缓存

---

## 💡 解题技巧

### 1. 网络故障排查思路

**问题：无法访问网站**

**排查步骤**：
1. **检查物理连接**
   ```bash
   # 检查网线是否插好、网卡指示灯是否正常
   ip link show  # Linux
   ```

2. **检查IP配置**
   ```bash
   ipconfig /all  # Windows
   ip addr  # Linux
   ```

3. **检查网关连通性**
   ```bash
   ping 192.168.1.1  # 假设网关是192.168.1.1
   ```

4. **检查DNS解析**
   ```bash
   nslookup www.baidu.com
   ```

5. **检查路由**
   ```bash
   tracert www.baidu.com  # Windows
   traceroute www.baidu.com  # Linux
   ```

6. **检查防火墙**
   ```bash
   # Windows
   netsh advfirewall show allprofiles
   
   # Linux
   sudo iptables -L
   ```

### 2. 抓包分析技巧

**技巧1：快速定位问题**
- 使用过滤器缩小范围
- 关注TCP重传、RST包、ICMP错误等异常

**技巧2：分析TCP性能**
- 查看TCP窗口大小
- 分析往返时间（RTT）
- 检查是否有丢包和重传

**技巧3：提取文件**
- 对于HTTP传输，可以使用"Follow TCP Stream"保存文件
- 对于FTP传输，可以重组数据包提取文件

### 3. 协议分析技巧

**技巧1：理解标志位**
- TCP flags：SYN、ACK、FIN、RST、PSH、URG
- 组合含义：SYN+ACK（第二次握手）、FIN+ACK（关闭连接）

**技巧2：关注序列号**
- 序列号和确认号用于保证可靠传输
- 异常序列号可能表示攻击或错误

**技巧3：查看选项字段**
- TCP选项：MSS、Window Scale、SACK等
- IP选项：Record Route、Timestamp等

---

## 🛡️ 防御措施

### 1. 网络层防御

**措施1：使用防火墙**
- 配置访问控制列表（ACL）
- 限制不必要的端口开放
- 启用状态检测（Stateful Inspection）

**措施2：部署入侵检测/防御系统（IDS/IPS）**
- Snort、Suricata等开源方案
- 实时监控网络流量，检测异常行为

**措施3：网络分段**
- 使用VLAN隔离不同部门
- 关键服务器放在独立网段
- 使用DMZ隔离对外服务

### 2. 传输层防御

**措施1：禁用不必要的服务**
```bash
# Linux：禁用Telnet，使用SSH
sudo systemctl stop telnet
sudo systemctl disable telnet
```

**措施2：使用安全协议**
- 使用SSH替代Telnet
- 使用HTTPS替代HTTP
- 使用SFTP替代FTP

**措施3：限制连接数**
```bash
# Linux：限制SSH连接数
sudo iptables -A INPUT -p tcp --dport 22 -m connlimit --connlimit-above 3 -j REJECT
```

### 3. 应用层防御

**措施1：及时更新补丁**
- 定期更新操作系统和应用程序
- 启用自动更新

**措施2：使用强密码和双因素认证**
- 密码复杂度要求
- 启用2FA/MFA

**措施3：部署Web应用防火墙（WAF）**
- ModSecurity等开源WAF
- 防御SQL注入、XSS等攻击

### 4. 物理层防御

**措施1：物理安全**
- 机房门禁
- 监控摄像头
- 上锁的机柜

**措施2：加密传输**
- 使用VPN
- 使用HTTPS
- 避免明文传输

---

## 📝 课后练习

### 练习题1：理论题

1. **OSI模型和TCP/IP模型有什么区别？**
   - 提示：层数、实际应用、历史背景

2. **解释TCP三次握手的过程，为什么需要三次？**
   - 提示：防止已失效的连接请求到达服务器

3. **HTTP和HTTPS有什么区别？HTTPS如何保证安全？**
   - 提示：加密、证书、完整性验证

4. **什么是ARP欺骗？如何防御？**
   - 提示：虚假ARP消息、静态绑定、DAI

5. **DNS查询的流程是什么？什么是DNS隧道？**
   - 提示：递归查询、迭代查询、利用DNS传输数据

### 练习题2：实践题

1. **使用Wireshark捕获一次完整的HTTP访问过程，并分析：**
   - TCP三次握手
   - HTTP请求和响应
   - TCP四次挥手

2. **使用nmap扫描目标主机，识别开放端口和运行的服务**
   ```bash
   nmap -sS 192.168.1.100  # TCP SYN扫描
   nmap -sV 192.168.1.100  # 版本检测
   nmap -O 192.168.1.100  # 操作系统检测
   ```

3. **配置静态IP地址，并测试网络连通性**
   - Windows：通过网络适配器属性配置
   - Linux：编辑 `/etc/netplan/*.yaml` 或 `/etc/network/interfaces`

4. **使用Scapy构造自定义数据包**
   ```python
   from scapy.all import *
   
   # 构造ARP请求
   pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1")
   sendp(pkt)
   
   # 构造ICMP ping
   pkt = IP(dst="www.baidu.com") / ICMP()
   reply = sr1(pkt)
   reply.show()
   ```

### 练习题3：挑战题

1. **分析一个真实的网络攻击案例（如：Mirai僵尸网络），写出攻击原理和防御措施**

2. **设计一个小型企业网络安全方案，包括：**
   - 网络拓扑
   - 安全设备部署
   - 安全策略

3. **使用Python编写一个简单的端口扫描器**
   ```python
   import socket
   
   def port_scan(target, port):
       try:
           s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           s.settimeout(1)
           result = s.connect_ex((target, port))
           if result == 0:
               print(f"Port {port} is open")
           s.close()
       except Exception as e:
           print(f"Error: {e}")
   
   target = "192.168.1.100"
   for port in range(1, 1024):
       port_scan(target, port)
   ```

---

## ❓ FAQ（常见问题）

### Q1：为什么我的ping请求没有响应？

**可能原因**：
1. 目标主机离线或不存在
2. 防火墙阻止ICMP包
3. 网络不通（检查IP配置和网关）
4. 目标主机禁用ping响应

**解决方法**：
- 检查物理连接和IP配置
- 尝试ping网关
- 使用traceroute查看在哪里中断

### Q2：Wireshark看不到任何数据包怎么办？

**可能原因**：
1. 没有管理员权限
2. 选择了错误的网络接口
3. 网卡不支持混杂模式

**解决方法**：
- 以管理员身份运行Wireshark
- 确认选择的接口有流量
- 检查网卡驱动和设置

### Q3：ARP缓存中的"动态"和"静态"是什么意思？

**解释**：
- **动态**：通过ARP协议自动学习，有时间限制（通常2-20分钟）
- **静态**：手动配置的ARP条目，永久有效

**示例**：
```bash
# Windows：添加静态ARP条目
arp -s 192.168.1.1 00-11-22-33-44-55

# Linux：添加静态ARP条目
arp -s 192.168.1.1 00:11:22:33:44:55
```

### Q4：为什么访问网站时有时很慢？

**可能原因**：
1. DNS解析慢
2. 网络拥塞
3. 服务器响应慢
4. TCP连接建立慢（丢包、重传）

**排查方法**：
- 使用dig或nslookup测试DNS解析时间
- 使用ping测试网络延迟
- 使用Wireshark分析TCP性能
- 使用traceroute查看路径

### Q5：如何查看自己的公网IP地址？

**方法**：
1. 访问网站：https://www.ip138.com/ 或 https://ifconfig.me/
2. 使用命令：
   ```bash
   curl ifconfig.me
   curl ip.sb
   ```

### Q6：DHCP和静态IP哪个更好？

**回答**：
- **DHCP**：适合大多数场景，自动配置，减少管理成本
- **静态IP**：适合服务器、打印机等需要固定地址的设备

**建议**：
- 客户端使用DHCP
- 服务器、网络设备等使用静态IP

### Q7：什么是端口转发？如何配置？

**解释**：
端口转发（Port Forwarding）将外部网络的请求转发到内部网络的特定主机和端口。

**应用场景**：
- 从外网访问内网的Web服务器
- 远程桌面连接到内网电脑

**配置示例（路由器）**：
```
外部端口：8080
内部IP：192.168.1.100
内部端口：80
协议：TCP
```

### Q8：如何判断网络是否被监听？

**迹象**：
1. 网络速度明显变慢
2. ARP缓存中存在异常的IP-MAC映射
3. 使用Wireshark发现大量未知流量

**检测方法**：
- 使用ARP防火墙检测ARP欺骗
- 使用入侵检测系统（IDS）
- 定期检查网络设备的配置

---

## 📊 总结

### 关键知识点回顾

1. **网络分层模型**
   - OSI七层模型和TCP/IP四层模型
   - 数据封装和解封装过程

2. **核心协议**
   - 以太网帧、IP数据包、TCP/UDP段的结构
   - HTTP/HTTPS、DNS、DHCP、ARP、ICMP协议

3. **网络工具**
   - Wireshark抓包分析
   - 常用网络命令：ping、traceroute、nslookup、netstat、ss

4. **安全防御**
   - 常见网络攻击：ARP欺骗、DNS劫持、DHCP攻击
   - 防御措施：防火墙、IDS/IPS、静态绑定、加密传输

### 学习建议

1. **理论与实践结合**
   - 不要只看书，要多动手实验
   - 搭建自己的实验环境

2. **深入理解协议**
   - 使用Wireshark分析真实流量
   - 阅读RFC文档（如：RFC 793 - TCP）

3. **关注安全动态**
   - 订阅安全邮件列表
   - 关注CVE漏洞公告

4. **持续学习**
   - 网络技术不断发展，要保持学习热情
   - 学习新的协议和技术（如：HTTP/3、QUIC）

### 下一步学习方向

1. **进阶网络知识**
   - BGP协议
   - MPLS
   - SDN（软件定义网络）

2. **网络安全**
   - 渗透测试
   - 入侵检测
   - 安全运维

3. **网络编程**
   - Socket编程
   - 使用Scapy构造数据包
   - 开发网络工具

---

## 📚 参考资料

### 书籍
1. 《TCP/IP详解 卷1：协议》 - W. Richard Stevens
2. 《计算机网络：自顶向下方法》 - James F. Kurose
3. 《Wireshark网络分析实战》 - 林沛满

### 在线资源
1. Wireshark官方文档：https://www.wireshark.org/docs/
2. RFC文档：https://www.ietf.org/rfc/
3. Kali Linux文档：https://www.kali.org/docs/

### 工具下载
1. Wireshark：https://www.wireshark.org/download.html
2. Nmap：https://nmap.org/download.html
3. Scapy：https://scapy.net/

---

**课程完成时间**：________  
**学员签名**：________  
**教练评语**：________

---

**恭喜你完成了第04章的学习！** 🎉

你现在已经掌握了计算机网络的基础知识，能够使用各种网络工具进行故障排查和安全分析。在接下来的课程中，我们将学习更多高级主题，包括渗透测试、漏洞分析、恶意代码分析等。

记住：网络安全是一个持续学习的过程，保持好奇心和实践精神，你一定能够成为一名优秀的网络安全专家！

**下一部分预告**：第05章 - 信息收集与侦察

---

*文档版本：v1.0*  
*最后更新：2026年6月*  
*作者：红客教学团队*
