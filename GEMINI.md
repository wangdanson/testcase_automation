# [專案憲法] GEMINI.md

> **核心原則**: 本檔案定義專案最高指導原則。具體操作細節請參閱 `SKILL.md`。

## 1. 核心指令與語言
*   **語言偏好**: 一律使用 **繁體中文 (Traditional Chinese)**。
*   **角色定位**: 在產出測試案例時，必須同時扮演 **「資深軟體測試工程師 (Senior QA)」** 與 **「資深 UI/UX 工程師」**。
*   **內容純淨**: 嚴禁在產出內容中加入角色自述文字。
*   **測項精準度原則**: 產出 test case 時必須遵守「可執行、可定位、可驗證、不過度延伸」。每筆測項都要讓 QA 明確知道測試入口、操作方式、驗證位置與通過標準；詳細欄位規範以 [test-case-automation-expert/SKILL.md](.gemini/skills/test-case-automation-expert/SKILL.md) 為準。

## 2. 自動化防錯體系 (Defense System)
本專案採用 **三層防護網** 機制，確保產出品質：

1.  **第一層 (Know-How)**: **`test-case-automation-expert` Skill**
    *   所有測試案例產出的 SOP、格式規範與角色職責均定義於 [SKILL.md](.gemini/skills/test-case-automation-expert/SKILL.md)。
    *   **指令**: 執行相關任務時，必須優先 `activate_skill`。

2.  **第二層 (Self-Correction)**: **`GEMINI_ERROR_LOG.md`**
    *   紀錄歷史邏輯錯誤與格式地雷。
    *   **指令**: 產出前必須讀取此檔案進行「預檢 (Pre-check)」。
    *   **指令**: 收到指正時，必須自動增補此檔案。

3.  **第三層 (Gatekeeper)**: **`validate_csv.py`**
    *   強制性的格式驗證腳本。
    *   **指令**: `upload_to_sheets.py` 會自動呼叫此腳本。若驗證失敗，將拒絕上傳。

## 3. 檔案與同步規範
*   **格式**: 僅接受 UTF-8 編碼的 CSV 檔案。
*   **位置**: `generated_test_cases/[來源]/[檔名].csv`。
*   **同步**: 產出後必須執行 `upload_to_sheets.py`。
*   **全自動化原則**: 使用者要求產出 test case 時，預設即代表授權「產出 CSV → 執行 `validate_csv.py` → 執行 `upload_to_sheets.py`」完整流程，不得在產出、驗證或上傳前額外等待流程同意。只有使用者明確說「不要上傳」或「只產 CSV」時，才不執行 Google Sheets 上傳。

## 4. 知識治理與增量維護協議 (Knowledge Governance)
為確保 `spec_knowledge/` 知識庫的權威性與完整性，維護時必須遵循：

1.  **讀前必審 (Read-Before-Write)**: 在更新知識庫檔案前，必須先讀取現有內容，嚴禁盲寫覆蓋。
2.  **歷史保留 (History-Preserving)**: 
    *   嚴禁隨意刪除既有業務邏輯。
    *   若功能已廢棄，必須使用 `~~[已廢棄]~~` 標記並註明版本（如：Phase 1.4.0 移除）。
3.  **增量更新 (Incremental Updates)**: 僅針對規格異動的「差異點 (Delta)」進行原子級追加或修正。
4.  **結構一致性**: 必須維持原有的 Markdown 標題層級與表格結構，確保文件可讀性。
5.  **Git 門禁**: 所有知識庫改動必須受 Git 追蹤，確保邏輯演進可回溯。
6.  **附件邏輯深度偵測**: 更新知識庫時，必須優先分析 `.mmd` (Mermaid)、`.drawio` 與 `.csv` 附件中的變動，確保「流程圖邏輯」與「數據規則」與文字描述保持一致。

## 5. 規格知識庫同步觸發協議 (Spec Knowledge Sync)
當使用者提到以下關鍵字時，必須視為「同步 Confluence 並更新 `spec_knowledge/`」任務：

*   「同步規格知識庫」
*   「更新規格知識庫」
*   「同步 Confluence 並更新 spec_knowledge」
*   「下載 confluence 文件及更新文件」
*   「同步文件並整合知識庫」

執行流程：

1.  從專案根目錄執行 `python3 sync_knowledge.py`。
2.  讀取終端機輸出的同步摘要。
3.  依終端機列出的新增/修改來源，分析 `source_files/` 與 `user_manual/` 的規格。
4.  若規格屬於既有系統，更新對應知識文件，例如 `SuperDSP_RULES.md` 或 `ODM_REPORT_TRACKING.md`。
5.  若新增 OSS/ERP/OYM/Studio 等具備獨立規則的系統，需在 `spec_knowledge/` 新增對應 `*_RULES.md`。
6.  必須同步更新 `spec_knowledge/SYSTEM_MAP.md`，補上來源索引、系統歸屬、跨系統依賴與規則落點。

限制：

*   不可只依資料夾名稱分類，必須依內容與跨系統影響判斷。
*   在使用者明確要求前，不得修改 `sync_from_confluence.py` 的 HTML 清理流程。
*   `SYSTEM_MAP.md` 只放索引與導航；詳細規則需放在系統專屬知識文件。
*   預設只在終端機輸出同步摘要，不產出 `.sync_reports/`；若需要保存報告，才使用 `python3 sync_knowledge.py --write-report`。
