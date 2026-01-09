# QEPotcar
A pseudopotential library for use with the DFT code Quantum ESPRESSO

QE-PotLib: The "POTCAR" Experience for Quantum ESPRESSO
📌 Overview

In VASP, the POTCAR directories provide a unified, predictable structure for functional and methodology types. Quantum ESPRESSO users, however, often have to manually download and sort files from various legacy tables.

QE-PotLib is a suite of automation scripts designed to "fill the gap." It scrapes official QE legacy databases (PSLibrary and FHI) and organizes them into a standardized, hierarchical structure: Functional > Relativity > Method (PAW/USPP/NC) > Element.UPF
🚀 Features

    Automated Scraping: Pulls from PSLibrary (1.0.0) and FHI (Abinit) tables.

    Smart Mapping: Automatically categorizes pz as LDA.

    Hierarchy Enforcement: Mimics the VASP organizational style for high-throughput workflow compatibility.

    Version Control: Prioritizes psl.1.0.0 to ensure the highest quality potentials are used.

📂 Standardized Output Structure

After running the scripts, your library will look like this:
Plaintext

QE_Pseudo_Library/
├── PBE/
│   ├── scalar/
│   │   ├── PAW/  <-- (e.g., Ac.pbe-spfn-kjpaw_psl.1.0.0.UPF)
│   │   ├── USPP/ <-- (e.g., Ac.pbe-spfn-rrkjus_psl.1.0.0.UPF)
│   │   └── NC/   <-- (From FHI table)
│   └── full/
│       ├── PAW/
│       └── USPP/
└── LDA/
    ├── scalar/
    └── full/

🛠 The Toolset
1. fetch_pslibrary.py

Targets: PSLibrary Legacy Tables. This script performs heavy lifting for Projector Augmented Wave (PAW) and Ultrasoft (USPP) potentials.
Python

# Key Logic: Sorting by Relativity and Method
ptype = "PAW" if "kjpaw" in fname else "USPP" if "rrkjus" in fname else None
rel = "full" if "rel-" in fname else "scalar"
save_path = os.path.join(TARGET_DIR, functional.upper(), rel, ptype)

2. fetch_fhi_pbe.py

Targets: FHI-PP from Abinit. Fills the gap for Norm-Conserving (NC) potentials, specifically filtering for PBE functionals to ensure consistency across the library.
3. reorganize_lib.py

A utility script to pivot existing flat downloads into the nested hierarchy shown above using shutil and os.walk.
📥 Installation & Usage

    Clone the repository:
    Bash

git clone https://github.com/yourusername/QE-PotLib.git
cd QE-PotLib

Install dependencies:
Bash

pip install requests beautifulsoup4

Run the generators:
Bash

    python3 fetch_pslibrary.py
    # Follow the prompt to enter your destination path

🤝 Contribution

If you find a legacy table that isn't mapped yet (e.g., GBRV or SG15), feel free to open a Pull Request!
Why this matters for the QE Community:

Standardizing the pseudopotential directory is the first step toward automation. With this structure, you can write simple Python wrappers to automatically generate &ATOMIC_SPECIES cards for your pw.x input files, just like VASP wrappers do for POTCAR.
