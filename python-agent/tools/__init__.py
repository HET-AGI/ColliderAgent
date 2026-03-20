"""
Collider Agent Tools

Tool set for FeynRules model generation, MadGraph5 simulation, and MadAnalysis5 analysis.

Available tools:
- read: Read file contents
- write: Write content to file
- edit: Perform string replacement in file
- generate_ufo_model: Generate UFO model from FeynRules .fr file
- validate_feynrules: Validate .fr model for physical consistency
- madgraph_compile: Compile a MadGraph5 process (model + processes → process directory)
- madgraph_launch: Generate events from a compiled process directory
- generate_simulation_yaml: Create YAML-based simulation configuration
- run_from_yaml: Run MadGraph5 simulation from YAML configuration
- read_event_index: Parse event_index.yaml to locate event files for a process
- madanalysis_process: Run MadAnalysis5 analysis and produce plots/cutflows
"""

from .file_tools import read, write, edit
from .feynrules_to_ufo import generate_ufo_model
from .feynrules_validation import validate_feynrules
from .madgraph_tools import madgraph_compile, madgraph_launch
from .simulation_yaml_to_madgraph import generate_simulation_yaml, run_from_yaml
from .madanalysis_tools import read_event_index, madanalysis_process

__all__ = [
    "read",
    "write",
    "edit",
    "generate_ufo_model",
    "validate_feynrules",
    "madgraph_compile",
    "madgraph_launch",
    "generate_simulation_yaml",
    "run_from_yaml",
    "read_event_index",
    "madanalysis_process",
]
