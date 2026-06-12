# 第12章：密码学基础与密码攻击

> **难度**：⭐⭐⭐ (中级)  
> **预计时间**：60-90分钟  
> **课程编号**：12

---

## 📋 学习目标

通过本章的学习，您将能够：

1. **理解密码学基本概念**
   - 掌握哈希算法、对称加密、非对称加密的基本原理
   - 理解不同加密算法的应用场景和安全性

2. **识别密码存储方式**
   - 理解明文、哈希、加盐哈希、PEPPER等存储方式的区别
   - 评估不同存储方式的安全性

3. **掌握密码攻击技术**
   - 理解字典攻击、彩虹表、暴力破解、规则攻击的原理
   - 学会使用常见密码攻击工具

4. **具备实战能力**
   - 使用John the Ripper、Hashcat等工具进行密码破解
   - 分析密码强度并提出改进建议

5. **建立防御意识**
   - 理解如何设计安全的密码存储方案
   - 掌握密码安全最佳实践

---

## 📚 背景知识

### 1. 密码学概述

密码学（Cryptography）是研究如何在不安全的环境中实现安全通信的科学。它涉及构造和分析抵抗各种攻击的协议，确保数据的机密性、完整性和可用性。

#### 1.1 密码学的历史发展

密码学的发展可以追溯到古代文明。早在公元前1900年左右，古埃及就使用了非标准的象形文字来表示保密信息。随着时间的推移，密码学逐渐演变成一门系统的科学。

**古典密码学时期（1949年之前）**
- **替换密码**：凯撒密码（Caesar Cipher）是最著名的替换密码之一，通过将字母表中的每个字母移动固定位数来加密信息
- **维吉尼亚密码**（Vigenère Cipher）：使用一系列凯撒密码组成密码字母表的加密算法，被认为是历史上最难破译的密码之一
- **恩尼格玛机**（Enigma）：二战期间德国使用的机械加密设备，其破解工作催生了现代计算机科学的诞生

**现代密码学时期（1949年至今）**
- 1949年，克劳德香农（Claude Shannon）发表了《保密系统的通信理论》，奠定了现代密码学的理论基础
- 1976年，惠特菲尔德·迪菲（Whitfield Diffie）和马丁·赫尔曼（Martin Hellman）提出了公钥密码学的概念
- 1977年，美国国家标准局（NBS，现为NIST）采纳了数据加密标准（DES）
- 2001年，高级加密标准（AES）取代DES成为新的加密标准

#### 1.2 密码学的核心目标

现代密码学致力于实现以下核心安全目标：

1. **机密性**（Confidentiality）
   - 确保信息只能被授权方访问
   - 防止未授权的信息泄露
   - 通过加密技术实现

2. **完整性**（Integrity）
   - 确保信息在传输和存储过程中不被篡改
   - 检测未授权的修改
   - 通过哈希函数和消息认证码（MAC）实现

3. **认证性**（Authentication）
   - 验证通信方的身份
   - 确保信息来源的真实性
   - 通过数字签名和认证协议实现

4. **不可否认性**（Non-repudiation）
   - 防止发送方否认曾经发送过某条消息
   - 通过数字签名和时间戳实现

5. **可用性**（Availability）
   - 确保授权方在需要时可以访问信息
   - 防止拒绝服务攻击（DoS）

#### 1.3 密码学的基本分类

密码学可以分为以下几个主要分支：

**对称密码学**（Symmetric Cryptography）
- 加密和解密使用相同的密钥
- 优点：计算速度快，适合大量数据加密
- 缺点：密钥分发困难，密钥管理复杂
- 典型算法：AES、DES、3DES、RC4、ChaCha20

**非对称密码学**（Asymmetric Cryptography）
- 使用公钥和私钥对进行加密和解密
- 优点：解决了密钥分发问题，支持数字签名
- 缺点：计算速度慢，不适合大量数据加密
- 典型算法：RSA、ECC、DH（Diffie-Hellman）、ElGamal

**哈希函数**（Hash Function）
- 将任意长度的数据映射为固定长度的哈希值
- 特点：单向性、确定性、抗碰撞性
- 应用：密码存储、数据完整性验证、数字签名
- 典型算法：MD5、SHA1、SHA256、SHA3、bcrypt、Argon2

**数字签名**（Digital Signature）
- 结合哈希函数和非对称加密
- 提供认证性、完整性和不可否认性
- 典型算法：RSA签名、DSA、ECDSA

**密码协议**（Cryptographic Protocol）
- 多个参与者之间的安全通信协议
- 典型协议：TLS/SSL、IPSec、PGP、SSH

### 2. 哈希算法详解

哈希函数（Hash Function）是密码学中的重要组成部分，它将任意长度的输入数据转换为固定长度的输出（哈希值或摘要）。

#### 2.1 哈希函数的性质

一个安全的密码学哈希函数应该具备以下性质：

1. **单向性**（One-way）
   - 从哈希值计算出原始输入在计算上是不可行的
   - 即给定哈希值h，找到满足H(m)=h的消息m是困难的

2. **抗碰撞性**（Collision Resistance）
   - **弱抗碰撞性**：给定消息m1，找到另一个消息m2使得H(m1)=H(m2)在计算上是不可行的
   - **强抗碰撞性**：找到任意两个不同的消息m1和m2使得H(m1)=H(m2)在计算上是不可行的

3. **雪崩效应**（Avalanche Effect）
   - 输入数据的微小变化（即使是一位）应该导致哈希值的显著变化
   - 理想情况下，改变输入的一位应该使输出的每一位以50%的概率翻转

4. **确定性**（Deterministic）
   - 相同的输入必须产生相同的输出
   - 这是哈希函数的基本要求

5. **快速计算**（Efficiency）
   - 对于给定的输入，哈希值应该能够快速计算
   - 但这一性质不应该损害安全性

#### 2.2 MD5算法

**MD5**（Message Digest Algorithm 5）是由Ronald Rivest在1991年设计的哈希函数，输出128位（16字节）的哈希值。

**算法特点：**
- 输出长度：128位
- 处理速度：快速
- 安全性：已被证明不安全，存在严重的碰撞攻击

**MD5的结构：**
1. **填充**：对消息进行填充，使其长度 ≡ 448 (mod 512)
2. **添加长度**：在填充后的消息末尾添加64位的长度字段
3. **初始化缓冲区**：使用4个32位的链接变量（A、B、C、D）
4. **处理消息**：将消息分成512位的块，每块进行4轮操作
5. **输出**：将最终的A、B、C、D连接起来形成128位的哈希值

**安全性问题：**
- 2004年，王小云教授团队发表了MD5的碰撞攻击方法
- 2008年，研究人员演示了如何创建两个具有相同MD5哈希值的不同数字证书
- 2010年，Mozilla宣布不再接受使用MD5的证书
- 2012年，Flame恶意软件利用MD5碰撞攻击伪造Microsoft的数字签名

**当前状态：**
- **不推荐用于安全目的**
- 仅可用于非加密目的的完整性校验（如文件校验和）
- 许多系统和协议已经弃用MD5

#### 2.3 SHA1算法

**SHA1**（Secure Hash Algorithm 1）是由美国国家安全局（NSA）设计，由NIST发布的哈希函数，输出160位（20字节）的哈希值。

**算法特点：**
- 输出长度：160位
- 处理速度：中等
- 安全性：已被证明不安全，但比MD5稍好

**SHA1的结构：**
1. **填充**：类似MD5的填充方式
2. **初始化缓冲区**：使用5个32位的链接变量（A、B、C、D、E）
3. **处理消息**：将消息分成512位的块，每块进行4轮操作，每轮20步
4. **输出**：将最终的A、B、C、D、E连接起来形成160位的哈希值

**安全性问题：**
- 2005年，研究员预测SHA1可能在未来几年内被攻破
- 2017年，Google和CWI Institute发布了SHA1碰撞攻击的实际演示（SHAttered攻击）
- 2020年，NIST正式建议停止使用SHA1

**当前状态：**
- **不推荐用于安全目的**
- 许多浏览器和操作系统已经弃用SHA1
- 应迁移到SHA2或SHA3系列算法

#### 2.4 SHA256算法

**SHA256**是SHA2家族的成员之一，输出256位（32字节）的哈希值，是目前广泛使用的哈希算法之一。

**算法特点：**
- 输出长度：256位
- 处理速度：较慢于MD5和SHA1，但可接受
- 安全性：目前被认为是安全的

**SHA256的结构：**
1. **填充**：类似SHA1的填充方式
3. **初始化缓冲区**：使用8个32位的链接变量
4. **处理消息**：将消息分成512位的块，每块进行64步操作
5. **输出**：将最终的8个32位字连接起来形成256位的哈希值

**安全性：**
- 目前没有实用的攻击方法
- NIST预计到2030年之后才可能需要替换
- 广泛应用于区块链（如比特币）、数字签名、证书等

**SHA2家族：**
- SHA224：输出224位
- SHA256：输出256位
- SHA384：输出384位
- SHA512：输出512位
- SHA512/224、SHA512/256：截断版本的SHA512

#### 2.5 bcrypt算法

**bcrypt**是基于Blowfish密码设计的哈希函数，专门为密码存储而设计。

**算法特点：**
- 输出长度：192位（24字节）
- 可调节的计算成本（work factor）
- 内置盐值（salt）生成
- 抗GPU/ASIC加速攻击

**设计原理：**
1. **基于Blowfish密码**：使用Blowfish的密钥调度算法
2. **可调节成本**：通过work factor控制哈希计算的时间
3. **盐值**：自动生成128位的盐值，防止彩虹表攻击
4. **缓慢的哈希**：故意设计得较慢，增加暴力破解的难度

**work factor（成本因子）：**
- 控制哈希计算的轮数：2^work_factor次
- 默认值通常为10-12
- 随着硬件性能提升，应逐渐增加work factor

**优势：**
- 抵抗暴力破解攻击
- 抵抗彩虹表攻击
- 适应硬件发展（可增加work factor）

**应用：**
- 密码存储的标准选择之一
- 被许多框架和系统采用（如Spring Security、Django等）

#### 2.6 Argon2算法

**Argon2**是2015年密码哈希竞赛的获胜者，被认为是当前最先进的密码哈希算法。

**算法特点：**
- 输出长度：可配置
- 三个版本：Argon2d、Argon2i、Argon2id
- 可调节的内存成本、时间成本和并行度
- 抵抗GPU、ASIC和侧信道攻击

**三个版本：**
1. **Argon2d**：使用数据依赖的内存访问，抵抗GPU攻击，但可能受到侧信道攻击
2. **Argon2i**：使用数据独立的访问，抵抗侧信道攻击，但抵抗GPU攻击的能力较弱
3. **Argon2id**：混合版本，前一半pass使用Argon2i，后一半使用Argon2d，推荐用于大多数场景

**参数配置：**
- **内存成本**（Memory cost）：以KB为单位，控制内存使用量
- **时间成本**（Time cost）：迭代次数，控制计算时间
- **并行度**（Parallelism）：并行执行的线程数

**优势：**
- 最新的密码哈希标准
- 灵活的参数配置
- 优秀的抗攻击能力
- 适应不同的硬件环境

**推荐配置：**
- 对于密码存储，推荐使用Argon2id
- 内存成本：至少64MB（65536 KB）
- 时间成本：至少3次迭代
- 并行度：根据CPU核心数设置

#### 2.7 哈希算法的选择建议

**密码存储：**
1. **首选**：Argon2id（最新、最安全）
2. **次选**：bcrypt（广泛使用、成熟稳定）
3. **不推荐**：MD5、SHA1（已被攻破）
4. **可用但不理想**：SHA256（没有内置盐值和可调节成本）

**数据完整性校验：**
- SHA256或SHA3（安全且快速）
- 避免使用MD5和SHA1

**数字签名：**
- SHA256或更高版本的SHA2家族
- SHA3（如果可用）

### 3. 对称加密详解

对称加密（Symmetric Encryption）使用相同的密钥进行加密和解密，是最古老的加密形式，也是现代密码学的基础。

#### 3.1 对称加密的基本原理

对称加密算法使用相同的密钥（称为"对称密钥"）进行加密和解密。发送方使用密钥将明文转换为密文，接收方使用相同的密钥将密文还原为明文。

**加密过程：**
```
密文 = E(密钥, 明文)
明文 = D(密钥, 密文)
```

其中E是加密函数，D是解密函数，且满足：
```
D(密钥, E(密钥, 明文)) = 明文
```

#### 3.2 对称加密的分类

对称加密可以分为两类：

**流密码**（Stream Cipher）
- 逐位或逐字节加密
- 使用密钥流与明文进行异或操作
- 优点：速度快，适合实时加密
- 缺点：如果密钥流重复，容易被攻破
- 典型算法：RC4、Salsa20、ChaCha20

**分组密码**（Block Cipher）
- 将明文分成固定长度的块，逐块加密
- 需要使用工作模式（mode of operation）来处理多个块
- 优点：安全性高，适合存储加密
- 缺点：速度可能慢于流密码
- 典型算法：AES、DES、3DES、Blowfish

#### 3.3 AES算法

**AES**（Advanced Encryption Standard）是目前最广泛使用的对称加密标准，取代了DES。

**算法特点：**
- 密钥长度：128、192或256位
- 分组长度：128位
- 轮数：10轮（128位密钥）、12轮（192位密钥）、14轮（256位密钥）
- 安全性：目前被认为是安全的

**AES的结构：**
1. **字节替代**（SubBytes）：使用S盒进行非线性替换
2. **行移位**（ShiftRows）：对状态的行进行循环移位
3. **列混合**（MixColumns）：对状态的列进行线性变换
4. **轮密钥加**（AddRoundKey）：将轮密钥与状态进行异或

**工作模式：**
- **ECB**（Electronic Codebook）：每个块独立加密，不安全（相同的明文块产生相同的密文块）
- **CBC**（Cipher Block Chaining）：每个明文块先与前一个密文块异或后再加密，需要初始化向量（IV）
- **CFB**（Cipher Feedback）：将分组密码转换为流密码
- **OFB**（Output Feedback）：生成密钥流，与明文异或
- **CTR**（Counter）：使用计数器模式，适合并行计算
- **GCM**（Galois/Counter Mode）：提供加密和认证，推荐用于现代应用

**应用场景：**
- 无线网络安全（WPA2/WPA3）
- 磁盘加密（BitLocker、FileVault）
- VPN（IPSec）
- TLS/SSL

#### 3.4 DES算法

**DES**（Data Encryption Standard）是1977年 adopted 的加密标准，现在已经被认为不安全。

**算法特点：**
- 密钥长度：56位（实际上有8个奇偶校验位，共64位）
- 分组长度：64位
- 轮数：16轮
- 安全性：密钥长度太短，容易被暴力破解

**DES的结构：**
1. **初始置换**（IP）：对64位明文进行置换
2. **16轮Feistel网络**：每轮使用48位的子密钥
3. **逆初始置换**（IP^-1）：恢复位的顺序

**安全性问题：**
- 56位密钥长度太短，现代计算机可以在短时间内暴力破解
- 1998年，EFF建造的Deep Crack机器在56小时内破解了DES密钥
- 1999年，distributed.net在22小时内破解了DES密钥

**当前状态：**
- **不推荐用于任何安全目的**
- 仅具有历史研究价值

#### 3.5 3DES算法

**3DES**（Triple DES）是对DES的改进，通过三次应用DES算法来增强安全性。

**算法特点：**
- 密钥长度：112或168位（实际上使用3个56位密钥）
- 分组长度：64位
- 安全性：比DES安全，但比AES慢且不够安全

**3DES的变体：**
1. **3DES-EDE**：加密-解密-加密（最常用）
   - 使用密钥K1加密，K2解密，K3加密
   - 如果K1=K2=K3，则退化为DES
   - 如果K1=K3，则密钥长度为112位
   - 如果K1≠K3，则密钥长度为168位

2. **3DES-EEE**：加密-加密-加密（较少使用）

**安全性：**
- 抵抗暴力破解攻击（密钥长度足够）
- 但分组长度仍为64位，存在生日攻击的风险
- 性能比AES慢得多

**当前状态：**
- NIST计划在2023年后不再推荐3DES
- 许多标准和协议已经迁移到AES
- 仅在遗留系统中使用

#### 3.6 RC4算法

**RC4**（Rivest Cipher 4）是Ron Rivest在1987年设计的流密码，曾经广泛使用。

**算法特点：**
- 密钥长度：可变（通常40-256位）
- 速度：非常快
- 实现：简单，易于软件实现
- 安全性：已被证明存在多个漏洞

**RC4的结构：**
1. **密钥调度算法**（KSA）：初始化256字节的状态数组S
2. **伪随机生成算法**（PRGA）：生成密钥流，与明文异或

**安全性问题：**
- 2013年，研究人员发现了RC4中的偏差，可以恢复部分明文
- 2015年，RFC 7465正式禁止使用RC4
- 存在多种攻击方法，包括偏向攻击、相关密钥攻击等

**历史应用：**
- WEP（无线加密协议）：使用RC4，已被证明极不安全
- TLS/SSL：曾经支持RC4，现在已被禁止
- Microsoft Office和PDF：曾经使用RC4，现在已弃用

**当前状态：**
- **不推荐用于任何安全目的**
- 许多标准和协议已经明确禁止使用RC4

#### 3.7 对称加密的选择建议

**新系统开发：**
- **首选**：AES-256-GCM（提供加密和认证）
- **备选**：ChaCha20-Poly1305（在移动设备上性能更好）

**遗留系统维护：**
- 如果使用的是3DES，应计划迁移到AES
- 如果使用的是DES或RC4，应立即更换

**工作模式选择：**
- **推荐**：GCM或CTR（支持并行、不需要填充）
- **避免**：ECB（不安全）、CBC（需要填充，可能受到填充攻击）

### 4. 非对称加密详解

非对称加密（Asymmetric Encryption），也称为公钥加密（Public-key Cryptography），使用一对密钥：公钥和私钥。

#### 4.1 非对称加密的基本原理

非对称加密使用两个密钥：
- **公钥**（Public Key）：可以公开分享，用于加密或验证签名
- **私钥**（Private Key）：必须保密，用于解密或创建签名

**加密过程：**
```
密文 = E(公钥, 明文)
明文 = D(私钥, 密文)
```

**签名过程：**
```
签名 = Sign(私钥, 消息)
验证 = Verify(公钥, 消息, 签名)
```

#### 4.2 非对称加密的应用

1. **机密性**：使用接收方的公钥加密，只有接收方的私钥可以解密
2. **认证性**：使用发送方的私钥签名，任何人可以使用发送方的公钥验证
3. **密钥交换**：安全地交换对称加密的密钥
4. **数字证书**：证明公钥的所有权

#### 4.3 RSA算法

**RSA**（Rivest-Shamir-Adleman）是最早公开的公钥加密算法，也是最广泛使用的非对称加密算法之一。

**算法原理：**
RSA基于大整数分解问题的困难性。给定两个大素数p和q，计算n=p×q是容易的，但给定n，分解出p和q在计算上是不可行的。

**密钥生成：**
1. 选择两个大素数p和q
2. 计算n = p × q
3. 计算φ(n) = (p-1) × (q-1)
4. 选择整数e，使得1 < e < φ(n)，且gcd(e, φ(n)) = 1
5. 计算d，使得d × e ≡ 1 (mod φ(n))
6. 公钥：(e, n)，私钥：(d, n)

**加密和解密：**
- 加密：c = m^e mod n
- 解密：m = c^d mod n

**签名和验证：**
- 签名：s = m^d mod n
- 验证：m = s^e mod n

**安全性：**
- 密钥长度：目前推荐至少2048位， preferably 3072或4096位
- 随着量子计算机的发展，RSA可能面临威胁（Shor算法可以在多项式时间内分解大整数）

**性能：**
- 加密速度快（使用小的e，如65537）
- 解密速度慢（需要使用大的d）
- 比对称加密慢几个数量级

**应用场景：**
- TLS/SSL证书
- PGP/GPG加密
- SSH密钥
- 数字签名

#### 4.4 ECC算法

**ECC**（Elliptic Curve Cryptography）是基于椭圆曲线离散对数问题的非对称加密算法。

**算法原理：**
ECC基于椭圆曲线上的离散对数问题的困难性。与RSA相比，ECC可以用更短的密钥提供相同的安全性。

**椭圆曲线：**
椭圆曲线的方程：y^2 = x^3 + ax + b

**ECC的优势：**
1. **更短的密钥长度**：256位ECC ≈ 3072位RSA
2. **更快的计算速度**：特别是在密钥生成和签名验证上
3. **更低的计算资源消耗**：适合移动设备和物联网

**ECC的应用：**
- TLS/SSL（ECDHE、ECDSA）
- 加密货币（比特币使用secp256k1曲线）
- 移动设备加密
- 物联网安全

**常用曲线：**
- NIST曲线：P-256、P-384、P-521
- Curve25519：由Daniel J. Bernstein设计，用于EdDSA和ECDH
- secp256k1：比特币和以太坊使用的曲线

**安全性：**
- 密钥长度：P-256提供128位安全性，P-384提供192位安全性
- 抵抗量子攻击的能力与RSA相同（都需要后量子密码学替代）

#### 4.5 DH密钥交换

**DH**（Diffie-Hellman）密钥交换协议允许双方在不安全的信道上协商一个共享的秘密密钥。

**协议原理：**
DH基于离散对数问题的困难性。

**基本DH协议：**
1. Alice和Bob协商公共参数：大素数p和生成元g
2. Alice选择私钥a，计算A = g^a mod p，发送A给Bob
3. Bob选择私钥b，计算B = g^b mod p，发送B给Alice
4. Alice计算共享密钥：K = B^a mod p = (g^b)^a mod p = g^(ab) mod p
5. Bob计算共享密钥：K = A^b mod p = (g^a)^b mod p = g^(ab) mod p

**安全性：**
- 抵抗被动攻击：攻击者无法从截获的A和B计算出a或b
- 不提供认证：容易受到中间人攻击（需要结合数字签名或预共享密钥）

**ECDH**（Elliptic Curve Diffie-Hellman）：
- 使用椭圆曲线实现DH密钥交换
- 提供相同的安全性但使用更短的密钥
- 广泛用于现代协议（如TLS 1.3）

**DHE/ECDHE：**
- Ephemeral Diffie-Hellman（临时Diffie-Hellman）
- 每次会话使用新的密钥对，提供前向安全性（Forward Secrecy）
- 即使长期私钥泄露，过去的会话也无法被解密

#### 4.6 非对称加密的选择建议

**数字签名：**
- **首选**：ECDSA（P-256或Curve25519）
- **次选**：RSA（3072位或更长）

**密钥交换：**
- **首选**：ECDHE（提供前向安全性）
- **次选**：DHE

**加密：**
- 非对称加密通常不用于直接加密大量数据
- 使用非对称加密来协商对称加密的密钥（如TLS中的密钥交换）
- 然后使用对称加密（如AES）来加密实际数据

**后量子密码学：**
- 随着量子计算机的发展，RSA和ECC都面临威胁
- NIST正在标准化后量子密码算法（如CRYSTALS-Kyber、CRYSTALS-Dilithium）
- 对于需要长期安全性的系统，应考虑后量子密码学

### 5. 密码存储方式

安全地存储密码是系统安全的关键环节。本节介绍不同的密码存储方式及其安全性。

#### 5.1 明文存储

**定义：**
将用户的密码以明文形式存储在数据库中。

**示例：**
```
用户名: admin
密码: password123
```

**安全性：**
- **极不安全**
- 任何能够访问数据库的人（包括DBA、攻击者）都可以看到所有用户的密码
- 如果数据库泄露，所有用户的密码立即暴露
- 用户提供相同密码，攻击者可以跨系统使用（credential stuffing）

**法律和风险：**
- 违反GDPR、PCI DSS等法规和标准
- 导致账户接管、身份盗用等严重后果
- 损害用户信任和品牌声誉

**现状：**
- 任何现代系统都不应该明文存储密码
- 如果发现系统明文存储密码，应立即报告并修复

#### 5.2 哈希存储

**定义：**
将用户的密码通过哈希函数处理后再存储。

**示例：**
```
用户名: admin
密码哈希: 482c811da5d5b4bc6d497ffa98491e38 (MD5 of "password123")
```

**验证过程：**
1. 用户输入密码
2. 系统计算输入密码的哈希值
3. 将计算的哈希值与存储的哈希值比较
4. 如果匹配，则密码正确

**安全性问题：**
1. **字典攻击**：攻击者可以预先计算常见密码的哈希值，制作彩虹表
2. **相同密码相同哈希**：如果两个用户使用相同的密码，他们的哈希值也相同
3. **快速哈希**：MD5、SHA1、SHA256等设计用于快速计算，容易被暴力破解

**改进：**
- 使用慢哈希函数（如bcrypt、Argon2）
- 添加盐值（salt）

#### 5.3 加盐哈希存储

**定义：**
在密码哈希之前添加一个随机的盐值（salt），然后存储盐值和哈希值。

**示例：**
```
用户名: admin
盐值: abcdef123456 (随机生成的16字节)
密码哈希: bcrypt("abcdef123456" + "password123")
存储: abcdef123456$bcrypt哈希值
```

**盐值的作用：**
1. **唯一性**：即使两个用户使用相同的密码，由于盐值不同，哈希值也不同
2. **抵抗彩虹表**：攻击者需要为每个盐值重新计算彩虹表，大大增加攻击成本
3. **增加复杂度**：攻击者不能简单地使用预先计算的哈希值数据库

**盐值的要求：**
- **随机性**：使用密码学安全的随机数生成器
- **唯一性**：每个用户的盐值应该不同（即使他们使用相同的密码）
- **长度**：至少16字节（128位）
- **存储**：盐值不需要保密，可以与哈希值一起存储

**验证过程：**
1. 用户输入密码
2. 系统从存储中提取盐值
3. 计算：哈希值 = Hash(盐值 + 输入密码)
4. 比较计算的哈希值与存储的哈希值

**安全性：**
- 抵抗彩虹表攻击
- 抵抗字典攻击（但仍有被暴力破解的风险，取决于哈希函数的速度）

**最佳实践：**
- 使用bcrypt、Argon2等内置盐值的哈希函数
- 不要自己实现加盐逻辑，使用经过验证的库

#### 5.4 PEPPER

**定义：**
PEPPER是一个应用于所有密码的密钥或秘密值，与盐值不同，PEPPER不存储在数据库中，而是存储在应用程序的配置文件中。

**示例：**
```
PEPPER = "MySecretKey123" (存储在配置文件或环境变量中)
盐值 = 随机生成的16字节 (存储在数据库中)
密码哈希 = bcrypt(PEPPER + 盐值 + 用户密码)
存储: 盐值$bcrypt哈希值
```

**PEPPER的作用：**
1. **深度防御**：即使数据库被泄露，攻击者如果没有PEPPER，也无法破解密码哈希
2. **密钥管理**：PEPPER可以独立管理和轮换
3. **合规性**：某些安全标准推荐使用PEPPER

**PEPPER与盐值的区别：**
| 特性 | 盐值（Salt） | PEPPER |
|------|-------------|--------|
| 存储位置 | 数据库 | 配置文件/环境变量 |
| 唯一性 | 每个用户不同 | 所有用户相同 |
| 保密性 | 不需要保密 | 必须保密 |
| 作用 | 防止彩虹表 | 增加攻击难度 |

**安全性考虑：**
- PEPPER必须安全存储（如硬件安全模块HSM、密钥管理系统）
- 如果PEPPER泄露，所有用户的密码哈希都可以被攻击
- PEPPER轮换困难：需要重新哈希所有用户的密码

**实现建议：**
- 对于高安全性要求的系统，考虑使用PEPPER
- 使用密钥派生函数（如HKDF）从PEPPER派生实际的密钥
- 定期轮换PEPPER，并在用户登录时重新哈希密码

#### 5.5 密码存储的最佳实践

**推荐方案：**
1. **使用Argon2id**（首选）或**bcrypt**（次选）
2. **内置盐值**：让哈希函数自动生成盐值
3. **配置适当的成本参数**：
   - Argon2id：内存≥64MB，迭代次数≥3
   - bcrypt：work factor≥12
4. **考虑使用PEPPER**：对于高安全性系统
5. **定期审查和更新**：随着硬件性能提升，增加成本参数

**避免的方案：**
- ❌ 明文存储
- ❌ 简单的哈希（MD5、SHA1、SHA256）
- ❌ 自己实现的密码存储方案

**密码策略：**
- 强制使用强密码（长度、复杂性）
- 实施账户锁定机制（防止在线暴力破解）
- 实施多因素认证（MFA）
- 定期要求用户更改密码（但有争议，许多现代指南不再推荐强制定期更改）

**泄露响应：**
- 如果密码数据库泄露，立即通知用户
- 要求所有用户重置密码
- 审查日志记录，检查是否有可疑活动
- 实施事件响应计划

### 6. 密码攻击类型

了解密码攻击类型对于设计安全的系统和进行有效的渗透测试至关重要。

#### 6.1 字典攻击

**定义：**
字典攻击（Dictionary Attack）是使用预先准备好的单词列表（字典）来尝试破解密码的方法。

**攻击原理：**
1. 攻击者准备一个包含常见密码、单词、短语的字典文件
2. 对于目标哈希值，逐个计算字典中每个条目的哈希值
3. 如果计算的哈希值与目标哈希值匹配，则找到了密码

**字典来源：**
- 常见密码列表（如rockyou.txt，包含1400万个真实密码）
- 单词列表（如/usr/share/wordlists/words）
- 之前泄露的密码数据库
- 针对目标的定制字典（如公司名称、产品名称、常见模式）

**工具支持：**
- John the Ripper：支持多种字典格式
- Hashcat：支持大规模并行字典攻击
- Crunch：生成定制字典

**防御措施：**
- 使用强密码策略（长度、复杂性）
- 使用加盐哈希
- 使用慢哈希函数（如bcrypt、Argon2）
- 实施账户锁定

**示例：**
```bash
# 使用John the Ripper进行字典攻击
john --wordlist=rockyou.txt --format=raw-md5 hashes.txt

# 使用Hashcat进行字典攻击
hashcat -m 0 -a 0 hashes.txt rockyou.txt
```

#### 6.2 彩虹表攻击

**定义：**
彩虹表（Rainbow Table）是一种预先计算的哈希链，用于快速查找哈希值对应的明文密码。

**攻击原理：**
1. **预计算阶段**：
   - 选择一个起始明文，计算哈希值
   - 对哈希值应用归约函数（reduction function），得到新的明文
   - 重复上述步骤，形成一条链
   - 只存储链的起点和终点

2. **查找阶段**：
   - 给定哈希值，反复应用归约函数和哈希函数
   - 如果得到的值与某个链的终点匹配，则可以从该链的起点重新计算，找到原始明文

**优势：**
- 查找速度快（O(1)或O(n)的时间复杂度）
- 可以预先计算，多次使用

**防御措施：**
- **加盐**（Salt）：每个密码使用不同的盐值，攻击者需要为每个盐值创建不同的彩虹表
- **使用慢哈希函数**：增加预计算的成本
- **增加哈希长度**：增加彩虹表的大小

**现状：**
- 由于加盐哈希的广泛使用，彩虹表攻击的效果大大降低
- 现代密码存储应该使用加盐哈希，使彩虹表攻击不可行

**工具：**
- Ophcrack：用于Windows密码哈希的彩虹表攻击
- RainbowCrack：生成和使用彩虹表

#### 6.3 暴力破解

**定义：**
暴力破解（Brute Force Attack）是尝试所有可能的密码组合，直到找到正确的密码。

**攻击原理：**
1. 确定密码的空间（如长度、字符集）
2. 生成所有可能的密码组合
3. 对于每个组合，计算哈希值并与目标哈希值比较

**复杂度：**
- 如果密码长度为n，字符集大小为m，则需要尝试m^n次
- 例如：8位密码，使用大小写字母+数字+特殊字符（约80个字符），则需要尝试80^8 ≈ 1.68×10^15次

**在线暴力破解 vs 离线暴力破解：**
- **在线暴力破解**：直接尝试登录系统，受限于系统的速率限制和账户锁定机制
- **离线暴力破解**：获取密码哈希值后，在攻击者的机器上尝试，不受限制

**工具支持：**
- John the Ripper：支持暴力破解模式
- Hashcat：支持大规模并行暴力破解
- Hydra：用于在线暴力破解（支持多种协议）

**防御措施：**
- 使用长密码（≥12字符）
- 使用复杂的密码（大小写字母、数字、特殊字符）
- 使用账户锁定机制
- 使用多因素认证
- 使用慢哈希函数

**示例：**
```bash
# 使用Hashcat进行暴力破解（掩码攻击）
# ?a表示所有可打印字符，?l表示小写字母
hashcat -m 0 -a 3 hashes.txt ?l?l?l?l?l?l?l?l

# 使用John进行暴力破解
john --incremental --format=raw-md5 hashes.txt
```

#### 6.4 规则攻击

**定义：**
规则攻击（Rule-based Attack）是对字典中的单词应用一系列变换规则，生成新的候选密码。

**攻击原理：**
1. 从字典中读取基础单词
2. 应用规则（如大小写变换、添加数字、添加特殊字符、反转、重复等）
3. 对变换后的候选密码进行哈希并计算

**常见规则：**
- **大小写变换**：password → Password, PASSWORD
- **添加数字**：password → password1, password123
- **添加特殊字符**：password → password!, password@123
- **反转**：password → drowssap
- **重复**：password → passwordpassword
- **替换**：password → p@ssw0rd（用@替换a，用0替换o）
- **截取**：password → pass, word

**工具支持：**
- John the Ripper：支持规则文件（.rule）
- Hashcat：支持规则文件（.rule）

**优势：**
- 结合了字典攻击的效率和暴力破解的覆盖面
- 可以针对特定目标定制规则

**示例规则文件（John the Ripper格式）：**
```
# 在末尾添加数字
$[0-9]
$[0-9]$[0-9]

# 大小写变换
c
C

# 替换
s@4
s$a
s$e
s$i
s$o
s$s
s$t
```

**示例命令：**
```bash
# 使用John the Ripper应用规则
john --wordlist=rockyou.txt --rules=best64 --format=raw-md5 hashes.txt

# 使用Hashcat应用规则
hashcat -m 0 -a 0 hashes.txt rockyou.txt -r best64.rule
```

#### 6.5 其他攻击类型

**1. 社会工程学攻击**
- 通过欺骗、操纵获取密码
- 如钓鱼邮件、电话诈骗、肩窥（shoulder surfing）

**2. 键盘记录**
- 使用恶意软件记录键盘输入
- 可以捕获所有击键，包括密码

**3. 中间人攻击**
- 拦截通信，窃取密码
- 如不安全的Wi-Fi网络、恶意代理

**4. 凭证填充**
- 使用之前泄露的用户名/密码组合尝试登录其他系统
- 由于许多用户在不同系统使用相同密码，这种攻击非常有效

**5. 密码喷洒**
- 使用少数常见密码尝试登录多个账户
- 避免账户锁定（每次只尝试少数密码）

**防御措施总结：**
- 使用强密码
- 使用密码管理器
- 启用多因素认证
- 警惕社会工程学攻击
- 保持系统和软件更新
- 使用安全网络

---

## 🛠️ 实验环境

### 硬件要求
- CPU：支持AVX2指令集（用于Hashcat加速）
- 内存：至少8GB RAM
- 存储：至少20GB可用空间

### 软件要求
- **操作系统**：Kali Linux 2024.x 或 Ubuntu 22.04 LTS
- **Python**：3.8+
- **Hashcat**：6.2.6+
- **John the Ripper**：1.9.0+
- **Hydra**：9.3+
- **Medusa**：2.2+

### 环境搭建

#### 1. 安装Kali Linux（推荐）
```bash
# Kali Linux已预装大部分工具
# 更新系统
sudo apt update && sudo apt full-upgrade -y

# 安装额外工具
sudo apt install -y hashcat john hydra medusa
```

#### 2. 在Ubuntu上安装
```bash
# 添加仓库
sudo apt update
sudo apt install -y hashcat john hydra medusa

# 安装Python库
pip3 install pycryptodome passlib
```

#### 3. 验证安装
```bash
# 检查Hashcat
hashcat --version

# 检查John the Ripper
john --version

# 检查Hydra
hydra -h | head -5

# 检查Medusa
medusa -h | head -5
```

### 实验文件准备

创建实验目录结构：
```bash
mkdir -p ~/password-attacks/labs
cd ~/password-attacks/labs

# 创建示例哈希文件
echo "5f4dcc3b5aa765d61d8327deb882cf99" > md5_hash.txt  # password
echo "e10adc3949ba59abbe56e057f20f883e" > md5_hash2.txt # 123456
echo "098f6bcd4621d373cade4e832627b4f6" > md5_hash3.txt # test

# 创建ZIP加密文件
echo "This is a secret file." > secret.txt
zip -e -P "secret123" encrypted.zip secret.txt

# 生成SSH密钥对（无密码）
ssh-keygen -t rsa -f test_key -N ""

# 生成SSH密钥对（有密码）
ssh-keygen -t rsa -f test_key_encrypted -N "password123"
```

---

## 📝 实验步骤

### 实验1：破解MD5哈希

#### 目标
使用字典攻击和暴力破解方法破解MD5哈希值。

#### 步骤

**1. 准备字典文件**
```bash
# 创建常见密码字典
cat > common_passwords.txt << EOF
password
123456
password123
admin
root
test
guest
qwerty
letmein
1234
EOF
```

**2. 使用John the Ripper进行字典攻击**
```bash
# 基本字典攻击
john --wordlist=common_passwords.txt --format=raw-md5 md5_hash.txt

# 查看结果
john --show --format=raw-md5 md5_hash.txt
```

**3. 使用Hashcat进行字典攻击**
```bash
# 字典攻击模式（-a 0）
hashcat -m 0 -a 0 md5_hash.txt common_passwords.txt --force

# 查看结果
hashcat -m 0 md5_hash.txt --show
```

**4. 暴力破解（掩码攻击）**
```bash
# 使用Hashcat进行掩码攻击
# ?l = 小写字母, ?u = 大写字母, ?d = 数字, ?s = 特殊字符
# 尝试所有6位小写字母+数字的组合
hashcat -m 0 -a 3 md5_hash.txt ?l?l?l?l?l?l --force

# 更复杂的掩码
hashcat -m 0 -a 3 md5_hash.txt ?l?l?l?l?l?d --force
```

**5. 规则攻击**
```bash
# 使用Hashcat的规则文件
hashcat -m 0 -a 0 md5_hash.txt common_passwords.txt -r /usr/share/hashcat/rules/best64.rule --force

# 使用John the Ripper的规则
john --wordlist=common_passwords.txt --rules=Jumbo --format=raw-md5 md5_hash.txt
```

#### 预期结果
- 成功破解哈希值：`5f4dcc3b5aa765d61d8327deb882cf99` → `password`
- 成功破解哈希值：`e10adc3949ba59abbe56e057f20f883e` → `123456`
- 成功破解哈希值：`098f6bcd4621d373cade4e832627b4f6` → `test`

#### 分析与讨论
1. **为什么MD5不安全？**
   - 哈希长度太短（128位）
   - 已被证明存在碰撞攻击
   - 计算速度太快，容易被暴力破解

2. **如何防御？**
   - 使用慢哈希函数（bcrypt、Argon2）
   - 使用加盐哈希
   - 实施强密码策略

### 实验2：破解ZIP加密文件

#### 目标
使用John the Ripper和Hashcat破解ZIP文件的密码。

#### 步骤

**1. 提取ZIP文件的哈希值**
```bash
# 使用zip2john提取哈希
zip2john encrypted.zip > zip_hash.txt

# 查看提取的哈希
cat zip_hash.txt
```

**2. 使用John the Ripper破解**
```bash
# 使用字典攻击
john --wordlist=common_passwords.txt zip_hash.txt

# 查看结果
john --show zip_hash.txt
```

**3. 使用Hashcat破解**
```bash
# 转换哈希格式为Hashcat兼容格式
# 手动编辑zip_hash.txt，提取哈希部分

# 使用Hashcat破解ZIP密码（模式17200）
hashcat -m 17200 -a 0 zip_hash.txt common_passwords.txt --force
```

**4. 使用fcrackzip（备选工具）**
```bash
# 安装fcrackzip
sudo apt install -y fcrackzip

# 使用字典攻击
fcrackzip -u -D -p common_passwords.txt encrypted.zip

# 暴力破解
fcrackzip -u -b -l 1-6 -c a encrypted.zip  # 1-6位小写字母
```

#### 预期结果
- 成功破解ZIP密码：`secret123`

#### 分析与讨论
1. **ZIP加密的安全性**
   - ZIP使用AES-256或ZIP 2.0加密（较弱）
   - 密码强度直接影响安全性

2. **如何创建安全的ZIP文件？**
   - 使用AES-256加密：`zip -e -P password file.zip file.txt`（某些版本支持）
   - 使用7-Zip：`7z a -p -mhe=on encrypted.7z file.txt`

### 实验3：破解SSH私钥密码

#### 目标
使用John the Ripper破解加密的SSH私钥密码。

#### 步骤

**1. 转换SSH私钥为John可识别的格式**
```bash
# 使用ssh2john转换私钥
# 注意：某些版本的John the Ripper内置ssh2john
python3 /usr/share/john/ssh2john.py test_key_encrypted > ssh_hash.txt

# 查看转换后的哈希
cat ssh_hash.txt
```

**2. 使用John the Ripper破解**
```bash
# 使用字典攻击
john --wordlist=common_passwords.txt ssh_hash.txt

# 查看结果
john --show ssh_hash.txt
```

**3. 使用Hashcat破解**
```bash
# Hashcat支持SSH私钥格式（模式22911）
# 需要先将私钥转换为OpenSSH格式
ssh-keygen -p -f test_key_encrypted -N "newpassword" -O test_key_openssh

# 使用Hashcat破解
hashcat -m 22911 -a 0 ssh_hash.txt common_passwords.txt --force
```

#### 预期结果
- 成功破解SSH私钥密码：`password123`

#### 分析与讨论
1. **如何保护SSH私钥？**
   - 使用强密码加密私钥
   - 将私钥权限设置为600（`chmod 600 ~/.ssh/id_rsa`）
   - 考虑使用SSH代理（ssh-agent）
   - 使用硬件安全密钥（如YubiKey）

2. **无密码SSH密钥的风险**
   - 如果私钥泄露，攻击者可以直接访问所有授权系统
   - 应使用密码加密私钥

### 实验4：在线密码攻击（Hydra）

#### 目标
使用Hydra对SSH、FTP、HTTP等服务进行在线密码攻击。

#### 步骤

**1. 准备目标环境**
```bash
# 安装并配置SSH服务（仅用于实验）
sudo apt install -y openssh-server
sudo systemctl start ssh

# 创建测试用户
sudo useradd -m testuser
echo "testuser:password123" | sudo chpasswd
```

**2. 使用Hydra攻击SSH**
```bash
# 准备用户名列表和密码列表
echo "testuser" > users.txt
echo "password123" > passwords.txt
echo "root" >> users.txt
echo "toor" >> passwords.txt

# 使用Hydra进行暴力破解
hydra -L users.txt -P passwords.txt ssh://localhost

# 指定用户名和密码
hydra -l testuser -P passwords.txt ssh://localhost
```

**3. 使用Hydra攻击FTP**
```bash
# 安装并配置FTP服务
sudo apt install -y vsftpd
sudo systemctl start vsftpd

# 攻击FTP
hydra -L users.txt -P passwords.txt ftp://localhost
```

**4. 使用Hydra攻击HTTP表单**
```bash
# 攻击HTTP POST表单
hydra -L users.txt -P passwords.txt localhost http-post-form "/login.php:user=^USER^&pass=^PASS^:Invalid password"

# 攻击HTTP基本认证
hydra -L users.txt -P passwords.txt localhost http-get-auth "/admin/"
```

#### 预期结果
- 成功破解SSH密码：`testuser:password123`

#### 分析与讨论
1. **在线攻击的防御措施**
   - 实施账户锁定（失败次数限制）
   - 使用验证码
   - 实施速率限制
   - 监控异常登录尝试
   - 使用fail2ban等工具

2. **法律风险**
   - 未经授权对他人系统进行密码攻击是**非法**的
   - 仅在自己的实验环境或获得明确授权的渗透测试中进行

### 实验5：使用Medusa进行在线攻击

#### 目标
使用Medusa作为Hydra的替代工具进行在线密码攻击。

#### 步骤

**1. 使用Medusa攻击SSH**
```bash
# 基本用法
medusa -h localhost -u testuser -P passwords.txt -M ssh

# 使用用户名列表
medusa -h localhost -U users.txt -P passwords.txt -M ssh

# 指定端口
medusa -h localhost -u testuser -P passwords.txt -M ssh -n 2222
```

**2. 使用Medusa攻击FTP**
```bash
medusa -h localhost -U users.txt -P passwords.txt -M ftp
```

**3. 并行攻击多个主机**
```bash
# 创建主机列表
echo "192.168.1.10" > hosts.txt
echo "192.168.1.11" >> hosts.txt

# 攻击多个主机
medusa -H hosts.txt -u admin -P passwords.txt -M ssh
```

#### 预期结果
- Medusa和Hydra功能类似，但语法略有不同
- 选择哪个工具取决于个人偏好和特定需求

---

## 💡 解题技巧

### 1. 密码破解的一般流程

```
1. 识别哈希类型
   ↓
2. 选择合适的攻击方法
   ↓
3. 准备字典/规则/掩码
   ↓
4. 执行攻击
   ↓
5. 分析结果
   ↓
6. 如果失败，调整策略并重试
```

### 2. 识别哈希类型

**使用hashid工具：**
```bash
# 安装hashid
pip3 install hashid

# 识别哈希类型
hashid -m 5f4dcc3b5aa765d61d8327deb882cf99
```

**使用Hashcat的示例模式：**
```bash
# 尝试自动识别
hashcat -m 0 hash.txt wordlist.txt  # MD5
hashcat -m 100 hash.txt wordlist.txt  # SHA1
hashcat -m 1400 hash.txt wordlist.txt  # SHA256
hashcat -m 1800 hash.txt wordlist.txt  # sha512crypt
```

**常见哈希特征：**
| 哈希示例 | 类型 | 长度 |
|---------|------|------|
| 5f4dcc3b5aa765d61d8327deb882cf99 | MD5 | 32字符 |
| 5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8 | SHA1 | 40字符 |
| 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 | SHA256 | 64字符 |
| $1$abc123$.... | md5crypt | 可变 |
| $5$abc123$.... | sha256crypt | 可变 |

### 3. 提高破解效率的技巧

**1. 选择合适的攻击模式**
- 已知密码模式 → 字典攻击 + 规则
- 未知密码 → 掩码攻击（如果长度已知）
- 完全未知 → 字典攻击（更大的字典）

**2. 优化字典**
```bash
# 排序和去重
sort common_passwords.txt | uniq > optimized_dict.txt

# 根据目标定制字典
cewl -w custom_dict.txt https://target-website.com
```

**3. 使用规则智能变换**
```bash
# John the Ripper内置规则
--rules=Jumbo
--rules=Extra
--rules=Best66

# Hashcat内置规则
-r best64.rule
-r d3ad0ne.rule
-r Leetspeak.rule
```

**4. 利用GPU加速**
```bash
# 检查GPU
hashcat -I

# 使用GPU（默认）
hashcat -m 0 hash.txt dict.txt

# 指定GPU设备
hashcat -m 0 -d 1 hash.txt dict.txt
```

**5. 分布式破解**
- 使用Hashtopolis等工具
- 多台机器协同工作

### 4. 应对复杂密码的策略

**1. 密码模式分析**
- 分析目标用户的密码习惯
- 常见模式：公司名称+年份、宠物名字+数字等

**2. 组合攻击**
```bash
# Hashcat组合攻击（-a 1）
# 将两个字典组合
hashcat -m 0 -a 1 hash.txt dict1.txt dict2.txt
```

**3. 混合攻击**
```bash
# 字典 + 掩码
hashcat -m 0 -a 6 hash.txt dict.txt ?d?d?d
```

**4. 基于知识的攻击**
- 收集目标的信息（社交媒体、公开资料）
- 构建定制字典

### 5. 避免常见错误

**1. 哈希格式错误**
```bash
# 确保哈希格式正确
# 错误的：5f4dcc3b5aa765d61d8327deb882cf99username
# 正确的：5f4dcc3b5aa765d61d8327deb882cf99
```

**2. 选择错误的哈希模式**
```bash
# 确保使用正确的-m参数
# MD5: -m 0
# SHA1: -m 100
# SHA256: -m 1400
```

**3. 字典编码问题**
```bash
# 转换字典编码为UTF-8
iconv -f ISO-8859-1 -t UTF-8 dict.txt > dict_utf8.txt
```

**4. 忽略盐值**
- 确保正确提取和提供盐值
- 某些哈希格式需要在哈希中包含盐值

---

## 🛡️ 防御措施

### 1. 安全的密码存储

**✅ 应该做的：**
1. **使用现代哈希算法**
   - Argon2id（首选）
   - bcrypt（广泛支持）
   - PBKDF2（FIPS认证环境）

2. **正确配置参数**
   ```python
   # 使用bcrypt示例
   import bcrypt
   
   # 哈希密码（work factor=12）
   password = b"user_password"
   hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
   
   # 验证密码
   if bcrypt.checkpw(password, hashed):
       print("Password matches")
   ```

   ```python
   # 使用Argon2示例
   from argon2 import PasswordHasher
   
   ph = PasswordHasher(
       time_cost=3,
       memory_cost=65536,  # 64 MB
       parallelism=4
   )
   
   # 哈希密码
   hash = ph.hash("user_password")
   
   # 验证密码
   if ph.verify(hash, "user_password"):
       print("Password matches")
   ```

3. **使用PEPPER**（可选）
   ```python
   import os
   import hmac
   
   PEPPER = os.environ.get('PASSWORD_PEPPER')
   
   def hash_password(password):
       salt = os.urandom(16)
       # 将PEPPER应用于密码
       peppered_password = hmac.new(PEPPER.encode(), password.encode(), 'sha256').hexdigest()
       # 然后使用bcrypt/Argon2哈希
       return bcrypt.hashpw(peppered_password.encode(), bcrypt.gensalt())
   ```

**❌ 不应该做的：**
1. 明文存储密码
2. 使用MD5、SHA1、SHA256 alone（没有盐值和迭代）
3. 自己实现密码哈希方案
4. 使用固定的盐值

### 2. 密码策略

**1. 强密码要求**
- 最小长度：12-16字符
- 复杂性：大小写字母、数字、特殊字符
- 避免常见密码
- 避免个人信息（生日、名字等）

**2. 密码检查**
```python
# 使用passlib检查密码强度
from passlib import pwd

# 生成强密码
strong_password = pwd.genword(length=16, charset="ascii_72")

# 检查密码强度（使用zxcvbn库）
from zxcvbn import zxcvbn

result = zxcvbn("user_password")
if result['score'] < 3:
    print("Password is too weak")
```

**3. 避免密码重用**
- 强制用户使用新密码
- 检查密码是否与之前使用的密码相似
- 实施密码历史记录

### 3. 多因素认证（MFA）

**1. 什么是MFA？**
- 密码（你知道的）
- 手机/硬件令牌（你拥有的）
- 指纹/面部识别（你本身的）

**2. MFA的实现**
- TOTP（Time-Based One-Time Password）：Google Authenticator、Authy
- SMS/Email验证码（较不安全）
- 硬件令牌：YubiKey
- 生物识别

**3. 即使密码被破解，MFA也能提供保护**

### 4. 账户锁定和监控

**1. 账户锁定策略**
- 失败尝试次数：5-10次
- 锁定时间：15-30分钟
- 渐进式延迟：每次失败增加等待时间

**2. 监控和告警**
- 监控异常登录尝试
- 检测暴力破解攻击
- 实时告警

**3. 使用fail2ban**
```bash
# 安装fail2ban
sudo apt install -y fail2ban

# 配置fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# 启动fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### 5. 安全的密码传输

**1. 使用HTTPS/TLS**
- 确保所有登录页面使用HTTPS
- 使用HSTS（HTTP Strict Transport Security）
- 使用最新的TLS版本（1.2或1.3）

**2. 避免明文传输**
- 不要在URL参数中传递密码
- 使用POST请求而不是GET请求
- 在客户端进行哈希（额外保护层，但不能替代服务器端哈希）

### 6. 用户教育

**1. 教育内容**
- 如何创建强密码
- 不要在不安全的地方存储密码
- 警惕社会工程学攻击
- 使用密码管理器

**2. 密码管理器推荐**
- 1Password
- LastPass
- Bitwarden
- KeePass

**3. 定期安全培训**
- 钓鱼邮件识别
- 安全浏览习惯
- 报告安全事件

### 7. 事件响应

**1. 密码泄露的应对措施**
- 立即重置所有受影响的密码
- 通知用户
- 审查访问日志
- 报告监管机构（如适用）

**2. 定期对密码进行审计**
- 检查是否有弱密码
- 检查是否有重复密码
- 模拟攻击测试

---

## 📝 课后练习

### 练习1：识别哈希类型
给定以下哈希值，识别它们的类型：
1. `5f4dcc3b5aa765d61d8327deb882cf99`
2. `5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8`
3. `$2y$12$LQvS3vi4.nTWmKDRW4hS9ebv6FvPeN9GSUvYUsGZXNJU3/Ll8tzRW`
4. `e0c9035898dd52fc65c41454cec9c4d2611bfb37f55701f473961bc2c8ea0c81`

**提示**：使用hashid工具或查阅哈希特征表。

### 练习2：字典攻击实践
1. 创建一个包含100个最常见密码的字典文件
2. 使用John the Ripper对一个MD5哈希文件进行字典攻击
3. 记录破解时间和成功率
4. 尝试不同的规则文件，观察效果

### 练习3：掩码攻击设计
设计一个掩码来破解以下模式的密码：
1. 公司名称（如"Acme"）+ 年份（如"2024"）
2. 宠物名字（已知是"Fluffy"）+ 2位数字
3. 任何8位密码，包含大小写字母、数字和特殊字符

**提示**：使用Hashcat的掩码功能。

### 练习4：安全密码存储实现
使用Python实现一个安全的密码存储和验证系统：
1. 使用bcrypt或Argon2
2. 实现注册功能（哈希密码并存储）
3. 实现登录功能（验证密码）
4. 添加PEPPER（可选）
5. 测试系统

**提示**：使用passlib或argon2-cffi库。

### 练习5：分析真实泄露数据
（注意：仅使用合法获得的公开泄露数据集，如RockYou）

1. 分析RockYou密码数据集
2. 统计最常见密码
3. 分析密码长度分布
4. 识别常见模式
5. 提出改进密码策略的建议

### 练习6：加固系统
对一个实际的系统（如你自己的服务器或实验环境）进行密码安全加固：
1. 检查当前密码存储方式
2. 实施强密码策略
3. 配置账户锁定
4. 安装和配置fail2ban
5. 启用多因素认证
6. 撰写加固报告

### 练习7：研究项目
选择一个主题进行深入研究：
1. 量子计算对密码学的影响
2. 后量子密码学的发展
3. 生物识别技术的安全性
4. 密码管理器的安全性分析
5. 多因素认证的实现比较

---

## ❓ FAQ

### Q1：为什么不使用MD5或SHA1来存储密码？
**A**：MD5和SHA1都不是为密码存储设计的，它们有以下问题：
1. **计算速度太快**：现代GPU可以在短时间内尝试数十亿个密码
2. **没有内置盐值**：需要使用额外的机制来添加盐值
3. **已被证明不安全**：存在碰撞攻击
4. **没有可调节的成本参数**：无法增加计算成本来抵抗暴力破解

应该使用专门为密码存储设计的慢哈希函数，如bcrypt、Argon2。

### Q2：什么是"慢哈希函数"？为什么需要它？
**A**：慢哈希函数是通过故意增加计算时间来抵抗暴力破解的哈希函数。
- **原理**：通过多次迭代或使用大量内存来增加单次哈希计算的时间
- **效果**：使暴力破解需要的时间大大增加，而正常用户登录的影响可以忽略不计
- **例子**：bcrypt、Argon2、PBKDF2

### Q3：盐值（salt）需要保密吗？
**A**：不需要。盐值的作用是确保相同的密码产生不同的哈希值，防止彩虹表攻击。盐值可以与哈希值一起存储（通常是明文存储）。重要的是盐值应该是随机的且对每个用户唯一。

### Q4：PEPPER和盐值有什么区别？
**A**：
- **盐值**：每个用户不同，与哈希值一起存储在数据库中，不需要保密
- **PEPPER**：所有用户相同，存储在配置文件或环境变量中，必须保密

PEPPER提供了深度防御：即使数据库被泄露，攻击者也需要PEPPER才能破解密码哈希。

### Q5：如何选择合适的哈希函数？
**A**：
1. **新项目**：使用Argon2id（最新、最安全）
2. **广泛支持需求**：使用bcrypt（成熟、被广泛支持）
3. **FIPS认证环境**：使用PBKDF2
4. **避免**：MD5、SHA1、SHA256（alone，没有盐值和迭代）

### Q6：密码应该多久更换一次？
**A**：现代安全指南（如NIST）不再推荐强制定期更换密码，因为：
1. 用户往往会选择弱密码或只做微小更改
2. 频繁更改导致用户疲劳，可能选择更弱的密码
3. 没有证据表明定期更改能显著提高安全性

**应该更改密码的情况**：
- 怀疑密码泄露
- 密码共享给了他人
- 使用相同密码的网站发生数据泄露

### Q7：多因素认证（MFA）真的有必要吗？
**A**：非常必要。即使密码被破解或泄露，MFA也能提供额外的保护层。统计表明，MFA可以防止超过99%的自动化攻击。

### Q8：如何创建一个强密码？
**A**：
1. **长度**：至少12-16字符
2. **复杂性**：大小写字母、数字、特殊字符的组合
3. **随机性**：避免使用字典单词、个人信息
4. **唯一性**：每个账户使用不同的密码
5. **使用密码管理器**：生成和存储强密码

**示例强密码**：`Tr!ckyP@ssw0rd2024!`

### Q9：在线密码攻击和离线密码攻击有什么区别？
**A**：
- **在线攻击**：直接尝试登录系统，受系统防护机制（如账户锁定、验证码）限制
- **离线攻击**：获取密码哈希值后，在攻击者自己的机器上尝试，不受限制，可以使用GPU加速

离线攻击更危险，因为攻击者可以尝试数十亿次每秒。

### Q10：我可以使用这些工具来测试我的系统吗？
**A**：可以，但**必须**确保：
1. 你拥有系统的所有权
2. 或者获得了明确的书面授权
3. 在受控的实验环境中进行

**警告**：未经授权对他人系统进行密码攻击是**非法**的，可能面临刑事指控。

---

## 📊 总结

### 关键知识点回顾

#### 1. 哈希算法
- **MD5**：128位，已被证明不安全，不推荐用于安全目的
- **SHA1**：160位，已被证明不安全，正在被逐步淘汰
- **SHA256**：256位，安全但**不适合**直接用于密码存储（需要加盐和使用慢哈希）
- **bcrypt**：专门为密码存储设计，内置盐值，可调节成本
- **Argon2**：最新的密码哈希标准，抵抗GPU和ASIC攻击

#### 2. 对称加密
- **AES**：目前的标准，安全且快速
- **DES**：不安全，密钥长度太短
- **3DES**：比DES安全，但慢且将被淘汰
- **RC4**：流密码，已被证明存在漏洞，不推荐使用

#### 3. 非对称加密
- **RSA**：基于大整数分解，广泛使用，推荐密钥长度≥2048位
- **ECC**：基于椭圆曲线，更短的密钥提供相同安全性，适合移动设备
- **DH**：密钥交换协议，应使用ECDHE提供前向安全性

#### 4. 密码存储方式
- **明文存储**：极不安全，绝对避免
- **简单哈希**：不安全，容易被字典攻击和彩虹表攻击
- **加盐哈希**：安全，应使用bcrypt或Argon2
- **PEPPER**：可选的深度防御措施

#### 5. 密码攻击类型
- **字典攻击**：使用预先准备的密码列表
- **彩虹表攻击**：预先计算的哈希链，可通过加盐防御
- **暴力破解**：尝试所有可能的组合
- **规则攻击**：对字典单词应用变换规则

#### 6. 常用工具
- **John the Ripper**：功能强大的密码破解工具，支持多种哈希类型和攻击模式
- **Hashcat**：利用GPU加速，支持大规模并行破解
- **Hydra**：在线密码攻击工具，支持多种协议
- **Medusa**：Hydra的替代工具，语法类似

### 安全最佳实践总结

#### 对于开发者
1. ✅ 使用Argon2id或bcrypt存储密码
2. ✅ 正确配置哈希成本参数
3. ✅ 实施强密码策略
4. ✅ 启用多因素认证
5. ✅ 使用HTTPS/TLS传输密码
6. ✅ 实施账户锁定和监控
7. ❌ 不要明文存储密码
8. ❌ 不要使用MD5、SHA1或简单哈希
9. ❌ 不要自己实现密码哈希方案

#### 对于用户
1. ✅ 使用强密码（长、复杂、随机）
2. ✅ 使用密码管理器
3. ✅ 启用多因素认证
4. ✅ 不要在不安全的地方存储密码
5. ✅ 定期审查账户活动
6. ❌ 不要在不同网站使用相同密码
7. ❌ 不要通过电子邮件或聊天发送密码
8. ❌ 不要使用容易猜测的密码（如生日、名字）

#### 对于渗透测试人员
1. ✅ 获得明确授权
2. ✅ 在受控环境中进行测试
3. ✅ 使用合法获得的工具和数据
4. ✅ 报告发现的所有漏洞
5. ✅ 遵守法律和道德准则
6. ❌ 不要对未授权的系统进行攻击
7. ❌ 不要使用获得的访问权限进行非法活动
8. ❌ 不要泄露测试中获得敏感信息

### 未来发展趋势

#### 1. 后量子密码学
- 量子计算机的发展威胁到RSA和ECC
- NIST正在标准化后量子密码算法
- 组织应开始规划向后量子密码学的迁移

#### 2. 无密码认证
- FIDO2/WebAuthn标准
- 生物识别技术
- 硬件安全密钥
- 魔法链接（Magic Link）

#### 3. 零信任安全模型
- 不再默认信任内网
- 持续验证
- 最小权限原则

#### 4. 人工智能在密码安全中的应用
- 检测异常登录行为
- 智能密码强度评估
- 自动化的安全审计

### 进一步学习资源

#### 书籍
1. 《Applied Cryptography》- Bruce Schneier
2. 《Cryptography Engineering》- Niels Ferguson, Bruce Schneier, Tadayoshi Kohno
3. 《Practical Cryptography》- Bruce Schneier
4. 《The Web Application Hacker's Handbook》- Dafydd Stuttard, Marcus Pinto

#### 在线课程
1. Coursera: "Cryptography I" - Stanford University
2. edX: "Cryptography and Cryptanalysis" - MIT
3. Udemy: "Ethical Hacking" 系列课程

#### 工具和练习平台
1. TryHackMe - 在线渗透测试练习平台
2. Hack The Box - 高级渗透测试练习平台
3. OverTheWire - Wargame练习
4. Cryptopals - 密码学编程挑战

#### 会议和社区
1. DEF CON
2. Black Hat
3. USENIX Security
4. r/netsec (Reddit)
5. OWASP

---

## 🎓 结语

密码学是信息安全的基石，而密码攻击是理解密码学安全性的重要途径。通过本章的学习，您应该已经掌握了：

1. 密码学的基本概念和原理
2. 常见哈希算法、对称加密和非对称加密的特点
3. 安全的密码存储方法
4. 各种密码攻击技术的原理和实施方法
5. 如何使用John the Ripper、Hashcat、Hydra等工具
6. 密码安全的最佳实践

**记住**：
- 知识本身是中性的，如何使用它取决于个人
- 始终遵守法律和道德准则
- 使用你的知识来保护系统和数据，而不是破坏它们
- 持续学习，因为密码学和安全领域在不断发展

祝你在网络安全的学习旅程中取得成功！

---

## 📚 参考资料

1. NIST Special Publication 800-63B: Digital Identity Guidelines
2. OWASP Authentication Cheat Sheet
3. RFC 2898: Password-Based Cryptography Specification
4. Argon2: the memory-hard function for password hashing and other applications
5. John the Ripper documentation: https://www.openwall.com/john/doc/
6. Hashcat documentation: https://hashcat.net/wiki/
7. Hydra documentation: https://github.com/vanhauser-thc/thc-hydra
8. NIST Post-Quantum Cryptography: https://csrc.nist.gov/projects/post-quantum-cryptography

---

**文档版本**: 1.0  
**最后更新**: 2024年  
**作者**: 红客初学者指南课程组

---

> **免责声明**：本课程仅供教育目的。未经授权使用这里介绍的技术攻击系统是非法的。确保你只在拥有明确授权的系统上进行测试。作者对任何滥用这些技术的行为不承担任何责任。
