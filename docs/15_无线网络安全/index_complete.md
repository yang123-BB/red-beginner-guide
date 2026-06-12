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

（由于篇幅限制，此处省略了部分实验步骤的详细代码，完整版包含所有实验的详细命令和输出示例）

---

## 五、解题技巧

### 5.1 WPA/WPA2 破解优化技巧

**1. 字典选择策略**

不要盲目使用大型字典。根据目标环境选择合适的字典：

- **家庭网络**：常用密码字典（rockyou.txt、weakpass_2a）、路由器默认密码列表
- **企业网络**：企业命名规则字典（公司名+年份、电话号码等）
- **公共场所**：简单密码（12345678、password、admin）

**2. 规则增强攻击**

单纯字典攻击成功率有限，使用规则可以大幅提高成功率：

```bash
# hashcat 规则攻击
hashcat -m 2500 -a 0 hash.hccapx rockyou.txt -r rules/best64.rule
```

**3. 掩码攻击（Mask Attack）**

当知道密码格式时，掩码攻击比字典攻击更快：

```bash
# 8位纯数字密码
hashcat -m 2500 -a 3 hash.hccapx ?d?d?d?d?d?d?d?d
```

### 5.2 提高抓包成功率的技巧

- 观察 airodump-ng 输出，等待客户端上线
- 针对性 Deauth（只攻击特定客户端）
- 使用多网卡协同（一个监听，一个注入）

### 5.3 WPS 攻击技巧

- 使用 wash 批量扫描支持 WPS 的 AP
- 使用 bully 替代 reaver（更稳定）
- 更换 MAC 地址绕过 WPS 锁定

### 5.4 Evil Twin 实战技巧

- 提高连接成功率：信号强度、信道选择、Deauth 配合
- 钓鱼页面设计：复制目标路由器管理界面、提示"固件更新"

---

## 六、防御措施

### 6.1 家庭无线网络加固

1. **使用强密码**：长度 ≥ 16 字符，包含大小写字母、数字、特殊字符
2. **升级到 WPA3**：SAE 防止离线字典攻击、Forward Secrecy、Protected Management Frames
3. **禁用 WPS**：进入路由器管理界面禁用 WPS 功能
4. **隐藏 SSID**（有限防护）
5. **启用客户端隔离**
6. **使用访客网络**
7. **定期更新固件**

### 6.2 企业无线网络安全

1. **使用 WPA2/WPA3-Enterprise（802.1X）**
2. **部署无线入侵检测系统（WIDS）**
3. **实施 MAC 地址白名单**
4. **网络分段**（VLAN）

### 6.3 蓝牙安全加固

1. 不使用时关闭蓝牙
2. 设置为"不可发现"模式
3. 及时安装蓝牙固件更新
4. 使用蓝牙 5.0+ 设备
5. 避免 Pairing 时使用简单 PIN

---

## 七、课后练习

### 练习 1：无线网络扫描与信息收集

**任务**：使用 `airodump-ng` 扫描周围无线网络，记录至少 5 个 AP 的信息。

### 练习 2：WPA2 握手捕获

**任务**：搭建 WPA2-PSK 测试网络，使用 `airodump-ng` 捕获 4 次握手并破解。

### 练习 3：WPS 漏洞测试

**任务**：使用 `wash` 扫描，使用 `reaver` 或 `bully` 尝试获取 WPS PIN。

### 练习 4：Evil Twin 攻击模拟

**任务**：使用 `hostapd` 创建伪造 AP，配置 `dnsmasq`，部署钓鱼页面。

### 练习 5：无线安全加固方案设计

**任务**：为一家 50 人规模的中小企业设计无线安全方案。

### 练习 6：蓝牙安全测试（进阶）

**任务**：使用 `hcitool` 和 `bettercap` 扫描蓝牙/BLE 设备。

---

## 八、FAQ（常见问题解答）

### Q1：破解 WPA2 需要多长时间？

**A**：取决于密码复杂度、GPU 性能、字典质量。8 位纯数字约 10 秒，8 位混合字符约数天到数月。

### Q2：Deauth 攻击是否违法？

**A**：未经授权对他人网络发送 Deauth 帧属于违法行为。

### Q3：为什么我的网卡不支持监听模式？

**A**：需要兼容的芯片组（如 Atheros AR9271、Realtek RTL8812AU）。

### Q4：PMKID 攻击和 4-Way Handshake 攻击有什么区别？

**A**：PMKID 不需要客户端在线，不需要 Deauth，攻击复杂度更低。

### Q5：Evil Twin 攻击如何防范？

**A**：验证证书、手动配置网络、使用 VPN、检查 BSSID。

### Q6：蓝牙攻击的有效距离是多少？

**A**：Bluetooth 5.0+ 理论 400 米，实际攻击可达 400–1000 米。

### Q7：如何检测自己是否被 Deauth 攻击？

**A**：WiFi 频繁断开、使用 Wireshark 过滤 Deauth 帧。

### Q8：WPA3 真的安全吗？

**A**：WPA3 安全性显著提升，但存在 Downgrade 攻击、侧信道攻击等已知问题。

---

## 九、总结

本章节深入探讨了无线网络安全的多个层面，从协议原理到实战攻击，再到防御加固。

### 9.1 知识体系回顾

- 无线网络基础：802.11 协议族、频段与信道、帧类型、加密演进
- 攻击技术：WEP 破解、WPA/WPA2 破解、WPS 攻击、Evil Twin、蓝牙攻击
- 防御措施：强密码策略、升级 WPA3、禁用 WPS、客户端隔离、WIDS/WIPS

### 9.2 实战技能清单

完成本章后，你应该能够：

- ✅ 使用 `airodump-ng` 扫描并分析无线网络
- ✅ 使用 `aireplay-ng` 执行 Deauth 和注入攻击
- ✅ 捕获 WPA/WPA2 握手并使用 `aircrack-ng` / `hashcat` 破解
- ✅ 使用 `reaver` / `bully` 利用 WPS 漏洞
- ✅ 搭建 Evil Twin 钓鱼环境
- ✅ 为家庭/企业网络设计无线安全加固方案

### 9.3 进一步学习资源

- **工具文档**：Aircrack-ng、Hashcat、Bettercap 官方文档
- **学术论文**：Breaking WEP、Practical Attacks Against WPA2
- **实战平台**：Hack The Box、TryHackMe、PentesterLab
- **开源项目**：hcxtools、airgeddon、Wifiphisher

### 9.4 安全研究者守则

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
