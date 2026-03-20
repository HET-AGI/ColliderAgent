#!/usr/bin/env wolframscript
(* ::Package:: *)

(* ================================================= *)
(* FeynRules 模型自洽性检测脚本                       *)
(* ================================================= *)
(* 
   用法: wolframscript -script check_fr.wls <model.fr> [restriction.rst]
   
   该脚本加载 FeynRules, 再根据模型类型自动决定加载方式:
   - 独立模型 (含 M$GaugeGroups, 如 SM.fr): 仅加载该文件
   - 扩展模型 (如 output_modified 中的 NP 模型): 加载 SM.fr + 该文件
   
   自动检测 Lagrangian, 并在两种规范下运行自洽性检测 (同 validation.nb):
   
   检测项目:
   1. CheckHermiticity            - Lagrangian 是否 Hermitian
   2. CheckDiagonalQuadraticTerms - 二次项是否对角
   3. CheckDiagonalMassTerms      - 质量项是否对角
   4. CheckKineticTermNormalisation - 动能项归一化是否正确
   
   规范选取:
   - Feynman gauge  (FeynmanGauge = True)
   - Unitary gauge  (FeynmanGauge = False)
   
   每个检测输出 PASS 或 FAIL, 最后给出汇总结果。
   退出码: 0 = 全部通过, 1 = 有检测未通过或出错。
   
   示例:
     wolframscript -script check_fr.wls output_modified/model_1.fr
     wolframscript -script check_fr.wls Scalar_Model.fr Restriction.rst
*)


(* ========== 解析命令行参数 ========== *)
If[Length[$ScriptCommandLine] < 2,
  Print["用法: wolframscript -script check_fr.wls <model.fr> [restriction.rst] [--ufo-test=true/false] [--keep-ufo=true/false]"];
  Print["  <model.fr>         FeynRules 模型文件路径"];
  Print["  [restriction.rst]  (可选) 限制文件路径，不以 -- 开头"];
  Print["  --ufo-test=value   (可选) 是否运行 UFO 生成测试，默认 true"];
  Print["  --keep-ufo=value   (可选) UFO 测试后是否保留输出目录，默认 false"];
  Exit[1];
];

frFile = ExpandFileName[$ScriptCommandLine[[2]]];
restArgs = Drop[$ScriptCommandLine, 2];
rstFile = None;
If[Length[restArgs] >= 1 && !StringStartsQ[restArgs[[1]], "--"],
  rstFile = ExpandFileName[restArgs[[1]]];
  restArgs = Drop[restArgs, 1]
];

(* 只解析 --key=value 形式，不识别 --key value *)
ufoTestEnabled = True;
keepUFO = False;
parseBoolFlag[optName_String, optValue_String] := Module[{lc = ToLowerCase[StringTrim[optValue]]},
  Which[
    lc === "true", True,
    lc === "false", False,
    True,
    Print["[WARN] ", optName, " 仅支持 true/false, 当前值无效: ", optValue, "，将使用默认值。"];
    $Failed
  ]
];
optArgs = Select[restArgs, StringStartsQ[#, "--"] &];
Do[
  arg = optArgs[[idx]];
  If[StringStartsQ[arg, "--ufo-test="],
    parsed = parseBoolFlag["--ufo-test", StringDrop[arg, StringLength["--ufo-test="]]];
    If[parsed =!= $Failed, ufoTestEnabled = parsed];
  ,
    If[StringStartsQ[arg, "--keep-ufo="],
      parsed = parseBoolFlag["--keep-ufo", StringDrop[arg, StringLength["--keep-ufo="]]];
      If[parsed =!= $Failed, keepUFO = parsed];
    ,
      Print["[WARN] 未识别参数，已忽略: ", arg];
    ];
  ];
, {idx, Length[optArgs]}];

Print["[INFO] UFO 测试开关: --ufo-test=", ToString[ufoTestEnabled], ", --keep-ufo=", ToString[keepUFO]];
If[!ufoTestEnabled,
  Print["[INFO] 未进行 UFO 测试，不会生成 UFO 文件。"];
];

If[!FileExistsQ[frFile],
  Print["[ERROR] 文件不存在: ", frFile];
  Exit[1];
];


(* ========== 加载 FeynRules ========== *)
$FeynRulesPath = $UserBaseDirectory <> "/Applications/FeynRules";
<< FeynRules`;

(* ========== 设置工作目录为模型文件所在目录 ========== *)
SetDirectory[DirectoryName[frFile]];


(* ========== 读取模型文件内容 (用于后续自动检测) ========== *)
NPModelFile = FileNameTake[frFile];
frContent = ReadString[frFile];


(* ========== 加载模型 ========== *)
(* 
   判断模型类型: 
   - 如果 .fr 文件中定义了 M$GaugeGroups, 说明是包含完整规范结构的独立模型
     (如 SM.fr), 只需加载该文件本身;
   - 否则, 说明是扩展模型 (如 output_modified 中的 NP 模型), 
     需要先加载 SM.fr 再加载该文件。
*)
isStandaloneModel = StringContainsQ[frContent, "M$GaugeGroups"];
SMModelPath = $FeynRulesPath <> "/Models/SM/SM.fr";

If[isStandaloneModel,
  Print["[INFO] 检测到独立模型 (含 M$GaugeGroups), 仅加载: ", NPModelFile];
  LoadModel[NPModelFile];
,
  Print["[INFO] 检测到扩展模型, 加载: SM.fr + ", NPModelFile];
  LoadModel[SMModelPath, NPModelFile];
];


(* ========== 加载限制文件 ========== *)
If[rstFile =!= None,
  (* 用户指定了限制文件 *)
  If[FileExistsQ[rstFile],
    Print["[INFO] 加载限制文件: ", rstFile];
    LoadRestriction[rstFile];
  ,
    Print["[WARN] 限制文件不存在: ", rstFile];
  ];
,
  (* 在模型文件同目录下自动搜索 .rst 文件 *)
  localRst = FileNames["*.rst"];
  If[Length[localRst] > 0,
    Print["[INFO] 自动检测到限制文件: ", First[localRst]];
    LoadRestriction[First[localRst]];
  ];
];

(* 匹配赋值语句: LXyz := ... 或 LXyz = ... (行首) *)
lagMatches = StringCases[frContent,
  RegularExpression["(?m)^\\s*(L[A-Za-z]\\w*)\\s*:?="] :> "$1"];

(* 过滤掉明显不是 Lagrangian 的符号名 *)
lagMatches = Select[lagMatches,
  !StringMatchQ[#, "Load*" | "Latex*" | "List*" | "Log*" | "Length*"] &];

If[Length[lagMatches] == 0,
  Print["[ERROR] 未在模型文件中找到 Lagrangian 定义"];
  Exit[1];
];

(* 最后一个赋值通常是总 Lagrangian (各分量之和) *)
lagName = Last[lagMatches];
Print["[INFO] 检测到 Lagrangian: ", lagName];
Print["[INFO] 全部匹配到的 Lagrangian 符号: ", lagMatches];
Clear[LNP];
LNP := ToExpression[lagName];


(* ========== 直接运行检测 (避免封装带来的求值差异) ========== *)
(* 
   这里刻意采用与 validation.wls 一致的“直接调用”风格:
   result = CheckXxx[LNP]
   不使用字符串分发或封装函数, 以避免 Hold/上下文差异导致行为变化。
*)
isCheckPassed[result_] := TrueQ[result] || result === {} || result === 0;
isNoTermsPass[result_] := isCheckPassed[result] || result === Null;
isKineticCheckPassed[result_] := isNoTermsPass[result] ||
  (result =!= False && result =!= $Failed && result =!= $Aborted);

feynmanResults = {};
unitaryResults = {};


(* ========== 在两种规范下分别执行检测 ========== *)
FeynmanGauge = True;
Print[""];
Print["============================================"];
Print["  FeynRules 模型自洽性检测"];
Print["  模型:       ", NPModelFile];
Print["  Lagrangian: ", lagName];
Print["  规范:       Feynman gauge (FeynmanGauge = True)"];
Print["============================================"];
Print[""];

Print["---------- 1. CheckHermiticity ----------"];
result = CheckHermiticity[LNP];
passed = isCheckPassed[result];
AppendTo[feynmanResults, {"CheckHermiticity", passed}];
Print[">>> CheckHermiticity: ", If[passed, "PASS", "FAIL"]];
Print[""];

Print["---------- 2. CheckDiagonalQuadraticTerms ----------"];
result = CheckDiagonalQuadraticTerms[LNP];
passed = isNoTermsPass[result];
AppendTo[feynmanResults, {"CheckDiagonalQuadraticTerms", passed}];
Print[">>> CheckDiagonalQuadraticTerms: ", If[passed, "PASS", "FAIL"]];
Print[""];

Print["---------- 3. CheckDiagonalMassTerms ----------"];
result = CheckDiagonalMassTerms[LNP];
passed = isNoTermsPass[result];
AppendTo[feynmanResults, {"CheckDiagonalMassTerms", passed}];
Print[">>> CheckDiagonalMassTerms: ", If[passed, "PASS", "FAIL"]];
Print[""];

Print["---------- 4. CheckKineticTermNormalisation ----------"];
result = CheckKineticTermNormalisation[LNP];
passed = isKineticCheckPassed[result];
AppendTo[feynmanResults, {"CheckKineticTermNormalisation", passed}];
Print[">>> CheckKineticTermNormalisation: ", If[passed, "PASS", "FAIL"]];
Print[""];

FeynmanGauge = False;
Print[""];
Print["============================================"];
Print["  FeynRules 模型自洽性检测"];
Print["  模型:       ", NPModelFile];
Print["  Lagrangian: ", lagName];
Print["  规范:       Unitary gauge (FeynmanGauge = False)"];
Print["============================================"];
Print[""];

Print["---------- 1. CheckHermiticity ----------"];
result = CheckHermiticity[LNP];
passed = isCheckPassed[result];
AppendTo[unitaryResults, {"CheckHermiticity", passed}];
Print[">>> CheckHermiticity: ", If[passed, "PASS", "FAIL"]];
Print[""];

Print["---------- 2. CheckDiagonalQuadraticTerms ----------"];
result = CheckDiagonalQuadraticTerms[LNP];
passed = isNoTermsPass[result];
AppendTo[unitaryResults, {"CheckDiagonalQuadraticTerms", passed}];
Print[">>> CheckDiagonalQuadraticTerms: ", If[passed, "PASS", "FAIL"]];
Print[""];

Print["---------- 3. CheckDiagonalMassTerms ----------"];
result = CheckDiagonalMassTerms[LNP];
passed = isNoTermsPass[result];
AppendTo[unitaryResults, {"CheckDiagonalMassTerms", passed}];
Print[">>> CheckDiagonalMassTerms: ", If[passed, "PASS", "FAIL"]];
Print[""];

Print["---------- 4. CheckKineticTermNormalisation ----------"];
result = CheckKineticTermNormalisation[LNP];
passed = isKineticCheckPassed[result];
AppendTo[unitaryResults, {"CheckKineticTermNormalisation", passed}];
Print[">>> CheckKineticTermNormalisation: ", If[passed, "PASS", "FAIL"]];
Print[""];

(* ---------- 5. WriteUFO (可选) ---------- *)
(* UFO 输出到与 .fr 同目录。keep-ufo=true: 目录名为「模型名称_UFO」；keep-ufo=false: 加随机后缀以便区分，测试后删除 *)
ufoPassed = True;
If[ufoTestEnabled,
  Print["---------- 5. WriteUFO ----------"];
  SetDirectory[DirectoryName[frFile]];
  ufoBase = StringReplace[NPModelFile, ".fr" -> ""];
  ufoDirName = If[keepUFO,
    ufoBase <> "_UFO",
    ufoBase <> "_UFO_" <> StringJoin[RandomChoice[Join[CharacterRange["a", "z"], CharacterRange["0", "9"]], 8]]
  ];
  If[DirectoryQ[ufoDirName], DeleteDirectory[ufoDirName, DeleteContents -> True]];
  ufoResult = If[isStandaloneModel,
    Check[WriteUFO[LNP, Output -> ufoDirName], $Failed],
    Check[WriteUFO[LSM, LNP, Output -> ufoDirName], $Failed]
  ];
  ufoPassed = (ufoResult =!= $Failed);
  Print[">>> WriteUFO: ", If[ufoPassed, "PASS", "FAIL"]];
  If[ufoPassed,
    ufoAbsPath = FileNameJoin[{DirectoryName[frFile], ufoDirName}];
    If[keepUFO,
      Print["[INFO] UFO 文件已生成（与 .fr 同目录），输出目录: ", ufoAbsPath];
    ,
      If[DirectoryQ[ufoAbsPath], DeleteDirectory[ufoAbsPath, DeleteContents -> True]];
      Print["[INFO] UFO 测试通过，输出目录已删除（未保留）。"];
    ];
  ,
    (* WriteUFO 报错时不删除已生成/部分生成目录，便于排查 *)
    If[DirectoryQ[ufoDirName],
      ufoAbsPath = FileNameJoin[{DirectoryName[frFile], ufoDirName}];
      Print["[INFO] WriteUFO 未通过，已保留输出目录便于排查: ", ufoAbsPath];
    ];
  ];
  Print[""];
];


(* ========== 汇总报告 ========== *)
Print["============================================"];
Print["  测试结果汇总"];
Print["============================================"];
Print["  模型:       ", NPModelFile];
Print["  Lagrangian: ", lagName];

Print[""];
Print["  [ Feynman gauge ]"];
Do[
  {name, passed} = feynmanResults[[i]];
  Print["    ", If[passed, "[PASS]", "[FAIL]"], " ", name];
, {i, Length[feynmanResults]}];

Print[""];
Print["  [ Unitary gauge ]"];
Do[
  {name, passed} = unitaryResults[[i]];
  Print["    ", If[passed, "[PASS]", "[FAIL]"], " ", name];
, {i, Length[unitaryResults]}];

Print[""];
Print["  [ UFO generation ]"];
If[ufoTestEnabled,
  Print["    ", If[ufoPassed, "[PASS]", "[FAIL]"], " WriteUFO"];
  If[ufoPassed,
    If[keepUFO,
      Print["    [INFO] UFO 文件已生成（与 .fr 同目录），输出目录: ", FileNameJoin[{DirectoryName[frFile], StringReplace[NPModelFile, ".fr" -> ""] <> "_UFO"}]];
    ,
      Print["    [INFO] UFO 测试通过，输出已删除（未保留）。"];
    ];
  ,
    Print["    [INFO] UFO 未成功生成。"];
  ];
,
  Print["    [INFO] 未进行 UFO 测试，未生成 UFO 文件。"];
];

Print[""];
allPassed = And @@ Join[feynmanResults[[All, 2]], unitaryResults[[All, 2]]] && (If[ufoTestEnabled, ufoPassed, True]);
Print[If[allPassed,
  "结论: 所有检测均通过 (Feynman gauge + Unitary gauge" <> If[ufoTestEnabled, " + UFO", ""] <> ")。",
  "结论: 部分检测未通过。"]];

Exit[If[allPassed, 0, 1]];