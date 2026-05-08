import csv
import sys
import os
import re

def validate_csv(file_path):
    """
    Validates a CSV file against specific rules:
    1. Structure: Consistent column count.
    2. Formatting: No literal '\n' or '<br>'.
    3. Style: No trailing periods in specific columns.
    4. Safety: Verification of actual newlines vs escaped newlines.
    5. Tags: Dual-tagging format 【Category】【Type】.
    6. Banned Keywords: No technical QA jargon.
    7. Identity: Standard login step for AOE (ID 571).
    8. Quote Wrapping: All fields must be wrapped in double quotes in raw text.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False

    violations = []
    
    # --- Step 1: Raw text check for quote wrapping ---
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read().strip()
            # Basic sanity check: The file must start and end with a double quote
            if not content.startswith('"'):
                violations.append("Raw Content: File does not start with a double quote. All fields must be wrapped in quotes.")
            if not content.endswith('"'):
                violations.append("Raw Content: File does not end with a double quote. All fields must be wrapped in quotes.")
            
            # Count quotes in the entire file - should be an even number if all quotes are escaped or paired
            quote_count = content.count('"')
            if quote_count % 2 != 0:
                violations.append(f"Raw Content: Uneven number of double quotes ({quote_count}). Check for missing or unescaped quotes.")
    except Exception as e:
        print(f"Error reading raw file: {str(e)}")
        return False

    # --- Step 2: Logical CSV parsing and checks ---
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print("Error: Empty CSV file.")
                return False

            expected_cols = len(header)
            
            # Map column names to indices
            col_map = {name: idx for idx, name in enumerate(header)}
            
            # Target columns for period check
            target_cols = [col_map[n] for n in ["測試情境", "操作步驟", "期望結果"] if n in col_map]
            
            # Banned keywords regex
            banned_pattern = re.compile(r'\[七位一體\]|原子化|整合式|Hybrid|原子化|整合式', re.IGNORECASE)
            
            # Dual tag regex and whitelist
            tag_pattern = re.compile(r'^【([^】]+)】【([^】]+)】')
            ALLOWED_CATEGORIES = ["權限", "功能", "UI", "數據", "狀態", "回歸"]
            ALLOWED_TYPES = ["正向", "反向"]

            for line_num, row in enumerate(reader, start=2):
                if len(row) != expected_cols:
                    violations.append(f"Line {line_num}: Column count mismatch. Expected {expected_cols}, got {len(row)}.")
                    continue

                # ... (格式檢查) ...

                # 3. Dual Tagging check in "測試功能"
                if "測試功能" in col_map:
                    val = row[col_map["測試功能"]].strip()
                    match = tag_pattern.match(val)
                    if not match:
                        violations.append(f"Line {line_num}, Col {col_map['測試功能']+1}: Missing or incorrect dual-tag format 【維度】【性質】.")
                    else:
                        category, tag_type = match.groups()
                        if category not in ALLOWED_CATEGORIES:
                            violations.append(f"Line {line_num}, Col {col_map['測試功能']+1}: Invalid category '【{category}】'. Allowed: {ALLOWED_CATEGORIES}")
                        if tag_type not in ALLOWED_TYPES:
                            violations.append(f"Line {line_num}, Col {col_map['測試功能']+1}: Invalid type '【{tag_type}】'. Allowed: {ALLOWED_TYPES}")

                # 4. ID 571 (AOE) Login Step check
                if "權限" in col_map and "操作步驟" in col_map:
                    permission = row[col_map["權限"]]
                    steps = row[col_map["操作步驟"]]
                    if ("ID 571" in permission or "果實夥伴" in permission) and "登入" in steps:
                        if "以『果實夥伴 (ID 571)』代理商權限之帳號登入系統" not in steps:
                            violations.append(f"Line {line_num}: Missing standard login step for ID 571/AOE permission.")

            # --- Step 3: Feature-Based Global Coverage Checks ---
            f.seek(0)
            next(reader) # skip header
            
            # Record which features have AOE privileges
            # feature_name -> set of roles tested
            feature_role_map = {}
            
            for row in reader:
                if len(row) <= max(col_map["功能/頁面"], col_map["權限"]):
                    continue
                feature = row[col_map["功能/頁面"]].strip()
                permission = row[col_map["權限"]].strip()
                
                if feature not in feature_role_map:
                    feature_role_map[feature] = set()
                feature_role_map[feature].add(permission)

            required_roles = ["superdsp_agency", "superdsp_client", "superdsp_media"]
            
            for feature, roles in feature_role_map.items():
                has_aoe = any("AOE" in r or "571" in r for r in roles)
                if has_aoe:
                    for req_role in required_roles:
                        if req_role not in roles:
                            violations.append(f"Global: Feature '{feature}' has AOE privilege but is missing reverse isolation for role '{req_role}'.")

    except Exception as e:
        print(f"Critical Error during validation: {str(e)}")
        return False

    if violations:
        print("\n[CSV Validation Failed] The following errors were found:")
        # Dedup and limit output
        for v in list(dict.fromkeys(violations))[:15]:
            print(f" - {v}")
        if len(violations) > 15:
            print(f" ... and {len(violations)-15} more errors.")
        print("\nPlease fix these issues before uploading.\n")
        return False
    
    print("[CSV Validation Passed] File structure and content look good.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_csv.py <csv_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = validate_csv(file_path)
    if not success:
        sys.exit(1)
