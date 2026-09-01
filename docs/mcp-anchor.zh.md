**中文** | [English](mcp-anchor.md) | [日本語](mcp-anchor.ja.md)

# Remote MCP Anchor 搜尋 Bundle

自 2026-06-04 起,hosted Remote MCP 端點 `https://tlr.dr-legal.com.tw/mcp` 的
`search_judgments` 改用 anchor 式回應。

本文適用於 hosted MCP 工具面。開源 CLI 維持 retrieval-only,仍以 TLR 為遠端檢索
端點。

## 改了什麼

Remote MCP 流程中的 `search_judgments` 現在回傳 anchor bundle。伺服器先讀入最相關
判決的理由摘錄,回傳：

- `allowed_citations`:可作為 authority 引用的 citation ID。
- `judgments`:理由摘錄實際被讀入本次回應的判決。
- `unread_candidates`:理由未被讀入 bundle 的候選：原因可能是 payload 額度、全文
  無法取得/為空,或(對 `search_bundle` 而言)落在 `read_top` 之外。各附 `reason`,
  不得引為 authority。
- `verification_instructions`:要求下游 AI 只引用 `allowed_citations` 的規則。

只有列在 `allowed_citations` 的判決可以作為法院論理引用。

## 為什麼

先前的純 listing 流程,太容易讓下游 AI 引一個真實的台灣案號,卻對該案捏造或錯掛
法律命題。anchor bundle 給 AI 讀入的摘錄而非只有標題,降低這種「標題式誤引」風險。

伺服器仍不呼叫任何 LLM,只做檢索與打包。任何答案都由使用者自己的 AI 工具生成。

## 重要限制

這不保證下游 AI 忠實。TLR 無法控制檢索之後的 Claude、ChatGPT、Gemini 或本地模型。
anchor bundle 降低標題式誤引風險,但使用者仍應自行檢視引用的判決。

`unread_candidates` 不是 authority,只作為檢索中介資料附上,不得引為法院論理。

## 與 CLI bundle 及 hosted `search_bundle` 的關係

CLI 的 `pack` 指令把判決與引用規則打包給使用者自備的 AI 工具。CLI 在本地組 bundle
且讀入每一筆回傳判決,所以其 `allowed_citations` 永遠與內含摘錄一致。

Hosted Remote MCP 對兩個工具套用同一套 read-whitelist 哲學：

- `search_judgments`(anchor):伺服器在 payload 額度內讀入最相關摘錄;
  `allowed_citations` 只含摘錄實際被讀入的判決。
- `search_bundle`(hosted `/v1/pack`):當 `read_top < max_results`,只有前
  `read_top` 筆被完整讀入。自 2026-06-26 起,`allowed_citations` **只**含這些已讀
  判決;其餘結果仍列在 `judgments` 供瀏覽,但移入 `unread_candidates`,不得引為
  authority。(先前未讀結果曾被錯誤地以空殼形式列入 `allowed_citations`，已修正。)

三個介面規則一致:只引用 `allowed_citations`;`unread_candidates` 視為檢索中介
資料,非 authority。

## v1.1: `case_history` 與見解層自查

- 已讀判決(`fulltext_available=true`)附 `case_history`:資料庫記錄的上下審級
  (`upper` / `lower`,各項含 `citation_text`、`doc_type`、`jdate`、`main_flag`)。
  `main_flag` 為「主文含『廢棄』」時,該判決已被上級審廢棄,不得當現行有效見解引用。
  無上級審記錄僅代表資料庫未收錄,不代表裁判確定。
- `verification_instructions.rules` 新增 OPINION-LAYER SELF-CHECK:要求下游模型
  作答後逐一核對見解出處、裁判結果方向(勝訴/敗訴/廢棄/駁回/發回)、以及
  `case_history` 的廢棄標記。
- `search_judgments` 對完整裁判字號自動切換精確調卷;查無時 `note` 欄位明示
  「查無不代表不存在,不得臆測」。

## 2026-07-26: 重複查詢指引與過期 token 復原

Hosted MCP 面兩項面向 client 的行為更新：

- **工具描述現在指示重用 bundle。**`search_bundle` 與 `search_judgments` 告訴
  client:同一問題若在對話稍早已搜尋過,重用那些結果,不要重發相同查詢。相同查詢
  回傳相同判決;堆疊重複 bundle 會劣化答案品質。
- **過期 `result_token` 錯誤改為可行動。**`get_judgment_fulltext` 帶過期或不符的
  `result_token` 時回 HTTP 400 `result_token_invalid_or_expired`,並提示重跑一次
  搜尋取得新 token。(文件不存在的 HTTP 404 不變。)

## 2026-08-04: `get_legal_reference` — 行政函釋字號精確查詢(hosted MCP)

Hosted MCP 新增第四個工具 `get_legal_reference`(另有 REST
`POST /v1/legal_reference`),以**發文字號**精確查詢台灣主管機關行政函釋/令函,
回傳全文與**效力狀態欄位**。開源 CLI 目前未接此工具;本工具同樣**不呼叫任何 LLM**。

### 用途

引用函釋前的存在性與效力驗證:書狀或法律分析引到「台財稅第○○號函」時,先查這支
函釋是否存在於語料庫、資料庫是否記錄其已廢止/停止適用。

### 輸入

- `serial`(必填):發文字號,如 `台財稅第881945861號`、`(79)台勞保二字第17914號`。
  伺服器端自動正規化:全半形、臺/台、「字第」/「第」、尾綴「函/令/公告」、
  中文數字(第○六八五四號)、年度前綴(（79）)等格式差異都會收斂,不需先整理格式。
- `authority`(可選):機關名稱提示,僅用於同字號多機關時的排序,不做過濾。

裁判字號(含「年度」,如 `112年度台上字第9號`)會被擋下並提示改用
`search_judgments`：函釋與判決是兩類文書,永不混排。

### 輸出

`matches[]` 每筆含:`authority`、`serial_no`(正規化後)、`title`、`issue_date`、
`fulltext`、`source_url`,以及效力狀態欄位:

| `status` | 意義 | 呼叫方應對 |
|---|---|---|
| `active_verified` | 資料庫已驗證仍為現行有效 | 可引用(仍建議核對原文) |
| `unknown` | **尚未完成效力驗證** | 不代表失效、也不代表確認有效;引用前向主管機關法規系統確認 |
| `repealed` / `ceased` | 資料庫記錄已廢止/停止適用 | 勿引為現行有效法源 |
| `superseded` | 已被後令取代 | 改查 `superseded_by` 所指字號 |

`status` 為 `unknown` 時回應會附明確警語,不隱藏、也不假裝 active。彙整/修正令
一筆記錄可能涵蓋多支字號,以其中任一支字號查詢皆可命中。

### 查無的語義(重要)

查無時回傳收錄範圍聲明(收錄機關數與筆數)。**查無不代表該函釋不存在**，本庫非
全量收錄,不得因查無而認定字號有誤或函釋係捏造。查無的字號會回饋為語料補收的
優先參考(用量驅動涵蓋率)。

### 限制

- 效力狀態為**資料庫記錄**,非法律意見;引用前請以主管機關公告為準。
- 回傳為主管機關行政函釋/命令資料,**非法院裁判**,不得作為法院見解引用;每筆
  回應皆附此提醒。
- 函釋的主題/關鍵字探索請用 `search_legal_references`(見下節);本工具是這對
  工具中負責精確查證與效力核驗的一半。

## 2026-08-08:`search_legal_references`:函釋語義檢索(hosted MCP)

hosted MCP 新增第五個工具 `search_legal_references`(亦提供 REST
`POST /v1/legal_references/search`):以**自然語言**對台灣行政函釋/令函、
行政規則、釋字與憲判字做語義檢索。與本介面其他工具一樣
**全程零 LLM**,且**刻意不做相關性判斷**:只回傳語義相似候選,判斷權交給
呼叫端模型。

### 輸入

- `query`(必填):自然語言主題查詢,如「扣繳義務人未依限申報扣繳憑單之處罰」。
- `authority`(可選):機關名稱精確過濾,如「財政部」。與 `get_legal_reference`
  的 hint 不同,此參數**會過濾**。
- `source_kind`(可選):`administrative_interpretation` /
  `administrative_order` / `tax_interpretation` /
  `constitutional_interpretation` / `constitutional_judgment` 之一。
- `max_results`(可選,1–10,預設 5)。

裁判字號會被拒絕並提示改用 `search_judgments`,與 `get_legal_reference` 同。

### 輸出

`results[]` 每筆含 `citation`、`serial_no`、`authority`、`title`、
`issue_date`、`source_kind`、與 `get_legal_reference` 同一套效力 `status`
欄位、相似分數 `score` 與摘錄 `excerpt`。未通過伺服器端確定性完整性檢核的
候選(含資料庫記錄為已廢止/停止適用者)會被剔除並**計入 `rejected`**:
剔除必揭露,絕不靜默。

### 呼叫端自驗契約(本工具的核心)

回傳為**語義相似候選,不是已驗證的答案**。分數高不代表與你的問題相關、
不代表現行有效、也不代表具權威性。引用任何候選前,呼叫端模型必須:

1. 閱讀摘錄,自行判斷相關性;
2. 以候選的 `serial_no` 呼叫 `get_legal_reference` 取得全文與效力狀態
   (`repealed`/`ceased` 勿引為現行法;`unknown` 為效力未驗證);
3. 只引用在取回全文中逐字存在的文字。

兩工具成對設計:`search_legal_references` 找到真實字號,讓模型不必憑記憶
臆測字號;`get_legal_reference` 再驗證存在性、原文與效力。

### 限制

- 查無結果**不代表**不存在相關函釋:本庫非全量收錄,語義檢索亦非窮舉。
- 回傳為主管機關資料,**非法院裁判**:不得引為法院見解,不得與判決引用
  混排;每筆回應皆附此提醒。
- 函釋與判決維持嚴格分流:本工具絕不回傳判決,判決工具絕不回傳函釋。


## 2026-08-20 更新（search_bundle / get_judgment_fulltext）

- `search_bundle` 回應頂層新增 `result_token`：bundle 內任一 doc_id（含
  `unread_candidates`）皆可用 `get_judgment_fulltext` 補讀全文。unread 判決
  「列出但未讀不可引」的紀律不變，補讀後始可引用。
- `judgments[]` 新增 `hit_excerpt`（命中段落預覽）。引用請以理由全文為準，
  勿以此欄代替全文核對。
- `get_judgment_fulltext` 新增 `excerpt_offset` 參數與 `fulltext_total_chars`
  欄位；`fulltext_truncated=true` 時以 offset 續讀。請讀到相關章節再下結論，
  勿憑首窗斷定某論述不存在。
- 詞彙檢索模式（`keyword` / `phrase`）改為相關性排序；零命中回空。

## 2026-09-01:`get_law_article` — 現行法條精確查詢(hosted MCP)

hosted MCP 新增第六個工具 `get_law_article`(亦提供 REST
`POST /v1/law_article`):以**法規名稱＋條號**精確查詢現行條文。與本介面其他
工具相同,**不呼叫任何 LLM**。法條語料鏡自全國法規資料庫,定期同步。

### 用途

引用法條前的查證:條號是否存在、現行條文逐字為何、法規有無廢止註記。修法會
使條號位移,而憑模型記憶背出的條文常是似真的幻覺;本工具用查詢取代記憶。

### 輸入

- `law_name`(必填):官方全名或常用縮寫(勞基法、刑法、憲法、民訴法等均可
  解析);黏著引述字的寫法(依民法、次按勞基法)亦可解析。
- `article_no`(必填):`184`、`第184條`、`47-1`、`第47條之1`、中文數字
  (第十八條)皆接受。

### 輸出

`matches[]` 各筆含官方 `law_name`、`law_level`(法規層級)、
`law_modified_date`(最後修正日期)、`law_url`(官方資料庫連結)、
`abolished`(廢止註記旗標)、正規化後的 `article_no`,以及
`article_content`(該條現行全文)。條文引用**只得**逐字取自
`article_content`。

### 查無的語義

- 法規解析成功而條號查無:回應會明確說明並附該法條文總數。本庫按法規整部
  收錄,此情形通常表示條號有誤或已因修法整編變動。
- 法規名稱查無:`law_candidates` 列出名稱包含查詢字串的收錄法規,供改用
  完整名稱重查。查無**不**代表該法規不存在:自治條例、自治規則與部分行政
  規則不在收錄範圍。

### 限制

- **僅現行整編版本**,不含歷史版本:不得以本工具驗證行為時法(修法前舊條文)
  之引文,請循 `law_url` 至官方沿革查詢。
- 僅限法規:行政函釋請用 `get_legal_reference`,裁判請用 `search_judgments`。
