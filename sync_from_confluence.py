import os
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from urllib.parse import urlparse
import hashlib
import time

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
    if os.path.getsize(output_path) < 100:
        print(f"        [!] Warning: Downloaded file is suspiciously small ({os.path.getsize(output_path)} bytes)")

def get_attachments(page_id):
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}/child/attachment"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.json().get("results", [])

def sanitize_filename(filename, is_image=False, original_url=None):
    clean = re.sub(r'[\\/*?:"<>|]', "_", filename)
    if len(clean) > 150:
        base, ext = os.path.splitext(clean)
        suffix = f"_{hashlib.md5(original_url.encode()).hexdigest()[:8]}" if original_url else ""
        clean = base[:130] + suffix + ext
    return clean

def get_img_name_from_url(url):
    parsed = urlparse(url)
    clean_name = parsed.path.split('/')[-1]
    if not clean_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        clean_name += ".png"
    return sanitize_filename(clean_name, is_image=True, original_url=url)

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

def sync():
    if not all([CONFLUENCE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN, CONFLUENCE_PARENT_ID]):
        print("Error: Missing Confluence configuration in .env")
        return

    parent_ids = [pid.strip() for pid in CONFLUENCE_PARENT_ID.split(",") if pid.strip()]
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)

    total_updates = 0
    for root_id in parent_ids:
        print(f"\n>>> Executing Hierarchical Sync for Parent ID: {root_id}...")
        try:
            pages = search_all_descendants(root_id)
        except Exception as e:
            print(f"Error during search: {str(e)}")
            continue

        print(f"Found {len(pages)} pages in total hierarchy.")

        for page in pages:
            page_id = page["id"]
            title = page["title"]
            current_version = page["version"]["number"]
            page_dir = build_hierarchical_path(page, root_id)

            if state.get(page_id) == current_version and os.path.exists(page_dir):
                # We still print skip to keep output flowing and prevent timeout
                print(f"    [-] Skipped: '{title}'", flush=True)
                continue

            print(f"    [+] Syncing: '{title}' -> {page_dir}...", flush=True)
            os.makedirs(page_dir, exist_ok=True)

            # 1. Attachments
            try:
                attachments = get_attachments(page_id)
                att_map = {} 
                for att in attachments:
                    download_url = att["_links"]["download"]
                    local_name = get_img_name_from_url(download_url)
                    local_path = os.path.join(page_dir, local_name)
                    try:
                        download_file(download_url, local_path)
                        att_map[download_url] = local_name
                    except Exception as e:
                        print(f"        [!] Attachment error: {str(e)}")
            except Exception as e:
                print(f"    [!] Failed to get attachments for '{title}': {str(e)}")
                att_map = {}

            # 2. HTML
            try:
                html_content = page["body"]["view"]["value"]
                soup = BeautifulSoup(html_content, "html.parser")
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if src:
                        for remote_path, local_name in att_map.items():
                            if src in remote_path or remote_path in src:
                                img["src"] = local_name
                                if img.get("data-base-url"): del img["data-base-url"]
                                break
                
                html_path = os.path.join(page_dir, f"{sanitize_filename(title)}.html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                state[page_id] = current_version
                total_updates += 1
            except Exception as e:
                print(f"    [!] Failed to process HTML for '{title}': {str(e)}")

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

    print(f"\nDone! Sync completed. Total pages integrated: {total_updates}")

if __name__ == "__main__":
    sync()
