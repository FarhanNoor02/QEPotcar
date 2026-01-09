import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#MIT License--------------------------------------------------------------------

#Copyright (c) 2026 Farhan

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#----------------------------------------------------------------------------------

# --- CONFIGURATION ---
BASE_URL = "https://pseudopotentials.quantum-espresso.org/legacy_tables/ps-library"
ROOT_DOMAIN = "https://pseudopotentials.quantum-espresso.org"
TARGET_DIR = input("Enter download path (e.g., /home/farhan/PseudoPot): ").strip()

# We include 'pz' because LDA is often named 'pz' in the PS Library
FUNCTIONAL_MAP = {
    "pbe": "pbe",
    "pbesol": "pbesol",
    "lda": "lda",
    "pz": "lda"  # Maps pz files into the lda folder
}
TYPES = ["paw", "uspp"]
RELATIVITY = ["scalar", "full"]

def get_element_links():
    print("Fetching list of all elements from PSlibrary...")
    try:
        response = requests.get(BASE_URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "/legacy_tables/ps-library/" in href:
                parts = href.rstrip('/').split('/')
                if len(parts[-1]) <= 3: # Elements like H, Li, Si
                    elements.append(urljoin(ROOT_DOMAIN, href))
        return sorted(list(set(elements)))
    except Exception as e:
        print(f"Error fetching main list: {e}")
        return []

def download_file(url, folder):
    fname = url.split('/')[-1]
    local_path = os.path.join(folder, fname)
    if os.path.exists(local_path):
        return False
    
    try:
        r = requests.get(url, stream=True, timeout=20)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            return True
    except:
        return False
    return False

def scrape_and_download():
    element_links = get_element_links()
    total = len(element_links)
    print(f"Found {total} elements. Starting categorized downloads...\n")

    for i, el_link in enumerate(element_links, 1):
        el_name = el_link.rstrip('/').split('/')[-1].upper()
        print(f"[{i}/{total}] Processing {el_name}...")
        
        try:
            response = requests.get(el_link, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            downloaded_for_this_el = set()

            # Priority: Look for 1.0.0 versions first
            all_links = [urljoin(ROOT_DOMAIN, l['href']) for l in soup.find_all('a', href=True) if l['href'].lower().endswith('.upf')]
            
            for full_url in all_links:
                fname = full_url.lower()
                
                # 1. Identify Functional & Map it
                matched_func_key = next((k for k in FUNCTIONAL_MAP.keys() if k in fname), None)
                if not matched_func_key: continue
                target_folder_name = FUNCTIONAL_MAP[matched_func_key]
                
                # 2. Identify Type (kjpaw=PAW, rrkjus=USPP)
                ptype = "paw" if "kjpaw" in fname else "uspp" if "rrkjus" in fname else None
                if not ptype: continue
                
                # 3. Identify Relativity
                rel = "full" if "rel-" in fname else "scalar"

                # 4. Version Check (Prefer psl.1.0.0)
                # If this isn't 1.0.0, but a 1.0.0 exists for this combo, skip it
                combo_key = f"{target_folder_name}_{ptype}_{rel}"
                is_latest = "psl.1.0.0" in fname
                has_latest_available = any(f"{matched_func_key}" in l and "psl.1.0.0" in l and ptype in l for l in all_links)
                
                if has_latest_available and not is_latest:
                    continue

                if combo_key not in downloaded_for_this_el:
                    save_path = os.path.join(TARGET_DIR, el_name, target_folder_name, rel)
                    os.makedirs(save_path, exist_ok=True)
                    
                    if download_file(full_url, save_path):
                        print(f"    + Saved {rel} {target_folder_name} {ptype}: {fname.split('/')[-1]}")
                        downloaded_for_this_el.add(combo_key)
                        
        except Exception as e:
            print(f"    ! Connection error on {el_name}. Skipping to next...")

if __name__ == "__main__":
    if not TARGET_DIR:
        print("Error: No directory specified.")
    else:
        scrape_and_download()
        print(f"\nSuccess! Library complete at: {TARGET_DIR}")
