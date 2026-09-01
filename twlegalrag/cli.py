"""Taiwan Legal RAG CLI — retrieve Taiwan court judgments for use with your own AI.

    twlegalrag search "勞資 加班費"                 # list matching judgments
    twlegalrag pack "車禍對方全責能求償什麼?" -o b.json  # bundle for your AI tool
    twlegalrag check b.json answer.txt              # citation check an answer
    twlegalrag law 民法 184                          # exact statute article
    twlegalrag ref "台財稅第881945861號"              # interpretation by serial
    twlegalrag ref-search "扣繳義務人未申報之處罰"      # interpretation topic search
    twlegalrag health

This tool retrieves judgments and packages them for use with your own AI tools.
It does not generate legal advice and does not call any LLM.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# Windows console (cp950/cp1252) cannot encode CJK / box-drawing characters and
# crashes rich table rendering with UnicodeEncodeError (issue #12). Reconfigure
# the standard streams to UTF-8 before any rich Console is constructed.
if sys.platform == "win32":  # pragma: no cover
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .bundle import AI_USE_NOTICE, build_bundle
from .config import get_tlr_api_key, get_tlr_base_url
from .retrieval import RetrievalError, TLRClient
from .verify import VerifyReport, citation_check

app = typer.Typer(
    add_completion=False,
    help="Taiwan Legal RAG — retrieve Taiwan court judgments for use with your own AI tools.",
)
console = Console()
err = Console(stderr=True)

_STATUS_STYLE = {"pass": "green", "needs_review": "yellow", "fail": "bold red"}
_STATUS_LABEL = {"pass": "通過", "needs_review": "待人工", "fail": "不在bundle/錯誤"}

# Ledger validity statuses (legal_reference / ref-search). Anything not
# positively current renders yellow so callers look before citing.
_ACTIVE_STATUSES = {"active", "active_verified"}
_DEAD_STATUSES = {"repealed", "superseded", "ceased", "abolished", "inactive"}


def _status_markup(status: str) -> str:
    s = (status or "unknown").strip() or "unknown"
    if s in _ACTIVE_STATUSES:
        return f"[green]{s}[/]"
    if s in _DEAD_STATUSES:
        return f"[bold red]{s}[/]"
    return f"[yellow]{s}[/]"


def _print_notes(notes) -> None:
    seen = set()
    for n in notes or []:
        if n in seen:  # server emits one note per hit; identical notes add nothing
            continue
        seen.add(n)
        console.print(f"[dim]註: {n}[/]")


def _client() -> TLRClient:
    return TLRClient(base_url=get_tlr_base_url(), api_key=get_tlr_api_key())


@app.command()
def health() -> None:
    """Check the TLR retrieval service is up."""
    try:
        with _client() as c:
            h = c.health()
    except RetrievalError as e:
        err.print(f"[bold red]TLR unreachable:[/] {e}")
        raise typer.Exit(1)
    ok = h.get("status") == "ok"
    console.print(
        Panel(
            f"status: {h.get('status')}\nretrieval: {h.get('retrieval')}",
            title="TLR health",
            border_style="green" if ok else "red",
        )
    )


@app.command()
def search(
    query: str = typer.Argument(..., help="搜尋字詞 (口語/關鍵字皆可)"),
    n: int = typer.Option(5, "--n", "-n", min=1, max=10, help="結果筆數 (1-10)"),
    search_type: str = typer.Option("hybrid", "--type", help="hybrid | keyword | phrase"),
    read: bool = typer.Option(False, "--read", help="同時抓取判決理由全文片段 (excerpt)"),
) -> None:
    """Retrieval only — list matching judgments (no LLM, no cost)."""
    try:
        with _client() as c:
            hits = (
                c.search_and_read(query, search_type=search_type, max_results=n)
                if read
                else c.search(query, search_type=search_type, max_results=n)
            )
    except RetrievalError as e:
        err.print(f"[bold red]檢索失敗:[/] {e}")
        raise typer.Exit(1)
    # Server retrieval note (e.g. exact docket lookup / case number not found —
    # 查無不代表該裁判不存在, 不得臆測). stderr so it never pollutes piped output.
    _note = getattr(c, "last_search_note", None)
    if _note:
        err.print(f"[yellow]ℹ {_note}[/]")
    if not hits:
        console.print("[yellow]無結果[/]")
        return
    table = Table(show_lines=False)
    table.add_column("#", justify="right", style="dim")
    table.add_column("字號", style="cyan")
    table.add_column("摘要")
    if read:
        table.add_column("全文字數", justify="right")
    for j in hits:
        row = [str(j.rank), j.citation_text, j.snippet[:60]]
        if read:
            row.append(str(len(j.fulltext or "")))
        table.add_row(*row)
    console.print(table)


def _print_report(rep: VerifyReport) -> None:
    style = _STATUS_STYLE.get(rep.overall, "white")
    header = (
        f"整體: [{style}]{_STATUS_LABEL.get(rep.overall, rep.overall)}[/]   "
        f"引用 {rep.citations_found} 筆 "
        f"(在 bundle 內 {rep.in_bundle} / 不在 bundle {rep.out_of_bundle})"
    )
    console.print(Panel(header, title="引用檢查 (citation check, bundle-level)", border_style=style))
    if rep.verdicts:
        table = Table(show_lines=False)
        table.add_column("狀態")
        table.add_column("引用字號", style="cyan")
        table.add_column("對應判決", style="dim")
        table.add_column("原因")
        for v in rep.verdicts:
            s = _STATUS_STYLE.get(v.status, "white")
            table.add_row(
                f"[{s}]{_STATUS_LABEL.get(v.status, v.status)}[/]",
                v.citation_text[:36],
                v.doc_id or "—",
                ", ".join(v.reasons),
            )
        console.print(table)
    qp = rep.quote_presence
    if qp.get("status") != "pass":
        s = _STATUS_STYLE.get(qp["status"], "white")
        console.print(
            f"引文存在性檢查 (bundle 層級): [{s}]{_STATUS_LABEL.get(qp['status'])}[/] ({qp['reason']})"
        )
    if rep.out_of_bundle:
        console.print(
            "[bold red]⚠ 偵測到引用了不在 bundle 內的判決字號 — 高度疑似捏造,請勿直接採信。[/]"
        )
    console.print(
        "[dim]註: 此檢查僅驗「引用字號是否在 bundle 內」+「逐字引文是否出現在 bundle 文字某處」。"
        "引文存在性是 bundle 層級,不保證引文出自答案所指那篇判決;也不檢查見解讀對、"
        "當事人主張被當成法院見解。請自行核對判決全文。[/]"
    )


@app.command()
def pack(
    question: str = typer.Argument(..., help="你的法律問題 (白話即可)"),
    n: int = typer.Option(5, "--n", "-n", min=1, max=10, help="檢索判決筆數 (1-10)"),
    out: Optional[Path] = typer.Option(
        None, "--out", "-o", help="輸出 bundle JSON 路徑 (預設印到 stdout)"
    ),
    read_top: Optional[int] = typer.Option(
        None, "--read-top", help="抓全文的前 N 筆 (預設全部)"
    ),
) -> None:
    """Retrieve judgments and package them as a bundle for your own AI tool.

    The bundle (JSON) carries the judgments, stable citation ids (J1, J2, ...),
    full-text excerpts, allowed_citations, and verification instructions you can
    hand to ChatGPT / Claude / Gemini / a local model. No LLM is called here.
    """
    try:
        with _client() as c:
            err.print(f"[dim]檢索判決中... (TLR: {c.base_url})[/]")
            hits = c.search_and_read(question, max_results=n, read_top=read_top)
    except RetrievalError as e:
        err.print(f"[bold red]檢索失敗:[/] {e}")
        raise typer.Exit(1)
    _note = getattr(c, "last_search_note", None)
    if _note:
        err.print(f"[yellow]ℹ {_note}[/]")
    if not hits:
        err.print("[yellow]檢索無結果。[/]")
        raise typer.Exit(1)
    data = build_bundle(question, hits)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if out:
        out.write_text(payload, encoding="utf-8")
        err.print(f"[green]已寫入 {out}[/] ({len(hits)} 篇判決, allowed_citations={data['allowed_citations']})")
    else:
        console.print_json(payload)
    # Always remind, on stderr so it never pollutes piped JSON.
    err.print(f"\n[yellow]{AI_USE_NOTICE}[/]")


@app.command()
def check(
    bundle_path: Path = typer.Argument(..., help="pack 產生的 bundle JSON"),
    answer_path: Path = typer.Argument(..., help="要檢查的答案文字檔 (來自任何 AI)"),
) -> None:
    """Citation-check an answer against a bundle (bundle-level, best-effort).

    Verifies only that the answer's cited case numbers are in the bundle and that
    narrow verbatim quotes appear in the retrieved text. It does NOT verify legal
    reasoning or whether a holding was read correctly — read the judgments yourself.
    """
    try:
        data = json.loads(bundle_path.read_text(encoding="utf-8"))
    except Exception as e:
        err.print(f"[bold red]讀取 bundle 失敗:[/] {e}")
        raise typer.Exit(1)
    # Refuse files that are not a twlegalrag bundle: without this, any JSON
    # "passes" with 0 citations, which looks like a successful check.
    if not isinstance(data, dict) or not str(data.get("schema", "")).startswith("twlegalrag.bundle/"):
        err.print(
            "[bold red]不是 twlegalrag bundle:[/] 檔案缺少 schema 標記 "
            "(應為 pack 指令的輸出)。"
        )
        raise typer.Exit(1)
    try:
        answer = answer_path.read_text(encoding="utf-8")
    except OSError as e:
        err.print(f"[bold red]讀取答案檔失敗:[/] {e}")
        raise typer.Exit(1)
    # Rebuild Judgment objects from the bundle so the checker has doc_id + fulltext.
    from .retrieval import Judgment
    hits = [
        Judgment(
            rank=i + 1,
            doc_id=j.get("doc_id", ""),
            citation_text=j.get("citation_text", ""),
            court_name=j.get("court_name", ""),
            jdate=j.get("jdate", ""),
            snippet=j.get("listing", ""),
            citation_url=j.get("citation_url", ""),
            citation_markdown="",
            result_token="",
            case_category=j.get("case_category"),
            fulltext=j.get("fulltext_excerpt", ""),
            cited_articles=j.get("cited_articles", []),
        )
        for i, j in enumerate(data.get("judgments", []))
    ]
    rep = citation_check(answer, hits)
    _print_report(rep)


@app.command()
def law(
    law_name: str = typer.Argument(..., help="法規名稱 (全名或常用縮寫, 如 民法 / 勞基法)"),
    article_no: str = typer.Argument(..., help="條號 (如 184 / 第184條 / 47-1)"),
) -> None:
    """Exact current-statute article lookup — retrieval only, current version only."""
    try:
        with _client() as c:
            data = c.law_article(law_name, article_no)
    except RetrievalError as e:
        err.print(f"[bold red]查詢失敗:[/] {e}")
        raise typer.Exit(1)
    for m in data.get("matches") or []:
        head = f"{m.get('law_name', '')} {m.get('article_no', '')}"
        lines = [m.get("article_content", "").rstrip()]
        meta = [
            f"層級: {m.get('law_level', '')}",
            f"最後修正: {m.get('law_modified_date', '')}",
            f"全國法規資料庫: {m.get('law_url', '')}",
        ]
        if m.get("abolished"):
            meta.insert(0, "[bold red]此法規已廢止[/]")
        if m.get("article_content_truncated"):
            meta.append("[yellow]條文過長已截斷, 完整內容請開連結[/]")
        lines.append("")
        lines.extend(meta)
        console.print(Panel("\n".join(lines), title=head, border_style="green"))
    if not data.get("found"):
        console.print(f"[yellow]查無: {law_name} {article_no}[/]")
        cands = data.get("law_candidates") or []
        if cands:
            table = Table(title="法規名稱候選 (請換精確名稱重查)")
            table.add_column("法規名稱", style="cyan")
            table.add_column("層級")
            for cand in cands:
                table.add_row(cand.get("law_name", ""), cand.get("law_level", ""))
            console.print(table)
    _print_notes(data.get("notes"))


@app.command()
def ref(
    serial: str = typer.Argument(..., help="函釋發文字號, 如 台財稅第881945861號"),
    authority: Optional[str] = typer.Option(None, "--authority", help="機關名稱提示 (排序用, 非過濾)"),
    full: bool = typer.Option(False, "--full", help="連同函釋全文一併輸出"),
) -> None:
    """Exact interpretation lookup by serial — validity status passthrough, no LLM."""
    try:
        with _client() as c:
            data = c.legal_reference(serial, authority=authority)
    except RetrievalError as e:
        err.print(f"[bold red]查詢失敗:[/] {e}")
        raise typer.Exit(1)
    matches = data.get("matches") or []
    if not data.get("found"):
        console.print(f"[yellow]查無此字號: {serial}[/]")
        console.print("[dim]查無不代表不存在: 請確認字號寫法, 或改用 ref-search 以主題檢索。[/]")
    for m in matches:
        lines = [
            f"標題: {m.get('title', '')}",
            f"發文日期: {m.get('issue_date', '')}",
            f"效力狀態: {_status_markup(m.get('status'))}",
        ]
        if m.get("superseded_by"):
            lines.append(f"[bold red]為後令取代:[/] {m['superseded_by']}")
        if m.get("status_effective_at"):
            lines.append(f"狀態生效日: {m['status_effective_at']}")
        lines.append(f"來源: {m.get('source_url', '')}")
        if m.get("last_verified_at"):
            lines.append(f"[dim]效力最後查核: {m['last_verified_at']}[/]")
        console.print(Panel(
            "\n".join(lines),
            title=f"{m.get('authority', '')} {m.get('serial_no', '')}",
            border_style="green",
        ))
        if full and m.get("fulltext"):
            console.print("[dim]全文 (主管機關來源頁轉存, 可能夾雜網頁雜訊):[/]")
            console.print(m["fulltext"])
            if m.get("fulltext_truncated"):
                console.print("[yellow]全文過長已截斷, 完整內容請開來源連結[/]")
    _print_notes(data.get("notes"))


@app.command("ref-search")
def ref_search(
    query: str = typer.Argument(..., help="自然語言查詢, 如: 扣繳義務人未依限申報之處罰"),
    n: int = typer.Option(5, "--n", "-n", help="結果筆數 (1-10)"),
    authority: Optional[str] = typer.Option(None, "--authority", help="機關名稱過濾 (精確名, 如 財政部)"),
    kind: Optional[str] = typer.Option(
        None, "--kind",
        help="來源類型過濾: administrative_interpretation / administrative_order / "
             "tax_interpretation / constitutional_interpretation / constitutional_judgment",
    ),
    excerpt: bool = typer.Option(False, "--excerpt", help="每筆加印命中段落"),
) -> None:
    """Semantic topic search over interpretations — listing only, verify with `ref`."""
    try:
        with _client() as c:
            data = c.search_legal_references(
                query, authority=authority, source_kind=kind, max_results=n
            )
    except RetrievalError as e:
        err.print(f"[bold red]檢索失敗:[/] {e}")
        raise typer.Exit(1)
    hits = data.get("results") or []
    if not hits:
        console.print("[yellow]無結果[/]")
        _print_notes(data.get("notes"))
        return
    table = Table(show_lines=False)
    table.add_column("#", justify="right", style="dim")
    table.add_column("引用", style="cyan")
    table.add_column("效力")
    table.add_column("相關度", justify="right")
    table.add_column("標題")
    for i, h in enumerate(hits, 1):
        table.add_row(
            str(i),
            h.get("citation", "") or f"{h.get('authority', '')} {h.get('serial_no', '')}",
            _status_markup(h.get("status")),
            f"{h.get('score', 0):.3f}",
            (h.get("title", "") or "")[:30],
        )
    console.print(table)
    if excerpt:
        for i, h in enumerate(hits, 1):
            text = (h.get("excerpt") or "").strip()
            if text:
                console.print(Panel(text[:1200], title=f"#{i} 命中段落", border_style="dim"))
    console.print(
        "[dim]相關性判斷由你的 AI 負責; 引用任一字號前, 先用 `twlegalrag ref <字號>` 查證效力與原文。[/]"
    )
    _print_notes(data.get("notes"))


@app.callback(invoke_without_command=True)
def _main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="顯示版本"),
) -> None:
    if version:
        console.print(f"twlegalrag {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


def main() -> None:  # console_scripts entry
    app()


if __name__ == "__main__":
    app()
