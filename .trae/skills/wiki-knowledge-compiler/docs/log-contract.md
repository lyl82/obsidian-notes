# Log 契约

## 目的

用 `index + log` 实现导航与溯源：
- index：入口与导航
- log：每次 ingest / lint 的执行记录，便于回溯“什么时候、为什么、改了什么”

## log 文件位置

- 建议：`0_Inbox/Wikis/log.md`

## 表格字段

| 字段 | 含义 |
| --- | --- |
| time | 执行时间（ISO） |
| op | 操作类型：ingest / lint / query |
| raw_count | 本次进入处理队列的 raw 数量 |
| write_count | 本次实际写入（create/update）的文件数量 |
| validate | 校验结果：pass / fail |
| notes | 简短说明或异常信息 |

## 写入原则

- 每次 ingest 完成后必须追加一行
- 若校验失败，也必须写入一行，且 validate=fail
- log 追加必须是 append，不重写历史
