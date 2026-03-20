# tools/feynrules_to_ufo.py
import json
import traceback
from typing import Any, Dict, Optional
from dotenv import load_dotenv; load_dotenv()
import magnus


__all__ = [
    "generate_ufo_model",
]


def generate_ufo_model(
    feynrules_model_path: str,
    lagrangian_symbol: str,
    ufo_path: str,
    rst_restriction_path: Optional[str] = None,
)-> Dict[str, Any]:
    """
    Generate UFO model from a FeynRules .fr file.

    Model type is auto-detected: if the .fr file contains M$GaugeGroups it is
    treated as a standalone model; otherwise it is a BSM extension and the
    FeynRules built-in SM.fr is loaded first automatically.

    Args:
        feynrules_model_path: Path to .fr model file — standalone and BSM
            extensions both accepted (SM.fr auto-loaded for extensions).
        lagrangian_symbol: Lagrangian symbol from .fr file
            (e.g., "LSNP", "LNEWPHYSICS").
        ufo_path: Output path for the generated UFO directory
            (e.g., "tools/assets/NP_S_UFO").
        rst_restriction_path: Path to .rst restriction file (optional;
            SM restrictions auto-loaded for BSM extensions).

    Returns:
        dict with keys:
            - success (bool): Whether generation succeeded
            - ufo_path (str): Path to generated UFO directory (if success)
            - message (str): Human-readable status message

    Example:
        >>> result = generate_ufo_model(
        ...     feynrules_model_path="tools/assets/Scalar_Model.fr",
        ...     lagrangian_symbol="LSNP",
        ...     ufo_path="tools/assets/NP_S_UFO",
        ... )
        >>> if result["success"]:
        ...     print(f"UFO model at: {result['ufo_path']}")
    """

    try:
        args = {
            "model": feynrules_model_path,
            "lagrangian": lagrangian_symbol,
            "output": ufo_path,
        }
        if rst_restriction_path:
            args["restriction"] = rst_restriction_path

        result = magnus.run_blueprint("generate-ufo", args=args)
        assert result is not None
        return json.loads(result)
    except:
        return {
            "success": False,
            "error": traceback.format_exc(),
        }
