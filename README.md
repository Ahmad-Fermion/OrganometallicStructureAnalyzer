# OrganometallicStructureAnalyzer

A Python toolkit for analyzing organometallic structures, focusing on **metallocenes** and **inverse sandwich complexes**.

## Overview

This repository provides two Python scripts to analyze organometallic compounds, calculating geometric properties such as **distances**, **angles**, and **dihedral angles**:

- **`ring_analyzer.py`**: A command-line tool for analyzing **metallocenes** (2 rings, 1 metal) and **inverse sandwich complexes** (3 rings, 2 metals).
- **`ring_analyzer_interactive.py`**: An interactive version that prompts users for input during execution.

Both scripts support structures with **5- or 6-membered rings** (e.g., cyclopentadienyl, benzene) and handle **inverse sandwich complexes** (e.g., Ring1-Metal1-Ring2-Metal2-Ring3).

## Features

- Places dummy atoms (`X`) at ring centroids.
- Calculates **metal-centroid distances**:
  - For 2 rings: Metal1 to Ring1 and Ring2 centroids.
  - For 3 rings: Metal1 to Ring1 and Ring2 centroids, Metal2 to Ring2 and Ring3 centroids, and Metal1 to Metal2 distance.
- Computes **angles**:
  - For 2 rings: CoM1-Metal1-CoM2.
  - For 3 rings: CoM1-Metal1-CoM2, CoM1-CoM2-CoM3, CoM2-Metal2-CoM3, Metal1-CoM2-Metal2.
- For 3-ring cases, calculates:
  - **Bond distances** in the middle ring (ring2, e.g., `C3--C61: 1.4555 Å`).
  - **Dihedral angles** in the middle ring (ring2).
- Outputs modified **XYZ files** with dummy atoms at centroids.
- For **`ring_analyzer.py`** (3-ring case): Dynamically assigns Metal1 to the metal closer to Ring1 and Metal2 to the metal closer to Ring3, ensuring consistent results regardless of input order.
- Supports **5- or 6-membered rings**.

## Requirements

- **Python 3.x**
- **`numpy`** (install with `pip3 install numpy --user`)

## Installation

Clone the repository:

```bash
git clone https://github.com/Ahmad-Fermion/OrganometallicStructureAnalyzer.git
cd OrganometallicStructureAnalyzer
```

**Example (2 rings):**

```bash
python ring_analyzer.py ferrocene.xyz --ring1 1 2 3 4 5 --ring2 6 7 8 9 10 --metal1 11
```

**Example (3 rings):**

```bash
python ring_analyzer.py inverse_sandwich.xyz --ring1 2 4 5 7 9 --ring2 3 61 6 8 64 118 --ring3 62 63 65 66 67 --metal1 1 --metal2 60
```

**ring_analyzer_interactive.py (Interactive):**

```bash
python ring_analyzer_interactive.py
```
