# utils/wolfram_script_templates
__all__ = [
    "feynrules_validation_template",
    "ufo_generation_template",
]


def feynrules_validation_template(
    feynrules_model_path: str,
    lagrangian_symbol: str = "LSM",
    start_marker: str = "__JSON_START__",
    end_marker: str = "__JSON_END__",
)-> str:

    lagrangian_symbol = lagrangian_symbol.strip()

    return f"""
(* Initialize FeynRules *)
<< FeynRules`;

(* Result -- base fields; per-gauge checks added by runChecks *)
result = <|
    "success" -> False,
    "verdict" -> "Validation did not complete.",
    "model_name" -> "Unknown",
    "lagrangian_name" -> "{lagrangian_symbol}",
    "model_loading" -> <| "status" -> False, "message" -> Null |>
|>;

(* Output result JSON and exit *)
bail[] := (
    Print["{start_marker}"];
    Print[ExportString[result, "JSON", "Compact" -> True]];
    Print["{end_marker}"];
    Exit[]
);

(* 1. Model Loading *)
(* Auto-detect: standalone model (has M$GaugeGroups) vs BSM extension (needs SM.fr base) *)
frContent = Quiet[ReadString["{feynrules_model_path}"]];
If[!StringQ[frContent],
    result["model_loading", "message"] = "Cannot read model file: {feynrules_model_path}";
    result["verdict"] = "Model file unreadable.";
    bail[];
];
isStandaloneModel = StringContainsQ[frContent, "M$GaugeGroups"];

loadingStatus = Check[
    Block[{{$Output = {{}}}},
        If[isStandaloneModel,
            LoadModel["{feynrules_model_path}"],
            LoadModel[FileNameJoin[{{$FeynRulesPath, "Models", "SM", "SM.fr"}}], "{feynrules_model_path}"]
        ]
    ],
    $Failed
];

If[loadingStatus === $Failed,
    result["model_loading", "message"] = "LoadModel failed (Syntax error or missing dependencies).";
    result["verdict"] = "Model failed to load.";
    bail[];
];

result["model_loading", "status"] = True;
result["model_loading", "message"] = "Model loaded successfully";
If[ValueQ[M$ModelName], result["model_name"] = M$ModelName];

(* 2. Verify Lagrangian Symbol *)
If[OwnValues[{lagrangian_symbol}] === {{}},
    result["model_loading", "message"] = "The variable '{lagrangian_symbol}' is not defined in the model.";
    result["verdict"] = "Lagrangian symbol '{lagrangian_symbol}' not found in model.";
    bail[];
];

(* 3. Physical Validation — 4 checks x 2 gauges *)

(* Unified safe-call helper: captures return value, $MessageList diff, and Print output.
   OpenWrite[] may fail on restricted filesystems — falls back to suppressing output. *)
SetAttributes[safeCall, HoldFirst];
safeCall[func_] := Module[{{nc, ms, res, stream, prints = Null}},
    nc = Length[$MessageList];
    stream = Quiet[OpenWrite[]];
    If[Head[stream] === OutputStream,
        Block[{{$Output = {{stream}}}},
            res = Check[func, $Aborted];
        ];
        Close[stream];
        With[{{file = First@stream}},
            prints = Quiet[ReadString[file]];
            If[!StringQ[prints] || prints === "", prints = Null];
        ];
    ,
        Block[{{$Output = {{}}}},
            res = Check[func, $Aborted];
        ];
    ];
    ms = Drop[$MessageList, nc];
    <| "value" -> res,
       "messages" -> If[ms =!= {{}}, ToString /@ ms, {{}}],
       "prints" -> prints |>
];

(* Build an "inconclusive" result entry *)
inconclusiveEntry[label_, sc_] := <|
    "passed" -> False,
    "status" -> "inconclusive",
    "detail" -> StringJoin[label, " returned ", ToString[sc["value"]]],
    "messages" -> sc["messages"],
    "prints" -> sc["prints"]
|>;

(* Pass criteria — aligned with expert reference script *)
isCheckPassed[res_] := TrueQ[res] || res === {{}} || res === 0;
isNoTermsPass[res_] := isCheckPassed[res] || res === Null;
isKineticCheckPassed[res_] := isNoTermsPass[res] ||
    (res =!= False && res =!= $Failed && res =!= $Aborted);

(* Run all 4 checks for the current gauge setting.
   Returns <| "checks" -> <|...|>, "all_passed" -> bool |>. *)
runChecks[lag_] := Module[{{hermSC, hermVal, quadSC, quadVal, massSC, massVal,
                            normSC, normVal, checks = <||>, passList = {{}}}},

    (* 3.1 Hermiticity — returns list of non-Hermitian terms *)
    hermSC = safeCall[CheckHermiticity[lag]];
    hermVal = hermSC["value"];
    If[hermVal === $Aborted || !ListQ[hermVal],
        checks["hermiticity"] = inconclusiveEntry["CheckHermiticity", hermSC];
    ,
        If[hermVal === {{}},
            checks["hermiticity"] = <| "passed" -> True, "is_hermitian" -> True |>;
        ,
            checks["hermiticity"] = <| "passed" -> False, "is_hermitian" -> False,
                "non_hermitian_terms" -> (ToString /@ hermVal) |>;
        ];
    ];
    AppendTo[passList, isCheckPassed[hermVal]];

    (* 3.2 CheckDiagonalQuadraticTerms *)
    quadSC = safeCall[CheckDiagonalQuadraticTerms[lag]];
    quadVal = quadSC["value"];
    If[quadVal === $Aborted,
        checks["diagonal_quadratic_terms"] = inconclusiveEntry["CheckDiagonalQuadraticTerms", quadSC];
    ,
        checks["diagonal_quadratic_terms"] = <| "passed" -> isNoTermsPass[quadVal] |>;
    ];
    AppendTo[passList, isNoTermsPass[quadVal]];

    (* 3.3 CheckDiagonalMassTerms — always runs independently *)
    massSC = safeCall[CheckDiagonalMassTerms[lag]];
    massVal = massSC["value"];
    If[massVal === $Aborted,
        checks["diagonal_mass_terms"] = inconclusiveEntry["CheckDiagonalMassTerms", massSC];
    ,
        checks["diagonal_mass_terms"] = <| "passed" -> isNoTermsPass[massVal] |>;
    ];
    AppendTo[passList, isNoTermsPass[massVal]];

    (* Goldstone mixing: quadratic False + mass passed -> expected at classical level *)
    If[quadVal === False && isNoTermsPass[massVal],
        checks["diagonal_quadratic_terms", "warning"] =
            "Likely Goldstone-gauge boson mixing (expected at classical Lagrangian level).";
    ];

    (* 3.4 CheckKineticTermNormalisation *)
    normSC = safeCall[CheckKineticTermNormalisation[lag]];
    normVal = normSC["value"];
    If[normVal === $Aborted || normVal === $Failed,
        checks["kinetic_term_normalisation"] = inconclusiveEntry["CheckKineticTermNormalisation", normSC];
    ,
        checks["kinetic_term_normalisation"] = <| "passed" -> isKineticCheckPassed[normVal] |>;
        If[normVal === Null,
            checks["kinetic_term_normalisation", "warning"] =
                "CheckKineticTermNormalisation returned Null (treated as passed).";
        ];
    ];
    AppendTo[passList, isKineticCheckPassed[normVal]];

    <| "checks" -> checks, "all_passed" -> And @@ passList |>
];

(* Run in Feynman gauge *)
FeynmanGauge = True;
fgResult = runChecks[{lagrangian_symbol}];
result["feynman_gauge"] = fgResult["checks"];

(* Run in Unitary gauge *)
FeynmanGauge = False;
ugResult = runChecks[{lagrangian_symbol}];
result["unitary_gauge"] = ugResult["checks"];

(* 4. Final Determination *)
(* success: based on Unitary gauge — Feynman gauge Goldstone artifacts are benign *)
result["success"] = ugResult["all_passed"];

(* 5. Verdict — intelligent summary *)
Module[{{ugFails, fgFails, fgQuadGoldstone, fgDesc, ugDesc, hint}},
    ugFails = Select[
        {{"hermiticity", "diagonal_quadratic_terms", "diagonal_mass_terms", "kinetic_term_normalisation"}},
        result["unitary_gauge", #, "passed"] =!= True &
    ];
    fgFails = Select[
        {{"hermiticity", "diagonal_quadratic_terms", "diagonal_mass_terms", "kinetic_term_normalisation"}},
        result["feynman_gauge", #, "passed"] =!= True &
    ];
    fgQuadGoldstone = MemberQ[fgFails, "diagonal_quadratic_terms"] &&
        StringQ[result["feynman_gauge", "diagonal_quadratic_terms", "warning"]];

    Which[
        ugFails === {{}} && fgFails === {{}},
            result["verdict"] = "All checks pass in both gauges.",

        ugFails === {{}} && fgFails === {{"diagonal_quadratic_terms"}} && fgQuadGoldstone,
            result["verdict"] = "Model is valid. Feynman gauge shows expected Goldstone-gauge boson mixing in quadratic terms.",

        ugFails === {{}},
            fgDesc = If[fgQuadGoldstone,
                StringRiffle[DeleteCases[fgFails, "diagonal_quadratic_terms"], ", "] <>
                    " (+ expected Goldstone mixing in quadratic terms)",
                StringRiffle[fgFails, ", "]
            ];
            result["verdict"] = "Model is valid (Unitary gauge clean). Feynman gauge issues: " <> fgDesc <> ".",

        MemberQ[ugFails, "hermiticity"],
            result["verdict"] = "Lagrangian is not Hermitian -- model has errors that must be fixed.",

        True,
            ugDesc = StringRiffle[ugFails, ", "];
            hint = Which[
                SubsetQ[ugFails, {{"diagonal_quadratic_terms", "diagonal_mass_terms"}}],
                    " Physical field mixing likely present; mass matrix may need diagonalisation.",
                MemberQ[ugFails, "diagonal_quadratic_terms"] && !MemberQ[ugFails, "diagonal_mass_terms"],
                    " Quadratic terms not diagonal but mass terms OK; check scalar-vector mixing.",
                MemberQ[ugFails, "kinetic_term_normalisation"] && Length[ugFails] === 1,
                    " Kinetic terms not canonically normalised; check field definitions.",
                True,
                    ""
            ];
            result["verdict"] = "Unitary gauge failed: " <> ugDesc <> "." <> hint;
    ];
];

bail[];
"""


def ufo_generation_template(
    model_path: str,
    lagrangian_symbol: str = "LSNP",
    ufo_output_name: str = "NP_S_UFO",
    restriction_path: str = "",
    start_marker: str = "__JSON_START__",
    end_marker: str = "__JSON_END__",
)-> str:

    lagrangian_symbol = lagrangian_symbol.strip()

    # Build restriction loading block
    restriction_block = ""
    if restriction_path:
        restriction_block = f'LoadRestriction["{restriction_path}"];'

    return f"""
(* Initialize FeynRules *)
<< FeynRules`;

(* Result container *)
result = <|
    "success" -> False,
    "message" -> "UFO generation did not complete."
|>;

(* Output result JSON and exit *)
bail[] := (
    Print["{start_marker}"];
    Print[ExportString[result, "JSON", "Compact" -> True]];
    Print["{end_marker}"];
    Exit[]
);

(* 1. Auto-detect: standalone model (has M$GaugeGroups) vs BSM extension *)
frContent = Quiet[ReadString["{model_path}"]];
If[!StringQ[frContent],
    result["message"] = "Cannot read model file: {model_path}";
    bail[];
];
isStandaloneModel = StringContainsQ[frContent, "M$GaugeGroups"];

(* 2. Load Model *)
loadingStatus = Check[
    Block[{{$Output = {{}}}},
        If[isStandaloneModel,
            LoadModel["{model_path}"],
            LoadModel[FileNameJoin[{{$FeynRulesPath, "Models", "SM", "SM.fr"}}], "{model_path}"]
        ]
    ],
    $Failed
];

If[loadingStatus === $Failed,
    result["message"] = "LoadModel failed (syntax error or missing dependencies).";
    bail[];
];

(* 3. Load Restrictions *)
{restriction_block}
If[!isStandaloneModel,
    LoadRestriction[
        FileNameJoin[{{$FeynRulesPath, "Models", "SM", "Massless.rst"}}],
        FileNameJoin[{{$FeynRulesPath, "Models", "SM", "DiagonalCKM.rst"}}]
    ];
];

(* 4. Verify Lagrangian Symbol *)
If[OwnValues[{lagrangian_symbol}] === {{}},
    result["message"] = "Lagrangian symbol '{lagrangian_symbol}' is not defined in the model.";
    bail[];
];

(* 5. Write UFO *)
If[isStandaloneModel,
    WriteUFO[{lagrangian_symbol}, Output -> "{ufo_output_name}"],
    WriteUFO[LSM, {lagrangian_symbol}, Output -> "{ufo_output_name}"]
];

(* 6. Check output *)
If[DirectoryQ["{ufo_output_name}"],
    result["success"] = True;
    result["message"] = "UFO model generated successfully.";
,
    result["message"] = "WriteUFO completed but output directory '{ufo_output_name}' not found.";
];

bail[];
"""
