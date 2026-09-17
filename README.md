# 日志分析工具 · log-kb-lite

> Web 端直接打开即用，无需后端。流程：**语料导入 → 关键字与分类 → 日志分析 → 结果验收与导出**。数据仅存浏览器本地，刷新不上传。

在线演示：直接打开 `web/index.html` 即可使用（见下方快速开始）。

## 下载

- **Web 版（免安装）**：直接打开 `web/index.html` 或访问 GitHub Pages（如已开启）
- **桌面版 exe**：到 [Releases](https://github.com/scottchen123/log-kb-lite/releases) 下载最新 `log-kb-lite Setup *.exe`，双击安装即可离线使用

> 首次发布 exe：执行 `git tag v0.1.0 && git push origin v0.1.0` 会触发 Actions 自动打包并上传到 Releases

---



---

## 使用指引

### ① 语料导入
- 支持 `.md` / `.txt` / `.csv` 批量导入，每行一条语料；也支持单条手动追加。
- 点击 **加载示例语料 12 条** 可一键载入 `server/kb/sample_corpus.md` 的示例（含 VDI / Kafka / ES / PG 等）。
- 右侧实时显示当前语料条数与列表，支持清空与导出。

### ② 关键字与分类
- 每个分类配置一组关键字（逗号分隔），支持新增 / 编辑 / 删除 / ↑↓ 调整顺序。
- 匹配模式三选一：`包含匹配`（默认）/ `词边界 \b` / `正则 RegExp`。
- 顺序即优先级，首条命中即归类；未命中归入**未分类**。

### ③ 日志分析
- 支持文件导入或粘贴输入（每行一条日志），批量分析生成结果。
- 可选 **关联语料**：命中关键字时在结果中展示相关语料，便于核对。

### ④ 结果与验收
- 顶部 4 项统计：总量 / 已分类 / 未分类 / 分类数，以及分类占比明细。
- 明细表：日志原文 | 命中关键字 | 分类（可改） | 关联语料 | 验收勾选。
- 支持一键全部验收、导出 `analysis_result.csv`。

---

## 快速开始

### 仅 Web（零依赖，推荐）
```bash
open web/index.html
# 或双击文件
# 步骤：加载示例语料 → 配置关键字 → 导入日志 → 分析 → 验收并导出
```

### 启用 Python 后端（团队共享，可选）
```bash
cd server
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# 浏览器打开 http://localhost:8000/web/
```

### 打包为桌面应用（可选）
```bash
cd electron
npm install
npm run pack   # 输出到 dist/
```

---

## 目录结构

```
log-kb-lite/
├── web/index.html          # Web 前端（纯前端，localStorage）
├── server/
│   ├── main.py             # FastAPI（可选）
│   ├── requirements.txt
│   └── kb/sample_corpus.md # 示例语料 12 条
├── electron/
│   ├── main.js             # Electron 壳，加载 web/index.html
│   └── package.json
├── Dockerfile
└── docker-compose.yml
```

## 技术说明

- **Web**：原生 HTML/CSS/JS，无构建步骤，`localStorage` 本地持久化
- **Server**（可选）：FastAPI + SQLite，提供 `/api/kb`、`/api/rules`、`/api/analyze` 接口
- **语料示例**：`server/kb/sample_corpus.md`

## 许可

MIT
