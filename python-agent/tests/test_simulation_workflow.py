#!/usr/bin/env python3
"""
Tests for the YAML-based simulation workflow.

Tests cover:
- YAML generation and roundtrip (generate_simulation_yaml)
- MG5 script building (_build_setup_script, _build_launch_script)
- Config loading and validation (_load_config, _validate_config)
- Run mode detection (_is_first_run)
- Compatibility with Workflow-Example simulation.yaml schema

Usage:
    pytest tests/test_simulation_workflow.py -v
    python tests/test_simulation_workflow.py
"""

from pathlib import Path

import yaml
import pytest

from tools.simulation_yaml_to_madgraph import (
    generate_simulation_yaml,
    run_from_yaml,
    _build_setup_script,
    _build_launch_script,
    _load_config,
    _validate_config,
    _resolve_model_path,
    _is_first_run,
    _get_next_run_number,
)


# ---------------------------------------------------------------------------
# Test generate_simulation_yaml
# ---------------------------------------------------------------------------

class TestGenerateSimulationYaml:
    """Tests for generate_s`imulation_yaml()."""

    def test_basic_generation(self, tmp_path):
        """Test basic YAML generation with minimal arguments."""
        yaml_path = str(tmp_path / "sim.yaml")
        result = generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt",
        )

        assert result["success"] is True
        assert result["process_name"] == "pp_to_tt"
        assert Path(yaml_path).exists()

        # Load and verify structure
        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        assert "pp_to_tt" in data
        assert isinstance(data["pp_to_tt"], list)
        assert len(data["pp_to_tt"]) == 1

        entry = data["pp_to_tt"][0]
        assert "14TeV" in entry

        config = entry["14TeV"]
        assert config["model"] == "sm"
        assert config["processes"] == ["p p > t t~"]
        assert config["output_dir"] == "outputs/pp_to_tt"

    def test_default_values(self, tmp_path):
        """Test that default run_settings and physics_params are populated."""
        yaml_path = str(tmp_path / "sim.yaml")
        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_ee",
            model="sm",
            processes=["p p > e+ e-"],
            output_dir="outputs/pp_to_ee",
        )

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        config = data["pp_to_ee"][0]["14TeV"]

        # Check defaults
        assert config["run_settings"]["shower"] == "OFF"
        assert config["run_settings"]["detector"] == "OFF"
        assert config["run_settings"]["analysis"] == "OFF"
        assert config["run_settings"]["nevents"] == 10000
        assert config["physics_params"]["ebeam1"] == 6500.0
        assert config["physics_params"]["ebeam2"] == 6500.0

    def test_custom_settings(self, tmp_path):
        """Test generation with custom run_settings and physics_params."""
        yaml_path = str(tmp_path / "sim.yaml")
        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt_3l",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt_3l",
            event_set_name="13TeV",
            definitions=["p = p b b~"],
            run_settings={
                "shower": "Pythia8",
                "detector": "Delphes",
                "nevents": 100000,
            },
            physics_params={
                "ebeam1": 6500.0,
                "ebeam2": 6500.0,
                "MT": 172.76,
            },
            model_params={"MH": 125.0},
            scan_params={"mH0": [20, 40, 60, 80]},
            extra_commands=["set ptj 20"],
            card={"delphes": "cards/delphes_card.dat"},
        )

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        config = data["pp_to_tt_3l"][0]["13TeV"]
        assert config["definitions"] == ["p = p b b~"]
        assert config["run_settings"]["shower"] == "Pythia8"
        assert config["run_settings"]["detector"] == "Delphes"
        assert config["run_settings"]["nevents"] == 100000
        assert config["physics_params"]["MT"] == 172.76
        assert config["model_params"]["MH"] == 125.0
        assert config["scan_params"]["mH0"] == [20, 40, 60, 80]
        assert config["extra_commands"] == ["set ptj 20"]
        assert config["card"]["delphes"] == "cards/delphes_card.dat"

    def test_append_new_process(self, tmp_path):
        """Test appending a new process to existing YAML."""
        yaml_path = str(tmp_path / "sim.yaml")

        # Create initial YAML
        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt",
        )

        # Append a second process
        result = generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_ee",
            model="sm",
            processes=["p p > e+ e-"],
            output_dir="outputs/pp_to_ee",
            append=True,
        )

        assert result["success"] is True

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        assert "pp_to_tt" in data
        assert "pp_to_ee" in data

    def test_append_new_event_set(self, tmp_path):
        """Test appending a new event set to an existing process."""
        yaml_path = str(tmp_path / "sim.yaml")

        # Create initial YAML
        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt_14",
            event_set_name="14TeV",
        )

        # Append a new event set to the same process
        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt_13",
            event_set_name="13TeV",
            append=True,
        )

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        assert len(data["pp_to_tt"]) == 2
        event_set_names = []
        for entry in data["pp_to_tt"]:
            event_set_names.extend(entry.keys())
        assert "14TeV" in event_set_names
        assert "13TeV" in event_set_names

    def test_replace_existing_event_set(self, tmp_path):
        """Test that appending with the same event_set_name replaces it."""
        yaml_path = str(tmp_path / "sim.yaml")

        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt_v1",
            event_set_name="14TeV",
        )

        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt_v2",
            event_set_name="14TeV",
            append=True,
        )

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        # Should still be 1 entry, not 2
        assert len(data["pp_to_tt"]) == 1
        assert data["pp_to_tt"][0]["14TeV"]["output_dir"] == "outputs/pp_to_tt_v2"

    def test_creates_parent_directories(self, tmp_path):
        """Test that parent directories are created if needed."""
        yaml_path = str(tmp_path / "subdir" / "deep" / "sim.yaml")
        result = generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="test",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/test",
        )
        assert result["success"] is True
        assert Path(yaml_path).exists()

    def test_overwrite_without_append(self, tmp_path):
        """Test that without append=True, file is overwritten."""
        yaml_path = str(tmp_path / "sim.yaml")

        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt",
        )

        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_ee",
            model="sm",
            processes=["p p > e+ e-"],
            output_dir="outputs/pp_to_ee",
        )

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        # Only the second process should exist
        assert "pp_to_ee" in data
        assert "pp_to_tt" not in data


# ---------------------------------------------------------------------------
# Test script builders
# ---------------------------------------------------------------------------

class TestBuildSetupScript:
    """Tests for _build_setup_script()."""

    def test_basic_setup(self):
        """Test basic setup script generation."""
        config = {
            "model": "sm",
            "processes": ["p p > t t~"],
        }
        script = _build_setup_script(config, "outputs/pp_to_tt")

        assert "import model sm" in script
        assert "generate p p > t t~" in script
        assert "output outputs/pp_to_tt" in script

    def test_with_definitions(self):
        """Test setup script with multi-particle definitions."""
        config = {
            "model": "sm",
            "definitions": ["p = p b b~", "l+ = e+ mu+"],
            "processes": ["p p > t t~"],
        }
        script = _build_setup_script(config, "outputs/test")

        assert "define p = p b b~" in script
        assert "define l+ = e+ mu+" in script

    def test_multiple_processes(self):
        """Test setup script with multiple processes."""
        config = {
            "model": "sm",
            "processes": ["p p > t t~", "p p > t t~ j"],
        }
        script = _build_setup_script(config, "outputs/test")

        assert "generate p p > t t~" in script
        assert "add process p p > t t~ j" in script

    def test_ufo_model_path(self):
        """Test setup script with UFO model path."""
        config = {
            "model": "/path/to/MyModel_UFO",
            "processes": ["p p > x1 x1~"],
        }
        script = _build_setup_script(config, "outputs/test")

        assert "import model /path/to/MyModel_UFO" in script


class TestBuildLaunchScript:
    """Tests for _build_launch_script()."""

    def test_basic_launch(self):
        """Test basic launch script generation."""
        config = {
            "run_settings": {"nevents": 10000},
            "physics_params": {"ebeam1": 6500, "ebeam2": 6500},
        }
        script = _build_launch_script(config, "outputs/test")

        assert "launch outputs/test" in script
        assert "set nevents 10000" in script
        assert "set ebeam1 6500" in script
        assert "set ebeam2 6500" in script
        # Should end with "done"
        lines = script.strip().split("\n")
        assert lines[-1] == "done"

    def test_shower_detector(self):
        """Test launch script with shower and detector settings."""
        config = {
            "run_settings": {
                "shower": "Pythia8",
                "detector": "Delphes",
                "analysis": "OFF",
                "nevents": 1000,
            },
        }
        script = _build_launch_script(config, "outputs/test")

        assert "shower=Pythia8" in script
        assert "detector=Delphes" in script
        assert "analysis=OFF" in script

    def test_model_params(self):
        """Test launch script with param_card parameters."""
        config = {
            "model_params": {"MH": 125.0, "MX1": 500},
        }
        script = _build_launch_script(config, "outputs/test")

        assert "set param_card MH 125.0" in script
        assert "set param_card MX1 500" in script

    def test_scan_params(self):
        """Test launch script with parameter scan."""
        config = {
            "scan_params": {"mH0": [20, 40, 60, 80, 100]},
        }
        script = _build_launch_script(config, "outputs/test")

        assert "set param_card mH0 scan:[20,40,60,80,100]" in script

    def test_delphes_card(self):
        """Test launch script with Delphes card path."""
        config = {
            "card": {"delphes": "cards/delphes_card_CMS.dat"},
            "run_settings": {"detector": "Delphes"},
        }
        script = _build_launch_script(config, "outputs/test")

        assert "cards/delphes_card_CMS.dat" in script

    def test_extra_commands(self):
        """Test launch script with extra commands."""
        config = {
            "extra_commands": ["set ptj 20", "set etaj 5.0"],
        }
        script = _build_launch_script(config, "outputs/test")

        assert "set ptj 20" in script
        assert "set etaj 5.0" in script

    def test_complete_launch_script(self):
        """Test a complete launch script with all options."""
        config = {
            "run_settings": {
                "shower": "Pythia8",
                "detector": "Delphes",
                "analysis": "OFF",
                "nevents": 50000,
            },
            "physics_params": {
                "ebeam1": 7000,
                "ebeam2": 7000,
            },
            "model_params": {"MT": 172.76},
            "scan_params": {},
            "extra_commands": ["set ptj 30"],
            "card": {"delphes": "cards/delphes_card.dat"},
        }
        script = _build_launch_script(config, "outputs/pp_to_tt")

        lines = script.strip().split("\n")
        assert lines[0] == "launch outputs/pp_to_tt"
        assert "shower=Pythia8" in script
        assert "detector=Delphes" in script
        assert "set nevents 50000" in script
        assert "set ebeam1 7000" in script
        assert "set param_card MT 172.76" in script
        assert "set ptj 30" in script


# ---------------------------------------------------------------------------
# Test config loading/validation
# ---------------------------------------------------------------------------

class TestLoadConfig:
    """Tests for _load_config()."""

    def test_load_valid_config(self, tmp_path):
        """Test loading a valid config from YAML."""
        yaml_path = str(tmp_path / "sim.yaml")
        data = {
            "pp_to_tt": [
                {"14TeV": {"model": "sm", "processes": ["p p > t t~"], "output_dir": "out"}},
                {"13TeV": {"model": "sm", "processes": ["p p > t t~"], "output_dir": "out2"}},
            ]
        }
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        config = _load_config(yaml_path, "pp_to_tt", "14TeV")
        assert config["model"] == "sm"

        config2 = _load_config(yaml_path, "pp_to_tt", "13TeV")
        assert config2["output_dir"] == "out2"

    def test_load_missing_process(self, tmp_path):
        """Test that missing process raises ValueError."""
        yaml_path = str(tmp_path / "sim.yaml")
        data = {"pp_to_tt": [{"14TeV": {"model": "sm"}}]}
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        with pytest.raises(ValueError, match="not found"):
            _load_config(yaml_path, "nonexistent", "14TeV")

    def test_load_missing_event_set(self, tmp_path):
        """Test that missing event set raises ValueError."""
        yaml_path = str(tmp_path / "sim.yaml")
        data = {"pp_to_tt": [{"14TeV": {"model": "sm"}}]}
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        with pytest.raises(ValueError, match="not found"):
            _load_config(yaml_path, "pp_to_tt", "99TeV")


class TestValidateConfig:
    """Tests for _validate_config()."""

    def test_valid_config(self):
        """Test that valid config passes validation."""
        config = {"model": "sm", "processes": ["p p > t t~"], "output_dir": "out"}
        _validate_config(config)  # Should not raise

    def test_missing_fields(self):
        """Test that missing required fields raise ValueError."""
        with pytest.raises(ValueError, match="Missing required"):
            _validate_config({"model": "sm"})

    def test_empty_processes(self):
        """Test that empty processes list raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            _validate_config({"model": "sm", "processes": [], "output_dir": "out"})


# ---------------------------------------------------------------------------
# Test helper functions
# ---------------------------------------------------------------------------

class TestResolveModelPath:
    """Tests for _resolve_model_path()."""

    def test_builtin_model(self):
        assert _resolve_model_path("sm") == "sm"
        assert _resolve_model_path("mssm") == "mssm"

    def test_absolute_path(self):
        assert _resolve_model_path("/path/to/UFO") == "/path/to/UFO"

    def test_relative_path(self):
        result = _resolve_model_path("models/MyUFO")
        assert Path(result).is_absolute()


class TestIsFirstRun:
    """Tests for _is_first_run()."""

    def test_no_output_dir(self, tmp_path):
        assert _is_first_run(str(tmp_path / "nonexistent")) is True

    def test_empty_events_dir(self, tmp_path):
        events = tmp_path / "Events"
        events.mkdir()
        assert _is_first_run(str(tmp_path)) is True

    def test_with_run_dirs(self, tmp_path):
        run_dir = tmp_path / "Events" / "run_01"
        run_dir.mkdir(parents=True)
        assert _is_first_run(str(tmp_path)) is False


class TestGetNextRunNumber:
    """Tests for _get_next_run_number()."""

    def test_no_events_dir(self, tmp_path):
        assert _get_next_run_number(str(tmp_path)) == 1

    def test_existing_runs(self, tmp_path):
        for i in [1, 2, 3]:
            (tmp_path / "Events" / f"run_{i:02d}").mkdir(parents=True)
        assert _get_next_run_number(str(tmp_path)) == 4


# ---------------------------------------------------------------------------
# Test YAML roundtrip compatibility
# ---------------------------------------------------------------------------

class TestYamlCompatibility:
    """Test that generated YAML is compatible with the expected schema."""

    def test_roundtrip(self, tmp_path):
        """Generate YAML, reload, verify full structure."""
        yaml_path = str(tmp_path / "simulation.yaml")

        generate_simulation_yaml(
            yaml_path=yaml_path,
            process_name="pp_to_tt_3l",
            model="sm",
            processes=["p p > t t~"],
            output_dir="outputs/pp_to_tt",
            event_set_name="14TeV",
            definitions=["p = p b b~"],
            run_settings={
                "shower": "Pythia8",
                "detector": "Delphes",
                "analysis": "OFF",
                "nevents": 100000,
            },
            physics_params={
                "aEWM1": 127.9,
                "MT": 172.76,
                "ebeam1": 7000.0,
                "ebeam2": 7000.0,
            },
            model_params={},
            scan_params={},
            extra_commands=[],
            card={"delphes": "path/to/card.dat"},
        )

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        # Validate schema structure
        assert isinstance(data, dict)
        process = data["pp_to_tt_3l"]
        assert isinstance(process, list)

        event_set = process[0]
        assert isinstance(event_set, dict)
        assert "14TeV" in event_set

        config = event_set["14TeV"]
        assert config["model"] == "sm"
        assert config["definitions"] == ["p = p b b~"]
        assert config["processes"] == ["p p > t t~"]
        assert config["output_dir"] == "outputs/pp_to_tt"
        assert config["run_settings"]["shower"] == "Pythia8"
        assert config["physics_params"]["MT"] == 172.76
        assert config["card"]["delphes"] == "path/to/card.dat"

    def test_load_handwritten_yaml(self, tmp_path):
        """Test loading a hand-written YAML matching Workflow-Example format."""
        yaml_content = """
pp_to_tt_3l:
  - 14TeV:
      model: sm
      definitions:
        - "p = p b b~"
      processes:
        - "p p > t t~"
      output_dir: outputs/pp_to_tt
      run_settings:
        shower: Pythia8
        detector: Delphes
        analysis: "OFF"
        nevents: 100000
      physics_params:
        aEWM1: 127.9
        MT: 172.76
        ebeam1: 7000.0
        ebeam2: 7000.0
      model_params: {}
      scan_params: {}
      extra_commands: []
      card:
        delphes: path/to/card.dat
"""
        yaml_path = str(tmp_path / "handwritten.yaml")
        with open(yaml_path, "w") as f:
            f.write(yaml_content)

        # Load it using our internal function
        config = _load_config(yaml_path, "pp_to_tt_3l", "14TeV")
        _validate_config(config)

        assert config["model"] == "sm"
        assert config["processes"] == ["p p > t t~"]
        assert config["run_settings"]["nevents"] == 100000

        # Build scripts from it
        setup = _build_setup_script(config, config["output_dir"])
        assert "import model sm" in setup
        assert "define p = p b b~" in setup

        launch = _build_launch_script(config, config["output_dir"])
        assert "shower=Pythia8" in launch
        assert "set nevents 100000" in launch


# ---------------------------------------------------------------------------
# CLI runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
