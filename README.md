# OrganometallicStructureAnalyzer
A Python toolkit for analyzing organometallic structures, starting with tools for metallocenes and inverse sandwich complexes.

## Overview
This repository provides scripts to analyze organometallic compounds, focusing on geometric properties like distances and angles. The initial tool, `ring_analyzer.py`, handles:
- **Metallocenes**: Structures with 2 rings (5 or 6 atoms) and 1 metal (e.g., ferrocene).
- **Inverse Sandwich Complexes**: Structures with 3 rings and 2 metals (e.g., Ring1-Metal1-Ring2-Metal2-Ring3).

Future expansions will include additional scripts or features for broader organometallic analysis.

## Features
- Places dummy atoms ('X') at ring centroids.
- Calculates metal-centroid distances.
- Computes angles:
  - 2 rings: CoM1-Metal1-CoM2.
  - 3 rings: CoM1-Metal1-CoM2, CoM1-CoM2-CoM3, CoM2-Metal2-CoM3, Metal1-CoM2-Metal2.
- Supports 5- or 6-membered rings (e.g., Cp, benzene).
- Outputs modified XYZ files.

## Requirements
- Python 3.x
- `numpy` (`pip3 install numpy --user`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/OrganometallicStructureAnalyzer.git
   cd OrganometallicStructureAnalyzer
