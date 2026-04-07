# Gemini CLI 錯誤學習紀錄 (Error Log)

> **自動化守門員狀態**: ✅ **Active** (`validate_csv.py`)
> 此檔案紀錄歷史錯誤與修正邏輯，用於產出前的自我預檢 (Self-Correction)。

## 1. 🛑 [Critical] 系統邏輯與權限 (Logic & Permissions)

| 模組 | 規則描述 | 避坑指南 | 來源/案例 |
|---|---|---|---|
| **Identity** | **AOE 身分對等原則** | **Agency ID 571 專屬於 AOE 使用**。產出案例時應統一角色認知，所有歸屬於 ID 571 的操作即代表 AOE 權限行為。 | User Correction |
| **Style** | **嚴禁技術標籤外流** | **絕對禁止**在 CSV 的「測試功能」或「測試情境」中出現 `[七位一體]`、`原子化`、`整合式`、`Hybrid` 等 QA 技術標記。僅允許 `SKILL.md` 定義之全形標籤（如 `【正向】`）。 | **Repeated Error (Fixing)** |
| **Budget** | **超跑顯示與預算回收** | 1. 移除花費上限限制。2. `ABORTED` 狀態必須釋放剩餘預算。 | Pilot Phase 1 |
| **Identity** | **果實夥伴 (ID 571) 特權** | 1. 素材免審核。2. 產業類別必填且可見。3. 進階設定權限。 | Pilot Phase 2 |

## 2. ⚠️ [Major] 資料整合與 UI 連動

| 模組 | 規則描述 | 避坑指南 | 來源/案例 |
|---|---|---|---|
| **Logic** | **權限正負向分離原則** | 權限測試**必須拆分**為獨立的正向（開啟）與反向（屏蔽）案例，嚴禁寫在同一列。 | User Correction |
| **Style** | **文字純淨化** | 情境描述應改用「驗證...機制」、「檢查...完整性」，嚴禁使用「作為使用者...」模板。 | User Correction |
| **Strategy** | **雙標籤強制規範** | **必須**使用兩類標籤組成，格式為 `【分類】【性質】功能名稱`（如 `【權限】【正向】`），嚴禁只使用單一標籤。 | User Correction (Pilot Phase 2) |
| **Strategy** | **過濾瑣碎技術邏輯** | **禁止**將純技術欄位名稱映射（如 MIB -> MIC）列為測試項目。應專注於業務價值與 UI 變更之測試。 | User Correction (Pilot Phase 2) |
| **Identity** | **ODM 審核查核角色** | 驗證 ODM 列表中 AOE 素材過濾之行為，測試角色應使用 **Onead User (AOE Admin)**，而非 PAD。 | User Correction (Pilot Phase 2) |
| **L10n** | **繁中語系標籤修正** | 確保姓氏在前、名字在後，對應 `lastName` 與 `firstName`。 | Pilot Phase 1 |

## 3. 🎨 [Style] 格式與排版
*   **全欄位包裹雙引號 (")**：✅ 強制執行。
*   **實體換行**：✅ 禁止使用 `\n`。
*   **行末不加句號**：✅ 嚴格移除所有欄位結尾的句號。
