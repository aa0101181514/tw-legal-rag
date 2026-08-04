# Taiwan Legal RAG (`twlegalrag`)

> Open-source CLI for **semantic** Taiwan legal judgment retrieval, powered by
> Legal Detective's 22M-judgment retrieval infrastructure.

Taiwan Legal RAG CLI retrieves Taiwan court judgments from Legal Detective's
public TLR endpoint and packages them for use with **your own AI tools**. It
does **not** generate legal advice, does **not** call any LLM, and does **not**
guarantee semantic faithfulness of third-party model outputs. Its built-in
citation check only verifies whether cited judgments belong to the retrieved
bundle.

繁中：Taiwan Legal RAG CLI 是一個開源命令列工具,連接法律偵探建置的 2,200 萬筆
台灣裁判語義檢索服務,讓你能用自然語言搜尋判決,並將檢索結果帶入自己的 AI 工具使用。

## 為什麼不一樣

這不是一般關鍵字判決搜尋工具。背後連到的是法律偵探長期建置的 TLR 檢索服務：

- 約 **2,200 萬筆**台灣裁判資料,經過結構化處理與向量化。
- 經過上千小時的 retrieval pipeline optimization。
- 支援**語義模糊搜尋**——不是只靠案號、法院、關鍵字,能用自然語言查找
  「概念相近但用詞不同」的判決。
- **案號精確調卷**(v1.1)——query 是完整裁判字號(如「最高法院112年度台上字第9號」)
  時自動切換精確調卷,回傳該案號在庫內的文書(民/刑同號並列標注);**查無時明確
  告知**「查無不代表該裁判不存在,不得臆測該案內容」,不會拿語義近似結果充數。
- **審級關聯 `case_history`**(v1.1)——讀全文時附上該判決在資料庫記錄的上下審級
  (含「主文含『廢棄』」標記)。**引用前就能看到這篇判決是否已被上級審廢棄**;
  無上級審記錄僅代表資料庫未收錄,不代表裁判已確定。
- **行政函釋字號精確查詢 `get_legal_reference`**(2026-08, hosted MCP)——以發文字號
  (如「台財稅第881945861號」)查函釋全文與**效力狀態**(已驗證有效/未驗證/已廢止/
  停止適用/已被取代)。引用函釋前先驗存在性與效力;查無時明確告知**查無不代表
  該函釋不存在**。函釋與判決嚴格分流,不混排、不得引為法院見解。詳見
  [`docs/mcp-anchor.md`](docs/mcp-anchor.md)。
- **引用防護是一等公民,不是事後補丁**——bundle 附 `allowed_citations` 白名單
  (只含實際讀入理由全文的判決)、`unread_candidates` 標記(未讀入理由的判決不得
  引為 authority)、寫進每個 bundle 的 verification instructions(含見解層自查),
  加上 CLI 端的 bundle 層級 citation check。整套設計針對法律 AI 最痛的幻覺型態:
  **字號真實、見解捏造**。一般檢索工具把資料丟給模型就結束,這裡把「引用紀律」
  做成資料格式本身。
- 開源 CLI 本身**不內建判決庫**,也不暴露後端模型權重或向量索引;它是連接公開
  TLR retrieval endpoint 的工具。

### 與「官方網站 wrapper」型工具的差異

另一類常見做法是即時轉打司法院/法規官網的站內搜尋。兩者定位不同,可以互補：

| | 官網 wrapper | Taiwan Legal RAG |
|---|---|---|
| 搜尋方式 | 官方站內關鍵字搜尋 | 自建 2,200 萬筆語料的語義檢索,概念相近、用詞不同也找得到 |
| 引用防護 | 通常無 | read-whitelist + 驗證指示 + citation check |
| 案號調卷 | 依官網功能 | 精確調卷,查無時明確告知不得臆測 |
| 審級關聯 | 需自行逐案追 | `case_history` 直接附上,含廢棄標記 |
| 可用性 | 受官網 WAF / 改版影響,常需本地跑瀏覽器繞驗證 | hosted endpoint,零本地環境需求 |
| 資料即時性 | 官網即時 | 極新公告的裁判請以官網為準 |

官網 wrapper 的強項是即時性與官方來源直連;本工具的強項是語義檢索品質與引用
紀律。

> Unlike keyword-only legal search tools, Taiwan Legal RAG CLI connects to a
> production semantic retrieval backend built on 22M+ Taiwan court judgments,
> enabling fuzzy concept-level search while keeping model weights, infrastructure,
> and private indexes server-side.

（措辭說明：開源的是 **CLI**,不是模型或向量庫;後端的檢索服務、模型權重、私有
索引都留在伺服器端,不隨本工具公開。）

## 它做什麼 / 不做什麼

**做**：用自然語言檢索判決 → 取得結構化清單、判決全文片段(excerpt)、引用連結 →
打包成 bundle 交給你自己的 AI;並可對 AI 產生的答案做 bundle 層級的引用檢查。

**不做**：本工具**不呼叫任何 LLM、不生成法律意見、不背書**任何模型輸出。答案要由
你自己選的 AI(ChatGPT / Claude / Gemini / 本地模型)生成。

### 內建的 citation check 能檢查什麼

`check` 是 **bundle 層級、盡力而為**的字串檢查,只驗：

- 答案引用的判決字號**是否在 bundle 內**(抓「引用了不在 bundle 的字號」= 疑似捏造);
- 是否引用 bundle 外、或不存在的判決;
- **引文存在性(bundle 層級)**:答案宣稱「法院說……」的逐字句,是否出現在 bundle
  文字的**某處**。

### 它**不能**檢查什麼（重要）

- 引文是否出自**答案所指的那一篇**判決(存在性檢查只看「整個 bundle 裡有沒有這句」,
  不綁定到特定判決);
- 法院見解是否**讀對**;
- 是否把**當事人主張**(原告/被告/上訴人)當成**法院見解**;
- 是否把**附帶論述**當成判決**核心權威**;
- paraphrase(改寫)型的見解幻覺。

這些都需要閱讀判決全文才能判斷——這也是為什麼 bundle 內附上判決全文片段與
verification instructions,要求下游模型自行核對。**`pass` 只代表「引用的字號身份對得上
bundle」,不代表「法律推論正確」或「引文確實出自那篇」。** 另外,`check` 只比對
**bundle 內的內容**,不是整個法律偵探資料庫——若你事後自己開判決全文再改寫答案,
`check` 仍只看 bundle 當初打包的片段。

## 安裝

```bash
pip install twlegalrag
```

只依賴 `httpx` / `typer` / `rich`。不需要任何 LLM 套件或金鑰——本工具不呼叫 LLM。

## 使用

```bash
# 1) 純檢索 — 列出符合的判決
twlegalrag search "勞資 加班費" -n 5 --read

# 2) 打包 — 產生可交給任何 AI 的 bundle ★主流程
twlegalrag pack "車禍對方全責,我可以求償什麼?" -o bundle.json
#   → 把 bundle.json 貼給 ChatGPT / Claude / Gemini,要求它只引用 bundle 內的判決

# 3) 引用檢查 — 對任何 AI 產生的答案做 bundle 層級檢查
twlegalrag check bundle.json answer.txt

# 服務是否正常
twlegalrag health
```

`pack` 產生的 bundle 包含 `query`、每筆判決的 `citation_id`(J1, J2, ...)、
`citation_text`、`citation_url`、`doc_id`、Layer-1 listing、`fulltext_excerpt`
(判決理由的擷取片段,有長度上限)、`case_history`(資料庫記錄的審級關聯,v1.1)、
`allowed_citations`,以及一段 `verification_instructions`,明確要求下游模型只引用
bundle 內判決、把不支持的命題標為 unverified。stderr 也會印一段 AI USE NOTICE。

v1.1 起 `verification_instructions` 額外包含**見解層自查規則**(OPINION-LAYER
SELF-CHECK),要求下游模型在作答後逐一回頭核對:(a) 歸給某判決的見解確實出現在
該判決的 excerpt(不是別篇的、不是推論的);(b) 裁判結果方向(勝訴/敗訴/廢棄/駁回/
發回)沒有顛倒;(c) `case_history` 顯示已被廢棄的判決,不得當成現行有效見解引用。
這與 `check` 的 bundle 層級字號檢查互補——字號真實不代表見解真實,見解層的核對
只能由**讀了全文的模型**自己做,這些規則就是把該動作寫進每個 bundle 的硬性指示。

`allowed_citations` 是「可引用判決」白名單,**只含實際讀入理由全文的判決**。CLI 的
`pack` 會讀入每一筆判決,所以兩者一致。Hosted Remote MCP 的 `search_bundle`
(`/v1/pack`)若 `read_top < max_results`,只讀入前 `read_top` 筆;其餘判決仍列在
`judgments` 供瀏覽,但會移到 `unread_candidates`(非 authority,不可引為法院論理)。
詳見 [`docs/mcp-anchor.md`](docs/mcp-anchor.md)。

## 設定(選用)

預設打公開端點 `https://tlr.dr-lawbot.com`,免金鑰即可使用。若服務方發給你 API key,
可放環境變數或 `~/.twlegalrag/config.toml`(已 git-ignore,**切勿** commit)：

```bash
export TWLEGALRAG_TLR_BASE_URL=https://tlr.dr-lawbot.com   # 預設
export TWLEGALRAG_TLR_API_KEY=...                          # 選用
```

```toml
[tlr]
# base_url = "https://tlr.dr-lawbot.com"
# api_key  = "..."
```

## 隱私與資料流向

先講清楚**哪些東西永遠不會經過 TLR 伺服器**：

- 你與 AI(Claude / ChatGPT / 本地模型)的**完整對話內容、上傳的文件、AI 生成的
  回答**,全部發生在你與你的 AI provider 之間,**從不經過** TLR。TLR 是 retrieval-only
  伺服器,唯一收到的是你的 AI client 決定送出的**檢索 query 字串**與後續調閱的
  判決編號。
- **不需要註冊帳號**：公開 REST 端點免金鑰即可使用,本服務沒有使用者帳號系統,
  查詢不與任何帳號身分綁定。
- 判決資料本身是台灣**公開**裁判書,查詢回傳的內容不含非公開個資。

其餘請務必理解的網路傳輸：

- 你的**搜尋字詞 / 問題**會送到 TLR 檢索端點(`https://tlr.dr-lawbot.com`)以取得判決。
- **TLR may log your query text, timestamp, IP-derived metadata, and result
  counts for retrieval-quality analysis. Do not submit personal secrets or
  confidential facts. Queries are not used to train generative models.**
  (TLR 後端可能以**明文**記錄你的查詢字串、時間、由 IP 推得的中介資料與結果筆數,
  供檢索品質分析之用。請勿送出個人機密或保密事實。查詢不會用於訓練生成模型。)
- 本工具**不呼叫 LLM、不使用 server-side token**;若你自行把 bundle 餵給某個 AI,
  那段傳輸與費用發生在**你與你選的 AI provider 之間**,與本工具無關。
- 端點 API 金鑰(若有)請放環境變數,不要 commit 設定檔。

## citation check 如何運作

`twlegalrag/faithful/` 是一組**零依賴純函式**(只用標準庫 `re` + `unicodedata`)。
給定答案文字與 bundle 內判決片段,回 `pass` / `needs_review` / `fail`。設計上保守:
不確定時回 `needs_review` 而非 `fail`,以壓低誤報。它**不呼叫 LLM、不碰資料庫**,是
確定性的字串分析。

⚠️ 這個目錄是內部程式的**快照**,裡面有些函式(如 `check_party_as_court` /
`run_all_checks`)CLI **並沒有用到**。它們存在**不代表** CLI 能做見解層 / 語義驗證——
CLI 只用其中兩個 bundle 層級檢查。請勿把檔案清單當功能清單。詳見
`twlegalrag/faithful/VENDORED.md`。

## 其他接法（同一個 TLR 後端）

這個 CLI 是接 TLR 檢索服務的方式之一。同一個後端 `tlr.dr-lawbot.com` 也支援把判決
搜尋透過 **Remote MCP** 直接接進你的 AI 工具。兩者填同一個 MCP 端點
`https://tlr.dr-lawbot.com/mcp`,連線時會自動完成 OAuth(動態註冊,無需自行申請或
設定 API key)：

- **Claude（Remote MCP）**：Settings → Connectors → Add custom connector,URL 填
  `https://tlr.dr-lawbot.com/mcp`。
- **ChatGPT（MCP connector）**：在 Connectors 新增自訂 MCP server,URL 填
  `https://tlr.dr-lawbot.com/mcp`。
- **Claude Code（Skill,走 CLI 非 MCP）**：本 repo 附了一個現成的 skill 在
  [`skills/tw-legal-rag/`](skills/tw-legal-rag/)，把整個資料夾放到你專案的
  `.claude/skills/` 即可。它包裝本 CLI 的 `pack` 子指令，讓 Claude 在你問到
  台灣判決／法律論據時自動檢索、並要求只引用 bundle 內的 `citation_id`。
  skill 內附的 `scripts/search_judgments.py` 會自動定位執行檔，並處理 Windows
  上的兩個踩雷點（詳見 skill 內的 `SKILL.md`）。

Remote MCP 介面現有四個工具:`search_bundle`、`search_judgments`、
`get_judgment_fulltext`,以及 2026-08 新增的 `get_legal_reference`(行政函釋字號
精確查詢,見 [`docs/mcp-anchor.md`](docs/mcp-anchor.md));後者尚未接入本 CLI。

不論走 CLI、MCP 還是 Claude Code skill,答案都由**你自己的 AI** 生成,本服務只提供
判決內容與可驗證的引用連結。

## 架構

```
你的問題
   │
[檢索]  TLR /v1/search   ──►  Layer-1 listings + result_token
   │    TLR /v1/fulltext ──►  每篇判決理由全文片段 (excerpt, 有上限)
   │
[打包]  pack ──► bundle.json (citation_id / allowed_citations / verification rules)
   │            └─► 交給你自己的 AI 工具
   │
[檢查]  check ──► bundle 層級引用檢查 (在/不在 bundle + bundle 內引文存在性)
```

判決庫、embedding、檢索邏輯都在伺服器端,**不在本 repo**。本 CLI 是開源客戶端
與引用檢查工具。

## 免責

本工具是分析輔助,不是法律意見,也不是律師。務必自行閱讀引用的判決全文。
透過 API 取得的判決為台灣公開裁判資料,你需為自己的使用負責。

## License

MIT.
