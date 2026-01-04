from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException

from ..pipeline import run_pipeline

app = FastAPI(title="Sleep Report Service")


@app.post("/reports/sleep")
def generate_sleep_report(source_dir: str, output_path: str | None = None) -> dict:
    source = Path(source_dir)
    if not source.exists():
        raise HTTPException(status_code=404, detail=f"目录不存在: {source}")
    output = Path(output_path) if output_path else source / "sleep_report.md"
    content = run_pipeline(source, output)
    return {
        "output_file": str(output),
        "entry_count": len(list(source.glob("*.md"))),
        "preview": content[:500],
    }
