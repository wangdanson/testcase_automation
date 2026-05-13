# Partners 核心業務邏輯與連動規則

> **本文件用途**: 將 `source_files` 中 Partners / OneAD Partners 相關規格整理成可直接支援 QA 測試案例產出的規則知識庫。
> **最後盤點日期**: 2026-05-13
> **覆蓋說明**: 本文件不是原始規格全文轉錄；附件、流程圖、PPT/PDF/EML 只作來源索引與輔助脈絡，測試規則以 HTML 規格內容為主。

---

## 一、來源覆蓋範圍

### 1. Phase 1 - 註冊、網站與基礎 API
*   `source_files/OneAD Partners Phase1/OneAD Partners 需求文件/OneAD Partners 需求文件.html`
*   `source_files/OneAD Partners Phase1/API/API.html`
*   `source_files/OneAD Partners Phase1/OneAD Partners Phase1.html`：容器頁，無實質規格內容。
*   相關附件包含網站主申請平台 wireframe、流程圖、註冊合約與需求簡報。

### 2. Phase 2 - 收益、請款與請款審核
*   `source_files/OneAD Partners Phase2/OneAD Partners Phase2 SDD Spec/OneAD Partners Phase2 SDD Spec.html`
*   `source_files/OneAD Partners Phase2/OneAD Partners Phase2 需求文件/OneAD Partners Phase2 需求文件.html`
*   `source_files/OneAD Partners Phase2/OneAD Partners Phase2.html`：容器頁，無實質規格內容。
*   相關附件包含請款流程圖、採購/請款 sequence 與計價方式圖。

### 3. Phase 3 - 多網站、銀行帳戶與跨系統調整
*   `source_files/OneAD Partners Phase3/OneAD Partners Phase3 SDD Spec/OneAD Partners Phase3 SDD Spec.html`
*   `source_files/OneAD Partners Phase3/OneAD Partners Phase 3.1/OneAD Partners Phase 3.1.html`
*   `source_files/OneAD Partners Phase3/OneAD Partners Phase 3.2/OneAD Partners Phase 3.2.html`
*   `source_files/OneAD Partners Phase3/OneAD Partners Phase 3.2/[0108] 銀行賬戶表單邏輯調整/[0108] 銀行賬戶表單邏輯調整.html`
*   `source_files/OneAD Partners Phase3/OneAD Partners (Phase 3.3_開放投放 FlashDrive 快閃廣告)/OneAD Partners (Phase 3.3_開放投放 FlashDrive 快閃廣告).html`
*   `source_files/OneAD Partners Phase3/OneAD Partners Phase3.html`：容器頁，無實質規格內容。

### 4. Phase 4 與後續跨部門需求
*   `source_files/Partners Phase4/Partners Phase4.html`
*   `source_files/Partners 前後端優化調整20241007[跨部門需求]/Partners 前後端優化調整20241007[跨部門需求].html`
*   `source_files/Partners 產品首頁修改與防呆優化/Partners 產品首頁修改與防呆優化.html`
*   `source_files/Partners 新增廣告格式需求, 前後端開發注意事項/Partners 新增廣告格式需求, 前後端開發注意事項.html`
*   `source_files/Partners 新增格式NativeDriveGroup[跨部門需求]/Partners 新增格式NativeDriveGroup[跨部門需求].html`
*   `source_files/Partners 媒體人工開放 特殊格式(FlashDrive_Cover_….)/Partners 媒體人工開放 特殊格式(FlashDrive_Cover_….).html`
*   `source_files/[Partners][SuperDSP 平台化 Phase 1.5.0] Commerce Ad/[Partners][SuperDSP 平台化 Phase 1.5.0] Commerce Ad.html`

---

## 二、角色、權限與狀態基本規則

### 1. 核心角色
*   **網站主**: 管理網站、申請廣告版位、取得嵌入碼、查看收益、提出請款與追蹤請款紀錄。
*   **PD / publisher_manager / partner_admin**: 審核網站、審核廣告格式、處理請款審核與必要的人工修正。
*   **partner 技術協助角色**: 可協助埋設嵌入碼，但不等同於可操作財務或網站審核。
*   **財務 / ERP/OSS 使用者**: 審核請款、駁回請款、通過請款與付款。

### 2. API 回應格式
*   成功回應需包含 `status` 與 `data`；錯誤回應需包含 `status` 與 `message`，可選 `code`。
*   權限不足、資料格式錯誤、資料值錯誤與 runtime error 都應回傳錯誤格式，前端不可只依 UI 阻擋。
*   需要登入的 API 需帶 `Authorization: Bearer {TOKEN}`，測試需覆蓋無 token、過期 token、停權帳號與權限不足。

### 3. 審核狀態
*   網站審核與廣告格式審核至少需覆蓋 `pending`、`approved`、`rejected`；網站另有停用情境。
*   `pending` 項目在審核列表需優先排序。
*   已審核過的項目，後端需阻擋重複審核或非法狀態變更；Phase 4 仍提出「核准網站後再駁回」流程缺口，相關測試需標註待確認。
*   廣告格式審核駁回時必須輸入或保留駁回原因，使用者需重新送審。

---

## 三、註冊、網站與帳號資料

### 1. 註冊流程
*   使用者註冊時需填寫帳號資料與網站資料，網站資料包含中英文名稱、分類、桌機網址、手機網址與網站簡介。
*   Phase 1 初版定義「一個帳號僅支援一個網站」，Phase 3 改為支援多網站；測試案例需依目標版本判斷預期。
*   一個網站視為一個媒體，具備獨立 `uid`；Partners 來源網站通常可依 `uid` 以 2 開頭識別。
*   個人轉公司或公司轉個人屬敏感帳務資料異動，需驗證既有請款紀錄不被錯誤改寫。

### 2. 網站與社群平台限制
*   網站網址必須支援嵌入 Javascript，因 OneAD 廣告代碼依賴 JS。
*   註冊與網站申請需阻擋不支援 JS 嵌入的社群平台網址前綴，例如 Facebook、Instagram、Threads、LINE、YouTube、TikTok、Discord。
*   受限網址需顯示明確錯誤：「不支援此平台網址，請使用可嵌入 JS 的網站」。
*   URL 提示 icon 需支援 hover / click 顯示說明，並在各 breakpoint 不影響排版。

### 3. 多網站
*   Phase 3 開放「網站管理 / 新增網站」；新增網站後，收益報表、請款申請、請款紀錄與審核明細都需可依網站區分。
*   收益報表 filter 需追加網站 id；請款紀錄明細需顯示 `media_id` 與 `media_name`。
*   多網站測試不可只驗證列表新增成功，還要驗證報表、請款、審核、ODM 媒體選單中的資料隔離。

### 4. 海外使用者資料
*   Phase 3.2 放寬手機限制，註冊與個人資料頁需支援國碼選擇。
*   手機號碼欄位至少不得為空；若啟用國碼驗證，需在選國碼後與送出前都驗證，正確顯示綠色勾勾，錯誤顯示紅框與「請輸入正確的手機號碼」。
*   個人資訊需支援本國/外國國籍選項；本國顯示身分證字號，外國顯示護照號碼。
*   銀行代碼需支援「其他」選項，供國外銀行由 PD 人工處理。

---

## 四、網站審核與廣告格式審核

### 1. 網站審核
*   PD 核准網站後需寄信通知使用者。
*   Phase 1 定義網站駁回不需填寫原因；Phase 3.2 改為駁回時跳出 modal 可填原因，mail 需帶入原因。
*   若未填寫駁回原因，通知信需顯示預設值：「因為您提供的網站，不符合「發布商政策」」。
*   網站審核 API 需支援 `note` 或等價欄位保存駁回說明。

### 2. 廣告格式申請
*   網站主可在廣告格式頁面取得嵌入碼，初版僅開放 TextDrive；後續加入 FlashDrive、NativeDriveGroup、Commerce Ad 等格式。
*   建立廣告格式申請時初始狀態為 draft 或 pending，送審後需通知 PD。
*   同一網站、同一格式不可重複申請。
*   PD 核准或駁回廣告格式時，Partners 與 OSS 審核列表狀態需一致，並需寄送核准/駁回通知信。
*   駁回廣告格式時需填寫失敗原因，供網站主修正埋碼或設定。

### 3. 主要 API
*   使用者：`/api/v1/one_sense/users/login`、`/logout`、`/forgot_password`、`/update_password_by_verification_code`、`/registration`、`/info`、`/update_info`、`/update_password`。
*   網站：`/api/v1/one_sense/medias/`、`/api/v1/one_sense/medias/options`、`/api/v1/one_sense/medias/{:id}`。
*   廣告格式：`/api/v1/one_sense/media_ad_format_type_reviews/options`、`/api/v1/one_sense/media_ad_format_type_reviews`、`/api/v1/one_sense/media_ad_format_type_reviews/:id`、`/:id/review`。
*   OSS 審核：`/one_sense/media_reviews`、`/one_sense/media_reviews/:id/review`、`/one_sense/media_ad_format_type_reviews`、`/one_sense/media_ad_format_type_reviews/check_review`。

---

## 五、收益、請款與帳務

### 1. 收益報表
*   網站主需可依月份查看廣告收益；Phase 2 新增收益明細頁，Phase 3 多網站後需支援網站篩選。
*   收益資料需包含媒體、廣告格式、計價模式、播放/曝光等量值與金額；特殊格式需確認 `profit-report` 與 `media-fee-cost` 都能吃到收益。
*   FlashDrive / Cover / GP+ 等人工開放格式也需出現在 Partners 收益報表與帳務流程中。

### 2. 請款申請
*   網站主當月 10 日前可申請上個月分潤；可請款月份需來自尚未請款或符合狀態的收益資料。
*   單次請款金額下限為 3000 元。
*   請款時需附上勞務報酬單或發票；請款後狀態變更為請款中 / pending。
*   請款申請 API `POST /api/v1/one_sense/my_checks` 需帶 `payment_info_id` 與 `media_months`。
*   金額計算需先對每月金額四捨五入，再加總；稅額為 `amount * 0.05` 後四捨五入。

### 3. 請款審核與紀錄
*   ERP/OSS 請款審核頁需支援搜尋、查看銀行帳戶影本、採購單與請款明細。
*   PD 駁回請款時必須輸入原因；請款狀態變更為駁回並通知網站主。
*   PD 通過請款時，請款狀態進入準備付款或後續付款狀態。
*   財務付款後，請款狀態變更為已付款。
*   請款紀錄 list 需顯示單號、明細、付款帳戶、總金額、申請狀態與 note。
*   請款紀錄狀態顯示需先判斷是否有發票；若有發票，顯示預計入帳日；若沒有發票，顯示自身 status 與備註。
*   送出請款當日若是假日，發票日期欄位仍可直接帶入該假日日期。

### 4. 請款與附件 API
*   請款審核：`/one_sense/my_checks_reviews`。
*   請款申請：`/api/v1/one_sense/my_checks`。
*   請款紀錄：`/api/v1/one_sense/my_checks_lists`、`/api/v1/one_sense/my_checks_lists/:id/note`。
*   勞務報酬單下載：`GET /api/v1/one_sense/my_checks/download_labor_remuneration`，需帶請款單號。
*   銀行存摺影本下載：`/one_sense/my_checks_reviews/{:id}/bank_book`。
*   採購單下載：`/one_sense/my_checks_reviews/{id}/download_purchase_order`，回傳 xlsx mime type、base64 content 與 encoding。

---

## 六、銀行帳戶與付款資料

### 1. 銀行帳戶基本規則
*   銀行帳戶資料包含帳戶類型、身分證/統編或護照、銀行代碼、戶名、帳號、存摺影本與同意儲存資料。
*   個人銀行帳戶需新增戶籍地址欄位，GET / POST / PUT 都需保留。
*   銀行代碼選項由 `/api/v1/one_sense/payment_infos/bank_code_option` 提供。
*   新增與修改銀行帳戶在後端都可視為新增一筆付款帳戶資料；測試需確認舊請款引用不被覆寫。

### 2. 單一付款帳戶與快照
*   Phase 3 規定銀行帳號只能設定一個，但請款紀錄必須以請款當下的銀行帳戶資訊作為匯款資料。
*   只要功能指向銀行帳戶，都需驗證是否指向該筆請款紀錄對應的付款帳戶，而不是目前最新的銀行帳戶。
*   請款後若要變更匯款銀行帳戶，需走人工調整流程，不應由一般使用者直接改動既有請款的付款資訊。
*   OSS 匯入媒體群組付款帳戶時，需確認空白欄位是否依規格補齊文字，且不破壞 Partners 的單帳戶規則。

### 3. Phase 4 風險
*   Phase 4 目標是調整請款作業與使用者銀行帳戶錯誤處理流程。
*   規格提到曾發生 PD 誤核准網站，但缺少「核准網站後再駁回」流程；相關測試需列為已知流程缺口。

---

## 七、廣告格式與嵌入碼

### 1. 新增廣告格式通用檢查
*   前端需確認 `/media_ad_format_type_reviews/options` 回傳最新格式選項。
*   TPM/PAD 需提供格式圖片、預覽素材、欄位增減規則、PC/mobile 預覽需求。
*   後端需確認 `ad_format_type_id`、`price_info`、嵌入碼、計價單位、OSS preview 用 demo link、前端 `image_url` 是否完整。
*   格式資料需新增到 `ad_format_type_bundle.rb` 或等價 ActiveHash 資料；嵌入碼中的 uid 必須改為變數，不可寫死。

### 2. TextDrive
*   初版僅開放 TextDrive；需提供嵌入碼、網站主申請、PD 審核、收益與請款流程。
*   新增廣告單元頁需顯示 TextDrive 文案：「支援桌機與手機裝置的 WebView 頁面（不包括 native APP）」。

### 3. FlashDrive
*   Phase 3.3 新增 FlashDrive 廣告格式，供網站主申請並取得嵌入碼。
*   合約需支援多種廣告格式與多計價方式；一個格式只會有一個計價單位。
*   `media_ad_format_type_reviews.ad_format_type_id` 需改為 ActiveHash id。
*   FlashDrive 格式選項由 `api/v1/one_sense/media_ad_format_type_reviews/options` 回傳，需包含 title、introduction、description、image_url 與多個 `ad_format_types`。
*   FlashDrive 申請成功後，系統需建立 FD 320 與 FD 300 兩個格式合約；已手動建立其中一個格式時需補齊另一個，手動價格優先於預設價格。
*   PD 核准 FD 後，ODM 廣告活動格式為 FD 320 / FD 300 時，該 Partners 網站需出現在媒體列表。
*   FD 收益計算預設 vCPM 為 40；若已手動調整價格，應以手動設定值為準。

### 4. NativeDriveGroup
*   NativeDriveGroup 新增格式細項 `ad_format_type_id = 231`。
*   嵌入碼需使用 `player_mode = "native-drive-group"`，`uid` 必須在實作時改為實際媒體變數。
*   過去格式文字調整不得影響使用者自行設定的文字；該文字調整需求已被規格標示忽略。

### 5. Commerce Ad in Partners
*   Commerce Ad 在 Partners 中歸類於 NativeDrive 原生廣告底下。
*   所有使用者至少需看到一次 Commerce Ad 上線通知彈窗；彈窗需有「下次不再顯示」勾選項、關閉按鈕與右上 X。
*   通知顯示狀態可用 Local Storage 紀錄，並需依上線期間設定停止顯示條件。
*   Partners / 廣告設定 / NativeDrive 原生廣告需新增手機版與電腦版預覽；電腦版需可切換 NativeDrive 與 Commerce Ad 預覽。
*   已申請 NativeDrive 的使用者，上線時需自動建立 Commerce Ad 合約資料。
*   未申請 NativeDrive 的使用者，按下「儲存並取得程式碼」後需同時建立 NativeDrive 與 Commerce Ad 兩種合約。
*   Commerce Ad 合約 `price_info` 需包含 `onead_price: 2`、`media_price: 2`、`gsp_buy_tech_license_fee: 0.5`、`media_buy_tech_license_fee: 0`、`rebate: 0`。

### 6. 人工開放特殊格式
*   FlashDrive / Cover / GP+ 等特殊格式可由 OSS 複製格式細項合約並修改 media id、uid 來人工開放。
*   若沒有合約審核紀錄，ODM 應視為 PD 直接建立，仍需可選到 Partners 媒體。
*   只要合約日期大於今天，Placement 區間外的合約仍可被選擇。
*   Partners 收益報表與 OSS `profit-report`、`media-fee-cost` 需能吃到人工開放格式收益。

---

## 八、ODM / OSS / ERP 跨系統連動

### 1. ODM 媒體選單
*   Partners 註冊網站需在 ODM 媒體設定清單中集中到 Partners 分類。
*   Partners 分類需支援展開/收合、全選/全不選與批次操作，避免媒體清單過長。
*   Partners 網站審核通過時，需依網站分類歸入 ODM 媒體選單。
*   以 `uid` 2 開頭判斷 Partners 媒體時，需測試非 2 開頭媒體不會被錯誤歸類。

### 2. OSS / ERP 審核與帳務
*   OSS 提供網站審核、廣告格式審核、請款審核、銀行存摺影本下載與採購單下載。
*   ERP 應付帳務需新增採購單號搜尋條件。
*   請款審核頁需能標註通過或駁回，並要求網站主修正資料。
*   Partners 請款、OSS 審核、ERP 付款三端的單號、狀態、金額、付款帳戶與附件需一致。

### 3. SuperDSP / Commerce AD 關聯
*   SuperDSP 推出 Commerce Ad 時，Partners 端需同步新增通知、預覽與合約建立。
*   Commerce Ad 在 SuperDSP / OYM / ERP 的 RTB、底價與帳務規則另見 `SuperDSP_RULES.md`；Partners 測試需聚焦網站主入口、合約與嵌入碼。

---

## 九、QA 產生測試案例時的硬性檢查清單

*   若規格涉及網站主資料、銀行帳戶、請款或發票，必須驗證舊紀錄快照不會被新資料覆寫。
*   若規格涉及多網站，必須同時驗證網站管理、收益報表、請款申請、請款紀錄、請款審核與 ODM 媒體選單。
*   若規格涉及廣告格式，必須覆蓋 options API、建立申請、重複申請防呆、嵌入碼、預覽、PD 審核、通知信、收益與請款。
*   若規格涉及人工開放格式，必須驗證 Partners 報表、OSS 報表成本、ODM 媒體選擇與合約日期判斷。
*   若規格涉及 Commerce Ad，必須分別覆蓋已申請 NativeDrive 與未申請 NativeDrive 使用者。
*   若規格涉及海外使用者，必須覆蓋國碼、護照號碼、國外銀行與「其他」銀行選項。
*   原始規格中的測試帳密不得沉澱到公開知識檔或測試案例輸出；需要測試資料時應引用環境資料管理機制。
