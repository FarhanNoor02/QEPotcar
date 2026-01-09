# QEPotcar
A pseudopotential library for use with the DFT code Quantum ESPRESSO

# QE-Potcar: The "POTCAR" Experience for Quantum ESPRESSO

## 📌 Overview
In VASP, the `POTCAR` directories provide a unified, predictable structure for functional and methodology types. Quantum ESPRESSO (QE) users, however, often have to manually download, rename, and sort files from various legacy tables, leading to inconsistent directory structures across different research groups. Often, the pseudopotentials have to be downloaded individually for each new project, making this cumbersome.

**QEPotcar** is a suite of automation scripts designed to "fill the gap." It scrapes official QE legacy databases (PSLibrary and FHI) and organizes them into a standardized, hierarchical structure mimicking the VASP experience:

`Functional > Relativity > Method (PAW/USPP/NC) > Element.UPF`

#### INCLUDE:
A complete and organized library <PseudoPot> with the pseudopotentials already organized allowing for rapid implementation, right away, including the collection of scripts used to develop this library in the first place.

---

## 🚀 Features
* **Automated Scraping**: Seamlessly pulls from PSLibrary (1.0.0) and FHI (Abinit) tables.
* **Smart Mapping**: Automatically identifies and categorizes functional variants (e.g., mapping `pz` to the `LDA` directory).
* **Hierarchy Enforcement**: Mimics the VASP organizational style to enable high-throughput workflow compatibility and easier scripting.
* **Version Control**: Prioritizes `psl.1.0.0` versions to ensure the highest quality, most recent potentials are used.

---

## 📂 Standardized Output Structure
After running the scripts, your local library will be structured as follows:

```text
Reorganized_PseudoPot/
├── PBE/
│   ├── scalar/
│   │   ├── PAW/
│   │   │   ├── Ac.pbe-spfn-kjpaw_psl.1.0.0.UPF
│   │   │   └── Ag.pbe-n-kjpaw_psl.1.0.0.UPF
│   │   └── USPP/
│   │       └── Ac.pbe-spfn-rrkjus_psl.1.0.0.UPF
│   └── full/
│       ├── PAW/
│       └── USPP/
└── LDA/
|   ├── scalar/
|   │   ├── PAW/
|   │   └── USPP/
|
|---NC-Martins-Troullier/

```
## Requirements
pip install requests beautifulsoup4

## 🛠 The Toolset

### 1. fetch_pslibrary.py

Targets: PSLibrary Legacy Tables. This script performs heavy lifting for Projector Augmented Wave (PAW) and Ultrasoft (USPP) potentials.
Python

#### Key Logic: Sorting by Relativity and Method
ptype = "PAW" if "kjpaw" in fname else "USPP" if "rrkjus" in fname else None
rel = "full" if "rel-" in fname else "scalar"
save_path = os.path.join(TARGET_DIR, functional.upper(), rel, ptype)

### 2. fetch_fhi_pbe.py

Targets: FHI-PP from Abinit. Fills the gap for Norm-Conserving (NC) potentials, specifically filtering for PBE functionals to ensure consistency across the library.

### 3. reorganize_lib.py

A utility script to pivot existing flat downloads into the nested hierarchy shown above using shutil and os.walk.

## PseudoPot
A library with all the pseudopotential files all ready reorganized and ready to be used immediately
