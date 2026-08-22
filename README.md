# Taiwan Legal RAG (`twlegalrag`)

<div align="center">

### 🌐 Language / 語言 / 言語

**繁體中文** ・ [**English**](README.en.md) ・ [**日本語**](README.ja.md)

</div>

---

> Source-available CLI for **semantic** Taiwan legal judgment retrieval, powered by
> Legal Detective's 22M-judgment retrieval infrastructure.

Taiwan Legal RAG CLI retrieves Taiwan court judgments from Legal Detective's
public TLR endpoint and packages them for use with **your own AI tools**. It
does **not** generate legal advice, does **not** call any LLM, and does **not**
guarantee semantic faithfulness of third-party model outputs. Its built-in
citation check only verifies whether cited judgments belong to the retrieved
bundle.

作者：黃思齊（Aaron Huang）律師，[法律偵探／Dr.Legal](https://dr-lawbot.com) 創辦人（[個人介紹](https://dr-lawbot.com/aaron)）。

繁中：Taiwan Legal RAG CLI 是一個公開原始碼命令列工具,連接法律偵探建置的 2,250 萬筆
台灣裁判語義檢索服務（22,527,498 筆，截至 2026-08-22）,讓你能用自然語言搜尋判決,並將檢索結果帶入自己的 AI 工具使用。

## 資料涵蓋（統計截至 2026-08-22，取自 production 資料庫）

**一、法規範（依法位階）**

| 位階 | 資料類型 | 數量 | 說明 |
|---|---|---:|---|
| 憲法 | 憲法 | 1 部／197 條 | 中華民國憲法，含增修條文 12 條 |
| 憲法 | 釋字與憲判字 | 870 筆 | 大法官解釋 813 筆、憲法法庭判決 57 筆，有拘束全國各機關及人民之效力 |
| 法律 | 法律 | 1,083 部／45,620 條 | 定名為法、律、條例或通則者（中央法規標準法 §2） |
| 命令 | 命令 | 7,474 部／132,760 條 | 定名為規程、規則、細則、辦法、綱要、標準或準則者（同法 §3） |
| 命令 | 行政規則 | 83,778 筆 | 78 個機關發布之解釋性規定與裁量基準（行政程序法 §159），對外不生法規範效力 |
| 沿革 | 已廢止法規 | 3,230 部 | 法律 254 部、命令 2,974 部，及動員戡亂時期臨時條款等憲法位階規範，標示廢止狀態供查考 |

**二、裁判與裁決**

| 資料類型 | 數量 | 說明 |
|---|---:|---|
| 裁判書（司法院各級法院） | 22,527,498 筆 | 語義檢索＋詞彙檢索＋案號精確調卷；每日增量同步司法院公開資料 |
| 不當勞動行為裁決（勞動部裁決委員會） | 400 筆 | 勞動議題查詢自動並列，明確標示為裁決、非法院判決 |

**三、輔助資料**

| 資料類型 | 數量 | 說明 |
|---|---:|---|
| 審級關聯（上訴鏈） | 4,510,000+ 筆 | 隨判決附 `case_history`，含主文「廢棄／駁回」旗標 |
| 函釋效力履歷 | 50,800+ 筆 | 廢止／停止適用／被取代狀態追蹤，引用前驗效力 |

法規範與裁判之取用方式：裁判書、行政規則走 hosted MCP 的語義檢索與字號精確查詢；
憲法、法律、命令於 [dr-lawbot.com](https://dr-lawbot.com) 站上檢索。

裁判書為每日增量同步（司法院公開資料釋出有數日時差，極新宣判的裁判請以官網為準）。
以上數字直接取自 production 資料庫並標註統計日，非估計值。

### 裁判書明細（依法院層級／案件類別）

| 法院層級 | 筆數 |
|---|---:|
| 地方法院 | 16,686,158 |
| 地方法院簡易庭 | 3,268,495 |
| 高等法院及分院 | 1,328,661 |
| 最高法院 | 399,290 |
| 高等行政法院 | 200,600 |
| 最高行政法院 | 122,964 |
| 地方行政訴訟庭 | 78,891 |
| 智慧財產及商業法院 | 23,678 |
| 高雄少年及家事法院 | 22,113 |
| 其他專業法庭・委員會 | 32,250 |
| 未帶法院代碼欄位（計入總數，不列層級） | 356,515 |
| **合計** | **22,527,498** |

| 案件類別 | 筆數 |
|---|---:|
| 民事 | 14,232,712 |
| 刑事 | 7,332,321 |
| 行政 | 573,417 |
| 其他 | 24,650 |

### 行政規則發布機關明細（依文號編排者 74,685 筆）

| 機關 | 筆數 |
|---|---:|
| 財政部 | 10,602 |
| 內政部國土管理署 | 8,769 |
| 經濟部智慧財產局 | 7,161 |
| 法務部 | 7,064 |
| 勞動部 | 6,257 |
| 行政院環境保護署 | 4,463 |
| 行政院公共工程委員會 | 4,104 |
| 銓敘部 | 3,988 |
| 經濟部 | 3,118 |
| 農業部 | 3,057 |
| 金管會 | 2,815 |
| 內政部 | 2,648 |
| 前司法行政部 | 1,432 |
| 法務部行政執行署 | 1,410 |
| 內政部戶政司 | 1,391 |
| 公務人員保障暨培訓委員會 | 684 |
| 主計總處 | 669 |
| 國科會 | 567 |
| 文化部文化資產局 | 561 |
| 農業部水保署 | 543 |
| 司法行政部 | 433 |
| 考選部 | 429 |
| 人事行政總處 | 322 |
| 核能安全委員會 | 227 |
| 原住民族委員會 | 224 |
| 海洋委員會 | 213 |
| 公平交易委員會 | 204 |
| 文化部 | 203 |
| 法務部矯正署 | 167 |
| 中央選舉委員會 | 112 |
| 農業部林業及自然保育署 | 103 |
| 客家委員會 | 97 |
| 國家發展委員會 | 86 |
| 考試院 | 85 |
| 個人資料保護委員會籌備處 | 73 |
| 故宮博物院 | 55 |
| 環境部 | 46 |
| 臺灣高等法院檢察署 | 41 |
| 法務部政風司 | 37 |
| 法務部廉政署 | 32 |
| 司法院 | 28 |
| 經濟部能源署 | 28 |
| 法務部調查局 | 20 |
| 其他 35 個機關（各未滿 20 筆） | 88 |
| **合計** | **74,685** |

（機關名稱依函釋原始發文機關記載，含已改制機關之歷史名稱，如「行政院環境保護署」
「前司法行政部」；改制前後分列、不合併，以保留原始發文脈絡。）

## 為什麼不一樣

這不是一般關鍵字判決搜尋工具。背後連到的是法律偵探長期建置的 TLR 檢索服務：

- **22,527,498 筆**台灣裁判資料（截至 2026-08-22），經過結構化處理與向量化。
- **語義模糊搜尋**——不是只靠案號、法院、關鍵字，用自然語言就能找到
  「概念相近但用詞不同」的判決；另有詞彙精確檢索模式供專有名詞查找。
- **案號精確調卷**——完整裁判字號自動切換精確調卷；查無時明確告知
  「查無不代表該裁判不存在」，不拿語義近似結果充數。
- **審級關聯 `case_history`**——隨判決附上資料庫記錄的上下審級與主文
  「廢棄／駁回」旗標，**引用前就能看到判決是否已被上級審廢棄**。
- **行政規則雙工具**——字號精確查詢（附效力狀態：已驗證有效／未驗證／已廢止／
  停止適用／已被取代）與語義檢索成對使用；函釋與判決嚴格分流，不混排、
  不得引為法院見解。詳見 [`docs/mcp-anchor.zh.md`](docs/mcp-anchor.zh.md)。
- **引用防護是一等公民**——`allowed_citations` 白名單（只含實際讀入理由全文的
  判決）、`unread_candidates` 標記、寫進每個 bundle 的驗證指示，加上 CLI 端的
  citation check。整套設計針對法律 AI 最痛的幻覺型態：**字號真實、見解捏造**。
- 本 CLI **不內建判決庫**，也不暴露後端模型權重、向量索引或檢索管線細節；
  它是連接公開 TLR retrieval endpoint 的工具。

### 與「官方網站 wrapper」型工具的差異

另一類常見做法是即時轉打司法院/法規官網的站內搜尋。兩者定位不同,可以互補：

| | 官網 wrapper | Taiwan Legal RAG |
|---|---|---|
| 搜尋方式 | 官方站內關鍵字搜尋 | 自建 2,250 萬筆語料的語義檢索,概念相近、用詞不同也找得到 |
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

（措辭說明：公開原始碼的是 **CLI**,不是模型或向量庫;後端的檢索服務、模型權重、私有
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
詳見 [`docs/mcp-anchor.zh.md`](docs/mcp-anchor.zh.md)。

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

## 2026-08-20 服務端更新（hosted MCP / REST）

- bundle 回應附 `result_token`，可對 bundle 內任一判決直接調閱全文。
- 每筆結果附 `hit_excerpt`（命中段落預覽）；引用仍以理由全文為準。
- `get_judgment_fulltext` 支援 `excerpt_offset` 分頁，長判決可完整讀畢。
- 詞彙精確檢索模式（`search_type: keyword` / `phrase`）強化，適合專有名詞
  與技術用語；概念性問題建議預設的 `hybrid`。

以上為伺服器端能力，REST 與 Remote MCP 介面即日可用。CLI **v2.1.0** 已跟進：
`pack` 自動分頁讀完長判決（bundle 每篇全文預算加倍），並將命中段落
`hit_excerpt` 帶入 bundle。

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

Remote MCP 介面現有五個工具:`search_bundle`、`search_judgments`、
`get_judgment_fulltext`,以及 2026-08 新增的 `get_legal_reference` 與
`search_legal_references`(行政函釋字號精確查詢與語義檢索,見
[`docs/mcp-anchor.zh.md`](docs/mcp-anchor.zh.md));後兩者尚未接入本 CLI。

本服務已登錄於官方 [MCP Server Registry](https://registry.modelcontextprotocol.io/),
名稱為 `io.github.aa0101181514/tw-legal-rag`。

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

判決庫、embedding、檢索邏輯都在伺服器端,**不在本 repo**。本 CLI 是公開原始碼的客戶端
與引用檢查工具。

## 免責

本工具是分析輔助,不是法律意見,也不是律師。務必自行閱讀引用的判決全文。
透過 API 取得的判決為台灣公開裁判資料,你需為自己的使用負責。

## License

v2.0.0 起採 **Elastic License 2.0（ELv2）**。可自由使用、複製、修改與
再散布,包含商業與企業內部使用,僅有兩項限制:不得將本軟體本身作為
託管/代管服務提供給第三人,以及不得移除授權與聲明保護。
1.2.2 以前的版本維持 MIT。

託管 API 與判決語料庫從未在程式碼授權範圍內,詳見 [`TERMS.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/TERMS.md)。
專案名稱與標識不在授權範圍,詳見 [`TRADEMARK.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/TRADEMARK.md)。
本專案不接受外部 pull request（單一作者授權策略）,詳見 [`CONTRIBUTING.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/CONTRIBUTING.md)。
