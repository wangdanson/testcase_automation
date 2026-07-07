import os
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from urllib.parse import urlparse, unquote
import hashlib
import time
import pandas as pd

# Load environment variables
load_dotenv()

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
CONFLUENCE_PARENT_ID = os.getenv("CONFLUENCE_PARENT_ID")
SOURCE_FILES_DIR = "source_files"
STATE_FILE = "confluence_state.json"

def get_session():
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.auth = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)
    return session

session = get_session()

def convert_excel_to_csv(file_path):
    """Convert Excel file to CSV. If multiple sheets, create multiple CSV files."""
    try:
        excel_file = pd.ExcelFile(file_path)
        base_path = os.path.splitext(file_path)[0]
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # 如果只有一個工作表，就用原檔名；否則附加上工作表名稱
            if len(excel_file.sheet_names) == 1:
                csv_path = f"{base_path}.csv"
            else:
                csv_path = f"{base_path}_{sanitize_filename(sheet_name)}.csv"
            
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"        [+] Converted Excel sheet '{sheet_name}' to: {os.path.basename(csv_path)}")
            
    except Exception as e:
        print(f"        [!] Excel conversion error for {os.path.basename(file_path)}: {str(e)}")

def search_all_descendants(parent_id):
    results = []
    url = f"{CONFLUENCE_URL}/rest/api/content/search?cql=ancestor={parent_id}+and+type=page&expand=version,body.view,ancestors&limit=100"
    
    while url:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        results.extend(data.get("results", []))
        
        next_link = data.get("_links", {}).get("next")
        if next_link:
            url = CONFLUENCE_URL + next_link if next_link.startswith("/") else next_link
        else:
            url = None
            
    return results

def get_page_by_id(page_id):
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}?expand=version,body.view,ancestors"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

def download_file(url, output_path):
    if url.startswith("/"):
        url = CONFLUENCE_URL + url
    
    response = session.get(url, stream=True, timeout=60)
    response.raise_for_status()
    
    # Safety Check: Ensure we're not downloading a login HTML page as an image
    content_type = response.headers.get('Content-Type', '')
    if 'text/html' in content_type:
        raise Exception(f"Redirected to HTML page instead of file download. Check permissions or Token.")

    # Save the file
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    # Final check: is it an empty or too small file?
    file_size = os.getsize(output_path) if hasattr(os, 'getsize') else os.path.getsize(output_path)
    if file_size < 100:
        print(f"        [!] Warning: Downloaded file is suspiciously small ({file_size} bytes)")
        return output_path

    # --- Excel 自動轉換為 CSV ---
    if output_path.lower().endswith(('.xlsx', '.xls')):
        convert_excel_to_csv(output_path)

    # --- 真假圖檔偵測 ---
    # 如果副檔名是 .png，但內容是特定文字格式，則更名
    if output_path.lower().endswith('.png'):
        try:
            with open(output_path, "rb") as f:
                header = f.read(1000).decode('utf-8', errors='ignore')
                
                # 偵測 Mermaid 語法
                mermaid_keywords = ['graph TB', 'graph TD', 'graph LR', 'flowchart TD', 'flowchart LR', 'sequenceDiagram', 'classDiagram', 'pie', 'gantt', 'stateDiagram']
                if any(keyword in header for keyword in mermaid_keywords):
                    new_path = output_path
                    if new_path.lower().endswith('.png'):
                        new_path = new_path[:-4]
                    if not new_path.lower().endswith('.mmd'):
                        new_path += '.mmd'
                    
                    if output_path != new_path:
                        if os.path.exists(new_path): os.remove(new_path)
                        os.rename(output_path, new_path)
                        print(f"        [!] Detected Mermaid diagram, renamed to: {os.path.basename(new_path)}")
                    return new_path

                # 偵測 draw.io XML
                if '<?xml' in header or '<mxfile' in header or '<mxlibrary' in header:
                    new_path = output_path
                    if new_path.lower().endswith('.png'):
                        new_path = new_path[:-4] 
                    if not new_path.lower().endswith('.drawio'):
                        new_path += '.drawio'
                    
                    if output_path != new_path:
                        if os.path.exists(new_path): os.remove(new_path)
                        os.rename(output_path, new_path)
                        print(f"        [!] Detected XML content in PNG, renamed to: {os.path.basename(new_path)}")
                    return new_path
                
                # 偵測 EML (電子郵件原始碼)
                if re.search(r'^(From:|Subject:|Date:|MIME-Version:|Return-Path:)', header, re.IGNORECASE | re.MULTILINE):
                    new_path = output_path
                    if new_path.lower().endswith('.png'):
                        new_path = new_path[:-4] 
                    if not new_path.lower().endswith('.eml'):
                        new_path += '.eml'
                        
                    if output_path != new_path:
                        if os.path.exists(new_path): os.remove(new_path)
                        os.rename(output_path, new_path)
                        print(f"        [!] Detected EML content in PNG, renamed to: {os.path.basename(new_path)}")
                    return new_path
                
                # 偵測 JSON / Swagger API 文件
                if '{"openapi":' in header or '{"swagger":' in header or '"paths": {' in header:
                    new_path = output_path
                    if new_path.lower().endswith('.png'):
                        new_path = new_path[:-4]
                    if not new_path.lower().endswith('.json'):
                        new_path += '.json'
                    
                    if output_path != new_path:
                        if os.path.exists(new_path): os.remove(new_path)
                        os.rename(output_path, new_path)
                        print(f"        [!] Detected JSON/Swagger API, renamed to: {os.path.basename(new_path)}")
                    return new_path
                    
        except Exception as e:
            print(f"        [!] Content check error: {str(e)}")
            
    return output_path

def get_attachments(page_id):
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}/child/attachment"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.json().get("results", [])

def sanitize_filename(filename, is_image=False, original_url=None):
    decoded_name = unquote(filename)
    decoded_name = re.sub(r'_[a-f0-9]{8,}(\.[a-zA-Z0-9]+)$', r'\1', decoded_name)
    clean = re.sub(r'[\\/*?:"<>|]', "_", decoded_name)
    if len(clean) > 150:
        base, ext = os.path.splitext(clean)
        suffix = f"_{hashlib.md5(original_url.encode()).hexdigest()[:8]}" if original_url else ""
        clean = base[:130] + suffix + ext
    return clean

def get_img_name_from_url(url):
    parsed = urlparse(url)
    if any(domain in parsed.netloc for domain in ["docs.google.com", "figma.com"]):
        return None
    raw_name = parsed.path.split('/')[-1]
    if raw_name.startswith('~') or '.tmp' in raw_name.lower():
        return None
    clean_name = sanitize_filename(raw_name, is_image=True, original_url=url)
    
    # 只要原本就有副檔名，就不要強行加上 .png
    # 這樣可以確保如 .sql, .py, .sh 等未定義在規則內的檔案能以原名下載
    base, ext = os.path.splitext(clean_name)
    if not ext:
        clean_name += ".png"
        
    return clean_name

def build_hierarchical_path(page, root_id):
    ancestors = page.get("ancestors", [])
    path_segments = [SOURCE_FILES_DIR]
    found_root = False
    for a in ancestors:
        if a["id"] == str(root_id):
            found_root = True
            continue 
        if found_root:
            path_segments.append(sanitize_filename(a["title"]))
    path_segments.append(sanitize_filename(page["title"]))
    return os.path.join(*path_segments)

def lean_html(soup):
    """Surgically clean HTML to reduce token usage while preserving semantic structure."""
    # 核心語意標籤
    allowed_tags = [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
        'p', 'br', 'hr',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'ul', 'ol', 'li',
        'b', 'strong', 'i', 'em', 'u',
        'a', 'img', 'code', 'pre'
    ]
    
    # 1. 徹底移除腳本、樣式與元數據
    for s in soup(['script', 'style', 'meta', 'link']):
        s.decompose()

    # 2. 移除無關測試的章節 (如專案時程, WBS)
    removal_keywords = ['專案時程', 'WBS', '工作分解結構', 'Project Schedule', '文件檢核狀態', '修訂紀錄']
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        header_text = header.get_text(strip=True)
        if any(kw in header_text for kw in removal_keywords):
            # 找到要刪除的章節起點，刪除該標題及其後續內容直到下一個標題
            curr = header
            next_node = curr.find_next_sibling()
            curr.decompose()
            while next_node and next_node.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                tmp = next_node.find_next_sibling()
                next_node.decompose()
                next_node = tmp

    # 3. 處理剩餘所有標籤
    for tag in list(soup.find_all(True)):
        if tag.name not in allowed_tags:
            tag.unwrap()
        else:
            attrs = dict(tag.attrs)
            tag.attrs = {}
            if tag.name == 'a' and 'href' in attrs:
                tag['href'] = attrs['href']
            if tag.name == 'img' and 'src' in attrs:
                tag['src'] = attrs['src']
                if 'alt' in attrs: tag['alt'] = attrs['alt']
    
    return soup

def sync():
    if not all([CONFLUENCE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN, CONFLUENCE_PARENT_ID]):
        print("Error: Missing Confluence configuration in .env")
        return
    parent_ids = [pid.strip() for pid in CONFLUENCE_PARENT_ID.split(",") if pid.strip()]
    
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
        except Exception:
            state = {}
    
    total_updates = 0
    for root_id in parent_ids:
        print(f"\n>>> Executing Hierarchical Sync for Parent ID: {root_id}...")
        try:
            pages = search_all_descendants(root_id)
        except Exception as e:
            print(f"Error during search: {str(e)}")
            continue

        if not pages:
            try:
                pages = [get_page_by_id(root_id)]
            except Exception as e:
                print(f"Error during parent page fetch: {str(e)}")
                continue
        
        print(f"Found {len(pages)} pages in total hierarchy.")
        for page in pages:
            page_id = page["id"]
            title = page["title"]
            # 安全獲取版本號，避免 KeyError
            version_data = page.get("version", {})
            current_page_version = version_data.get("number", 1)
            page_dir = build_hierarchical_path(page, root_id)
            
            # 初始化或遷移頁面狀態
            old_page_state = state.get(page_id, {})
            if not isinstance(old_page_state, dict):
                page_state = {"version": old_page_state, "attachments": {}}
            else:
                page_state = old_page_state
            
            if "version" not in page_state: page_state["version"] = 0
            if "attachments" not in page_state: page_state["attachments"] = {}
            
            needs_html_update = (page_state["version"] != current_page_version) or not os.path.exists(page_dir)
            
            try:
                attachments = get_attachments(page_id)
                att_map = {}
                any_attachment_changed = False
                
                # 建立資料夾
                os.makedirs(page_dir, exist_ok=True)
                
                for att in attachments:
                    att_id = att.get("id")
                    # 安全獲取附件版本號
                    att_version_data = att.get("version", {})
                    att_version = att_version_data.get("number", 1)
                    download_url = att.get("_links", {}).get("download")
                    if not download_url: continue
                    local_name = get_img_name_from_url(download_url)
                    if not local_name: continue
                    
                    local_path = os.path.join(page_dir, local_name)
                    # 檢查附件更新條件
                    last_att_version = page_state["attachments"].get(att_id)
                    att_needs_update = (str(att_version) != str(last_att_version)) or not os.path.exists(local_path)
                    
                    if att_needs_update:
                        print(f"        [+] Updating attachment: {local_name} (v{att_version})")
                        actual_path = download_file(download_url, local_path)
                        final_local_name = os.path.basename(actual_path)
                        att_map[download_url] = final_local_name
                        any_attachment_changed = True
                    else:
                        att_map[download_url] = local_name
                    
                    # 更新單個附件版本紀錄
                    page_state["attachments"][att_id] = att_version

                if not needs_html_update and not any_attachment_changed:
                    print(f"    [-] Skipped: '{title}'", flush=True)
                    state[page_id] = page_state
                    continue

                print(f"    [+] Syncing: '{title}' -> {page_dir}...", flush=True)
                
                html_content = page["body"]["view"]["value"]
                soup = BeautifulSoup(html_content, "html.parser")
                
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if src:
                        clean_src = src.split('?')[0]
                        for remote_path, local_name in att_map.items():
                            clean_remote = remote_path.split('?')[0]
                            if clean_src.endswith(clean_remote) or clean_remote.endswith(clean_src):
                                img["src"] = local_name
                                break
                
                soup = lean_html(soup)
                html_path = os.path.join(page_dir, f"{sanitize_filename(title)}.html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                
                # 更新頁面版本與最終狀態
                page_state["version"] = current_page_version
                state[page_id] = page_state
                total_updates += 1
                
            except Exception as e:
                print(f"    [!] Failed to process '{title}': {str(e)}")
    
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
    print(f"\nDone! Sync completed. Total pages integrated: {total_updates}")

if __name__ == "__main__":
    sync()
