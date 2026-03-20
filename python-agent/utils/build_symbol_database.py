"""
FeynRules Symbol Database Builder

Parses downloaded .fr model files and extracts:
- Predefined function usage (Ga, ProjM, ProjP, etc.)
- Particle class definitions
- LaTeX-to-FR mapping patterns
- Index structures

Generates a comprehensive JSON database for the agent to use.

Usage:
    python build_symbol_database.py [--input-dir DIR] [--output-file FILE]
"""

import os
import json
import re
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Predefined FeynRules functions to track
PREDEFINED_FUNCTIONS = [
    'Ga', 'ProjM', 'ProjP', 'DC', 'FS', 'HC', 'del',
    'Eps', 'ME', 'IndexDelta', 'CKM', 'ExpandIndices',
    'Index', 'Block', 'Conjugate', 'Transpose',
    'Dot', 'CC', 'anti', 'DiracSpinor'
]

# Index types
INDEX_TYPES = [
    'Generation', 'Colour', 'Spin', 'Lorentz',
    'SU2W', 'SU2D', 'Gluon', 'Adjoint'
]


class SymbolDatabaseBuilder:
    """Builds symbol database from .fr model files."""

    def __init__(self, input_dir: str = "test_fr"):
        """
        Initialize builder.

        Args:
            input_dir: Directory containing downloaded .fr files
        """
        self.input_dir = Path(input_dir)
        self.database = {
            "version": "1.0",
            "source": "Extracted from FeynRules official models",
            "last_updated": "",
            "predefined_functions": {},
            "particle_classes": {},
            "latex_to_fr_patterns": {},
            "human_additions": {
                "description": "User-defined mappings added dynamically",
                "mappings": []
            },
            "statistics": {
                "models_parsed": 0,
                "total_symbols": 0,
                "total_patterns": 0
            }
        }

        # Tracking for aggregation
        self.function_usage = defaultdict(list)  # function -> list of examples
        self.particle_definitions = {}  # particle name -> definition
        self.lagrangian_patterns = []  # list of (model, pattern) tuples

    def build_database(self) -> Dict:
        """
        Build the complete symbol database.

        Returns:
            Dictionary containing the symbol database
        """
        logger.info(f"Building symbol database from {self.input_dir}")

        # Parse all .fr files
        fr_files = list(self.input_dir.rglob("*.fr"))
        logger.info(f"Found {len(fr_files)} .fr files")

        for fr_file in fr_files:
            try:
                self._parse_fr_file(fr_file)
                self.database["statistics"]["models_parsed"] += 1
            except Exception as e:
                logger.error(f"Error parsing {fr_file}: {e}")

        # Aggregate results
        self._build_predefined_functions()
        self._build_particle_classes()
        self._build_latex_patterns()

        # Update statistics
        self.database["statistics"]["total_symbols"] = len(self.database["predefined_functions"])
        self.database["statistics"]["total_patterns"] = len(self.database["latex_to_fr_patterns"])

        # Update timestamp
        import time
        self.database["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"Database built: {self.database['statistics']}")
        return self.database

    def _parse_fr_file(self, fr_file: Path):
        """
        Parse a single .fr file.

        Args:
            fr_file: Path to the .fr file
        """
        logger.debug(f"Parsing {fr_file.name}")

        try:
            with open(fr_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Could not read {fr_file}: {e}")
            return

        model_name = fr_file.stem

        # Extract function usage
        self._extract_function_usage(content, model_name)

        # Extract particle class definitions
        self._extract_particle_classes(content, model_name)

        # Extract Lagrangian patterns
        self._extract_lagrangian_patterns(content, model_name)

    def _extract_function_usage(self, content: str, model_name: str):
        """Extract usage examples of predefined functions."""
        for func in PREDEFINED_FUNCTIONS:
            # Pattern: func[...] or func[...](...)
            pattern = rf'{re.escape(func)}\[([^\]]+)\]'
            matches = re.findall(pattern, content)

            for match in matches:
                example = f"{func}[{match}]"
                self.function_usage[func].append({
                    "example": example,
                    "model": model_name
                })

    def _extract_particle_classes(self, content: str, model_name: str):
        """Extract particle class definitions from M$ClassesDescription."""
        # Pattern for class definitions: F[1] == { ... } or V[3] == { ... }
        class_pattern = r'([FVSGT])\[(\d+)\]\s*==\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'

        for match in re.finditer(class_pattern, content, re.MULTILINE | re.DOTALL):
            particle_type = match.group(1)  # F, V, S, G, T
            index = match.group(2)
            definition = match.group(3)

            # Extract ClassName
            classname_match = re.search(r'ClassName\s*->\s*(\w+)', definition)
            if classname_match:
                classname = classname_match.group(1)

                # Extract other fields
                particle_info = {
                    "particle_type": particle_type,
                    "index": index,
                    "model": model_name,
                    "definition": definition.strip()[:500]  # Truncate for storage
                }

                # Extract ClassMembers if present
                members_match = re.search(r'ClassMembers\s*->\s*\{([^}]+)\}', definition)
                if members_match:
                    members = [m.strip() for m in members_match.group(1).split(',')]
                    particle_info["members"] = members

                # Store (may overwrite from different models, that's OK)
                self.particle_definitions[classname] = particle_info

    def _extract_lagrangian_patterns(self, content: str, model_name: str):
        """Extract Lagrangian pattern examples."""
        # Look for Lagrangian definitions: LSomething := ...
        lagr_pattern = r'(L\w+)\s*:=([^;]+);'

        for match in re.finditer(lagr_pattern, content, re.MULTILINE | re.DOTALL):
            lagr_name = match.group(1)
            lagr_expr = match.group(2).strip()

            # Only store if it contains interesting functions
            if any(func in lagr_expr for func in ['ProjM', 'ProjP', 'Ga', 'DC', 'FS']):
                self.lagrangian_patterns.append({
                    "name": lagr_name,
                    "expression": lagr_expr[:1000],  # Truncate
                    "model": model_name
                })

    def _build_predefined_functions(self):
        """Build predefined_functions section of database."""
        # Define known functions with metadata
        known_functions = {
            "Ga": {
                "description": "Dirac gamma matrices",
                "latex_symbols": ["\\gamma", "γ"],
                "indices": ["Lorentz"],
                "type": "matrix"
            },
            "ProjM": {
                "description": "Left-handed chirality projector (1-γ5)/2",
                "latex_symbols": ["P_L", "\\mathcal{P}_L", "P_-"],
                "indices": ["Spin", "Spin"],
                "type": "projector"
            },
            "ProjP": {
                "description": "Right-handed chirality projector (1+γ5)/2",
                "latex_symbols": ["P_R", "\\mathcal{P}_R", "P_+"],
                "indices": ["Spin", "Spin"],
                "type": "projector"
            },
            "DC": {
                "description": "Covariant derivative D_μ",
                "latex_symbols": ["D", "\\mathcal{D}"],
                "indices": ["Field", "Lorentz"],
                "type": "derivative"
            },
            "FS": {
                "description": "Field strength tensor F_μν",
                "latex_symbols": ["F"],
                "indices": ["Field", "Lorentz", "Lorentz"],
                "type": "tensor"
            },
            "HC": {
                "description": "Hermitian conjugate",
                "latex_symbols": ["†", "\\dagger"],
                "indices": [],
                "type": "operator"
            },
            "del": {
                "description": "Partial derivative ∂_μ",
                "latex_symbols": ["\\partial", "∂"],
                "indices": ["Field", "Lorentz"],
                "type": "derivative"
            },
            "Eps": {
                "description": "Levi-Civita tensor ε_ij",
                "latex_symbols": ["\\epsilon", "ε"],
                "indices": ["SU2", "SU2"],
                "type": "tensor"
            },
            "ME": {
                "description": "Minkowski metric η_μν",
                "latex_symbols": ["\\eta", "η"],
                "indices": ["Lorentz", "Lorentz"],
                "type": "metric"
            },
            "IndexDelta": {
                "description": "Kronecker delta δ_ij",
                "latex_symbols": ["\\delta", "δ"],
                "indices": ["Any", "Any"],
                "type": "delta"
            },
            "CKM": {
                "description": "CKM matrix element V_ij",
                "latex_symbols": ["V", "V_{CKM}"],
                "indices": ["Generation", "Generation"],
                "type": "matrix"
            },
            "ExpandIndices": {
                "description": "Expand flavor/gauge indices",
                "latex_symbols": [],
                "indices": [],
                "type": "function"
            }
        }

        for func_name, metadata in known_functions.items():
            examples = self.function_usage.get(func_name, [])

            # Take up to 5 most diverse examples
            unique_examples = []
            seen_patterns = set()
            for ex in examples:
                pattern = ex["example"]
                if pattern not in seen_patterns:
                    unique_examples.append(pattern)
                    seen_patterns.add(pattern)
                if len(unique_examples) >= 5:
                    break

            self.database["predefined_functions"][func_name] = {
                **metadata,
                "usage": f"{func_name}[...]",
                "examples": unique_examples
            }

    def _build_particle_classes(self):
        """Build particle_classes section of database."""
        # Organize by common categories
        for classname, info in self.particle_definitions.items():
            self.database["particle_classes"][classname] = {
                "ClassName": classname,
                "particle_type": info["particle_type"],
                "model_source": info["model"],
                "ClassMembers": info.get("members", []),
                "fr_notation": f"{classname}[...]",  # Generic
                "definition_snippet": info["definition"]
            }

    def _build_latex_patterns(self):
        """Build latex_to_fr_patterns section."""
        # Create pattern from user's example (from requirements)
        # This should be extended with more patterns from actual parsing
        self.database["latex_to_fr_patterns"]["scalar_lepton_coupling"] = {
            "latex_pattern": "$S \\bar{l}_i P_L l_j$",
            "fr_pattern": "H0 * (lbar[sp1, ii].ProjM[sp1, sp2].l[sp2, jj])",
            "description": "Scalar coupled to lepton bilinear with left-handed projection",
            "source_models": ["StandardModelScalars", "2HDM"],
            "variables": {
                "S": "H0",
                "l_i": "l[sp, ii]",
                "\\bar{l}_i": "lbar[sp, ii]",
                "P_L": "ProjM[sp1, sp2]",
                "l_j": "l[sp, jj]"
            }
        }

        # Add pattern from user's quark example
        self.database["latex_to_fr_patterns"]["scalar_quark_coupling"] = {
            "latex_pattern": "$S \\bar{u}_i P_L u_j$",
            "fr_pattern": "H0 * (uqbar[sp1, ii, cc].ProjM[sp1, sp2].uq[sp2, jj, cc])",
            "description": "Scalar coupled to up-quark bilinear with left-handed projection",
            "source_models": ["StandardModelScalars"],
            "variables": {
                "S": "H0",
                "u_i": "uq[sp, ii, cc]",
                "\\bar{u}_i": "uqbar[sp, ii, cc]",
                "P_L": "ProjM[sp1, sp2]",
                "u_j": "uq[sp, jj, cc]"
            }
        }

        # Could add more auto-detected patterns from lagrangian_patterns
        # For now, keeping it simple with the user-provided examples

    def save_database(self, output_file: str = "symbol_db/feynrules_symbols.json"):
        """
        Save database to JSON file.

        Args:
            output_file: Path to output JSON file
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, indent=2, ensure_ascii=False)

        logger.info(f"Database saved to {output_path}")
        logger.info(f"Statistics: {self.database['statistics']}")


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Build FeynRules symbol database from .fr files"
    )
    parser.add_argument(
        '--input-dir',
        default='test_fr',
        help='Input directory containing .fr files (default: test_fr)'
    )
    parser.add_argument(
        '--output-file',
        default='symbol_db/feynrules_symbols.json',
        help='Output JSON file (default: symbol_db/feynrules_symbols.json)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Build database
    builder = SymbolDatabaseBuilder(input_dir=args.input_dir)
    builder.build_database()
    builder.save_database(output_file=args.output_file)


if __name__ == "__main__":
    main()
