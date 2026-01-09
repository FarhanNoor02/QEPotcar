import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
BASE_URL = "https://pseudopotentials.quantum-espresso.org/legacy_tables/fhi-pp-from-abinit-web-site"
ROOT_DOMAIN = "https://pseudopotentials.quantum-espresso.org"
TARGET_DIR = input("Enter download path (e.g., /home/farhan/FHI_Library): ").strip()

# Setup Session with Retries for better stability
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def get_element_links():
    print("🔍 Fetching list of all elements from FHI Table...")
    try:
        response = session.get(BASE_URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Match only element sub-links
            if "/legacy_tables/fhi-pp-from-abinit-web-site/" in href:
                parts = href.rstrip('/').split('/')
                # Filter for element symbols (e.g., /li, /fe)
                if len(parts[-1]) <= 3:
                    elements.append(urljoin(ROOT_DOMAIN, href))
        return sorted(list(set(elements)))
    except Exception as e:
        print(f"❌ Error fetching main list: {e}")
        return []

def download_file(url, folder):
    fname = url.split('/')[-1]
    local_path = os.path.join(folder, fname)
    if os.path.exists(local_path):
        return False
    
    try:
        r = session.get(url, stream=True, timeout=20)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return True
    except:
        return False

def scrape_fhi():
    element_links = get_element_links()
    total = len(element_links)
    print(f"✅ Found {total} elements. Filtering for PBE functionals...\n")

    for i, el_link in enumerate(element_links, 1):
        el_name = el_link.rstrip('/').split('/')[-1].upper()
        print(f"[{i}/{total}] Processing {el_name}...")
        
        try:
            response = session.get(el_link, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all .UPF links on the element page
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                if not href.lower().endswith('.upf'):
                    continue
                
                full_url = urljoin(ROOT_DOMAIN, href)
                fname = href.split('/')[-1].lower()

                # LOGIC: Only download if 'pbe' is in the filename
                if 'pbe' in fname:
                    # In FHI table, these are almost all scalar and NC (Norm-Conserving)
                    # We will follow your hierarchy: PBE -> scalar -> NC
                    save_path = os.path.join(TARGET_DIR, "PBE", "scalar", "NC")
                    os.makedirs(save_path, exist_ok=True)
                    
                    if download_file(full_url, save_path):
                        print(f"    + Saved: {fname}")
                    else:
                        # If file already exists
                        pass
                        
        except Exception as e:
            print(f"    ⚠️ Error on {el_name}: {e}")

if __name__ == "__main__":
    if not TARGET_DIR:
        print("Error: No directory specified.")
    else:
        scrape_fhi()
        print(f"\n✨ Success! PBE FHI Library complete at: {TARGET_DIR}")
