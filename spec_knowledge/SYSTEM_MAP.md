# 🌐 系統規格迭代知識庫 (System Specification Iteration Map)

> **本文件用途**: 記錄 `source_files` 中已同步規格的系統邊界、迭代歷史、跨系統依賴與知識庫落點。  
> **最後盤點日期**: 2026-05-13  
> **維護原則**: `SYSTEM_MAP.md` 負責「來源覆蓋與系統關係」；各系統的測試規則沉澱在對應知識文件，例如 `SuperDSP_RULES.md`、`ODM_REPORT_TRACKING.md`、`PARTNERS_RULES.md`。

---

## 一、系統地圖 (System Overview)

| 系統 | 核心職責 | 關鍵關聯系統 | 主要知識文件 |
| :--- | :--- | :--- | :--- |
| **SuperDSP** | DSP 投放平台、Campaign / Ad Group、受眾定向、素材與第三方量測、Commerce AD / RTB | ODM, Studio, ERP/OSS, OYM, 外部媒體平台 | `SuperDSP_RULES.md` |
| **ODM** | 廣告管理、活動追蹤、素材審核、投放與成效報表、委刊單與追蹤碼 | SuperDSP, 外部媒體平台, ERP/OSS | `ODM_REPORT_TRACKING.md` |
| **Partners** | 網站主註冊、網站/廣告格式申請、嵌入碼、收益報表、請款與付款帳戶 | ODM, ERP/OSS, SuperDSP, OYM | `PARTNERS_RULES.md` |
| **Studio** | 動態素材與素材包製作、素材預覽、素材包回填 | SuperDSP, ODM | `SuperDSP_RULES.md` |
| **ERP/OSS** | 合約、帳務、媒體底價、月結報表、CCT code 管理、Partners 審核與請款 | SuperDSP, OYM, ODM, Partners | `SYSTEM_MAP.md`, `PARTNERS_RULES.md` |
| **OYM** | 媒體端設定、RTB 底價、媒體資料維護 | ERP/OSS, SuperDSP, Partners | `SYSTEM_MAP.md` |
| **外部媒體平台** | Google Ads / Meta / TikTok CCT code 與第三方投放資料 | ODM, SuperDSP, ERP/OSS | `ODM_REPORT_TRACKING.md`, `SuperDSP_RULES.md` |

---

## 二、SuperDSP 規格覆蓋索引

| 規格群組 | 來源路徑 | 覆蓋模組 | 規則落點 |
| :--- | :--- | :--- | :--- |
| SuperDSP 平台化總目錄 | `source_files/[SuperDSP 平台化]` | Phase 1.3.x、1.4.x、Commerce AD Phase 1-3 | `SuperDSP_RULES.md` |
| 權限管理 | `source_files/SuperDSP 權限整理` | Admin、Agency、Advertiser、Media、Read-only、Brand client | `SuperDSP_RULES.md` |
| IO 到 Sequence | `source_files/SuperDSP 從IO到Sequence` | Campaign、Ad Group、Sequence、狀態轉換 | `SuperDSP_RULES.md` |
| AOE Pilot Phase 1 | `source_files/SuperDSP Pilot for AOE (Phase 1)` | AOE 操作流程、前後端規格、Pilot 驗收 | `SuperDSP_RULES.md` |
| AOE Pilot Phase 2 | `source_files/SuperDSP Pilot for AOE (Phase 2)` | AOE 進階投放、權限、版位素材連動 | `SuperDSP_RULES.md` |
| Partners Commerce Ad | `source_files/[Partners][SuperDSP 平台化 Phase 1.5.0] Commerce Ad` | Partners 帳號、Commerce Ad 入口、NativeDrive/Commerce Ad 合約與 UI 權限 | `SuperDSP_RULES.md`, `PARTNERS_RULES.md` |
| Commerce AD Phase 1 | `source_files/[SuperDSP 平台化]/[Commerce AD Phase 1] Commerce AD & RTB` | Commerce AD 建立、RTB、CPC、Margin、Sequence | `SuperDSP_RULES.md` |
| Commerce AD Phase 2 | `source_files/[SuperDSP 平台化]/[Commerce AD Phase 2] Commerce AD 帳務管理 及 受眾洞察報告下載` | 帳務管理、受眾洞察報告、月報欄位 | `SuperDSP_RULES.md` |
| Commerce AD Phase 3 | `source_files/[SuperDSP 平台化]/[Commerce AD Phase 3] Commerce AD 媒體端 RTB 底價設定` | OYM/ERP 媒體底價、RTB floor price | `SuperDSP_RULES.md`, `SYSTEM_MAP.md` |
| Studio 串接 | `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.4.0] 串接 Studio 素材管理 PRD` | Studio 導流、素材包建立、回填、第三方素材包 | `SuperDSP_RULES.md` |
| IAS / 第三方量測 | `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.4.0] IAS 內文比對`, `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.4.0] 第三方量測設定` | IAS、DoubleVerify、DCM、Nielsen、Viewability、Media 禁用 | `SuperDSP_RULES.md` |
| 受眾與數據鎖定 | `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.3.0] 受眾鎖定 + 數據報告 + 權限設定`, `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.3.1] 受眾鎖定 新增 產業Shopper Graph & Webb 零售數據` | Shopper Graph、Webb、預估量體、受眾洞察報告 | `SuperDSP_RULES.md` |
| Phase 1.3.2 功能優化 | `source_files/[SuperDSP 平台化]/[SuperDSP 平台化 Phase 1.3.2] 功能優化 admin 廣告主權限設定 & 廣告活動受眾包優化 & 廣告活動報表輸出 sheet 命名規則優化` | Admin 權限、Impression 受眾包、報表 sheet 命名 | `SuperDSP_RULES.md` |
| 追蹤碼與受眾包 | `source_files/SuperDSP 新增追蹤碼 & 受眾打包` | 追蹤碼、受眾包、UU、排程、linked ad groups | `SuperDSP_RULES.md` |
| Custom Audience | `source_files/SuperDSP Custom Audience` | 自訂受眾包、生命週期、過期判斷、前後端規格 | `SuperDSP_RULES.md` |
| CCT | `source_files/SuperDSP CCT(Cross-Channel Targeting)` | Cross Channel Pixel、角色權限、Ad Group 綁定 | `SuperDSP_RULES.md` |
| 大數據 API | `source_files/SuperDSP 大數據API` | segment/demographic/interest/product_key event API、ODM 介接 | `SuperDSP_RULES.md` |
| Campaign Potential Models | `source_files/SuperDSP 新增 活動預測潛力模型 ( Campaign Potential Models )` | 活動預測模型、segment_ids、Ad Group API 分支 | `SuperDSP_RULES.md` |
| Segment Target v2 | `source_files/segment target v2` | Include/Exclude、Retargeting、權限錯誤 | `SuperDSP_RULES.md`, `ODM_REPORT_TRACKING.md` |
| 第三方媒體平台數據打通 | `source_files/[第三方媒體平台數據打通] 產業鑽石受眾` | Google/Meta/TikTok CCT code、AOE 產業類別自動帶入追蹤碼 | `SuperDSP_RULES.md`, `ODM_REPORT_TRACKING.md` |
| FlashDrive | `source_files/快閃廣告(FlashDrive) 上架 SuperDSP Phase1` | FlashDrive 格式、素材、pacing 待確認項 | `SuperDSP_RULES.md` |
| Preview 與正式投放 | `source_files/SuperDSP格式Preview與正式環境廣告投放` | 格式預覽、正式環境投放隔離 | `SuperDSP_RULES.md` |
| 聯絡我們 | `source_files/SuperDSP 聯絡我們表單功能` | 表單抽屜、字數限制、送出流程、CCT UI 參考 | `SuperDSP_RULES.md` |

---

## 三、SuperDSP 功能迭代歷史

| 版本 / 專案 | 核心功能改動 | 主要影響 | 狀態 |
| :--- | :--- | :--- | :--- |
| Phase 1.3.0 | IAS Pre-bid、廣告實名制、受眾鎖定、數據報告、權限設定 | 安全校驗、投放設定、報表、權限 | 已索引 |
| Phase 1.3.1 | 新增產業 Shopper Graph 與 Webb 零售數據 | 受眾定向、預估量體、受眾洞察報告 | 已索引 |
| Phase 1.3.2 | Admin 廣告主權限、Impression 受眾包、報表 Sheet 命名 | 權限、受眾包、報表匯出 | 已索引 |
| Phase 1.4.0 | Studio 素材管理、IAS 內文比對、第三方量測、Viewability | 素材、第三方追蹤、投放安全 | 已索引 |
| Partners / Phase 1.5.0 | Commerce Ad 入口與 Partners 權限 | Partners、Commerce AD、素材審核 | 已索引 |
| Commerce AD Phase 1 | Commerce AD 建立、RTB、CPC、Margin、Sequence | SuperDSP、OYM、Studio、投放引擎 | 已索引 |
| Commerce AD Phase 2 | 帳務管理與受眾洞察報告下載 | SuperDSP、ERP/OSS、報表 | 已索引 |
| Commerce AD Phase 3 | 媒體端 RTB 底價設定 | OYM、ERP/OSS、SuperDSP RTB | 已索引 |
| AOE Pilot Phase 1 | AOE Pilot 前後端流程 | AOE 操作、廣告設定、素材 | 已索引 |
| AOE Pilot Phase 2 | AOE Pilot 進階流程與版位素材連動 | 權限、狀態、版位、素材包 | 已索引 |
| CCT | Cross Channel Pixel | Pixel 管理、Ad Group 綁定、角色權限 | 已索引 |
| Custom Audience | 自訂受眾包 | 受眾包生命週期、過期判斷、排程 | 已索引 |
| Campaign Potential Models | 活動預測潛力模型 | 大數據 API、Ad Group segment_ids | 已索引 |
| FlashDrive | 快閃廣告上架 SuperDSP | 特殊格式、素材、pacing | 已索引 |
| Preview | 格式 Preview 與正式環境廣告投放 | 預覽隔離、正式投放 | 已索引 |
| Contact Form | 聯絡我們表單 | 抽屜表單、送出、字數限制 | 已索引 |

---

## 四、ODM 規格覆蓋索引

| 規格群組 | 來源路徑 | 覆蓋模組 | 規則落點 |
| :--- | :--- | :--- | :--- |
| ODM 使用手冊 | `user_manual/ODM/ODM_USER_MANUAL.md` | 操作入口、角色、活動、報表、素材、委刊單 | `ODM_REPORT_TRACKING.md` |
| ODM 報表 API 分析 | `source_files/[ODM] 報表API分析` | 報表生成、廣告成效、受眾報告 API、AII 注意力指標 | `ODM_REPORT_TRACKING.md` |
| ODM AII 報表 | `source_files/[ODM] 報表API分析/[ODM] AII(Attention Impact Index)注意力衝擊指標 報表 API分析` | AII 公式、注意力事件、標準格式 ID 137、API Gateway 查詢 | `ODM_REPORT_TRACKING.md` |
| ODM CTV HHID 報表 | `source_files/[ODM] CTV 投放成效報告 調整，基於 Household ID (HHID)` | Household ID、Unique HHID、CTV 家戶歸因、受眾報告分攤 | `ODM_REPORT_TRACKING.md` |
| ODM 活動追蹤 | `source_files/[ODM] 活動追蹤` | AOE 工作追蹤、Cue、執行項目 | `ODM_REPORT_TRACKING.md` |
| ODM 第三方追蹤碼 | `source_files/ODM 第三方追蹤碼勾選_需求文件`, `source_files/[ODM] 第三方追蹤碼-批次雙向設定` | 追蹤碼勾選、批次雙向設定 | `ODM_REPORT_TRACKING.md` |
| ODM 批次更新 | `source_files/[ODM] 批次更新走期 ＆ 媒體`, `source_files/[ODM] 批次更新走期 ＆ 媒體/API 開發規格文件 ([ODM] 批次更新)` | 走期、媒體、Pacing、頻次、IAS、逐筆失敗原因 | `ODM_REPORT_TRACKING.md` |
| ODM 頻次控制 | `source_files/[ODM] 最高觀看頻次設定調整`, `source_files/[ODM] 投放 id 與頻次設定調整，以達到跨裝置控制頻次` | Campaign Level 頻次、Placement Level 頻次、跨裝置頻次 | `ODM_REPORT_TRACKING.md` |
| ODM Video 流量管控 | `source_files/ODM Video 上傳 Bitrate 卡控 & m3u8 切片導入 (流量管控)` | Bitrate / fps / audio bitrate 卡控、m3u8 切片、影片資訊 | `ODM_REPORT_TRACKING.md` |
| TextDrive 倒數計時 | `source_files/TextDrive 新增倒數計時機制` | TextDrive 倒數計時互動機制 | `ODM_REPORT_TRACKING.md` |
| ODM SudoPlacement | `source_files/[ODM] 廣告活動投放條件建立流程簡化(SudoPlacement_)` | Placement 前後端欄位檢查、列表直接更新、投放門禁 | `ODM_REPORT_TRACKING.md` |
| 委刊單含稅總計 | `source_files/委刊單 Phase 1：新增「總計 (含稅)」` | 總計含稅、專案製作費 | `ODM_REPORT_TRACKING.md` |
| RMN 委刊單匯出 | `source_files/RMN 導入後, 委刊單匯出需求調整` | Cue 表、委刊單匯出、RMN 欄位 | `ODM_REPORT_TRACKING.md` |
| Segment Target v2 | `source_files/segment target v2` | Include/Exclude、Retargeting | `ODM_REPORT_TRACKING.md`, `SuperDSP_RULES.md` |
| 第三方媒體平台數據打通 | `source_files/[第三方媒體平台數據打通] 產業鑽石受眾` | CCT code、Campaign 追蹤碼自動生成 | `ODM_REPORT_TRACKING.md`, `SuperDSP_RULES.md` |
| 素材包與素材秒數匹配 | `source_files/Untitled folder 2025-06-13` | 素材秒數區間、Placement API / Packs API、錯誤提示與 API 失敗處理 | `ODM_REPORT_TRACKING.md` |
| SuperDSP 素材審查 | `user_manual/ODM/ODM_USER_MANUAL.md`, `source_files/SuperDSP Pilot for AOE (Phase 2)` | Reviewing / Passed / Rejected、Back to Reviewing、AOE/Partners 自動通過 | `ODM_REPORT_TRACKING.md`, `SuperDSP_RULES.md` |

---

## 五、Partners 規格覆蓋索引

| 規格群組 | 來源路徑 | 覆蓋模組 | 規則落點 |
| :--- | :--- | :--- | :--- |
| Partners Phase 1 | `source_files/OneAD Partners Phase1` | 網站主註冊、網站申請、TextDrive、基礎 API、網站/廣告格式審核 | `PARTNERS_RULES.md` |
| Partners Phase 2 | `source_files/OneAD Partners Phase2` | 收益明細、請款申請、請款紀錄、請款審核、勞務報酬單與附件下載 | `PARTNERS_RULES.md` |
| Partners Phase 3 | `source_files/OneAD Partners Phase3` | 多網站、ODM Partners 媒體群組、單一銀行帳戶、付款帳戶快照、國碼/護照/國外銀行 | `PARTNERS_RULES.md`, `ODM_REPORT_TRACKING.md` |
| Partners Phase 4 | `source_files/Partners Phase4` | 請款作業優化、銀行帳戶錯誤處理、核准後再駁回流程缺口 | `PARTNERS_RULES.md` |
| Partners 首頁與註冊防呆 | `source_files/Partners 產品首頁修改與防呆優化` | 首頁/FAQ/註冊 UI、URL 社群平台阻擋、提示 icon | `PARTNERS_RULES.md` |
| Partners 廣告格式通用規格 | `source_files/Partners 新增廣告格式需求, 前後端開發注意事項` | options API、ActiveHash、嵌入碼、預覽、price_info、格式資料完整性 | `PARTNERS_RULES.md` |
| NativeDriveGroup | `source_files/Partners 新增格式NativeDriveGroup[跨部門需求]` | `ad_format_type_id = 231`、NDG 嵌入碼、格式文字保護 | `PARTNERS_RULES.md` |
| FlashDrive / 特殊格式 | `source_files/OneAD Partners Phase3/OneAD Partners (Phase 3.3_開放投放 FlashDrive 快閃廣告)`, `source_files/Partners 媒體人工開放 特殊格式(FlashDrive_Cover_….)` | FD 320/300、人工合約、ODM 媒體選擇、vCPM、收益/請款 | `PARTNERS_RULES.md`, `ODM_REPORT_TRACKING.md` |
| Commerce Ad in Partners | `source_files/[Partners][SuperDSP 平台化 Phase 1.5.0] Commerce Ad` | 上線通知、NativeDrive/Commerce Ad 預覽、合約補建與新建 | `PARTNERS_RULES.md`, `SuperDSP_RULES.md` |
| Partners 前後端優化 | `source_files/Partners 前後端優化調整20241007[跨部門需求]` | 請款送出日為假日仍可帶入發票日期欄位 | `PARTNERS_RULES.md` |

---

## 六、Partners 功能迭代歷史

| 版本 / 專案 | 核心功能改動 | 主要影響 | 狀態 |
| :--- | :--- | :--- | :--- |
| Phase 1 | 網站主註冊、網站審核、TextDrive 廣告格式、基礎 API | Partners、OSS/ERP、OYM 報表 | 已索引 |
| Phase 2 | 收益明細、請款申請、請款紀錄、ERP 請款審核 | Partners、ERP/OSS、財務 | 已索引 |
| Phase 3 | 多網站、單一銀行帳戶、ODM Partners 媒體群組 | Partners、ODM、OSS | 已索引 |
| Phase 3.1 | 註冊頁聯絡入口與電子報 | Partners UI、GTM | 已索引 |
| Phase 3.2 | 駁回原因、國碼手機、國籍/護照、國外銀行 | Partners、OSS、通知信 | 已索引 |
| Phase 3.3 | FlashDrive 開放投放 | Partners、OSS、ODM、收益報表 | 已索引 |
| Phase 4 | 請款作業與錯誤銀行帳戶處理 | Partners、ERP/OSS、財務 | 已索引；部分流程待確認 |
| 2024 前後端優化 | 請款假日發票日期處理 | Partners 請款 | 已索引 |
| NativeDriveGroup | 新增 NDG 格式 | Partners 廣告格式與嵌入碼 | 已索引 |
| Commerce Ad | Partners 端同步 Commerce Ad | Partners、SuperDSP、合約 | 已索引 |
| 首頁防呆優化 | 網域社群平台阻擋與 UI 提示 | Partners 註冊/首頁 | 已索引 |

---

## 七、ODM 功能主題與測試切面

| 主題 | ODM 知識庫已沉澱重點 | 需要串接的系統 |
| :--- | :--- | :--- |
| 角色與權限 | ERP 權限同步、CIS 成員門禁、SuperDSP 審查管理員門禁、`動作:資源` 權限模型 | ERP/OSS, SuperDSP |
| 報表與數據指標 | AII、HHID、活動成效、投放報表、DSP 報表、受眾報告、Excel UTF-8 與 sheet 命名 | SuperDSP, OneDATA |
| SuperDSP 報表差異 | `source = superdsp` 時使用 `calculate_superdsp_by_stat`，需保留 SuperDSP 專屬欄位與排序 | SuperDSP |
| 追蹤碼與活動追蹤 | Campaign 自動帶碼、OSS 追蹤碼管理、Cue/委刊單觸發活動追蹤、灰階與封存邏輯 | OSS, SuperDSP, 外部媒體平台 |
| 第三方追蹤碼批次設定 | Campaign 層與 Placement 層雙向同步，CIS 操作與列表篩選 | ODM |
| 委刊單與 RMN | 含稅總計、專案製作費、RMN 接單公司、LOGO/Header/Email/媒體格式連結 | ERP/OSS |
| 批次更新與頻次 | 走期、媒體、裝置比例、逐筆失敗原因、跨裝置頻次、Campaign/Placement level 從嚴認定 | ODM |
| 影音與素材卡控 | Video bitrate、m3u8 切片、KBRO CTV fps、TextDrive 倒數計時、素材秒數匹配 | ODM, Studio |
| Placement 資料驗證 | SudoPlacement、列表直接更新、投放狀態門禁、Retargeting Segment Target v2 | ODM, SuperDSP |
| SuperDSP 素材審查 | Reviewing/Passed/Rejected 狀態、Back to Reviewing、AOE/Partners 免審核與狀態一致 | SuperDSP, Studio |

---

## 八、Partners 功能主題與測試切面

| 主題 | Partners 知識庫已沉澱重點 | 需要串接的系統 |
| :--- | :--- | :--- |
| 註冊與網站審核 | 網站資料、JS 嵌入限制、社群平台 URL 阻擋、駁回原因、審核通知 | OSS/ERP |
| 多網站 | `media_id/media_name`、網站 filter、報表與請款明細隔離 | ODM, OSS |
| 廣告格式 | TextDrive、FlashDrive、NativeDriveGroup、Commerce Ad、options API、重複申請防呆、嵌入碼 | OSS, ODM, SuperDSP |
| 收益報表 | 月收益、特殊格式收益、人工開放格式、vCPM 與計價單位 | OSS, ODM, OYM |
| 請款與附件 | 請款下限、請款狀態、勞務報酬單、發票日期、採購單、銀行存摺影本 | ERP/OSS, 財務 |
| 付款帳戶 | 單一銀行帳戶、請款當下快照、國外銀行、護照、人工調整流程 | ERP/OSS |
| ODM 媒體群組 | Partners 類型媒體集中、展開收合、全選/全不選、FD/特殊格式可選媒體 | ODM |
| Commerce Ad | 上線彈窗、NativeDrive/Commerce Ad 預覽、既有與新用戶合約建立 | SuperDSP, OSS |

---

## 九、跨系統關係與測試切面

### 1. SuperDSP ↔ Studio
*   SuperDSP 從 IO / Ad Group 流程導流 Studio 建立素材包。
*   Studio 回填素材包後，SuperDSP 需保存 material pack 與格式匹配資料。
*   取消、失敗、回填逾時、格式不符都需測試。

### 2. SuperDSP ↔ ODM
*   SuperDSP 素材與投放資料會影響 ODM 素材審核、活動追蹤與報表。
*   Partners/AOE 特殊來源可能觸發素材免審核或自動通過。
*   受眾、追蹤碼、CCT code、委刊單匯出與報表資料需要跨系統一致。
*   SuperDSP 報表進入 ODM 時需使用專屬計算邏輯，不可套用一般 ODM 報表公式。
*   SuperDSP 素材審查狀態需與 ODM Reviewing / Passed / Rejected 頁籤一致。

### 3. SuperDSP ↔ ERP/OSS ↔ OYM
*   Commerce AD RTB 需串接 OYM 媒體底價與 ERP/OSS 合約/帳務。
*   月結報表需區分交易模式，例如 RTB 競價與固定價格。
*   底價、CPC、Margin、實際競標價、累計金額與平均 CPC 需在三端一致。

### 4. ODM / SuperDSP ↔ 外部媒體平台
*   Google Ads、Meta、TikTok 的 CCT code 需依平台與產業分類獨立管理。
*   建立 Campaign 時可能根據 AOE 選擇的產業主次類別自動帶入追蹤碼。
*   CSV/XLSX 匯入、重複 code、平台欄位錯誤與無對應分類都需測試。

### 5. ODM ↔ ERP/OSS
*   ODM 登入權限、角色與部分營運門禁來自 ERP/OSS，測試角色異動時需驗證同步結果。
*   RMN 委刊單匯出需依接單公司、媒體格式連結與合約資料輸出不同 Header、Email、檔名與備註。
*   OSS 追蹤碼管理與 ODM Campaign 自動帶碼需保持平台、產業分類、事件名稱一致。

### 6. ODM ↔ OneDATA / 報表資料源
*   AII、HHID、受眾標籤、DSP 報表與活動成效指標需明確標示資料來源與更新週期。
*   CTV 報表以 HHID 聚合，不可用一般 Unique User 驗證。
*   報表測試需分開驗證 UI 顯示、API 計算、Excel 匯出與無資料狀態。

### 7. Partners ↔ OSS/ERP
*   Partners 網站審核、廣告格式審核、請款審核、銀行存摺影本與採購單下載都需透過 OSS/ERP 流程驗證。
*   請款資料的單號、金額、發票日期、付款帳戶、狀態與 note 需在 Partners、OSS/ERP 與財務流程一致。
*   駁回網站、駁回廣告格式、駁回請款都需保留原因並寄送通知，不可只改狀態。

### 8. Partners ↔ ODM
*   Partners 網站審核通過後，ODM 媒體選單需將 Partners 媒體集中到可展開/收合的 Partners 群組。
*   Partners FlashDrive / 特殊格式合約需影響 ODM 媒體可選性；FD 320/300 格式活動需能選到已核准或人工開放的 Partners 媒體。
*   多網站資料需在 ODM 端以正確 media id 區分，避免不同網站收益或投放設定混用。

### 9. Partners ↔ SuperDSP / Commerce AD
*   SuperDSP Commerce Ad 上線時，Partners 需同步顯示上線通知、NativeDrive/Commerce Ad 預覽與合約建立邏輯。
*   已申請 NativeDrive 與未申請 NativeDrive 的網站主需分別驗證既有合約補建與新申請雙合約建立。
*   Commerce Ad 的 RTB、底價、帳務主規則仍屬 SuperDSP/OYM/ERP；Partners 端測試聚焦網站主入口、合約與嵌入碼可用性。

---

## 十、規格分析狀態判定

| 判定項目 | 目前狀態 | 說明 |
| :--- | :--- | :--- |
| SuperDSP 來源資料夾 | 已完成知識庫層級索引 | 目前偵測到的 SuperDSP 相關資料夾已列入本文件與 `SuperDSP_RULES.md` |
| SuperDSP 測試規則 | 已完成核心規則沉澱 | 已按權限、Campaign、素材、受眾、追蹤碼、Commerce AD、報表、特殊產品整理 |
| ODM 來源資料夾 | 已完成知識庫層級索引 | `ODM_REPORT_TRACKING.md` 可用主題已整合為本文件的 ODM 覆蓋索引與測試切面 |
| ODM 測試規則 | 已完成核心規則沉澱 | 已按權限、報表、追蹤碼、委刊單、批次更新、頻次、影音、資料驗證、素材審查整理 |
| Partners 來源資料夾 | 已完成知識庫層級索引 | 19 份 Partners HTML 文件已列入本文件與 `PARTNERS_RULES.md` |
| Partners 測試規則 | 已完成核心規則沉澱 | 已按註冊、網站審核、多網站、廣告格式、收益、請款、銀行帳戶、跨系統連動整理 |
| 逐字全文轉錄 | 不採用 | 知識庫目標是 QA 可用規則與來源索引，不是替代原始規格全文 |
| 後續新增 source_files | 待增量同步 | 新同步的 Confluence 來源需再更新本地圖與對應規則文件 |

---

## 十一、維護規範

*   新增或同步 Confluence 規格後，先更新本文件的來源索引，再更新對應系統的規則文件。
*   若資料夾名稱未包含系統名，但內容涉及 SuperDSP/ODM/ERP/OYM/Studio，仍需依實際內容歸檔，不得只依資料夾名稱判斷。
*   產出測試案例前，必須先從本文件確認受影響系統，再讀對應規則文件。
*   若規格仍有待 PM 確認內容，測試案例需標註為待確認，不可視為已定義驗收標準。
*   跨系統專案至少要覆蓋建立、更新、狀態轉換、報表/匯出、權限負向與資料一致性六個切面。
