---
title: "我用Obsidian + Claude Code搭了一个健脑房"
url: "https://x.com/haoshanhong/status/2041013937815298207"
date: 2026-04-07
author:
  - "@haoshanhong"
"wiki-tags": " pending"
---


# 我用Obsidian + Claude Code搭了一个健脑房

**Source:** [X (Twitter)](https://x.com/haoshanhong/status/2041013937815298207)
**Published:** 2026-04-06 | **Clipped:** 2026-04-07


## Full Content
Obsidian不只有一种使用方法。如果你看了别人的教程一头雾水的话，那你大概率适合我这种方法。GitHub上开源了仓库模板，文末有链接，先收藏再看。

即便你不全盘采用，我相信有一些解决方案也一定会对你有启发。前六章是原则讲解，第七章开始是方案如何实现。

我有一个COO负责统筹整个仓库，我的大小事宜，从出门约会到产品推进节奏都经由他的手。

具体到每个项目，也有专人负责，比如产品有一个负责技术的CTO来和我商讨技术细节和工程师的任免。

此外，个人生活上也有个心理医生给我做不定期的疏导，确保我不会因为压力大出问题。

当然，他们要是有谁一直出错，那对不起，直接开除走人。结果无一例外，总是下一个更乖。

我是怎么用Obsidian+Claude Code实现稳定、高效的工作的？

![图像](https://pbs.twimg.com/media/HFMcDu2aYAA7nSV?format=png&name=large)

## 一、未经人脑处理的知识不进仓库

Obsidian不是我的第二大脑，不是我大脑的移动硬盘，而是我的“健脑房”和工作台。

我在四五年前也确实是把Obsidian当作个人知识管理来用的，把心理学、文学甚至数学知识放进去存储。结果大部分的知识到最后都用不到，虽说记的过程本身加深了印象，但总体来说还是白费功夫。

现如今，想要知道什么信息就让顶尖的AI来搜索一番，大概率比记的笔记准确全面，甚至可能更快速，那费尽心思维护的这些笔记是为了什么呢？更何况在今天记录到仓库的笔记很多本身就是AI生成的，一年后读着这老模型写出来的笔记，有什么益处呢？外来的信息就像一个放在家门口的快递包裹，在你拆开拿到家里之前，即便你说是你的，也很可能被别人偷走。

![图像](https://pbs.twimg.com/media/HFMeLIsa4AAaGIr?format=png&name=large)

老仓库的知识图谱

越是AI当道，人越要锻炼大脑。Obsidian不仅是一个生产力工具，还是锻炼和促使我思考的地方，而不只是一个记录的工具。

因此，我仓库中的第一个重要原则就是：**未经人脑处理的知识不进仓库**。外部信息止步于“收件箱”，只有经过我思考的内容才能进入“笔记”。

## 二、输入服务于输出

Obsidian原本是一个生产力工具，有产出才叫生产力工具。

这个软件的整体逻辑是服务于写作的：关于一个话题积累足够多链接的笔记/点子，于是把积少成多的智慧结晶集结成文或书。这就会导致一个只在Obsidian里囤积居奇而从不输出内容的人，用这个软件会非常的别扭。

现在有了一种新的用法。Karpathy把Obsidian做成了一个阅读器，一个自定义图书馆。把资料喂给AI，AI帮你编译成wiki，随时查随时问。用优质source，自己筛选，AI编译，研究质量确实高。他这个项目的名字也就叫“知识库”，完全是阅读的逻辑。这是Obsidian的一个创新用法，但实话讲，如果不用Obsidian他这个需求也完全可以用html干了。

![图像](https://pbs.twimg.com/media/HFMgbIebsAAXMvf?format=jpg&name=large)

当然一直以来Obsidian的阅读器属性和写作软件属性是并存的，不过由于我使用Obsidian的时间比较长，并且一直在基于自己的使用习惯和需求完善用法，所以我更多地把Obsidian当做一个内容产出工具，这也是为什么在文首我就说了Obsidian不只有一种使用方法。

作为产出内容的工具，我保留了Obsidian原本的双链功能。每一条经过思考，进入仓库的笔记，都会由AI打标，指向相关的项目，以备积少成多后使用。

这两种方法没有高下之分，如果你想要用Obsidian做深度研究，选取自己收集的信息作为信息源，那Karpathy的方式更适合你。如果你想要用Obsidian+LLM来写作、工作或帮助自己思考，那我的方案更适合你。

Haoshan-Vault中的第二个重要原则就是：**输入服务于输出。** 输入的内容要有一个出口可以出去，这样才不是漫无目的地停在电脑里。

## 三、这不是模型的上限

我作为一个没多少收入的学生，每个月花100刀充Claude Max，就是为了避免：出错之后，我不知道是AI的问题还是我的问题。现在的Claude Opus 4.6在精心调校下，是可以做到几乎不出错的。如果出了错，也是可以解决的，因为大部分时间是因为上下文太长了或者提示词不够细致。

在用Openclaw的过程中经常会出现我刚才描述的现象，当龙虾运行结果不如人意的时候，你需要排查问题究竟出在是龙虾的源码、造模型的厂家、卖API的中转商，还是用龙虾的你。这时候的你会很无助。

用Claude Code犯的错一般相当可控，我遇到的问题99%都是幻觉和没有遵从指令。这两种情况都是由对话窗口过长，上下文过载导致的。这种时候应该做的就是把当前的员工（一般是COO）开除，让他写一个离职报告（handoff.md，每个agent一个，和journal一样是一个文档滚动维护），解释自己为什么被开除，继任应该如何避免出现同样的问题。这样在新开一个session后，新的COO就可以保证不重蹈覆辙。

因为出错一般**不是模型能力达到上限**，而只是上下文过载。

开除/新开session的重要性也可见这篇文章：[https://x.com/0x\_kaize/status/2038286026284667239](https://x.com/0x_kaize/status/2038286026284667239)

## 四、把自己数字化

我在各种场合不止一次地推荐维护两个自身情况的文档，其中一个是传记形式的过往经历，另一个是自己当下的状态，包括财务、健康等等。

这两个文档既可以让AI给你更个性化的解答，也可以随时复制到其他大模型，从而不受任何产品记忆的限制。这两个文档也是在最开始使用Obsidian，什么笔记都还没有的时候，应该优先创建的。

具体创建的方法也很简单，开一个AI的对话窗口，让它不断地采访你，直到把你的经历全都问透。而你只需要找一个语音转文字的软件，一直说就可以了。

把这一点做到极致的是[@FarzaTV](https://x.com/@FarzaTV)，他把2500条日记、Apple Notes和iMessage对话让AI编译成了400篇个人百科，朋友、创业经历、研究方向、甚至喜欢的动漫都有专门的文章。他管这个叫Farzapedia。他做这个不是给自己看的，是给他的AI agent看的，让agent在帮他工作的时候能随时调用他的个人上下文。这个思路很聪明。

![图像](https://pbs.twimg.com/media/HFMgvAfaMAAzn0i?format=jpg&name=large)

## 五、日记的花活

每天的工作需要记录，既有利于人回顾，也有利于AI把控工作进度。

这可能并不是一个必要的工作，可能有人觉得一件事做了就做了。但由于AI在对话框里对时间，尤其是过去对话的时间没有概念，涉及到工作的时间节奏时幻觉会比较严重，维护一个日报是一个性价比很高的解决方案。

日报是为效率而生，不是少女花花绿绿的手办，没有必要记录每天的心情和天气，放上今天拍的美美的照片——没有必要。出于简洁的考虑，日报只需在仓库根目录放一个文件维护即可，每天的信息更新在最上方。

人工更新，或者让AI每个session更新，都是心有余而力不足，Claude桌面端的定时任务很好地解决了这个问题。让Claude每天读一下仓库，看一看最新的笔记，然后记录下来，这当然是一种方式。更酷的方式是让Claude每天结束之后定时把当天的更新git到GitHub上，再对比前一天，把变更作为今天的日记。

备份、总结，一举两得。

## 六、让旧笔记活动起来

“晨间发散”是我健脑房里最重要的器械之一。

起初是为了在睡觉时间消耗Claude token，我在每天的早上5点给Claude设了一个定时任务。由于我的笔记宁缺毋滥，所以都是我感兴趣的内容，于是我让Claude根据我的笔记进行发散，并进行深度研究，给我提供对我重要，但我可能忽略的重要信息。

这就给了我源源不断的知识。首先，这些内容从我的笔记发散，所以我很熟悉并感兴趣。其次，发散出的内容我没有写过笔记，也就是我没有思考过，这就是很好的健脑材料。

![图像](https://pbs.twimg.com/media/HFMdYVSb0AArTG8?format=jpg&name=large)

当然，如我前文所说，未经人脑处理的信息不进入仓库，晨间发散的笔记会存在我的收件箱里，等我思考过后才进入仓库。

## 七、实现

前面讲了原则，这里讲怎么落地。整个系统就是Obsidian加Claude Code，不需要别的工具。

Obsidian原来的很多功能在AI时代过时了，尤其是Metadata，原先需要填每个笔记的来源、日期、作者，不胜其烦，现在完全没必要了。tag也几乎失去了必要，AI根据文件夹整理笔记太简单了。但Obsidian本身作为本地markdown编辑器的价值反而更大了，因为vault就是一个文件夹，没有数据库，没有私有格式，AI最容易操作。

**文件夹结构**

CLAUDE.md — 系统规则 + COO角色设定 handoff.md — 离职报告（见第三章） journal.md — 每日日记（见第五章） todo.md — 待办事项 YYYY-MM-DD.md — 今日看板（见第五章） Inbox/ — 收件箱（见第一章） \_Important/ \_Mid/ \_Remove/ Notes/ — 你自己的思考（见第一章） Life/ Context/ — 你的数字分身（见第四章） Salon/ — 文艺伙伴 Therapist/ — 心理咨询师 Projects/ — 每个项目有自己的CLAUDE.md \_Archive/ — 死掉的项目 \_Temp/ — 临时任务

**角色系统**

AI角色由你打开的文件夹决定。每个文件夹里有一个CLAUDE.md，定义角色是谁、该怎么做、该读什么文件。子文件夹继承父文件夹的规则，层层叠加。

角色可以无限创建。在网上遇到喜欢的skills就新建一个Project，把prompt存进去，cd过来之后自动使用，与此同时你的个人信息都保留。比如可以创建一个健身/营养教练的project。

角色之间通过共享的journal.md和todo.md协作。第一次打开一个角色，它会问你几个问题来了解你，存下来之后以后每次都记得。

**CLAUDE.md**

每个角色的核心就是一个CLAUDE.md文件。我的COO的CLAUDE.md定义了：角色身份、每次session开始必须读哪些文件、该做什么不该做什么、以及一个Critical Facts表记录犯过的错。完整内容开源在GitHub上。

**定时任务**

三个定时任务在Claude Code的scheduled tasks里设置，具体的prompt在GitHub仓库的cron-prompts/文件夹里。

- **早上5点 — 晨间发散**（见第六章）
- **早上9点 — 今日看板**：生成当天的计划文件，整理收件箱
- **凌晨3点 — 自动日记**（见第五章）：基于git diff总结当天工作

**待改进的地方**

这个系统强在有问责机制，保护人的思考，作为生产非常稳定可靠。

但在研究和学习的效率方面确实有一定弊端。之后会持续完善。

## 八、怎么用

需要两样东西：Obsidian（obsidian.md，免费）和Claude Code（需要Node.js 18+，装好之后终端输入npm install -g [@anthropic](https://x.com/@anthropic)\-ai/claude-code）。

然后把我的模板仓库克隆下来：

git clone [https://github.com/hroyhong/Haoshan-Vault.git](https://github.com/hroyhong/Haoshan-Vault.git)git 克隆 [https://github.com/hroyhong/Haoshan-Vault.git](https://github.com/hroyhong/Haoshan-Vault.git)

用Obsidian把这个文件夹作为vault打开，然后在终端cd到这个文件夹，输入claude启动。

第一次启动，COO会像面试一样问你几个问题：你是谁、现在在做什么、最重要的事情是什么。你的回答会被存到Life/Context/profile.md和todo.md里，之后每次打开都记得。

定时任务的prompt在仓库的cron-prompts/文件夹里，复制到Claude Code的scheduled tasks就可以用。具体设置方法见GitHub的README。

用得越多，系统越了解你，输出越准确。

**GitHub:** [github.com/hroyhong/Haoshan-Vault](https://github.com/hroyhong/Haoshan-Vault)**GitHub：** [github.com/hroyhong/Haoshan-Vault](https://github.com/hroyhong/Haoshan-Vault)

## Highlights

