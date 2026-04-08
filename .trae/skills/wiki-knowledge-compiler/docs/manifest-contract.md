# Manifest 契约

## 目的

让 AI 的输出可以被脚本直接消费，避免“复制粘贴多个文件内容”的人肉流程。

## 文件格式

- JSON
- UTF-8

## 顶层结构

推荐顶层对象：

```json
{
  "changes": [
    {
      "path": "ABSOLUTE_PATH_TO_TARGET_FILE",
      "content": "FULL_MARKDOWN_FILE_CONTENT"
    }
  ]
}
```

## 字段说明

- `changes[]`
  - `path`：目标文件绝对路径（Windows 路径）
  - `content`：完整 Markdown 内容（包含 frontmatter）

## 写入原则

- AI 输出必须是“全量文件内容”，脚本不做补丁合并
- 对同一路径只允许出现一次，避免冲突
- 允许输出 `index.md`、`log.md` 等文件，但 log 推荐由脚本统一 append

## 与流程的关系

- AI 负责生成 manifest
- `apply-changes.ps1` 负责写入
- `validate-wiki.ps1` 负责校验
- 通过后再进行 raw 状态回写与 log 追加
