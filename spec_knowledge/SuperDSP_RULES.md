# ⚙️ SuperDSP 核心業務邏輯與連動規則 (Core Rules)

> **本文件用途**: 將 `source_files` 中所有已辨識為 SuperDSP 相關的規格，整理成可直接轉換為 QA 測試案例的核心規則。  
> **最後盤點日期**: 2026-05-13  
> **覆蓋說明**: 本文件不是逐字轉錄規格，而是將平台化、AOE、Commerce AD、CCT、Custom Audience、FlashDrive、Preview、Studio、第三方量測、受眾與追蹤碼等規格中的「測試必驗邏輯」集中沉澱。完整來源索引請見 `SYSTEM_MAP.md`；Partners 網站主與請款/格式申請規則另見 `PARTNERS_RULES.md`。

---

## 一、來源覆蓋範圍

### 1. SuperDSP 主系統與平台化規格
*   `source_files/[SuperDSP 平台化]`
*   `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.3.0] IAS Pre-bid + 廣告實名制`
*   `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.3.0] 受眾鎖定 + 數據報告 + 權限設定`
*   `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.3.1] 受眾鎖定 新增 產業Shopper Graph & Webb 零售數據`
*   `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.3.2] 功能優化 admin 廣告主權限設定 & 廣告活動受眾包優化 & 廣告活動報表輸出 sheet 命名規則優化`
*   `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.4.0] IAS 內文比對`
*   `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.4.0] 第三方量測設定`
*   `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.4.0] 串接 Studio 素材管理 PRD`
*   `source_files/SuperDSP 權限整理`
*   `source_files/SuperDSP 從IO到Sequence`

### 2. AOE、Partners、Commerce AD 與特殊投放產品
*   `source_files/SuperDSP Pilot for AOE (Phase 1)`
*   `source_files/SuperDSP Pilot for AOE (Phase 2)`
*   `source_files/[Partners][SuperDSP 平台化 Phase 1.5.0] Commerce Ad`
*   `source_files/OneAD Partners Phase3/OneAD Partners (Phase 3.3_開放投放 FlashDrive 快閃廣告)`
*   `source_files/Partners 媒體人工開放 特殊格式(FlashDrive_Cover_….)`
*   `source_files/[SuperDSP 平台化]/[Commerce AD Phase 1] Commerce AD & RTB`
*   `source_files/[SuperDSP 平台化]/[Commerce AD Phase 2] Commerce AD 帳務管理 及 受眾洞察報告下載`
*   `source_files/[SuperDSP 平台化]/[Commerce AD Phase 3] Commerce AD 媒體端 RTB 底價設定`
*   `source_files/快閃廣告(FlashDrive) 上架 SuperDSP Phase1`
*   `source_files/SuperDSP格式Preview與正式環境廣告投放`
*   `source_files/SuperDSP 聯絡我們表單功能`

### 3. 受眾、追蹤碼、CCT 與大數據 API
*   `source_files/SuperDSP 新增追蹤碼 & 受眾打包`
*   `source_files/SuperDSP Custom Audience`
*   `source_files/SuperDSP CCT(Cross-Channel Targeting)`
*   `source_files/SuperDSP 大數據API`
*   `source_files/SuperDSP 新增 活動預測潛力模型 ( Campaign Potential Models )`
*   `source_files/segment target v2`
*   `source_files/[第三方媒體平台數據打通] 產業鑽石受眾`

---

## 二、權限與身分識別規則

### 1. SuperDSP 角色權限基本原則
*   Admin 具備跨廣告主管理能力；新增廣告主時，Admin 的廣告主權限必須自動被加入。
*   一般使用者只能操作其被授權的 client / advertiser / campaign / audience pack。
*   Agency、Advertiser、Media、Read-only、Brand client 角色需要分別驗證可見資料、可操作按鈕、抽屜可編輯性與 API 權限。
*   權限不足時，前端需隱藏或 disabled 操作入口，後端仍必須回傳權限錯誤，不能只依賴 UI。
*   Media 身分不得使用第三方量測追蹤碼；即使具備其他廣告操作權限，也不能看到或送出第三方追蹤碼設定。

### 2. Partners 與 AOE 特殊帳號
*   Partners 帳號在 Commerce AD/AOE 相關流程具備特定 UI 與資料權限。
*   Partners 或特定 SuperDSP 來源上傳到 ODM 的素材，存在「素材審核自動通過」或「免審核綠色通道」情境，需驗證 SuperDSP 與 ODM 狀態同步。
*   Partners 本身的網站主註冊、網站審核、廣告格式申請、收益與請款規則不在 SuperDSP 主流程內；跨到 Commerce Ad、FlashDrive 或 ODM 媒體選擇時需同時讀 `PARTNERS_RULES.md`。
*   AOE Pilot 流程需要驗證廣告主/產業主次類別/素材包/版位格式/投放狀態之間的連動，不能只測單一表單欄位。
*   AOE 特定 advertiser 或帳號條件應以資料驅動方式驗證，不應把單一 ID 當成全域規則；若規格明確指定 ID，測試案例需同時包含正向與非指定 ID 負向案例。

### 3. CCT 權限
*   Cross Channel Pixel 需要獨立權限開關，並在使用者管理的進階設定中控管。
*   Read-only 與 Brand client 只能檢視 Pixel，不能新增或編輯。
*   具備編輯權限者可新增、編輯、搜尋、檢視 Pixel，並在 Ad Group 建立/編輯流程中綁定或移除 Pixel。
*   CCT 權限需同時驗證 Cross Channel 頁面、Ad Group 抽屜與 API 層級，不可只驗證列表頁。

---

## 三、Campaign、Ad Group、Sequence 核心流程

### 1. IO 到 Campaign / Ad Group / Sequence
*   SuperDSP 的投放主流程以 IO 建立 Campaign，再建立 Ad Group，最後產生或更新投放 Sequence。
*   建立、更新、複製 Ad Group 時，應同步驗證 campaign_id、ad_group_id、投放格式、版位、素材包、受眾、第三方量測與追蹤碼欄位是否完整保留。
*   Ad Group 類型包含一般、Instream、RTB 等分支；測試案例需按 API endpoint 與 UI 表單分支拆開，不應只覆蓋一般 Ad Group。
*   Ad Group 狀態轉換需驗證 draft、oncue、投放中、結束、刪除/回收站等門檻，尤其是狀態改變後哪些欄位不可再改。

### 2. 版位格式與素材包連動
*   編輯 Ad Group 時，只要版位格式或廣告格式變更，已選擇的指定素材包必須自動清空。
*   素材包清空後不得保留隱藏欄位值；送出 payload 中也不能殘留舊 material_pack_id。
*   若素材包與版位格式不匹配，需阻擋送出並提示原因。
*   素材包秒數、格式、尺寸、第三方素材包類型與投放格式需一致；FlashDrive、RichMedia、QualityTraffic、Pre-roll 等格式需分開驗證。

### 3. 狀態門禁與日期邏輯
*   Campaign / Ad Group 投放中時，產業類別、部分版位設定、投放核心條件需鎖定。
*   結束日期不可早於開始日期；已投放或已結束項目的日期調整需遵守規格中的允許範圍。
*   列表與詳情頁中的狀態需一致；狀態變更後，快捷按鈕、編輯按鈕、複製按鈕與 Viewability/CCT/素材包入口要同步更新。
*   「Back to Reviewing」或退回審核類狀態需驗證 SuperDSP 與 ODM/Studio 的狀態流一致，不可只改單一系統。

---

## 四、Studio、素材管理與 ODM 審核

### 1. SuperDSP 串接 Studio
*   SuperDSP 可從 IO / Ad Group 流程導流至 Studio 建立素材包。
*   導流需驗證 token、source、return path、postMessage 或 callback 資料，確保建立完成後可回填 SuperDSP。
*   Studio 素材包預覽、建立、回填與重新選擇需驗證資料一致性。
*   若從 SuperDSP 前往 Studio 後取消或失敗，SuperDSP 表單不得保留半成品素材包。

### 2. 第三方素材包與素材審核
*   第三方素材包需依規格區分一般素材包與第三方量測素材包。
*   IAS / DoubleVerify / DCM / Nielsen 等第三方量測設定需要在 Ad Group 層級集中管理。
*   廣告組合綁定之素材包 Pixel Tag 已遷移到第三方量測設定處統一管理，測試時要避免舊入口仍可修改造成資料分歧。
*   ODM 素材審核狀態與 SuperDSP 顯示狀態需同步，包含待審核、通過、退回、重新審核、自動通過。

---

## 五、第三方量測、IAS、Viewability 與安全性

### 1. IAS Pre-bid 與廣告實名制
*   IAS Pre-bid 需驗證設定入口、格式可用性、送出 payload、錯誤提示與投放 sequence 是否包含對應安全設定。
*   廣告實名制欄位需驗證必填、格式、顯示位置與投放資料輸出。
*   不同廣告格式對 IAS 支援程度不同，測試案例要包含支援與不支援格式。

### 2. IAS 內文比對
*   IAS 內文比對需驗證頁面級內容安全校驗與 Environment / Content Matching 設定。
*   日期區間變動欄位的數值需在報表與 UI 中一致，不能只驗證設定保存。
*   當資料不足或不適用時，應顯示明確空狀態或無資料提示。

### 3. Viewability 快捷操作
*   Campaign 或 Ad Group 列表上的 Viewability 快捷按鈕需依權限、狀態與可用格式顯示。
*   Viewability 類型可包含 IAS、DoubleVerify 或無；必填與選項限制需在新增與編輯都驗證。
*   快捷抽屜的修改需回寫 Ad Group 詳情，且列表刷新後仍一致。

---

## 六、受眾定向、受眾包與大數據 API

### 1. Shopper Graph、Webb 與數據鎖定
*   受眾鎖定支援產業 Shopper Graph 與 Webb 零售數據。
*   Include / Exclude 條件需同時存在，且要驗證互斥、交集、空集合、過量選取與重複選取。
*   年齡、性別、興趣、產品品類等 tag 需要按照規格排序，不可依 API 回傳原順序直接顯示。
*   受眾預估量體需在條件異動後重新計算；無資料時需顯示空狀態。

### 2. Segment Target v2 與 Retargeting
*   Segment Target v2 支援 include 與 exclude 同時設定。
*   不同頁面來源包含 ODM、SuperDSP 受眾包與 RMN/委刊單匯出關聯，測試資料需覆蓋跨系統使用情境。
*   無權限時需回傳權限錯誤，且 UI 不應提供可操作入口。
*   受眾包被 Ad Group 綁定後，需顯示 linked_ad_groups 或關聯數，並限制會破壞投放的刪除/修改行為。

### 3. SuperDSP 受眾包生命週期
*   受眾包可由追蹤碼、事件、Web audience、Impression 事件等來源生成。
*   受眾包需驗證建立、更新、排程更新、UU 更新、過期判斷、綁定 Ad Group、解除綁定與複製流程。
*   排程更新受眾包與 Sequence 時，需驗證排程時間、失敗重試、資料版本與前台顯示。
*   Custom Audience 需驗證前端列表、後端狀態、受眾包類型狀態流程、自訂受眾包生命週期與過期判斷。

### 4. 大數據 API 與 Campaign Potential Models
*   `segment_event`、`demographic_event`、`interest_event`、`product_key_event` 等 API 需驗證 SuperDSP 與 ODM 介接資料格式。
*   Campaign Potential Models 歸屬在 `segment_ids`，新增、更新、取得、複製 Ad Group 時都需保持一致。
*   無符合條件時，前端需顯示空白狀態與「無資料」提示。
*   活動預測模型需覆蓋一般、Instream、RTB Ad Group API 分支。

---

## 七、追蹤碼、CCT 與第三方媒體平台資料打通

### 1. SuperDSP 追蹤碼與受眾打包
*   追蹤碼建立後可用於受眾包打包，並與 Ad Group / Campaign 投放資料連動。
*   追蹤碼狀態機需驗證建立、啟用、停用、更新、刪除、被受眾包引用與被 Ad Group 引用。
*   批次或排程更新時需避免舊追蹤碼覆蓋新設定。
*   追蹤碼相關測試需同時檢查 UI 欄位、API payload、受眾包生成結果與報表可見性。

### 2. CCT Pixel
*   CCT Pixel 欄位包含 ID、Name、Channel、Pixel ID、Created Date、Settings。
*   列表支援依 ID / Name / Channel / Pixel ID 模糊搜尋。
*   新增或編輯抽屜需驗證字數限制、必填、placeholder、成功訊息與列表更新。
*   Ad Group 綁定 CCT Pixel 後，複製、編輯、狀態切換時需確認 Pixel 綁定不遺失。

### 3. 產業鑽石受眾與第三方媒體
*   第三方媒體平台數據打通需區分 Google Ads、Meta、TikTok 的 CCT code。
*   建立 Campaign 時，系統可依 AOE 選擇的產業主次類別自動帶入相對應追蹤碼。
*   若產業類別未對應 CCT code，不得產生錯誤追蹤碼，需給出空狀態或提示。
*   匯入 CSV/XLSX 型 CCT code 時需驗證欄位格式、重複 code、平台欄位與產業分類映射。

---

## 八、Commerce AD 與 RTB

### 0. Partners 端 Commerce Ad 入口
*   Commerce Ad 在 Partners 端歸類於 NativeDrive 原生廣告，需同步新增上線通知彈窗與手機/電腦版預覽。
*   已申請 NativeDrive 的 Partners 使用者，上線時需自動補建 Commerce Ad 合約；未申請者按「儲存並取得程式碼」後需同時建立 NativeDrive 與 Commerce Ad 合約。
*   Partners 端 Commerce Ad 合約、嵌入碼與通知規則詳見 `PARTNERS_RULES.md`；SuperDSP 測試需關注 Commerce AD / RTB / 帳務主流程是否與 Partners 合約資料一致。

### 1. Commerce AD Phase 1 - 建立與 RTB
*   Commerce AD 建立流程需驗證資料定向、受眾模式、環境模式、產業/產品類別、廣告格式、CPC 出價、Margin、Studio 素材包與其他投放設定。
*   CPC 出價最低值、CPC 小數位、Margin 整數限制、Margin 不得超過上限等表單限制需驗證。
*   實際競標價由 CPC 出價與 Margin 推導，測試案例需包含邊界值與顯示值一致性。
*   RTB Sequence 需包含地板價、競標價、出價、受眾包 ID 與 contextual key。
*   固定價格與 RTB 競價模式在報表、帳務與 sequence 欄位中需可區分。

### 2. Commerce AD Phase 2 - 帳務與受眾洞察
*   受眾洞察報表需驗證可下載、欄位維度、無資料狀態、排序與欄位以 `-` 呈現的情境。
*   帳務管理每月使用報告需驗證新增/修改欄位、排序、交易模式、累計金額、平均 CPC 與是否判斷超跑。
*   報表欄位需包含 campaign/ad_group/advertiser 等可回查資料，不可只輸出統計值。
*   Commerce AD 財務報表需與 ERP/OSS 帳務資料對齊。

### 3. Commerce AD Phase 3 - 媒體端 RTB 底價
*   OYM / ERP 媒體端需設定 RTB 底價，SuperDSP 投放時需帶入對應 floor price。
*   底價變更需驗證生效時間、歷史資料、合約關聯與投放中 Ad Group 的處理方式。
*   RTB 投放不得低於有效底價；若低於底價需阻擋或提示。
*   媒體端、廣告主端與財務端看到的價格與交易模式需一致。

---

## 九、報表、匯出與資料一致性

### 1. SuperDSP 活動報表
*   廣告活動報表輸出 Sheet 命名需符合規格，避免財務與資料分析後續處理失敗。
*   日期區間變動欄位需在 UI 與下載報表中一致。
*   無資料時需產出明確空狀態或空報表規則，不能產生格式錯誤檔案。
*   Agency、Advertiser、Admin 等不同角色下載報表時，資料範圍需隔離。

### 2. 受眾洞察報告
*   預打包 Segment 名稱異動、產品品類差異、輸出規範優化都需納入測試。
*   匯出欄位的排序、命名、空值呈現與多維度資料需符合規格。
*   Shopper Graph / Webb / Commerce AD / Campaign Potential Models 等新增資料來源需在報表中可追蹤。

### 3. 跨系統資料一致性
*   SuperDSP、ODM、Studio、ERP/OSS、OYM 的關聯欄位需能互相追查。
*   素材狀態、受眾包狀態、投放狀態、報表數據、帳務金額不應出現單系統更新成功但其他系統未同步的狀態。
*   測試案例需針對「建立後立即查詢」、「更新後下載報表」、「狀態轉換後跨系統檢視」設計驗證步驟。

---

## 十、特殊產品與輔助功能

### 1. FlashDrive
*   FlashDrive 上架 SuperDSP 需驗證格式是否可被選擇、素材包規格、pacing 條件與投放流程。
*   Partners Phase 3.3 另要求 FlashDrive 320/300 可由網站主申請、PD 審核、取得嵌入碼並進入收益/請款；ODM 中 FD 320/300 活動需能選到核准或人工開放的 Partners 媒體。
*   Partners 端 FD 預設 vCPM 為 40；若 PD/OSS 手動設定過價格，收益計算應以手動值為準。
*   若 FlashDrive 有待 PM 確認規則，測試案例需標註為待確認，不可當作已定義驗收標準。

### 2. Preview 與正式環境廣告投放
*   Preview 環境與正式投放環境需驗證使用不同資料來源或投放路徑。
*   Preview 不應污染正式投放資料；正式投放不可使用僅供 Preview 的暫存設定。
*   測試需涵蓋格式預覽、素材預覽、送出後正式投放與失敗回退。

### 3. 聯絡我們表單
*   聯絡我們表單需驗證抽屜開啟、必填、字數限制、送出成功/失敗、權限與追蹤資料。
*   CCT 文件引用聯絡我們的字數限制 UI，因此測試 CCT 抽屜時可沿用同類 UI 驗證規則。

---

## 十一、QA 產生測試案例時的硬性檢查清單

*   每個 SuperDSP 測試任務必須先確認規格來源是否在 `SYSTEM_MAP.md` 已索引。
*   只要涉及 Ad Group，必須檢查權限、狀態、版位格式、素材包、受眾、追蹤碼、第三方量測、報表至少其中相關的連動。
*   只要涉及 Commerce AD，必須檢查 SuperDSP、OYM、ERP/OSS、Studio、報表/帳務的跨系統一致性。
*   只要涉及受眾，必須檢查 include/exclude、UU、排程、linked ad groups、權限與無資料狀態。
*   只要涉及素材，必須檢查 Studio 回填、ODM 審核、素材包格式、第三方素材包與版位格式匹配。
*   只要涉及第三方量測或 CCT，必須檢查角色權限、表單限制、Ad Group 綁定、payload、投放 sequence 與報表可見性。
*   產出 CSV 測試案例時，操作步驟與期望結果需明確寫出「跨系統狀態一致」與「負向權限/格式阻擋」。
