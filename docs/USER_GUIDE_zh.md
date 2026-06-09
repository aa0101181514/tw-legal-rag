# 怎麼用 AI 搜尋台灣判決（使用者指南）

法律偵探的判決檢索服務（TLR）讓你**用自己的 AI**（ChatGPT / Claude / 或開發工具）
搜尋並引用 2,200 萬筆台灣裁判。你不需要寫程式、不需要 API key。

> ⚠️ 重要：本服務只負責「找出並提供判決」。**答案由你自己的 AI 生成,法律偵探不為
> AI 的回答內容背書。** 任何法律結論請務必點開判決連結、自行核對全文。這不是法律意見。

---

## 方式 A：Claude Desktop（最推薦,免安裝）

1. 打開 **Claude Desktop** App。
2. 左上角選單 → **Customize（自訂）** → **Connectors（連接器）**。
3. 點右上角 **+** → **Add custom connector（新增自訂連接器）**。
4. 填入：
   - **Name（名稱）**：`法律偵探`（隨你取）
   - **Remote MCP server URL**：`https://tlr.dr-lawbot.com/mcp`
5. 按 **Add**。完成——不需要 OAuth、不需要 API key。

之後直接用中文問,例如：

> 幫我找違反銀行法被判無罪的判決,並引用 3 個案號。

Claude 會自動搜尋判決庫、讀取相關判決,再用它自己的理解回答你,並附上可點擊的判決連結。

---

## 方式 B：ChatGPT（建一個自訂 GPT）

1. 在 ChatGPT 建立 **Custom GPT**（需 ChatGPT Plus）。
2. 編輯 → **Actions** → **Create new action** → **Import from URL**。
3. 貼上：`https://tlr.dr-lawbot.com/openapi.yaml`
4. **Authentication（認證）** 選 **None**。
5. 儲存後,在這個 GPT 裡用中文問問題即可,GPT 會自動呼叫判決搜尋。

---

## 方式 C：命令列工具（給開發者 / 進階）

如果你習慣終端,可以裝開源 CLI,把判決打包成檔案再貼給任何 AI：

```bash
pip3 install twlegalrag

# 搜尋判決清單
twlegalrag search "銀行法 無罪" -n 5

# 打包成 bundle（給你自己的 AI 用）
twlegalrag pack "違反銀行法被判無罪的案件" -o bundle.json
```

把 `bundle.json` 整包貼給 ChatGPT / Claude,並要求它「只引用 bundle 內的判決」。

---

## 常見問題

**Q：我問「給我銀行法無罪的判決」,結果出現有罪/民事的案件?**
A：搜尋是「找語義相關」不是「精準篩結果」。AI 拿到清單後會讀全文判斷,但**請務必自己
點開判決連結核對**——尤其「是不是無罪」這種結論,一定要看判決主文,不要只信 AI 的摘要。

**Q：我的問題會被記錄嗎?**
A：你的搜尋字串會送到檢索服務,並可能被記錄以改善檢索品質(不含個人身分、不用於訓練
生成模型)。**請勿在查詢中輸入個人機密或保密事實。**

**Q：要付費嗎?**
A：判決檢索免費、免註冊。AI 的使用費由你自己的 ChatGPT / Claude 帳號負擔——本服務不收
AI 使用費,也不替你呼叫 AI。

**Q：判決連結點不開 / 想看完整判決?**
A：每筆結果都附 `dr-lawbot.com` 的判決連結,點進去看完整全文。
