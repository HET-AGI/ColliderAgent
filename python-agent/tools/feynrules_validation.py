# tools/feynrules_validation.py
import json
import traceback
from typing import Any, Dict
from dotenv import load_dotenv; load_dotenv()
import magnus


__all__ = [
    "validate_feynrules",
]


def validate_feynrules(
    feynrules_model_path: str,
    lagrangian_symbol: str,
)-> Dict[str, Any]:
    
    """
    Validate a FeynRules model file (.fr) for physical consistency.

    Runs 4 checks in both Feynman gauge and Unitary gauge (8 total).
    Pass criteria are tiered per check type (aligned with expert reference):
      - Hermiticity: TrueQ or empty list or 0
      - DiagonalQuadraticTerms / DiagonalMassTerms: above + Null
      - KineticTermNormalisation: anything except False/$Failed/$Aborted

    Model type is auto-detected: if the .fr file contains M$GaugeGroups it is
    treated as a standalone model; otherwise it is a BSM extension and the
    FeynRules built-in SM.fr is loaded first automatically.

    Args:
        feynrules_model_path: Path to the .fr model file (e.g., "models/HillModel.fr").
            Both standalone models and BSM extensions are accepted — SM.fr
            base loading is handled automatically.
        lagrangian_symbol: The EXACT Lagrangian variable name defined in the .fr file
                           (e.g., "LSM", "LmZp", "Lag"). Must be explicitly assigned.

    Returns:
        dict — always present:
            "success" (bool): True iff all 4 Unitary gauge checks pass.
                Feynman gauge results are informational (Goldstone artifacts
                are expected for models with spontaneous symmetry breaking).
            "verdict" (str): Intelligent human-readable summary explaining
                the outcome — covers Goldstone mixing, field mixing, etc.
            "model_name", "lagrangian_name" (str).
            "model_loading": {"status": bool, "message": str}.
        present after model loads:
            "feynman_gauge", "unitary_gauge": each an object with 4 check keys:
                "hermiticity": {"passed": bool, "is_hermitian": bool,
                                "non_hermitian_terms"?: [...]}
                               or {"passed": false, "status": "inconclusive", ...}.
                "diagonal_quadratic_terms": {"passed": bool, "warning"?: str}
                               or {"passed": false, "status": "inconclusive", ...}.
                "diagonal_mass_terms": {"passed": bool}
                               or {"passed": false, "status": "inconclusive", ...}.
                "kinetic_term_normalisation": {"passed": bool, "warning"?: str}
                               or {"passed": false, "status": "inconclusive", ...}.
        on Python-level failure: {"success": false, "error": str}.

    Check order per gauge:
        1. CheckHermiticity  2. CheckDiagonalQuadraticTerms
        3. CheckDiagonalMassTerms  4. CheckKineticTermNormalisation

    Example:
        validate_feynrules("models/standard_model.fr", lagrangian_symbol="LSM")
        validate_feynrules("models/hill_model.fr", lagrangian_symbol="Lag")
    """
    
    try:
        result = magnus.run_blueprint(
            blueprint_id = "validate-feynrules",
            args = {
                # Also try CLI: magnus run validate-feynrules --model SM.fr --lagrangian LSM
                "model": feynrules_model_path,
                "lagrangian": lagrangian_symbol,
            }
        )
        assert result is not None
        result_dict = json.loads(result)
        return result_dict
    except:
        return {
            "success": False,
            "error": traceback.format_exc(),
        }
