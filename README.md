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
├── LICENSE                  # 專案授權條款
├── upload_to_sheets.py      # 自動化腳本：將產出的 CSV 上傳至 Google Sheets
├── validate_csv.py          # [守門員] 業務驗證腳本：檢查格式、標籤與「全角色隔離」矩陣
├── sync_from_sheets.py      # 反向同步腳本：將雲端變更同步回本地 CSV
├── sync_from_confluence.py  # 雲端同步腳本：從 Confluence 搜尋並抓取層級化規格文件
├── confluence_state.json    # [本地] 紀錄 Confluence 頁面版本號，用於增量同步 (已忽略)
├── .env.example             # 環境變數設定範例
├── knology_management/      # [紀錄] 存放專案技術決策、優化策略 (已忽略)
├── archive/                 # [封存] 存放舊版 SOP 或過時文件
├── credentials_stepsImg/    # [教學] 存放 README 使用的設置步驟截圖
├── user_manual/             # [手冊] 存放系統使用說明書 (如 ODM)
├── service_account/         # [資安] 存放 Google 服務帳號憑證
├── source_files/            # 原始規格文件儲存區 (依 Confluence 階層自動還原)
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
根據 Google Drive API 標準設定流程，請執行以下步驟：

1.  **建立新專案**: 登入 [Google Cloud Console](https://console.cloud.google.com/)，點選「選取專案」並選擇「新增專案」，為專案命名後點擊「建立」。
2.  **啟用 Google Drive API**: 在左側選單點擊「API 和服務」>「啟用 API 和服務」。搜尋「**Google Drive API**」並將其啟用。
    ![啟用 Google Drive API](credentials_stepsImg/credentials_step0.png)
3.  **前往憑證頁面**: 在左側選單選擇「API 和服務」>「憑證」。
    ![前往憑證頁面](credentials_stepsImg/credentials_step1.png)
4.  **授予服務帳號權限**: 到 google sheet 表單中，將產出的電子郵件帳號加入共用名單，並設定為「編輯者」。
    ![授予服務帳號權限](credentials_stepsImg/credentials_step2.png)
5.  **產生並下載 JSON 金鑰**: 
    *   在服務帳戶列表中點擊該帳戶的 Email。
    *   切換至「**金鑰 (Keys)**」頁籤。
        ![切換至金鑰頁籤](credentials_stepsImg/credentials_step3.png)
    *   點擊「新增金鑰」>「建立新的金鑰」> 選擇「**JSON**」並建立。
        ![建立新的金鑰](credentials_stepsImg/credentials_step4.png)
    *   系統會自動下載 JSON 檔案，請將其重新命名為 `google_credentials.json` 並放入 `service_account/` 資料夾。
6.  **啟用 Google Sheets API**: 在左側選單點擊「API 和服務」>「啟用 API 和服務」。搜尋「**Google Sheets API**」並將其啟用。
    ![啟用 Google Sheets API](credentials_stepsImg/credentials_step5.png)

#### B. Atlassian API Token (用於 Jira 與 Confluence)
1.  前往 [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) 建立一個名為 `Testcase-Automation` 的 Token。
2.  複製該 Token。

#### C. 設定環境變數
1.  將 `.env.example` 複製為 `.env`。
2.  填入您的 `SPREADSHEET_ID` 與 `CONFLUENCE_PARENT_ID`。
3.  **API Token 共用**: `JIRA_API_TOKEN` 與 `CONFLUENCE_API_TOKEN` 可填入同一個值。

---

## ☁️ 3. 雲端規格同步 (Confluence Sync)

本功能可自動將雲端規格書下載至本地，方便 AI 進行深度讀取。透過 `sync_from_confluence.py` 腳本，能精準還原雲端目錄結構並處理圖文一致性。

### A. 環境設定 (Environment Setup)
請在 `.env` 檔案中設定以下變數：
*   `CONFLUENCE_URL`: 您的 Confluence 基礎網址 (例如 `https://example.atlassian.net/wiki/`)。
*   `CONFLUENCE_EMAIL`: 登入 Confluence 的電子郵件。
*   `CONFLUENCE_API_TOKEN`: Atlassian API Token (參閱 [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens))。
*   `CONFLUENCE_PARENT_ID`: 目標規格目錄的 Parent ID (支援多個，以逗號分隔)。

### B. 執行與運作邏輯
**執行指令：**
```bash
python3 sync_from_confluence.py
```

**功能特色：**
*   **全深度搜尋**：採用 CQL 技術，一鍵抓取 Parent ID 下的所有子孫頁面，自動克服 API 斷鏈問題。
*   **階層還原**：自動解析 ancestors 數據鏈，並於 `source_files/` 下還原雲端的嵌套目錄結構。
*   **增量下載**：自動比對頁面版本號，僅針對有變動的內容進行更新。
*   **圖文一致性**：自動下載圖片附件，並修正 HTML 內部連結，支援完全離線讀取。
*   **自動化穩定性**：實作工業級重試機制與超時控制，並透過 MD5 映射處理超長檔名問題。

---

## 🤖 4. 自動化產生測試案例 (Workflow)

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

## 🔄 5. 反向同步 (Reverse Sync)

若您在 **Google Sheets** 上直接修改了內容，請對 Gemini CLI 下令：
> 「同步刚刚產出的 test case」 或 「Sync [專案名稱]」

手動執行指令：
```bash
python3 sync_from_sheets.py "generated_test_cases/[專案路徑]/[檔名].csv"
```

---

## 🛡️ 自動記錄錯誤 (Automatic Error Recording)

1.  **指正即學習 (Self-Learning)**: 當使用者指出錯誤時，Gemini 將自動分析並增補至 `GEMINI_ERROR_LOG.md`。
2.  **產出前預檢 (Pre-output Validation)**: 執行任何產出前，Gemini 必須強制讀取 Error Log 進行校驗。

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
