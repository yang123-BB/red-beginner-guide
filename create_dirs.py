import os

BASE = r"C:\Users\dell\.qclaw\workspace\红客初学者指南课件\docs"

chapters = [
    "01_红客之道：法律、伦理与职业操守",
    "02_搭建安全实验环境",
    "03_Linux基础与命令行精通",
    "04_计算机网络基础深度解析",
    "05_Python编程for_Hackers",
    "06_信息收集与OSINT",
    "07_漏洞扫描与评估",
    "08_Web安全与OWASP_Top_10",
    "09_Burp_Suite实战",
    "10_Metasploit_Framework精通",
    "11_权限提升（Privilege_Escalation）",
    "12_密码学基础与密码攻击",
    "13_后渗透与横向移动",
    "14_Active_Directory攻防",
    "15_无线网络安全",
    "16_社会工程学实战",
    "17_红队演练全流程",
    "18_认证体系与职业发展",
]

os.makedirs(BASE, exist_ok=True)
for ch in chapters:
    path = os.path.join(BASE, ch)
    os.makedirs(path, exist_ok=True)
    print(f"Created: docs/{ch}/")

print(f"\nTotal: {len(chapters)} directories created.")
