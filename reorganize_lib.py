import os
import shutil

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
SOURCE_DIR = input("Enter the current PseudoPot path (e.g., /home/farhan/PseudoPot): ").strip()
# Creates a new directory alongside your old one
DEST_BASE = os.path.join(os.path.dirname(SOURCE_DIR), "Reorganized_PseudoPot")

def get_type(filename):
    """Identifies if a file is PAW or USPP based on naming convention."""
    fname = filename.lower()
    if "kjpaw" in fname:
        return "PAW"
    elif "rrkjus" in fname:
        return "USPP"
    else:
        return "OTHER"

def reorganize():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: Source directory '{SOURCE_DIR}' not found!")
        return

    print(f"🚀 Starting reorganization into: {DEST_BASE}")

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith('.upf'):
                # path_parts example: ['...', 'PseudoPot', 'AC', 'pbe', 'scalar']
                path_parts = root.split(os.sep)
                
                try:
                    relativity = path_parts[-1]    # 'scalar' or 'full'
                    functional = path_parts[-2]    # 'pbe' or 'lda'
                    
                    # Determine PAW vs USPP
                    pseudo_type = get_type(file)
                    
                    # Construct new path: Reorganized_PseudoPot/PBE/scalar/PAW/
                    new_folder = os.path.join(
                        DEST_BASE, 
                        functional.upper(), 
                        relativity, 
                        pseudo_type
                    )
                    
                    os.makedirs(new_folder, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(os.path.join(root, file), os.path.join(new_folder, file))
                    
                except IndexError:
                    # This handles cases where the folder depth isn't what we expect
                    continue

    print(f"\n✅ Success! Your library is now organized at: {DEST_BASE}")

if __name__ == "__main__":
    reorganize()
