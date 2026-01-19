#中文-en-语言文字层 #思考

  wsl命令测试是否开启服务，如何--update 更新wsl核心

尝试下载Linux系统，比如Ubuntu，【提示了error，标识为【WslRegisterDistribution failed with error: 0x80370102
Please enable the Virtual Machine Platform Windows feature and ensure virtualization is enabled in the BIOS.】

按照提示，我检查了bios下的虚拟化功能，
下载并安装了最新的 WSL2 内核。
启用【**控制面板** > **程序和功能** > **启用或关闭 Windows 功能**。】 Hyper-V和虚拟机平台选项。
最后我也重启计算机，并且使用命令检查确定开启成功。

那么还有什么可能，我用来一个软件“clash for Windows”来上外网。我能够打开微软商店，这意味什么，我不知道。我的网络知识很匮乏，但是直觉上应该是和网络相关，毕竟我在中国，docker似乎是被ban的。这个问题本应该就是一个简单安装的操作。
另外，还有别的可能吗？是很有可能的。但是一个一个尝试。不然效率会大打折扣。

事实上，我的认知系统崩溃了，输出了长时间的不舒服感受在头部眼部的明显感受。
和[[gpt聊天-wsl]]；

我尝试安装其他Linux发行版本，提示仍然是一样的错误提示。这表明问题出现不在Ubuntu 版本。

我想起某个视频说到了配置端口

尝试clash for Windows，暴力尝试。

检查系统要求：x64系统 msinfo32 19045 满足虚拟化

查询越多内容，分支解决路径越多。决定放弃前我抱着试一试的态度，Google并看到一个。查询进程里的cpu虚拟化，发现昨天在bios确认过ivt是en但是在这是dis。
于是我重启bios开启虚拟化，
成功解决。
fuck！
好的，具体问题解决。不要再提具体问题。
对我的思考刚刚开始。

