import json
import os
from pathlib import Path
from typing import Dict, List, Optional


def find_chromium_bookmark_files() -> Dict[str, List[Path]]:
    results: Dict[str, List[Path]] = {}
    local_app_data = os.getenv("LOCALAPPDATA")
    if not local_app_data:
        return results
    candidates = {
        "Chrome": Path(local_app_data) / "Google" / "Chrome" / "User Data",
        "Edge": Path(local_app_data) / "Microsoft" / "Edge" / "User Data",
        "Brave": Path(local_app_data) / "BraveSoftware" / "Brave-Browser" / "User Data",
    }
    for browser, base in candidates.items():
        if not base.exists():
            continue
        paths: List[Path] = []
        for profile_dir in base.glob("*"):
            if not profile_dir.is_dir():
                continue
            bookmark_file = profile_dir / "Bookmarks"
            if bookmark_file.exists():
                paths.append(bookmark_file)
        if paths:
            results[browser] = paths
    return results


def load_bookmark_tree(path: Path) -> Optional[dict]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def collect_bookmarks(data: dict, browser: str, profile_name: str) -> List[dict]:
    items: List[dict] = []
    roots = data.get("roots") or {}

    def walk(node: dict, folders: List[str]) -> None:
        node_type = node.get("type")
        if node_type == "folder":
            name = node.get("name") or ""
            next_folders = folders + [name] if name else folders
            for child in node.get("children") or []:
                walk(child, next_folders)
            return
        if node_type == "url":
            title = node.get("name") or ""
            url = node.get("url") or ""
            if not url:
                return
            items.append(
                {
                    "title": title,
                    "url": url,
                    "browser": browser,
                    "profile": profile_name,
                    "folderPath": "/".join(folders),
                }
            )

    for root in roots.values():
        if isinstance(root, dict):
            walk(root, [])
    return items


def export_bookmarks() -> Path:
    base_dir = Path(__file__).resolve().parent
    output_path = base_dir / "bookmarks_view.html"
    bookmark_files = find_chromium_bookmark_files()
    all_items: List[dict] = []
    for browser, paths in bookmark_files.items():
        for p in paths:
            data = load_bookmark_tree(p)
            if not data:
                continue
            profile_name = p.parent.name
            all_items.extend(collect_bookmarks(data, browser, profile_name))
    all_items.sort(key=lambda x: (x.get("browser") or "", x.get("folderPath") or "", x.get("title") or ""))
    html = build_html(all_items)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def build_html(items: List[dict]) -> str:
    data_json = json.dumps(items, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>浏览器书签视图</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    margin: 0;
    padding: 16px;
    background: #f5f5f7;
    color: #222;
}}
h1 {{
    margin: 0 0 12px 0;
    font-size: 20px;
}}
.toolbar {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}}
input, select {{
    padding: 6px 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 14px;
}}
#search {{
    flex: 1 1 200px;
}}
.stats {{
    font-size: 12px;
    color: #666;
    margin-bottom: 8px;
}}
.table {{
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    overflow: hidden;
}}
.table-header, .row {{
    display: grid;
    grid-template-columns: 2fr 3fr 1.2fr 1.2fr;
    gap: 8px;
    padding: 8px 12px;
    align-items: center;
}
.table-header {{
    background: #f0f0f3;
    font-size: 12px;
    font-weight: 600;
    color: #555;
}}
.row:nth-child(odd) {{
    background: #fff;
}}
.row:nth-child(even) {{
    background: #fafafa;
}}
.row a {{
    color: #0066cc;
    text-decoration: none;
    word-break: break-all;
}}
.row a:hover {{
    text-decoration: underline;
}}
.folder-pill {{
    display: inline-flex;
    align-items: center;
    max-width: 100%;
    padding: 2px 6px;
    border-radius: 999px;
    background: #eef1ff;
    color: #334;
    font-size: 11px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.badge {{
    display: inline-flex;
    align-items: center;
    padding: 2px 6px;
    border-radius: 999px;
    font-size: 11px;
    background: #eee;
    color: #333;
}}
.empty {{
    padding: 12px;
    font-size: 13px;
    color: #777;
}}
@media (max-width: 720px) {{
    .table-header {{
        display: none;
    }}
    .row {{
        grid-template-columns: 1fr;
        gap: 4px;
        font-size: 14px;
    }}
}}
</style>
</head>
<body>
<h1>浏览器书签视图</h1>
<div class="toolbar">
    <input id="search" placeholder="搜索标题或网址">
    <select id="browserFilter">
        <option value="">全部浏览器</option>
    </select>
    <select id="folderFilter">
        <option value="">全部文件夹</option>
    </select>
</div>
<div class="stats" id="stats"></div>
<div class="table" id="table">
    <div class="table-header">
        <div>标题</div>
        <div>网址</div>
        <div>浏览器/配置</div>
        <div>文件夹</div>
    </div>
    <div id="rows"></div>
</div>
<script>
const allItems = {data_json};
const searchInput = document.getElementById("search");
const browserFilter = document.getElementById("browserFilter");
const folderFilter = document.getElementById("folderFilter");
const statsEl = document.getElementById("stats");
const rowsEl = document.getElementById("rows");

function unique(list) {{
    return Array.from(new Set(list)).filter(Boolean).sort();
}}

function initFilters() {{
    const browsers = unique(allItems.map(x => x.browser));
    const folders = unique(allItems.map(x => x.folderPath));
    for (const b of browsers) {{
        const opt = document.createElement("option");
        opt.value = b;
        opt.textContent = b;
        browserFilter.appendChild(opt);
    }}
    for (const f of folders) {{
        const opt = document.createElement("option");
        opt.value = f;
        opt.textContent = f;
        folderFilter.appendChild(opt);
    }}
}}

function render() {{
    const q = searchInput.value.trim().toLowerCase();
    const b = browserFilter.value;
    const f = folderFilter.value;
    const filtered = allItems.filter(x => {{
        if (b && x.browser !== b) return false;
        if (f && x.folderPath !== f) return false;
        if (!q) return true;
        const t = (x.title || "").toLowerCase();
        const u = (x.url || "").toLowerCase();
        return t.includes(q) || u.includes(q);
    }});
    statsEl.textContent = "共 " + allItems.length + " 个书签，当前显示 " + filtered.length + " 个";
    rowsEl.innerHTML = "";
    if (!filtered.length) {{
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "当前筛选条件下没有书签";
        rowsEl.appendChild(empty);
        return;
    }}
    for (const item of filtered) {{
        const row = document.createElement("div");
        row.className = "row";
        const titleCell = document.createElement("div");
        const link = document.createElement("a");
        link.href = item.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = item.title || item.url;
        titleCell.appendChild(link);
        const urlCell = document.createElement("div");
        urlCell.textContent = item.url;
        const browserCell = document.createElement("div");
        const badge = document.createElement("span");
        badge.className = "badge";
        const profile = item.profile ? " · " + item.profile : "";
        badge.textContent = item.browser + profile;
        browserCell.appendChild(badge);
        const folderCell = document.createElement("div");
        const folder = document.createElement("span");
        folder.className = "folder-pill";
        folder.textContent = item.folderPath || "未分类";
        folderCell.appendChild(folder);
        row.appendChild(titleCell);
        row.appendChild(urlCell);
        row.appendChild(browserCell);
        row.appendChild(folderCell);
        rowsEl.appendChild(row);
    }}
}}

initFilters();
render();
searchInput.addEventListener("input", render);
browserFilter.addEventListener("change", render);
folderFilter.addEventListener("change", render);
</script>
</body>
</html>"""


if __name__ == "__main__":
    output = export_bookmarks()
    print(str(output))
