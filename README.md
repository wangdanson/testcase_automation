# Testcase Automation

本專案旨在透過 **Gemini CLI** 實現廣告系統（SuperDSP, OYM, ERP/OSS）測試案例的自動化產出。透過專案憲法 **GEMINI.md** 與 **Self-Evolution Workflow**，能將資深測試與 UI/UX 工程師的思維邏輯轉化為精確、可驗證且具備「自我進化」能力的測試案例。

---

## 📋 專案概覽 (Project Overview)

*   **核心目標**: 將規格文件（PDF/圖片/HTML）自動轉化為結構化的 CSV 測試案例。
*   **雲端同步**: 支援一鍵從 Confluence 同步最新規格書及其圖片附件，並維持目錄階層。
*   **自我進化**: 具備「指正即學習」機制，能自動記錄錯誤教訓並在下次產出前執行「零觸發」預檢。
*   **自動化流程**: 產出測試案例後，自動通過「功能-角色矩陣」驗證並同步至 Google Sheets。

## 📁 目錄結構 (Directory Structure)

```text
/
├── GEMINI.md                # [核心] 專案憲法：定義全域回覆、自動化學習與產出預檢流程
├── GEMINI_ERROR_LOG.md      # [進化] 歷史錯誤日誌：紀錄邏輯錯誤、格式教訓與功能回歸防護
├── README.md                # 專案說明文件與快速上手指南
├── requirements.txt         # Python 環境相依套件清單
├── package.json             # 專案配置文件
├── upload_to_sheets.py      # 自動化腳本：將產出的 CSV 上傳至 Google Sheets
├── validate_csv.py          # [守門員] 業務驗證腳本：檢查格式、標籤與「全角色隔離」矩陣
├── sync_from_sheets.py      # 反向同步腳本：將雲端變更同步回本地 CSV
├── sync_from_confluence.py  # 雲端同步腳本：從 Confluence 搜尋並抓取層級化規格文件
├── confluence_state.json    # [本地] 紀錄 Confluence 頁面版本號，用於增量同步 (已忽略)
├── .env.example             # 環境變數設定範例
├── knology_management/      # [紀錄] 存放專案技術決策、優化策略與績效評估 (已忽略)
├── service_account/         # [資安] 存放 Google 服務帳號憑證
├── source_files/            # 原始規格文件儲存區 (依 Confluence 階層自動還原)
│   ├── [SuperDSP]/
│   │   ├── [SuperDSP 平台化]/
│   │   │   └── [IAS Pre-bid]/
│   │   │       ├── IAS Pre-bid.html
│   │   │       └── screenshot_48abecac.png
│   │   └── SuperDSP 從IO到Sequence/
│   └── SuperDSP 大數據API/
├── generated_test_cases/    # 產出的測試案例儲存區 (依來源專案分類)
└── .gemini/                 # Gemini CLI 配置資料夾
    ├── commands/            # 自定義 Speckit 系列指令
    └── skills/              # 核心專家技能 (test-case-automation-expert)
```

---

## 🚀 快速上手 (Quick Start)

### 0. 複製專案 (Clone Project)
```bash
git clone https://github.com/wangdanson/testcase_automation.git
cd testcase_automation
```

### 1. 安裝環境 (Environment Setup)
執行一鍵安裝指令：
```bash
npm run setup
```

### 2. 安全性設置 (Security Setup)

#### A. Google Sheets API (用於測試案例同步)
請參閱 `credentials_stepsImg/` 資料夾下的截圖教學，獲取服務帳號金鑰並存放於 `service_account/google_credentials.json`。

#### B. Atlassian API Token (用於 Jira 與 Confluence)
1.  前往 [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) 建立一個名為 `Testcase-Automation` 的 Token。
2.  複製該 Token。

#### C. 設定環境變數
1.  將 `.env.example` 複製為 `.env`。
2.  填入 `SPREADSHEET_ID` 與 `CONFLUENCE_PARENT_ID`。
3.  **API Token 共用**: `JIRA_API_TOKEN` 與 `CONFLUENCE_API_TOKEN` 可填入同一個值。

---

### ☁️ 3. 雲端規格同步 (Confluence Sync)

本功能可自動將雲端規格書下載至本地，方便 AI 進行深度讀取。

**執行指令：**
```bash
python3 sync_from_confluence.py
```

**功能特色：**
*   **全深度搜尋**：採用 CQL 技術，一鍵抓取 Parent ID 下的所有子孫頁面，自動克服 API 斷鏈問題。
*   **階層還原**：自動還原雲端的資料夾樹狀結構於 `source_files/` 下。
*   **增量下載**：自動比對頁面版本，僅下載有變動的內容與圖片。
*   **圖文一致性**：自動下載圖片附件並附加 **MD5 Hash** 確保唯一性，同時修正 HTML 內部連結，支援離線閱讀。

---

### 🤖 4. 自動化產生測試案例 (Workflow)

啟動 Gemini CLI：
```bash
gemini
```

**範例指令：**
> 「幫我產生 [source_files 下的資料夾路徑] 的 test case」

**產出標準 (七位一體框架)：**
1.  **功能地圖掃描**：產出前主動報備識別出的功能點。
2.  **二元回歸過濾**：僅針對具備邏輯聯動的舊功能產出回歸案例。
3.  **矩陣隔離校驗**：每個特權功能必須配齊 Agency, Client, Media 的反向隔離。
4.  **自動上傳驗證**：產出後自動執行 `validate_csv.py` 並上傳至 Sheets。

---

### 🔄 5. 反向同步 (Reverse Sync)

若在 **Google Sheets** 修改了內容，請下令：
> 「同步刚刚產出的 test case」 或 「Sync [專案名稱]」

---

## ⚙️ 產出規範 (Production Standards)

| 規則項目 | 說明 | 強制性 |
| :--- | :--- | :---: |
| **矩陣隔離** | 特權功能必須具備 Agency/Client/Media 三方反向隔離案例 | **Critical** |
| **全欄位包裹** | 所有欄位必須使用 **雙引號 (")** 包裹 | **Critical** |
| **實體換行** | 禁止使用 `\n`，必須使用真實換行 | **Critical** |
| **無句號結尾** | 測試項目文字結尾不加句號 `。` | **Mandatory** |

---

## 🛠 維護與貢獻
*   **專案憲法**: `GEMINI.md` 定義了核心行為規範。
*   **錯誤日誌**: 紀錄歷史教訓，實現 AI 的自我進化。

---
*Created and maintained by wangdanson.*
