### queue 表（核心，人生开始被推着走）

字段：

- `created_at`
    
- `source_log_id`（来自哪条 log    似乎可以用飞书自动生成行动）
    
- `action`（必须是 30 分钟内能完成的具体行为）新增一条子记录，
    
- `cost_energy`（0 / 1 / 2）
    
- `status`（todo / done / drop）
    

**关键规则：**

- queue 里的 action 必须能“现在就做”
    
- 做不了的，不准进 queue