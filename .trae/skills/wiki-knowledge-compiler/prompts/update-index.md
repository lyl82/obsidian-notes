# Prompt: Update Index

你现在负责增量更新 `wiki/index.md`。

## 目标

- 把本次新增的 summary 页面加入 index
- 必要时把本次新增或被激活的 concept 页面加入 index

## 输入

- 现有 `index.md`
- 本次新增的 summary 列表
- 本次新增或更新的 concept 列表
- `templates/index.template.md`

## 硬规则

1. 只做与本次任务相关的增量更新
2. 不重排整个 index，除非用户明确要求
3. 不删除旧入口，除非明确确认失效
4. 链接格式统一使用 `[[ @链接]]`

## 更新原则

- summary 按固定分区追加
- concept 按固定分区追加
- 避免重复条目
- 尽量保持 index 结构稳定
- 输出结构必须遵守 `index.template.md`

## 输出格式

- 输出完整的 `index.md` 文件内容
- 若需要脚本落盘，则额外输出一个 manifest（遵守 `docs/manifest-contract.md`）
