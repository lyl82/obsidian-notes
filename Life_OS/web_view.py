"""Minimal HTTP view to inspect 人生OS 1.0 data."""
from __future__ import annotations

import html as html_lib
import hashlib
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import List, Tuple
from urllib.parse import parse_qs, unquote
import json
import os

from database import connect, init_db
from importer import seed_example

FLOWCHART_PATH = Path(__file__).resolve().parent.parent / "人生OS" / "0_Inbox" / "system_flowchart.md"

def get_flowchart_content() -> str:
    if not FLOWCHART_PATH.exists():
        return "graph TD\n    A[数据流进来 log] --> B[审计阶段]"
    
    content = FLOWCHART_PATH.read_text(encoding="utf-8")
    # Extract content between ```mermaid and ```
    import re
    match = re.search(r"```mermaid\s+(.*?)\s+```", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "graph TD\n    A[数据流进来 log] --> B[审计阶段]"

def save_flowchart(content: str):
    """保存流程图内容到 markdown 文件"""
    # 保持 mermaid 块的结构
    full_content = f"```mermaid\n{content.strip()}\n```"
    FLOWCHART_PATH.parent.mkdir(parents=True, exist_ok=True)
    FLOWCHART_PATH.write_text(full_content, encoding="utf-8")

def _hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def add_log(content: str):
    if not content.strip():
        return
    content_hash = _hash_content(content)
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO logs (content, content_hash) VALUES (?, ?)",
            (content, content_hash),
        )
        conn.commit()


def add_rule(name: str, expression: str):
    if not name.strip() or not expression.strip():
        return
    with connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO rules (name, expression) VALUES (?, ?)",
            (name, expression),
        )
        conn.commit()


def fetch_tables() -> Tuple[List[tuple], List[tuple], List[tuple]]:
    with connect() as conn:
        logs = conn.execute(
            "SELECT id, recorded_at, content, content_hash FROM logs ORDER BY recorded_at DESC"
        ).fetchall()
        rules = conn.execute(
            "SELECT name, expression FROM rules ORDER BY name"
        ).fetchall()
        queue = conn.execute(
            "SELECT id, log_id, rule_name, status, created_at FROM queue ORDER BY id DESC"
        ).fetchall()
    return logs, rules, queue


class LifeOSHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"POST request received: {self.path}")
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(post_data)

        if self.path == "/add_log":
            content = params.get("content", [""])[0]
            add_log(content)
        elif self.path == "/add_rule":
            name = params.get("name", [""])[0]
            expression = params.get("expression", [""])[0]
            add_rule(name, expression)
        elif self.path == "/save_flowchart":
            content = params.get("content", [""])[0]
            save_flowchart(content)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Success")
            return
        else:
            self.send_error(404)
            return
            
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        # Handle paths with query parameters
        clean_path = self.path.split('?')[0]
        print(f"GET request received: {self.path} (clean: {clean_path})")
        
        if clean_path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if clean_path not in ("/", "/index.html"):
            # Ignore common noise
            if clean_path.endswith(('.ico', '.map', '.js', '.css')) or 'vite' in clean_path:
                self.send_response(404)
                self.end_headers()
                return
            self.send_error(404, f"Path {clean_path} not found")
            return

        try:
            logs, rules, queue = fetch_tables()
            mermaid_code = get_flowchart_content()
            # 转义 HTML 特殊字符，防止破坏 textarea/pre 标签
            escaped_mermaid = html_lib.escape(mermaid_code)
            html = self._render_html(logs, rules, queue, escaped_mermaid)
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            try:
                self.wfile.write(body)
            except (ConnectionAbortedError, ConnectionResetError) as e:
                print(f"Connection closed by client: {e}")
        except Exception as e:
            print(f"Error rendering page: {e}")
            try:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Internal Server Error: {e}".encode("utf-8"))
            except:
                pass

    def log_message(self, format: str, *args):
        # Default logging to stderr
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    @staticmethod
    def _render_html(logs: List[tuple], rules: List[tuple], queue: List[tuple], mermaid_code: str) -> str:
        def table_rows(rows: List[tuple]) -> str:
            return "".join(
                f"<tr>{''.join(f'<td>{cell}</td>' for cell in row)}</tr>" for row in rows
            )

        # Using a simple string replace to avoid f-string escape issues with JS/CSS
        template = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>人生OS 1.0 - 工作台</title>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      securityLevel: 'loose'
    });
  </script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 24px; background: #f7f9fb; color: #1f2933; }
    h1 { margin-bottom: 4px; }
    section { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px 18px; margin-bottom: 18px; box-shadow: 0 10px 30px -22px rgba(0,0,0,0.35); }
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th, td { padding: 8px 10px; border-bottom: 1px solid #edf1f5; text-align: left; }
    th { font-weight: 700; color: #4b5563; background: #f9fafb; }
    tr:hover td { background: #f3f6fb; }
    .pill { display: inline-block; padding: 2px 8px; border-radius: 10px; background: #e0f2fe; color: #075985; font-weight: 600; font-size: 12px; }
    footer { color: #6b7280; font-size: 13px; margin-top: 10px; }
    .mermaid { display: flex; justify-content: center; background: #fff; padding: 20px; border-radius: 8px; min-height: 150px; white-space: pre; transition: opacity 0.3s ease; }
    .mermaid.updating { opacity: 0.4; }
    .editor-container { display: flex; flex-direction: column; gap: 12px; }
    .editor-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .editor-box { display: flex; gap: 16px; height: 500px; }
    .editor-box textarea { flex: 1; font-family: 'Consolas', 'Monaco', monospace; font-size: 14px; background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; border: none; outline: none; transition: box-shadow 0.3s; }
    .editor-box textarea:focus { box-shadow: 0 0 0 2px #3b82f6; }
    .preview-box { flex: 1; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: auto; display: flex; justify-content: center; align-items: flex-start; padding: 20px; position: relative; }
    .interactive-panel { background: #f0f4f8; border-radius: 8px; padding: 16px; margin-top: 12px; border: 1px dashed #cbd5e1; transition: all 0.3s ease; }
    .interactive-panel:hover { border-color: #3b82f6; background: #ebf2ff; }
    .node-controls { display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap; }
    .control-item { display: flex; flex-direction: column; gap: 4px; }
    .control-item label { font-size: 12px; color: #64748b; font-weight: 600; }
    .node-controls select, .node-controls input { padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 14px; transition: border-color 0.2s; }
    .node-controls select:focus, .node-controls input:focus { border-color: #3b82f6; outline: none; }
    .btn-save { background: #059669; }
    .btn-save:hover { background: #047857; }
    .btn-add { background: #3b82f6; }
    .btn-add:hover { background: #2563eb; transform: translateY(-1px); }
    .btn-add:active { transform: translateY(0); }
    .status-msg { font-size: 12px; margin-right: 12px; color: #059669; font-weight: bold; opacity: 0; transition: opacity 0.3s; }
    .status-msg.show { opacity: 1; }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); } 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); } }
    .animated { animation: fadeIn 0.4s ease-out; }
    .pulse-effect { animation: pulse 0.6s ease-out; }
  </style>
</head>
<body>
  <h1>人生OS 1.0 工作台</h1>
  <p>实时录入数据并触发系统流程。</p>

  <section>
    <h2>1. 录入数据 (Input Log)</h2>
    <form action="/add_log" method="post" class="input-group">
      <textarea name="content" placeholder="输入新的 log 内容... (例如：晚上运动了 30 分钟)"></textarea>
      <button type="submit">录入系统</button>
    </form>
  </section>

  <section>
    <h2>2. 编写逻辑 (Edit Rules)</h2>
    <form action="/add_rule" method="post" class="input-group-vertical">
      <div class="row">
        <input type="text" name="name" placeholder="规则名称 (例如：健康提醒)" required>
        <input type="text" name="expression" placeholder="Python 表达式 (例如：'跑步' in content)" required>
      </div>
      <button type="submit">保存规则</button>
    </form>
  </section>

  <section class="animated">
    <h2>4. 系统逻辑流程图 (System Logic Flowchart)</h2>
    <p>在此编写系统逻辑，支持可视化实时预览与节点交互。</p>
    <div class="editor-container">
      <div class="editor-header">
        <span>Mermaid 源码编辑器</span>
        <div>
          <span id="status-msg" class="status-msg">已保存到本地</span>
          <button type="button" class="btn-save" onclick="saveToDisk()">保存流程图</button>
        </div>
      </div>
      <div class="editor-box">
        <textarea id="mermaid-input" spellcheck="false">[[MERMAID_CODE]]</textarea>
        <div class="preview-box">
          <pre id="mermaid-preview" class="mermaid">[[MERMAID_CODE]]</pre>
        </div>
      </div>
      
      <div class="interactive-panel">
        <strong>快速新增节点 (Quick Add)</strong>
        <div class="node-controls">
          <div class="control-item">
            <label>父节点 (From)</label>
            <select id="parent-node"></select>
          </div>
          <div class="control-item">
            <label>连接描述 (Link Text)</label>
            <input type="text" id="link-text" placeholder="例如: 匹配标签">
          </div>
          <div class="control-item">
            <label>新子节点内容 (To Node Content)</label>
            <input type="text" id="child-node-content" placeholder="输入新节点名称...">
          </div>
          <button type="button" class="btn-add" onclick="addNewNode()">确认添加</button>
        </div>
      </div>
    </div>
  </section>

  <script>
    const input = document.getElementById('mermaid-input');
    const preview = document.getElementById('mermaid-preview');
    const parentSelect = document.getElementById('parent-node');
    const statusMsg = document.getElementById('status-msg');

    // 解析当前代码中的所有节点
    function updateNodeList() {
      const code = input.value;
      const nodes = new Set();
      // 匹配节点定义 A[Content] 或 A(Content) 或 A
      const nodeRegex = /([A-Z0-9_]+)(\[[^\]]+\]|\([^)]+\))?/gi;
      let match;
      while ((match = nodeRegex.exec(code)) !== null) {
        if (match[1] !== 'graph' && match[1] !== 'TD' && match[1] !== 'subgraph' && match[1] !== 'end') {
          nodes.add(match[1]);
        }
      }
      
      const currentVal = parentSelect.value;
      parentSelect.innerHTML = '';
      Array.from(nodes).sort().forEach(node => {
        const opt = document.createElement('option');
        opt.value = node;
        opt.textContent = node;
        parentSelect.appendChild(opt);
      });
      if (nodes.has(currentVal)) parentSelect.value = currentVal;
    }

    let debounceTimer;
    function updatePreview() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(async () => {
        const code = input.value;
        preview.classList.add('updating');
        preview.removeAttribute('data-processed');
        preview.textContent = code;
        try {
          await mermaid.run({ nodes: [preview] });
          updateNodeList();
        } catch (e) {
          console.error("Mermaid error:", e);
        } finally {
          preview.classList.remove('updating');
        }
      }, 150);
    }

    function addNewNode() {
      const from = parentSelect.value;
      const link = document.getElementById('link-text').value;
      const toContent = document.getElementById('child-node-content').value;
      
      if (!toContent) return alert('请输入子节点内容');
      
      // 添加脉冲动画效果
      const panel = document.querySelector('.interactive-panel');
      panel.classList.add('pulse-effect');
      setTimeout(() => panel.classList.remove('pulse-effect'), 600);
      
      // 生成一个简单的 ID
      const toId = "Node_" + Math.random().toString(36).substring(2, 7).toUpperCase();
      
      let newEntry = "";
      if (link) {
        newEntry = "    " + from + " -->|" + link + "| " + toId + "[" + toContent + "]";
      } else {
        newEntry = "    " + from + " --> " + toId + "[" + toContent + "]";
      }
      
      // 在最后一个 end 之前插入，或者直接在末尾添加
      const lines = input.value.split('\\n');
      let insertIdx = lines.length;
      // 尝试找最后一个 subgraph 的位置插入
      for (let i = lines.length - 1; i >= 0; i--) {
        if (lines[i].trim() === 'end') {
          insertIdx = i;
          break;
        }
      }
      
      lines.splice(insertIdx, 0, newEntry);
      input.value = lines.join('\\n');
      
      // 清空输入
      document.getElementById('link-text').value = '';
      document.getElementById('child-node-content').value = '';
      
      updatePreview();
    }

    async function saveToDisk() {
      const btn = document.querySelector('.btn-save');
      const originalText = btn.textContent;
      btn.textContent = '保存中...';
      btn.disabled = true;
      
      const code = input.value;
      const formData = new URLSearchParams();
      formData.append('content', code);
      
      try {
        const resp = await fetch('/save_flowchart', {
          method: 'POST',
          body: formData
        });
        if (resp.ok) {
          statusMsg.classList.add('show');
          setTimeout(() => { statusMsg.classList.remove('show'); }, 2000);
        }
      } catch (e) {
        alert('保存失败: ' + e);
      } finally {
        btn.textContent = originalText;
        btn.disabled = false;
      }
    }

    input.addEventListener('input', updatePreview);
    window.addEventListener('load', () => {
      updatePreview();
    });
  </script>

  <section class="animated">
    <h2>5. 运行逻辑概览</h2>
    <p>系统核心组件及其交互关系。</p>
  </section>

  <section>
    <h2>Logs</h2>
    <table>
      <thead><tr><th>ID</th><th>时间</th><th>内容</th><th>Hash</th></tr></thead>
      <tbody>[[LOGS_TABLE]]</tbody>
    </table>
  </section>

  <section>
    <h2>Rules</h2>
    <table>
      <thead><tr><th>名称</th><th>表达式</th></tr></thead>
      <tbody>[[RULES_TABLE]]</tbody>
    </table>
  </section>

  <section>
    <h2>Queue</h2>
    <table>
      <thead><tr><th>ID</th><th>Log ID</th><th>规则</th><th>状态</th><th>创建时间</th></tr></thead>
      <tbody>[[QUEUE_TABLE]]</tbody>
    </table>
  </section>

  <footer>运行方式：python web_view.py （默认端口 8000）</footer>
</body>
</html>
"""
        html = template.replace("[[LOGS_TABLE]]", table_rows(logs)) \
                       .replace("[[RULES_TABLE]]", table_rows(rules)) \
                       .replace("[[QUEUE_TABLE]]", table_rows(queue))
        # 全局替换 MERMAID_CODE (textarea 和 pre 区域)
        return html.replace("[[MERMAID_CODE]]", mermaid_code)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    init_db()
    seed_example()
    server = HTTPServer((host, port), LifeOSHandler)
    print(f"Serving 人生OS 1.0 MVP at http://localhost:{port}")
    print(f"Also available at http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
