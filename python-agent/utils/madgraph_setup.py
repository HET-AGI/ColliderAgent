"""
MadGraph Environment Setup

Orchestrates complete MadGraph environment setup including:
- MadGraph5_aMC@NLO installation
- Pythia8 installation
- Delphes installation

Can be used as a standalone script or imported as a tool for the agent.

Usage:
    # As a tool
    from utils.madgraph_setup import setup_madgraph_environment
    result = setup_madgraph_environment()

    # As a script
    python utils/madgraph_setup.py
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from google.adk.tools import ToolContext
except ImportError:
    ToolContext = Any

# Import installers
try:
    from utils.install_madgraph import MadGraphInstaller
    from utils.install_pythia import PythiaInstaller
    from utils.install_delphes import DelphesInstaller
except ImportError:
    # Handle relative imports
    from install_madgraph import MadGraphInstaller
    from install_pythia import PythiaInstaller
    from install_delphes import DelphesInstaller


def setup_madgraph_environment(
    install_dir: str = "tools/madgraph",
    install_pythia: bool = True,
    install_delphes: bool = True,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Complete MadGraph environment setup.

    This is a FunctionTool that can be called by the agent to set up
    the complete MadGraph5_aMC@NLO environment including Pythia8 and Delphes.

    Args:
        install_dir: Directory to install MadGraph (default: tools/madgraph)
        install_pythia: Install Pythia8 for parton shower (default: True)
        install_delphes: Install Delphes for detector simulation (default: True)
        tool_context: ADK tool context (auto-injected)

    Returns:
        dict: {
            "success": bool,
            "mg5_installed": bool,
            "mg5_path": str,
            "pythia_installed": bool,
            "pythia_path": str,
            "delphes_installed": bool,
            "delphes_path": str,
            "detector_cards": list,
            "message": str,
            "errors": list
        }

    Example:
        >>> result = setup_madgraph_environment()
        >>> if result["success"]:
        ...     print(f"MadGraph installed at {result['mg5_path']}")
        ...     print(f"Pythia8: {result['pythia_installed']}")
        ...     print(f"Delphes: {result['delphes_installed']}")
    """
    logger.info("="*60)
    logger.info("Starting MadGraph environment setup")
    logger.info("="*60)

    result = {
        "success": False,
        "mg5_installed": False,
        "mg5_path": "",
        "pythia_installed": False,
        "pythia_path": "",
        "delphes_installed": False,
        "delphes_path": "",
        "detector_cards": [],
        "message": "",
        "errors": []
    }

    # Phase 1: Install MadGraph
    logger.info("\n[1/3] Installing MadGraph5_aMC@NLO...")
    logger.info("-" * 60)

    try:
        mg_installer = MadGraphInstaller(install_dir=install_dir)
        mg_result = mg_installer.install()

        result["mg5_installed"] = mg_result["success"]
        result["mg5_path"] = mg_result.get("mg5_path", "")

        if mg_result["success"]:
            logger.info(f"✓ MadGraph installed: {mg_result['mg5_path']}")

            # Add to PATH
            path_result = mg_installer.add_to_path()
            if path_result["success"]:
                logger.info(f"✓ Added to environment: {path_result['message']}")
        else:
            error_msg = f"MadGraph installation failed: {mg_result['message']}"
            logger.error(f"✗ {error_msg}")
            result["errors"].append(error_msg)
            result["message"] = error_msg
            return result

    except Exception as e:
        error_msg = f"MadGraph installation error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        result["errors"].append(error_msg)
        result["message"] = error_msg
        return result

    # Phase 2: Install Pythia8
    if install_pythia and result["mg5_path"]:
        logger.info("\n[2/3] Installing Pythia8...")
        logger.info("-" * 60)

        try:
            pythia_installer = PythiaInstaller(mg5_path=result["mg5_path"])

            # Check if already installed
            check_result = pythia_installer.check_installation()
            if check_result["installed"]:
                logger.info(f"✓ Pythia8 already installed: {check_result['pythia_path']}")
                result["pythia_installed"] = True
                result["pythia_path"] = check_result["pythia_path"]
            else:
                # Install
                pythia_result = pythia_installer.install(install_lhapdf=True)
                result["pythia_installed"] = pythia_result["success"]
                result["pythia_path"] = pythia_result.get("pythia_path", "")

                if pythia_result["success"]:
                    logger.info(f"✓ Pythia8 installed: {pythia_result['pythia_path']}")
                    if pythia_result.get("lhapdf_installed"):
                        logger.info("✓ LHAPDF also installed")
                else:
                    warning_msg = f"Pythia8 installation failed: {pythia_result['message']}"
                    logger.warning(f"⚠ {warning_msg}")
                    result["errors"].append(warning_msg)

        except Exception as e:
            warning_msg = f"Pythia8 installation error: {str(e)}"
            logger.warning(warning_msg, exc_info=True)
            result["errors"].append(warning_msg)
    else:
        logger.info("\n[2/3] Skipping Pythia8 installation")

    # Phase 3: Install Delphes
    if install_delphes and result["mg5_path"]:
        logger.info("\n[3/3] Installing Delphes...")
        logger.info("-" * 60)

        try:
            delphes_installer = DelphesInstaller(mg5_path=result["mg5_path"])

            # Check if already installed
            check_result = delphes_installer.check_installation()
            if check_result["installed"]:
                logger.info(f"✓ Delphes already installed: {check_result['delphes_path']}")
                result["delphes_installed"] = True
                result["delphes_path"] = check_result["delphes_path"]
                result["detector_cards"] = check_result["detector_cards"]
                logger.info(f"  Found {len(result['detector_cards'])} detector cards")
            else:
                # Install
                delphes_result = delphes_installer.install()
                result["delphes_installed"] = delphes_result["success"]
                result["delphes_path"] = delphes_result.get("delphes_path", "")
                result["detector_cards"] = delphes_result.get("detector_cards", [])

                if delphes_result["success"]:
                    logger.info(f"✓ Delphes installed: {delphes_result['delphes_path']}")
                    logger.info(f"  Found {len(result['detector_cards'])} detector cards")
                else:
                    warning_msg = f"Delphes installation failed: {delphes_result['message']}"
                    logger.warning(f"⚠ {warning_msg}")
                    result["errors"].append(warning_msg)

        except Exception as e:
            warning_msg = f"Delphes installation error: {str(e)}"
            logger.warning(warning_msg, exc_info=True)
            result["errors"].append(warning_msg)
    else:
        logger.info("\n[3/3] Skipping Delphes installation")

    # Final summary
    logger.info("\n" + "="*60)
    logger.info("Setup Summary")
    logger.info("="*60)
    logger.info(f"MadGraph:  {'✓ Installed' if result['mg5_installed'] else '✗ Failed'}")
    logger.info(f"Pythia8:   {'✓ Installed' if result['pythia_installed'] else '○ Not installed'}")
    logger.info(f"Delphes:   {'✓ Installed' if result['delphes_installed'] else '○ Not installed'}")

    # Determine overall success
    result["success"] = result["mg5_installed"]  # At minimum, MG5 must be installed

    if result["success"]:
        result["message"] = f"MadGraph environment setup complete. MG5 at {result['mg5_path']}"
        if result["errors"]:
            result["message"] += f" (with {len(result['errors'])} warnings)"
    else:
        result["message"] = "Setup failed. See errors for details."

    logger.info(f"\n{result['message']}")
    logger.info("="*60)

    return result


def check_madgraph_environment(
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Check current MadGraph environment status.

    This is a FunctionTool that checks if MadGraph and associated tools
    are already installed.

    Args:
        tool_context: ADK tool context (auto-injected)

    Returns:
        dict: {
            "mg5_available": bool,
            "mg5_path": str,
            "pythia_available": bool,
            "pythia_path": str,
            "delphes_available": bool,
            "delphes_path": str,
            "detector_cards": list,
            "message": str
        }
    """
    logger.info("Checking MadGraph environment...")

    result = {
        "mg5_available": False,
        "mg5_path": "",
        "pythia_available": False,
        "pythia_path": "",
        "delphes_available": False,
        "delphes_path": "",
        "detector_cards": [],
        "message": ""
    }

    # Check MadGraph
    try:
        from utils.install_madgraph import MadGraphInstaller
    except ImportError:
        from install_madgraph import MadGraphInstaller

    mg_installer = MadGraphInstaller()
    mg_path = mg_installer._find_mg5_executable()

    if mg_path and Path(mg_path).exists():
        result["mg5_available"] = True
        result["mg5_path"] = mg_path
        logger.info(f"✓ MadGraph found at {mg_path}")

        # Check Pythia8
        try:
            from utils.install_pythia import PythiaInstaller
        except ImportError:
            from install_pythia import PythiaInstaller

        pythia_installer = PythiaInstaller(mg5_path=mg_path)
        pythia_check = pythia_installer.check_installation()
        result["pythia_available"] = pythia_check["installed"]
        result["pythia_path"] = pythia_check.get("pythia_path", "")

        if pythia_check["installed"]:
            logger.info(f"✓ Pythia8 found at {pythia_check['pythia_path']}")

        # Check Delphes
        try:
            from utils.install_delphes import DelphesInstaller
        except ImportError:
            from install_delphes import DelphesInstaller

        delphes_installer = DelphesInstaller(mg5_path=mg_path)
        delphes_check = delphes_installer.check_installation()
        result["delphes_available"] = delphes_check["installed"]
        result["delphes_path"] = delphes_check.get("delphes_path", "")
        result["detector_cards"] = delphes_check.get("detector_cards", [])

        if delphes_check["installed"]:
            logger.info(f"✓ Delphes found at {delphes_check['delphes_path']}")
            logger.info(f"  {len(result['detector_cards'])} detector cards available")

        result["message"] = "MadGraph environment is set up"
    else:
        result["message"] = "MadGraph not found. Run setup_madgraph_environment() to install."
        logger.info(f"✗ {result['message']}")

    return result


def main():
    """CLI entry point for setup."""
    import argparse

    parser = argparse.ArgumentParser(description="Setup MadGraph environment")
    parser.add_argument("--install-dir", default="tools/madgraph", help="Installation directory")
    parser.add_argument("--skip-pythia", action="store_true", help="Skip Pythia8 installation")
    parser.add_argument("--skip-delphes", action="store_true", help="Skip Delphes installation")
    parser.add_argument("--check", action="store_true", help="Check current environment")

    args = parser.parse_args()

    if args.check:
        result = check_madgraph_environment()
        print(f"\n{result['message']}")
        if result["mg5_available"]:
            print(f"  MadGraph: {result['mg5_path']}")
            print(f"  Pythia8:  {'Yes' if result['pythia_available'] else 'No'}")
            print(f"  Delphes:  {'Yes' if result['delphes_available'] else 'No'}")
        return

    result = setup_madgraph_environment(
        install_dir=args.install_dir,
        install_pythia=not args.skip_pythia,
        install_delphes=not args.skip_delphes
    )

    print(f"\n{'='*60}")
    if result["success"]:
        print("✓ Setup complete!")
        print(f"  MadGraph: {result['mg5_path']}")
        if result["pythia_installed"]:
            print(f"  Pythia8:  {result['pythia_path']}")
        if result["delphes_installed"]:
            print(f"  Delphes:  {result['delphes_path']}")
    else:
        print("✗ Setup failed")
        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(f"  - {error}")
        exit(1)


if __name__ == "__main__":
    main()
