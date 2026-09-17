from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import re, pathlib, sqlite3, csv, io

app = FastAPI(title="log-kb-lite")

# Minimal in-memory fallback; SQLite file if exists
DB = pathlib.Path(__file__).parent / "kb.db"
KB_TXT = pathlib.Path(__file__).parent / "kb" / "sample_corpus.md"

class AnalyzeReq(BaseModel):
    logs: List[str]
    mode: str = "contains"  # contains|word|regex
    rules: Optional[List[dict]] = None  # [{cat, kws:[]}]
    use_kb: bool = False

DEFAULT_RULES = [
    {"cat":"故障类","kws":["503","超时","error","失败","red","卡顿"]},
    {"cat":"技术支持类","kws":["kafka","lag","partition","consumer"]},
    {"cat":"咨询类","kws":["咨询","如何","怎么","计费"]},
    {"cat":"Bug阻塞","kws":["bug","阻塞","deadlock"]},
]

def load_corpus():
    if KB_TXT.exists():
        return [l.strip() for l in KB_TXT.read_text(encoding="utf-8").splitlines() if l.strip()]
    return []

def match_one(line: str, kw: str, mode: str) -> bool:
    if not kw: return False
    if mode=="contains": return kw.lower() in line.lower()
    if mode=="word":
        esc=re.escape(kw)
        try: return re.search(rf"\b{esc}\b", line, flags=re.I) is not None
        except: return kw.lower() in line.lower()
    if mode=="regex":
        try: return re.search(kw, line, flags=re.I) is not None
        except: return kw.lower() in line.lower()
    return False

@app.get("/api/health")
def health(): return {"ok": True}

@app.get("/api/kb")
def get_kb(): return {"corpus": load_corpus()}

@app.get("/api/rules")
def get_rules(): return {"rules": DEFAULT_RULES}

@app.post("/api/analyze")
def analyze(req: AnalyzeReq):
    rules = req.rules or DEFAULT_RULES
    corpus = load_corpus()
    out=[]
    for idx, line in enumerate(req.logs,1):
        cat="未分类"; hit="-"; kb_hit="-"
        for r in rules:
            kw = next((k for k in r.get("kws",[]) if match_one(line, k, req.mode)), None)
            if kw: cat=r["cat"]; hit=kw; break
        if req.use_kb and hit!="-":
            f = next((s for s in corpus if hit.lower() in s.lower()), None)
            if f: kb_hit=f
        out.append({"idx":idx,"line":line,"cat":cat,"hit":hit,"kbHit":kb_hit,"accepted":False})
    return {"result": out}

# serve web statically at /web
web_dir = pathlib.Path(__file__).parent.parent / "web"
if web_dir.exists():
    app.mount("/web", StaticFiles(directory=str(web_dir), html=True), name="web")
