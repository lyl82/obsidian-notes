log表：

sop：系统的时间结构

在原始 log 上，额外加一列就够了：  
`status`：

只有三种值，别发明第四种：

- raw：只是发生了（默认）
    
- candidate：可能值得处理
    
- dead：确认无用
第一件该建的不是复杂结构，而是一个**固定时间的 Review 任务**。

审计阶段（分类原始记录和标签处理，：把 raw → candidate 或 dead。在最初阶段，只允许一条升级路径：

candidate → action（一个明确可执行动作）

不是想法，不是洞察，不是总结。  
是“我接下来要做什么”。（有个现实问题，实际记录candidate → action

