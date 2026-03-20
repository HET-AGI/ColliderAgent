"""
Build Default Mappings Database

This utility creates or updates the database/default_mappings.json file
with standard symbol conventions for FeynRules code generation.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_path() -> Path:
    """Get the path to the default mappings database."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    return project_root / "database" / "default_mappings.json"


def load_existing_mappings() -> Dict[str, Any]:
    """Load existing default mappings if they exist."""
    db_path = get_database_path()

    if db_path.exists():
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    return create_default_structure()


def create_default_structure() -> Dict[str, Any]:
    """Create the default structure for the mappings database."""
    return {
        "version": "2.0",
        "description": "Default symbol conventions for FeynRules code generation",
        "scalars": {},
        "leptons": {},
        "quarks": {},
        "operators": {},
        "gauge_bosons": {},
        "coupling_constants": {},
        "special_functions": {},
        "index_conventions": {},
        "common_patterns": {},
        "notes": {}
    }


def add_scalar(db: Dict, symbol: str, fr_notation: str, description: str, reference: str = "generic") -> None:
    """Add a scalar particle mapping."""
    db["scalars"][symbol] = {
        "fr_notation": fr_notation,
        "description": description,
        "reference": reference,
        "particle_type": "scalar",
        "index_structure": {}
    }
    logger.info(f"Added scalar: {symbol} → {fr_notation}")


def add_fermion(
    db: Dict,
    category: str,  # "leptons" or "quarks"
    symbol: str,
    fr_notation: str,
    description: str,
    index_structure: Dict[str, Any],
    reference: str = "SM.fr"
) -> None:
    """Add a fermion particle mapping."""
    db[category][symbol] = {
        "fr_notation": fr_notation,
        "description": description,
        "reference": reference,
        "particle_type": "fermion",
        "index_structure": index_structure
    }
    logger.info(f"Added {category[:-1]}: {symbol} → {fr_notation}")


def add_operator(
    db: Dict,
    symbol: str,
    fr_notation: str,
    description: str,
    operator_type: str,
    index_structure: Dict[str, Any],
    reference: str = "SM.fr"
) -> None:
    """Add an operator mapping."""
    db["operators"][symbol] = {
        "fr_notation": fr_notation,
        "description": description,
        "reference": reference,
        "operator_type": operator_type,
        "index_structure": index_structure
    }
    logger.info(f"Added operator: {symbol} → {fr_notation}")


def add_coupling(
    db: Dict,
    symbol: str,
    fr_notation: str,
    description: str,
    parameter_type: str,
    **kwargs
) -> None:
    """Add a coupling constant mapping."""
    db["coupling_constants"][symbol] = {
        "fr_notation": fr_notation,
        "description": description,
        "parameter_type": parameter_type,
        **kwargs
    }
    logger.info(f"Added coupling: {symbol} → {fr_notation}")


def add_common_pattern(
    db: Dict,
    pattern_id: str,
    latex: str,
    fr_code: str,
    description: str,
    sector: str
) -> None:
    """Add a common Lagrangian pattern."""
    db["common_patterns"][pattern_id] = {
        "latex": latex,
        "fr_code": fr_code,
        "description": description,
        "sector": sector
    }
    logger.info(f"Added pattern: {pattern_id}")


def verify_database(db: Dict) -> bool:
    """Verify the database structure and content."""
    required_sections = [
        "version", "scalars", "leptons", "quarks", "operators",
        "gauge_bosons", "coupling_constants", "special_functions",
        "index_conventions", "common_patterns", "notes"
    ]

    for section in required_sections:
        if section not in db:
            logger.error(f"Missing required section: {section}")
            return False

    logger.info("Database structure verification: PASS")

    # Verify content
    total_entries = (
        len(db["scalars"]) +
        len(db["leptons"]) +
        len(db["quarks"]) +
        len(db["operators"]) +
        len(db["gauge_bosons"]) +
        len(db["coupling_constants"]) +
        len(db["special_functions"]) +
        len(db["common_patterns"])
    )

    logger.info(f"Total entries: {total_entries}")
    logger.info(f"  Scalars: {len(db['scalars'])}")
    logger.info(f"  Leptons: {len(db['leptons'])}")
    logger.info(f"  Quarks: {len(db['quarks'])}")
    logger.info(f"  Operators: {len(db['operators'])}")
    logger.info(f"  Gauge bosons: {len(db['gauge_bosons'])}")
    logger.info(f"  Couplings: {len(db['coupling_constants'])}")
    logger.info(f"  Special functions: {len(db['special_functions'])}")
    logger.info(f"  Common patterns: {len(db['common_patterns'])}")

    return True


def save_database(db: Dict) -> None:
    """Save the database to JSON file."""
    db_path = get_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    logger.info(f"Database saved to: {db_path}")


def build_from_scratch() -> Dict[str, Any]:
    """Build the complete default mappings database from scratch."""
    logger.info("Building default mappings database from scratch...")

    db = create_default_structure()

    # Add scalars
    add_scalar(db, "S", "H0", "Scalar new particle", "Scalar_Model.fr")
    add_scalar(db, "H", "H", "Standard Model Higgs field", "SM.fr")
    add_scalar(db, "phi", "phi", "Generic scalar field", "generic")

    # Add leptons
    add_fermion(
        db, "leptons", "l_i", "l[sp, ii]",
        "Charged leptons (i=flavor index: e,μ,τ)",
        {
            "sp": {"type": "spinor", "range": "1-4"},
            "ii": {"type": "flavor", "range": "1-3"}
        }
    )
    add_fermion(
        db, "leptons", "lbar_i", "lbar[sp, ii]",
        "Dirac adjoint of charged leptons (l†γ⁰)",
        {
            "sp": {"type": "spinor", "range": "1-4"},
            "ii": {"type": "flavor", "range": "1-3"}
        }
    )

    # Add quarks
    add_fermion(
        db, "quarks", "u_i", "uq[sp, ii, cc]",
        "Up-type quarks (i=flavor: u,c,t)",
        {
            "sp": {"type": "spinor", "range": "1-4"},
            "ii": {"type": "flavor", "range": "1-3"},
            "cc": {"type": "color", "range": "1-3"}
        }
    )
    add_fermion(
        db, "quarks", "ubar_i", "uqbar[sp, ii, cc]",
        "Dirac adjoint of up-type quarks",
        {
            "sp": {"type": "spinor", "range": "1-4"},
            "ii": {"type": "flavor", "range": "1-3"},
            "cc": {"type": "color", "range": "1-3"}
        }
    )
    add_fermion(
        db, "quarks", "d_i", "dq[sp, ii, cc]",
        "Down-type quarks (i=flavor: d,s,b)",
        {
            "sp": {"type": "spinor", "range": "1-4"},
            "ii": {"type": "flavor", "range": "1-3"},
            "cc": {"type": "color", "range": "1-3"}
        }
    )
    add_fermion(
        db, "quarks", "dbar_i", "dqbar[sp, ii, cc]",
        "Dirac adjoint of down-type quarks",
        {
            "sp": {"type": "spinor", "range": "1-4"},
            "ii": {"type": "flavor", "range": "1-3"},
            "cc": {"type": "color", "range": "1-3"}
        }
    )

    # Add operators
    add_operator(
        db, "P_L", "ProjM[sp1, sp2]",
        "Left-handed projector (1-γ⁵)/2",
        "projector",
        {"sp1": {"type": "spinor"}, "sp2": {"type": "spinor"}}
    )
    add_operator(
        db, "P_R", "ProjP[sp1, sp2]",
        "Right-handed projector (1+γ⁵)/2",
        "projector",
        {"sp1": {"type": "spinor"}, "sp2": {"type": "spinor"}}
    )
    add_operator(
        db, "gamma_mu", "Ga[mu, sp1, sp2]",
        "Dirac gamma matrices",
        "dirac_matrix",
        {
            "mu": {"type": "lorentz", "range": "0-3"},
            "sp1": {"type": "spinor"},
            "sp2": {"type": "spinor"}
        }
    )

    # Add coupling constants
    add_coupling(
        db, "y_L", "YLL[ii, jj]",
        "Left-handed Yukawa coupling matrix",
        "yukawa_coupling",
        dimension="3x3"
    )
    add_coupling(
        db, "y_R", "YLR[ii, jj]",
        "Right-handed Yukawa coupling matrix",
        "yukawa_coupling",
        dimension="3x3"
    )

    # Add common patterns
    add_common_pattern(
        db, "yukawa_lepton_lr",
        r"S \bar{l}_i P_L l_j",
        "H0 * (lbar[sp1, ii].ProjM[sp1, sp2].l[sp2, jj])",
        "Scalar-lepton Yukawa with left projector",
        "lepton"
    )
    add_common_pattern(
        db, "yukawa_lepton_rr",
        r"S \bar{l}_i P_R l_j",
        "H0 * (lbar[sp1, ii].ProjP[sp1, sp2].l[sp2, jj])",
        "Scalar-lepton Yukawa with right projector",
        "lepton"
    )

    # Add index conventions
    db["index_conventions"] = {
        "spinor_indices": {
            "symbols": ["sp", "sp1", "sp2", "sp3"],
            "range": "1-4",
            "description": "Dirac spinor indices"
        },
        "flavor_indices": {
            "symbols": ["ii", "jj", "kk"],
            "range": "1-3",
            "description": "Fermion generation/flavor indices"
        },
        "color_indices": {
            "symbols": ["cc", "cc1", "cc2"],
            "range": "1-3",
            "description": "QCD color indices"
        },
        "lorentz_indices": {
            "symbols": ["mu", "nu", "rho", "sigma"],
            "range": "0-3",
            "description": "Spacetime Lorentz indices"
        }
    }

    # Add notes
    db["notes"] = {
        "index_summation": "Repeated indices are automatically summed (Einstein convention)",
        "hermiticity": "For Lagrangians, ensure L = L†. Use HC[] for hermitian conjugate",
        "gauge_invariance": "Use covariant derivatives for gauge-transforming fields",
        "spinor_flow": "Spinor indices flow: lbar[sp1] → operator[sp1,sp2] → l[sp2]"
    }

    logger.info("Database built successfully!")
    return db


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Build or verify default mappings database"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild database from scratch (overwrites existing)"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify existing database structure"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing database (preserves custom entries)"
    )

    args = parser.parse_args()

    if args.rebuild:
        db = build_from_scratch()
        save_database(db)
        verify_database(db)

    elif args.verify:
        db = load_existing_mappings()
        is_valid = verify_database(db)
        if is_valid:
            logger.info("✓ Database verification successful")
        else:
            logger.error("✗ Database verification failed")

    elif args.update:
        db = load_existing_mappings()
        # Preserve custom entries, update standard ones
        updated_db = build_from_scratch()
        # Merge (this is simplified - could be more sophisticated)
        for key in db:
            if key.startswith("custom_"):
                updated_db[key] = db[key]
        save_database(updated_db)
        logger.info("Database updated")

    else:
        # Default: verify existing or create if doesn't exist
        db_path = get_database_path()
        if db_path.exists():
            db = load_existing_mappings()
            verify_database(db)
        else:
            logger.info("No existing database found. Creating new one...")
            db = build_from_scratch()
            save_database(db)
            verify_database(db)


if __name__ == "__main__":
    main()
