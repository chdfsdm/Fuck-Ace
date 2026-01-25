# Fuck-Ace（ACE 我C尼玛）
这个项目主要目的是给某企鹅公司底下以ACE为开头的反作弊运行文件上debuff。

包含有：

        设置cpu优先级为低于正常。
        cpu亲和性位掩码为F00000（十六进制）。
        i/o优先级为低。
        gpu优先级为低于正常。
        为程序开启效能模式。

程序检测时间为30秒一次，可以在后台自动运行，兼容多种模式，无法重复启动。
因为改得太低可能会导致游戏闪退崩溃等问题，所以设置得比较保守。如有需要可以自行调整。

缺陷：会对其他以ace开头的运行程序造成误伤，不过作者孤陋寡闻，暂时没见过这种命名的程序。

使用方法：

        将代码打包成程序，程序复制到开机自启动文件夹里面，然后管理员运行一次。
        在任务管理器里面能找到跟文件名一样的程序就算成功。


# Fuck-Ace (Fk You ACE)
The main purpose of this project is to apply "debuffs" (penalties) to the anticheat executable files starting with "ACE" from a certain Penguin Company——Tencent.

Features include:

         CPU Priority: Set to "Below Normal".
         CPU Affinity: Bitmask set to F00000 (Hexadecimal).
         I/O Priority: Set to "Low".
         GPU Priority: Set to "Below Normal".
         Power Mode: Enables "Efficiency Mode" for the process.
        
The program scans every 30 seconds and runs automatically in the background. It is compatible with multiple modes and prevents duplicate startups.
The settings are kept conservative to prevent the game from crashing or freezing. You can adjust them manually if needed.

Known Defects:This may cause "friendly fire" (collateral damage) to other legitimate processes starting with "ace". However, the author hasn't encountered any such programs before.

Usage:

        1. Compile the code into an executable.
        2. Copy the program into your Startup folder.
        3. Run it once as Administrator.
        4. Verification: You can check Task Manager; if you see a process with the same name as the file, it means it's running successfully.
