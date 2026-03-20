"""
FeynRules Agent

Main agent class for converting LaTeX Lagrangians to FeynRules .fr files.
Uses Google ADK + LiteLLM following the pattern from analysis_agent.

Simplified architecture:
- Only 3 basic tools: read, write, edit
- All task-specific logic in system prompt
"""

import os
import logging
import json
import uuid
import time
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.adk.tools.function_tool import FunctionTool
from google.genai.types import UserContent, Content, Part

# Import tools
from tools import (
    read, write, edit, madgraph_compile, madgraph_launch,
    generate_simulation_yaml, run_from_yaml, generate_ufo_model,
    validate_feynrules,
    read_event_index, madanalysis_process,
)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("feynrules_agent.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class FeynRulesAgent:
    """Agent for generating FeynRules .fr files from LaTeX Lagrangians."""

    def __init__(self, output_dir: str = "outputs", feynrules_reference: str = "feynrules_reference.md"):
        """
        Initialize FeynRules agent.

        Args:
            output_dir: Directory for saving generated .fr files
            feynrules_reference: Name of the FeynRules reference document to use
                                 (e.g., "feynrules_reference.md", "feynrules_reference_minimal.md", 
                                  "feynrules_reference_modified.md")
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Store reference document name
        self.feynrules_reference = feynrules_reference

        # Load configuration from .env
        self.model_name = os.getenv("COLLIDER_AGENT_MODEL", "gpt-4")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize session
        self.session_id = str(uuid.uuid4())
        self.session_history = {
            "session_id": self.session_id,
            "timestamp": time.strftime("%Y%m%d_%H%M%S"),
            "conversions": [],
            "model": self.model_name,
            "feynrules_reference": self.feynrules_reference
        }

        # Build ADK agent
        self.agent = self._build_adk_agent()

        logger.info(f"FeynRules Agent initialized (session: {self.session_id}, reference: {self.feynrules_reference})")

    def _build_adk_agent(self) -> LlmAgent:
        """Build the ADK agent with LiteLLM and tools."""
        # Initialize LiteLLM
        llm = LiteLlm(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url
        )

        # System prompt
        system_prompt = self._build_system_prompt()

        # Initialize tools list
        tools = []

        # === Basic File Tools + FeynRules + MadGraph5 + Simulation Workflow + MadAnalysis5 ===
        tools.extend([
            FunctionTool(func=read),
            FunctionTool(func=write),
            FunctionTool(func=edit),
            FunctionTool(func=generate_ufo_model),
            FunctionTool(func=validate_feynrules),
            FunctionTool(func=madgraph_compile),
            FunctionTool(func=madgraph_launch),
            FunctionTool(func=generate_simulation_yaml),
            FunctionTool(func=run_from_yaml),
            FunctionTool(func=read_event_index),
            FunctionTool(func=madanalysis_process),
        ])

        # Create LlmAgent
        agent = LlmAgent(
            model=llm,
            name="feynrules_agent",
            description="Generate FeynRules .fr model files from LaTeX Lagrangian descriptions",
            instruction=system_prompt,
            tools=tools
        )

        logger.info(f"Agent created with {len(tools)} tools using model {self.model_name}")
        return agent

    def _load_reference_doc(self, doc_name: str) -> str:
        """Load a reference document from the prompts directory.

        Note: Google ADK uses {variable} syntax for template substitution in instructions.
        We need to escape literal braces in the document by doubling them: { -> {{, } -> }}
        """
        # Try multiple possible locations for the prompts directory
        possible_paths = [
            Path(__file__).parent / "prompts" / doc_name,
            Path.cwd() / "prompts" / doc_name,
            self.output_dir.parent / "prompts" / doc_name,
        ]

        for doc_path in possible_paths:
            if doc_path.exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Escape braces to prevent ADK template substitution
                # ADK interprets {var} as template variables, so we need {{ and }} for literal braces
                content = content.replace("{", "{{").replace("}", "}}")
                logger.info(f"Loaded reference doc from {doc_path}")
                return content

        logger.warning(f"Reference doc '{doc_name}' not found in any of: {possible_paths}")
        return ""

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the agent.

        NOTE: Google ADK uses regex {+[^{}]*}+ for template substitution,
        which means ANY braces (even doubled like {{}}) will be parsed.
        We CANNOT include Mathematica code with braces directly in the instruction.
        Instead, we tell the agent to read the reference doc dynamically.
        """

        # Get the path to reference docs for the agent to read
        feynrules_ref_path = self._get_reference_doc_path(self.feynrules_reference)
        madgraph_ref_path = self._get_reference_doc_path("madgraph_reference.md")
        madanalysis_ref_path = self._get_reference_doc_path("madanalysis_reference.md")

        # Main prompt: workflow and responsibilities
        # IMPORTANT: No curly braces allowed in this string!
        main_prompt = f"""You are an expert particle physics simulation agent. Your task is to:
1. Convert LaTeX Lagrangian descriptions into complete, validated FeynRules .fr model files
2. Generate UFO models from FeynRules files
3. Run MadGraph5 simulations to generate physics events
4. When requested, run MadAnalysis5 to analyze events (cutflows, histograms, plots, invariant mass, etc.)

## IMPORTANT: Read Reference Documentation First

Before starting any task, read the relevant reference documents:
- **FeynRules**: Use `read("{feynrules_ref_path}")` for .fr file syntax
- **MadGraph5**: Use `read("{madgraph_ref_path}")` for event generation
- **MadAnalysis5**: Use `read("{madanalysis_ref_path}")` for analysis syntax

## Available Tools

### File Operations
- `read(file_path)` - Read files
- `write(file_path, content)` - Save files
- `edit(file_path, old_string, new_string)` - Modify files

### UFO Model Generation
- `generate_ufo_model(feynrules_model_path, lagrangian_symbol, ufo_path, rst_restriction_path=None)`
  - `feynrules_model_path`: Path to .fr model file — standalone and BSM extensions both accepted (SM.fr auto-loaded for extensions)
  - `lagrangian_symbol`: Lagrangian symbol from .fr file (e.g., "LSNP", "LNEWPHYSICS")
  - `ufo_path`: Output path for the generated UFO directory (e.g., "tools/assets/NP_S_UFO")
  - `rst_restriction_path`: Path to .rst restriction file (optional; SM restrictions auto-loaded for BSM extensions)
  - Returns: dict with success, ufo_path, message

### FeynRules Model Validation
- `validate_feynrules(feynrules_model_path, lagrangian_symbol)` - Validate .fr model for physical consistency
  - `feynrules_model_path`: Path to .fr file — standalone models and BSM extensions both accepted (SM.fr base loaded automatically for extensions)
  - `lagrangian_symbol`: Lagrangian variable name in .fr file (e.g., "LSM", "Lag")
  - Returns: dict with success, verdict, feynman_gauge/unitary_gauge (each with hermiticity, diagonal_quadratic_terms, diagonal_mass_terms, kinetic_term_normalisation), model_loading
  - success = True iff all 4 Unitary gauge checks pass (Feynman gauge is informational)
  - verdict = intelligent summary explaining the outcome (Goldstone mixing, field mixing, etc.)
  - Use after writing .fr file to check correctness before UFO generation

### MadGraph5 Process Compilation & Event Generation
- `madgraph_compile(ufo_model_path, process, target_path, definitions="")` - Compile a MG5 process
  - `ufo_model_path`: Path to UFO model directory (from FeynRules → UFO generation)
  - `process`: Process definition, one per line. First = `generate`, rest = `add process`
  - `target_path`: Where to download compiled process directory
  - `definitions`: Multiparticle definitions, one per line without `define` prefix
  - Returns: success, process_dir, message

- `madgraph_launch(process_dir, launch_commands, target_path, pdf_set="")` - Generate events from compiled process
  - `process_dir`: Path to compiled process directory (from `madgraph_compile`)
  - `launch_commands`: Launch body — answers to MG5 prompts in order: shower/detector settings or `done` to skip, `done` to skip card editing (enters parameter mode), `set` params, `done` to start run.
    **NEVER** put two consecutive `done` before `set` commands — the second `done` ends parameter editing!
  - `target_path`: Where to download output directory (with Events/)
  - `pdf_set`: LHAPDF PDF set name to install (e.g. `"LUXlep-NNPDF31_nlo_as_0118_luxqed"`). Must also set `pdlabel` and `lhaid` in launch_commands.
  - Returns: success, output_dir, message

### YAML Simulation Workflow (Recommended for structured simulations)
- `generate_simulation_yaml(yaml_path, process_name, model, processes, output_dir, ...)` - Create/append YAML config
  - Generates a structured simulation.yaml compatible with Workflow-Example schema
  - Supports: definitions, run_settings (shower/detector/nevents), physics_params, model_params, scan_params, cards
  - Use `append=True` to add multiple processes to one YAML file
  - Returns: success, yaml_path, process_name, message

- `run_from_yaml(yaml_path, process_name, event_set_name="14TeV", ...)` - Run simulation from YAML
  - Reads YAML config and builds MG5 scripts automatically
  - `mode="auto"` detects first-run vs add-events based on existing output
  - `mode="first_run"` forces import/generate/output + launch
  - `mode="add_events"` only re-launches (output dir must exist)
  - Override nevents with the `nevents` parameter
  - Returns: success, output_dir, message

**YAML Workflow** (preferred for repeatable simulations):
1. Use `generate_simulation_yaml()` to create the config
2. Use `run_from_yaml()` to execute
This separates configuration from execution and enables reproducibility.

### MadAnalysis5 Event Analysis (when user asks for analysis/plots/invariant mass)
- `read_event_index(yaml_path, process_name, event_set_name="14TeV")` - Find event file paths from event_index.yaml
  - Call after MadGraph has produced events; use the same process_name as in the simulation
  - Returns: success, event_files (list of paths), base_path, runs, message
- `madanalysis_process(events_path, script, target_path, level="parton")` - Run MadAnalysis5 analysis
  - `events_path`: Process directory from madgraph_launch (contains Events/)
  - `script`: MA5 commands with EVENTS_DIR placeholder (in curly braces) for event file paths.
    Do NOT include a `submit` command — it is appended automatically.
  - `target_path`: Where to download analysis output
  - `level`: "parton" (LHE), "hadron" (HepMC), "reco" (LHCO/ROOT)
  - Returns: dict with success, output_dir, message

## Complete Workflow

### Phase 1: FeynRules Model Generation
1. Read feynrules_reference.md
2. Parse the LaTeX Lagrangian and identify all fields and couplings
3. Generate complete .fr file following the patterns in the reference doc
4. Use `write()` to save to the user-specified path

### Phase 2: Model Validation (unless --skip-mathematica)
1. Use `validate_feynrules()` to validate the model
   - `feynrules_model_path`: Path to the .fr file (e.g., "models/HillModel.fr")
   - `lagrangian_symbol`: The Lagrangian variable name in .fr file (e.g., "LSM", "Lag")
   - Returns per-gauge results (Feynman + Unitary) with intelligent verdict summary
2. If validation fails (success=False), read the verdict for guidance on what to fix, then use `edit()` and re-validate

### Phase 3: UFO Generation (unless --skip-wolfram)
1. Use `generate_ufo_model()` to generate UFO model
   - `feynrules_model_path`: Path to the .fr file you created (e.g., "tools/assets/Scalar_Model.fr")
   - `lagrangian_symbol`: Lagrangian symbol from .fr file (e.g., "LSNP", "LNEWPHYSICS")
   - `ufo_path`: Output path (e.g., "tools/assets/NP_S_UFO")
   - `rst_restriction_path`: Optional path to restriction file (default: None)

### Phase 3.5: Understanding UFO Model (CRITICAL for MadGraph!)
**When given a UFO model path (either generated or provided by user), you MUST read the UFO files before generating MadGraph commands:**

1. **Read particles.py** to find particle names:
   ```
   read("<ufo_path>/particles.py")
   ```
   Look for particle definitions like:
   - `name = 'h0'` - This is the MG5 particle name to use in process commands
   - `pdg_code = 50001` - PDG code for setting masses/widths
   - `mass = Param.mH0` - Mass parameter name
   - `width = Param.WH0` - Width parameter name

2. **Read parameters.py** to find parameter names and blocks:
   ```
   read("<ufo_path>/parameters.py")
   ```
   Look for parameter definitions like:
   - `lhablock = 'YQLU'` - Block name for param_card
   - `lhacode = [2, 3]` - Indices in block (e.g., YQLU 2 3 for Y^q_L,ct)
   - `name = 'YQLct'` - Parameter name

3. **Map user's physics notation to MG5 parameter names**:
   - User says `Y^q_{{L,ut}}` → Find parameter with indices [1,3] in YQLU block
   - User says `Y^q_{{L,ct}}` → Find parameter with indices [2,3] in YQLU block
   - User says `Y^l_{{L,μμ}}` → Find parameter with indices [2,2] in YLLE block
   - User says `m_S` → Find mass parameter for the scalar particle

4. **Distinguish Signal vs Background processes**:
   - **Signal processes** (involve BSM particles): Use `import model /path/to/UFO`
   - **Background processes** (pure SM): Use `import model sm`

   Example: If user asks for both "pp→tS" (signal) and "pp→tt̄" (background):
   - Signal: `import model /path/to/UFO` then `generate p p > t h0, ...`
   - Background: `import model sm` then `generate p p > t t~, ...`

   **Generate separate MG5 scripts for signal and background processes!**

### Phase 4: MadGraph5 Simulation (unless --skip-madgraph)
**IMPORTANT**: Read madgraph_reference.md FIRST for complete syntax reference!

**Two-step workflow**: Compile the process first, then launch event generation.

**Step 1: Compile** — enumerate Feynman diagrams and compile matrix element code:
```python
result = madgraph_compile(
    ufo_model_path="/path/to/UFO",
    process="p p > t t~, t > b l+ vl, t~ > b~ l- vl~",
    target_path="tmp/pp_ttbar",
    definitions="l+ = e+ mu+\nl- = e- mu-\nvl = ve vm\nvl~ = ve~ vm~",
)
```

**Step 2: Launch** — generate Monte Carlo events:

**launch_commands state machine** (critical for correct format):
After `launch <dir>`, MG5 enters a sequence of interactive prompts.
Your `launch_commands` string must answer them in order:
```
MG5 prompt 1: shower/detector? → setting lines or `done` to skip
MG5 prompt 2: edit cards? → `done` to skip, enters parameter-setting mode
Now in parameter-setting mode → `set` commands here
`done` → start run
```
- Parton-level (no shower/detector): `done\nset nevents 500\nset ebeam1 500\ndone`
- With Pythia8+Delphes: `shower=Pythia8\ndetector=Delphes\ndone\nCMS\ndone\nset nevents 1000\ndone`
- **NEVER** put two consecutive `done` before `set` commands — the second `done` ends parameter editing!

```python
# Parton-level example
result = madgraph_launch(
    process_dir="tmp/pp_ttbar",
    launch_commands="done\nset nevents 1000\nset ebeam1 7000\nset ebeam2 7000\ndone",
    target_path="tmp/pp_ttbar",
)

# With shower+detector example
result = madgraph_launch(
    process_dir="tmp/pp_ttbar",
    launch_commands="shower=Pythia8\ndetector=Delphes\ndone\nCMS\ndone\nset nevents 1000\nset ebeam1 7000\nset ebeam2 7000\ndone",
    target_path="tmp/pp_ttbar",
)
```

**Or use YAML Workflow** (preferred for repeatable simulations):
1. Use `generate_simulation_yaml()` to create the config
2. Use `run_from_yaml()` to execute (calls compile + launch internally)

**Key MG5 Syntax Elements**:
- Multiparticle definitions: `l+ = e+ mu+ ta+`, `vl = ve vm vt`, `j = g u c d s u~ c~ d~ s~`
- Decay chains: `p p > t t~, t > b l+ vl, t~ > b~ l- vl~`
- Add charge-conjugate: second `add process` line in `process` parameter
- Pythia8 shower: `shower=Pythia8` in launch_commands
- Delphes detector: `detector=Delphes` then `done` then `CMS` then `done`
- Auto-width: `set param_card DECAY <pdg_code> Auto`
- Mass scan: `set param_card MASS <pdg_code> scan:[20,40,60,80,100]`
- SM parameters: `set param_card SMINPUTS 1 127.9` (for aEWM1)
- Masses: `set param_card MASS 6 172.76` (top), `set param_card MASS 5 4.2` (bottom)
- PDF sets: pass `pdf_set="LUXlep-NNPDF31_nlo_as_0118_luxqed"` and add `set run_card pdlabel lhapdf\nset run_card lhaid 82400` in launch_commands

**Example BSM signal** (compile + launch):
```python
# Step 1: Compile
madgraph_compile(
    ufo_model_path="/absolute/path/to/NP_S_UFO",
    process="p p > t h0, t > b l+ vl, h0 > mu+ mu-\np p > t~ h0, t~ > b~ l- vl~, h0 > mu+ mu-",
    target_path="tmp/pp_tS_signal",
    definitions="l+ = e+ mu+\nl- = e- mu-\nvl = ve vm\nvl~ = ve~ vm~\nj = g u c d s u~ c~ d~ s~",
)

# Step 2: Launch
madgraph_launch(
    process_dir="tmp/pp_tS_signal",
    launch_commands="shower=Pythia8\ndetector=Delphes\ndone\nCMS\ndone\nset nevents 100\nset ebeam1 7000\nset ebeam2 7000\nset param_card SMINPUTS 1 127.9\nset param_card MASS 6 172.76\nset param_card MASS 5 4.2\nset param_card YQLU 2 3 0.001\nset param_card YLLE 2 2 1.0\nset param_card MASS 50001 scan:[20,40,60,80,100,120,140,160]\nset param_card DECAY 50001 Auto\ndone",
    target_path="tmp/pp_tS_signal",
)
```

Generate separate compile+launch calls for signal and background processes!

3. Report the location of generated events (Events/run_xx/unweighted_events.lhe.gz or tag_1_delphes_events.root)

### Phase 5: MadAnalysis5 Analysis (when user asks for analysis, cutflows, histograms, plots, invariant mass and etc.)
1. Locate event files: use `read_event_index("event_index.yaml", process_name)` (process_name = MG5 output dir, e.g. from run_from_yaml output_dir)
2. If event_index.yaml is missing or path differs, infer event path from run_from_yaml/output_dir (e.g. output_dir/Events/run_01/...)
3. Read `madanalysis_reference.md` for MA5 command syntax (plot M(...), import, set, etc.)
4. Build MA5 script using EVENTS_DIR placeholder (in curly braces) for event file paths: import, set dataset type/lumi, define plots.
   Do NOT include a `submit` command — it is appended automatically by the runner.
5. Call `madanalysis_process(events_path, script, target_path, level=...)` with level "parton" for LHE, "hadron" for HepMC, "reco" for Delphes LHCO/ROOT
6. Report where the MA5 output (HTML/plots) was written

## Skip Flags
- `--skip-mathematica`: Skip model validation (validate_feynrules)
- `--skip-wolfram`: Skip UFO generation (uses generate_ufo_model)
- `--skip-madgraph`: Skip all MadGraph related steps

Report the final status including (all paths relative to project root):
- .fr file path (e.g., "tools/assets/Scalar_Model.fr") and validation status
- UFO model path (e.g., "tools/assets/NP_S_UFO") if generated
- Events file path (if MadGraph was run)
- MadAnalysis5 output path / plot summary (if MA5 was run)
"""

        return main_prompt

    def _get_reference_doc_path(self, doc_name: str) -> str:
        """Get the path to a reference document.

        Returns the path string for the agent to use with read().
        """
        possible_paths = [
            Path(__file__).parent / "prompts" / doc_name,
            Path.cwd() / "prompts" / doc_name,
            self.output_dir.parent / "prompts" / doc_name,
        ]

        for doc_path in possible_paths:
            if doc_path.exists():
                return str(doc_path.resolve())

        # Return a default path even if not found - agent will get an error
        return str(possible_paths[0])

    def _build_system_prompt_legacy(self) -> str:
        """Legacy method - kept for reference but not used.

        This approach of embedding the reference doc in instruction doesn't work
        because Google ADK's template substitution regex {+[^{}]*}+ matches
        Mathematica's curly braces and tries to replace them as variables.
        """

        main_prompt = """..."""  # Not used

        feynrules_ref = self._load_reference_doc("feynrules_reference.md")

        if feynrules_ref:
            return main_prompt + feynrules_ref
        else:
            logger.warning("FeynRules reference doc not found, using minimal inline reference")
            return main_prompt + """## Technical Reference (Minimal)

A complete .fr file must contain:
1. `M$ModelName` and `M$Information` - Model metadata
2. `M$ClassesDescription` - Particle definitions (F[n] fermions, S[n] scalars, V[n] vectors)
3. `M$Parameters` - Coupling constants, masses, widths (External/Internal types)
4. Lagrangian - Complete interaction terms

Key conventions:
- Spinor indices: sp, sp1, sp2
- Flavor indices: ii, jj
- Color indices: cc
- Lorentz indices: mu, nu
- Common functions: Ga (gamma), ProjM/ProjP (projectors), DC (covariant derivative), HC (hermitian conjugate)
- ALWAYS ensure Lagrangian is Hermitian with HC[] terms
"""

    def run(self, task: str, max_turns: int = 20) -> Dict[str, Any]:
        """
        Run the agent on a task.

        Args:
            task: Task description (e.g., "Convert <LaTeX> to .fr")
            max_turns: Maximum conversation turns

        Returns:
            Dictionary with results
        """
        from google.adk.runners import RunConfig
        from google.genai import types
        import asyncio

        logger.info(f"Running agent on task: {task[:100]}...")

        # Create runner
        runner = InMemoryRunner(agent=self.agent, app_name="feynrules_agent")

        # Create session
        asyncio.run(
            runner.session_service.create_session(
                app_name="feynrules_agent",
                user_id="user",
                session_id="default"
            )
        )

        # Create run config
        run_config = RunConfig(max_llm_calls=max_turns)

        # Create user message
        user_message = types.Content(
            role="user",
            parts=[types.Part(text=task)]
        )

        # Run agent
        try:
            final_response = None
            turn_count = 0

            for event in runner.run(
                user_id="user",
                session_id="default",
                new_message=user_message,
                run_config=run_config
            ):
                turn_count += 1

                if hasattr(event, 'content') and event.content:
                    # Log the event
                    logger.debug(f"Turn {turn_count}: {type(event).__name__}")

                    # Capture final response
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                final_response = part.text
                                logger.info(f"Agent response: {final_response[:200]}...")

            # Record in session history
            self.session_history["conversions"].append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task": task,
                "turns": turn_count,
                "response": final_response
            })

            return {
                "success": True,
                "response": final_response,
                "turns": turn_count,
                "session_id": self.session_id
            }

        except Exception as e:
            logger.error(f"Agent execution error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "session_id": self.session_id
            }

    def save_session(self, filename: Optional[str] = None):
        """Save session history to JSON file."""
        if filename is None:
            filename = f"session_{self.session_id}.json"

        filepath = self.output_dir / filename

        with open(filepath, 'w') as f:
            json.dump(self.session_history, f, indent=2)

        logger.info(f"Session saved to {filepath}")
        return filepath


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="FeynRules Agent - Convert LaTeX to .fr files"
    )
    parser.add_argument(
        "task",
        nargs="?",
        default="Convert $S \\bar{l}_i P_L l_j$ to FeynRules code",
        help="Task description, LaTeX to convert, or path to markdown file"
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Output directory for results"
    )
    # Default max_turns: env COLLIDER_AGENT_MAX_TURNS, else 20
    try:
        _default_max_turns = int(os.getenv("COLLIDER_AGENT_MAX_TURNS", "20"))
    except ValueError:
        _default_max_turns = 20
    parser.add_argument(
        "--max-turns",
        type=int,
        default=_default_max_turns,
        help="Maximum agent conversation turns (default from COLLIDER_AGENT_MAX_TURNS or 20)"
    )
    parser.add_argument(
        "--save-session",
        action="store_true",
        help="Save session history to JSON"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        default=None,
        help="Output file path for the generated .fr file"
    )
    parser.add_argument(
        "--skip-mathematica",
        action="store_true",
        help="Skip model validation"
    )
    parser.add_argument(
        "--skip-wolfram",
        action="store_true",
        help="Skip UFO generation"
    )
    parser.add_argument(
        "--skip-madgraph",
        action="store_true",
        help="Skip all MadGraph related steps"
    )
    parser.add_argument(
        "--feynrules-reference",
        default="feynrules_reference.md",
        help="FeynRules reference document to use (default: feynrules_reference.md)"
    )

    args = parser.parse_args()

    # Build task with optional instructions
    task = args.task

    # Check if task is a markdown file path
    if task.endswith('.md'):
        task_path = Path(task).expanduser()
        if task_path.exists():
            with open(task_path, 'r', encoding='utf-8') as f:
                task = f.read()
            logger.info(f"Loaded task from markdown file: {args.task}")

    # Add output file instruction if specified
    if args.output_file:
        task += f"\n\n请将最终 .fr 文件写入：{args.output_file}"

    # Add skip instructions based on flags
    skip_instructions = []
    if args.skip_mathematica:
        skip_instructions.append("不要做模型验证 (validate_feynrules)")
    if args.skip_wolfram:
        skip_instructions.append("不要生成 UFO")
    if args.skip_madgraph:
        skip_instructions.append("不要做任何 MadGraph 相关步骤")

    if skip_instructions:
        task += "\n\n" + "，".join(skip_instructions) + "。"

    # Create and run agent
    agent = FeynRulesAgent(
        output_dir=args.output_dir,
        feynrules_reference=args.feynrules_reference
    )
    result = agent.run(task=task, max_turns=args.max_turns)

    # Print result
    print("\n" + "="*80)
    print("AGENT RESULT")
    print("="*80)
    if result["success"]:
        print(f"\nResponse:\n{result['response']}")
        print(f"\nTurns: {result['turns']}")
    else:
        print(f"\nError: {result['error']}")
    print("="*80 + "\n")

    # Save session if requested
    if args.save_session:
        filepath = agent.save_session()
        print(f"Session saved to: {filepath}")


if __name__ == "__main__":
    main()
