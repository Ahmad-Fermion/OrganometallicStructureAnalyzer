import numpy as np
import argparse
import sys
import os

class Molecule:
    def __init__(self, filename):
        """Initialize molecule from an XYZ file."""
        self.atoms = []
        self.coords = []
        self.read_xyz(filename)

    def read_xyz(self, filename):
        """Read XYZ file into atoms and coordinates."""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                n_atoms = int(lines[0].strip())
                for line in lines[2:2 + n_atoms]:
                    parts = line.strip().split()
                    if len(parts) < 4:
                        raise ValueError("Invalid XYZ format")
                    self.atoms.append(parts[0])
                    self.coords.append(list(map(float, parts[1:4])))
                self.coords = np.array(self.coords)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    def get_centroid(self, ring_atoms):
        """Calculate centroid of specified ring atoms (1-based indices)."""
        if not all(1 <= i <= len(self.coords) for i in ring_atoms):
            raise ValueError("Atom indices out of range")
        ring_coords = self.coords[np.array(ring_atoms) - 1]  # Convert to 0-based
        return np.mean(ring_coords, axis=0)

    def add_atom(self, atom_symbol, position):
        """Add a new atom at the specified position."""
        self.atoms.append(atom_symbol)
        self.coords = np.vstack([self.coords, position])

    def distance(self, idx1, idx2):
        """Calculate distance between two atoms (1-based indices)."""
        return np.linalg.norm(self.coords[idx1 - 1] - self.coords[idx2 - 1])

    def angle(self, idx1, idx2, idx3):
        """Calculate angle (degrees) between three atoms (1-based indices)."""
        v1 = self.coords[idx1 - 1] - self.coords[idx2 - 1]  # Vector from idx2 to idx1
        v2 = self.coords[idx3 - 1] - self.coords[idx2 - 1]  # Vector from idx2 to idx3
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Clamp to avoid floating-point errors
        return np.degrees(np.arccos(cos_theta))

    def dihedral(self, idx1, idx2, idx3, idx4):
        """Calculate dihedral angle (degrees) between four atoms (1-based indices)."""
        p0 = self.coords[idx1 - 1]
        p1 = self.coords[idx2 - 1]
        p2 = self.coords[idx3 - 1]
        p3 = self.coords[idx4 - 1]

        # Vectors for the three bonds
        b0 = p1 - p0
        b1 = p2 - p1
        b2 = p3 - p2

        # Normals to the planes
        n1 = np.cross(b0, b1)
        n2 = np.cross(b1, b2)

        # Normalize normals
        n1 = n1 / np.linalg.norm(n1)
        n2 = n2 / np.linalg.norm(n2)

        # Calculate dihedral angle
        cos_theta = np.dot(n1, n2)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Clamp to avoid floating-point errors
        angle = np.degrees(np.arccos(cos_theta))

        # Determine the sign of the dihedral angle
        if np.dot(b1, np.cross(n1, n2)) < 0:
            angle = -angle
        return angle

    def write_xyz(self, filename):
        """Write molecule to an XYZ file."""
        with open(filename, 'w') as f:
            f.write(f"{len(self.atoms)}\n")
            f.write("Generated by ring_analyzer.py\n")
            for atom, coord in zip(self.atoms, self.coords):
                f.write(f"{atom} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n")

def main():
    # Command-line argument parsing with detailed help
    parser = argparse.ArgumentParser(
        description="Metallocene and Inverse Sandwich Analyzer: Add dummy atoms to ring centroids, calculate distances, angles, and for 3-ring cases, middle ring bond distances, dihedral angles, and metal-metal distance.",
        epilog="""
        Example usage (2 rings):
          python ring_analyzer.py ferrocene.xyz --ring1 1 2 3 4 5 --ring2 6 7 8 9 10 --metal1 11
        
        Example usage (3 rings):
          python ring_analyzer.py inverse_sandwich.xyz --ring1 1 2 3 4 5 --ring2 6 7 8 9 10 --ring3 11 12 13 14 15 --metal1 16 --metal2 17
        
        Notes:
          - Atom indices are 1-based.
          - Rings can be 5 or 6 atoms.
          - For 2 rings: specify --metal1 only.
          - For 3 rings: specify --metal1 and --metal2.
          - For 3 rings: metal1 is assigned to the metal closer to ring1, metal2 to the metal closer to ring3.
          - For 3 rings: bond distances, dihedral angles, and metal-metal distance are calculated for the middle ring (ring2).
          - CAUTION: For the middle ring (ring2) in 3-ring cases, atom indices must be provided in the correct sequential order as they appear consecutively around the ring (e.g., for a benzene ring: C1 C2 C3 C4 C5 C6) to ensure accurate bond distance and dihedral angle calculations.
          - Output file name defaults to input file name with '_analyzed' appended (e.g., m.xyz -> m_analyzed.xyz).
        """
    )
    parser.add_argument("xyz_file", help="Input XYZ file with structure")
    parser.add_argument("--ring1", nargs="+", type=int, required=True,
                        help="Atom numbers (1-based) for the first ring (5 or 6 atoms)")
    parser.add_argument("--ring2", nargs="+", type=int, required=True,
                        help="Atom numbers (1-based) for the second ring (5 or 6 atoms)")
    parser.add_argument("--ring3", nargs="+", type=int,
                        help="Atom numbers (1-based) for the third ring (5 or 6 atoms, optional)")
    parser.add_argument("--metal1", type=int, required=True,
                        help="Atom number (1-based) of the first metal")
    parser.add_argument("--metal2", type=int,
                        help="Atom number (1-based) of the second metal (required for 3 rings)")
    parser.add_argument("--output", type=str,
                        help="Output XYZ file name (default: input file name with '_analyzed' appended)")

    args = parser.parse_args()

    # Generate output file name if not provided
    output_file = args.output if args.output else f"{os.path.splitext(args.xyz_file)[0]}_analyzed{os.path.splitext(args.xyz_file)[1]}"

    # Collect ring data
    rings = {"ring1": args.ring1, "ring2": args.ring2}
    if args.ring3:
        rings["ring3"] = args.ring3

    # Validate ring sizes and metal args
    for label, ring in rings.items():
        if len(ring) not in [5, 6]:
            print(f"Error: {label} must have 5 or 6 atoms.")
            sys.exit(1)
        print(f"{label} detected as a {len(ring)}-membered ring.")
    
    if len(rings) == 3 and not args.metal2:
        print("Error: --metal2 required for 3-ring structure.")
        sys.exit(1)
    if len(rings) == 2 and args.metal2:
        print("Error: --metal2 specified but only 2 rings provided.")
        sys.exit(1)

    # Load molecule
    mol = Molecule(args.xyz_file)

    # Calculate centroids and add dummy atoms
    centroids = {}
    dummy_indices = {}
    for i, (label, ring_atoms) in enumerate(rings.items(), 1):
        centroid = mol.get_centroid(ring_atoms)
        centroids[f"com{i}"] = centroid
        print(f"Ring {i} centroid: {centroid[0]:.4f}, {centroid[1]:.4f}, {centroid[2]:.4f}")
        mol.add_atom("X", centroid)
        dummy_indices[f"com{i}"] = len(mol.atoms)  # 1-based index

    print(f"Added {len(rings)} dummy atoms ('X') at ring centroids.")

    # Calculate distances
    metal1_idx = args.metal1
    metal1_symbol = f"{mol.atoms[metal1_idx - 1]}{metal1_idx}"

    if len(rings) == 3:
        metal2_idx = args.metal2
        metal2_symbol = f"{mol.atoms[metal2_idx - 1]}{metal2_idx}"

        # Dynamically assign metals based on proximity to ring1 and ring3
        dist_m1_r1 = mol.distance(metal1_idx, dummy_indices['com1'])
        dist_m1_r3 = mol.distance(metal1_idx, dummy_indices['com3'])
        dist_m2_r1 = mol.distance(metal2_idx, dummy_indices['com1'])
        dist_m2_r3 = mol.distance(metal2_idx, dummy_indices['com3'])

        # If metal1 is closer to ring3 than ring1, swap metal1 and metal2
        if dist_m1_r3 < dist_m1_r1 and dist_m2_r1 < dist_m2_r3:
            metal1_idx, metal2_idx = metal2_idx, metal1_idx
            metal1_symbol = f"{mol.atoms[metal1_idx - 1]}{metal1_idx}"
            metal2_symbol = f"{mol.atoms[metal2_idx - 1]}{metal2_idx}"
            print("Note: Swapped metal1 and metal2 based on proximity to ring1 and ring3.")

        print(f"Distance from {metal1_symbol} to Ring 1 centroid: {mol.distance(metal1_idx, dummy_indices['com1']):.4f} Å")
        print(f"Distance from {metal1_symbol} to Ring 2 centroid: {mol.distance(metal1_idx, dummy_indices['com2']):.4f} Å")
        print(f"Distance from {metal2_symbol} to Ring 2 centroid: {mol.distance(metal2_idx, dummy_indices['com2']):.4f} Å")
        print(f"Distance from {metal2_symbol} to Ring 3 centroid: {mol.distance(metal2_idx, dummy_indices['com3']):.4f} Å")
        print(f"Distance from {metal1_symbol} to {metal2_symbol}: {mol.distance(metal1_idx, metal2_idx):.4f} Å")

        # Calculate bond distances for middle ring (ring2)
        print("\nBond distances in middle ring (ring2):")
        ring2_atoms = args.ring2
        for i in range(len(ring2_atoms)):
            atom1 = ring2_atoms[i]
            atom2 = ring2_atoms[(i + 1) % len(ring2_atoms)]  # Cyclic: connects last to first
            atom1_symbol = f"{mol.atoms[atom1 - 1]}{atom1}"
            atom2_symbol = f"{mol.atoms[atom2 - 1]}{atom2}"
            dist = mol.distance(atom1, atom2)
            print(f"Distance {atom1_symbol}--{atom2_symbol}: {dist:.4f} Å")

        # Calculate dihedral angles for middle ring (ring2)
        print("\nDihedral angles in middle ring (ring2):")
        for i in range(len(ring2_atoms)):
            idx1 = ring2_atoms[i]
            idx2 = ring2_atoms[(i + 1) % len(ring2_atoms)]
            idx3 = ring2_atoms[(i + 2) % len(ring2_atoms)]
            idx4 = ring2_atoms[(i + 3) % len(ring2_atoms)]
            atom1_symbol = f"{mol.atoms[idx1 - 1]}{idx1}"
            atom2_symbol = f"{mol.atoms[idx2 - 1]}{idx2}"
            atom3_symbol = f"{mol.atoms[idx3 - 1]}{idx3}"
            atom4_symbol = f"{mol.atoms[idx4 - 1]}{idx4}"
            dihedral = mol.dihedral(idx1, idx2, idx3, idx4)
            print(f"Dihedral {atom1_symbol}-{atom2_symbol}-{atom3_symbol}-{atom4_symbol}: {dihedral:.2f} degrees")
    else:  # 2 rings
        print(f"Distance from {metal1_symbol} to Ring 2 centroid: {mol.distance(metal1_idx, dummy_indices['com2']):.4f} Å")

    # Calculate angles
    if len(rings) == 2:
        angle = mol.angle(dummy_indices["com1"], metal1_idx, dummy_indices["com2"])
        print(f"Angle CoM1-{metal1_symbol}-CoM2: {angle:.2f} degrees")
    else:  # 3 rings
        angle1 = mol.angle(dummy_indices["com1"], metal1_idx, dummy_indices["com2"])
        angle2 = mol.angle(dummy_indices["com1"], dummy_indices["com2"], dummy_indices["com3"])
        angle3 = mol.angle(dummy_indices["com2"], metal2_idx, dummy_indices["com3"])
        angle4 = mol.angle(metal1_idx, dummy_indices["com2"], metal2_idx)
        print(f"Angle CoM1-{metal1_symbol}-CoM2: {angle1:.2f} degrees")
        print(f"Angle CoM1-CoM2-CoM3: {angle2:.2f} degrees")
        print(f"Angle CoM2-{metal2_symbol}-CoM3: {angle3:.2f} degrees")
        print(f"Angle {metal1_symbol}-CoM2-{metal2_symbol}: {angle4:.2f} degrees")

    # Save modified structure
    mol.write_xyz(output_file)
    print(f"Modified structure with {len(rings)} dummy atoms saved to '{output_file}'.")

if __name__ == "__main__":
    main()
