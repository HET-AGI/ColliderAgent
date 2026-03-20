<!-- prettier-ignore -->
<div align="center">

# ⚛ Collider-Agent

**面向对撞机物理及更广泛领域的端到端自动化框架**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-7c3aed)](https://claude.ai/code)
![Status](https://img.shields.io/badge/状态-beta-orange)

> 从 LaTeX 拉格朗日量到可发表的图像——全流程自动化。

[概述](#概述) • [快速开始](#快速开始) • [安装](#安装) • [示例](#示例提示词) • [Python Agent](#python-agent) • [引用](#引用)

[English](README.md)

<img src="images/architecture.svg" alt="Architecture" width="900" />

</div>


## 概述

Collider-Agent 使 AI 编程智能体（Claude Code、Cursor、Windsurf 等）能够自主复现物理论文中的对撞机唯象学结果。它结合了专用子智能体与可复用技能模块，通过 [Magnus](https://github.com/Rise-AGI/magnus) 云平台与标准高能物理工具对接——**无需在本地安装任何 HEP 软件**。

**完整流程，全程自动化：**

- 解析 LaTeX 拉格朗日量，生成 FeynRules 模型文件
- 验证模型并为 MadGraph5 生成 UFO 输出
- 使用 MadGraph5 + Pythia8 进行部分子级和强子级事例产生
- 使用 Delphes 进行探测器模拟，使用 MadAnalysis5 施加分析截断
- 生成运动学分布图、截断流表格、参数空间排除等图像

## 路线图

| 状态 | 功能 |
|:---:| --- |
| ✅ | 从 LaTeX 拉格朗日量生成 FeynRules 模型 |
| ✅ | FeynRules 模型验证（厄密性、质量对角化、动能项归一化） |
| ✅ | 为 MadGraph5 生成 UFO 模型 |
| ✅ | MadGraph5 事例产生（含 Pythia8 部分子簇射） |
| ✅ | Delphes 探测器模拟 |
| ✅ | MadAnalysis5 普通模式分析 |
| ✅ | 全流程多智能体编排 |
| ⬜ | MadAnalysis5 专家模式支持 |
| ⬜ | Pythia 等工具的精细参数调节 |
| ⬜ | 更多论文复现示例（欢迎贡献！） |

## 安装

### 前提条件

- [Claude Code](https://claude.ai/code) — 推荐使用；完整支持子智能体与技能模块

  > 其他支持技能的智能体也可使用（仅限技能，不含子智能体）：Cursor、Windsurf、Gemini CLI、Cline、Goose、Roo Code 等，[详见下表](#支持的智能体及其全局技能路径)

- Python 3.10+（需要 `magnus-sdk>=0.7.0`）

### 配置步骤

**1. 克隆仓库：**

```bash
git clone https://github.com/HET-AGI/ColliderAgent.git
cd ColliderAgent
```

**2. 连接 Magnus 平台：**

首先安装 Magnus SDK：

```bash
pip install magnus-sdk
```

<details>
<summary>☁️ 选项 A：连接现有云实例</summary>

若您已有云端 Magnus 实例，使用以下命令登录：

```bash
magnus login
```

按提示输入服务器地址和 API 密钥，后续所有命令将自动路由至远端后端。

</details>

<details>
<summary>🖥️ 选项 B：本地部署</summary>

**额外前提条件：** Docker（守护进程已运行）、Node.js（可选，用于启用 Web UI）

启动本地后端：

```bash
magnus local start
```

此命令将拉取 Magnus 源码、安装后端依赖、在端口 `8017` 启动服务，并创建本地数据库和用户账户。若已安装 Node.js，Web UI 将同时在 `http://localhost:3011` 启动。

验证安装：

```bash
magnus run hello-world
```

成功运行后将输出 `Hello from Magnus!`。

</details>

> 完整 Magnus 文档及部署选项，请参阅 [github.com/Rise-AGI/magnus](https://github.com/Rise-AGI/magnus)。

**3. 将智能体和技能复制到您的智能体配置目录。**

对于 **Claude Code**（完整支持：子智能体 + 技能）：

```bash
cp -r src/agents ~/.claude/agents
cp -r src/skills ~/.claude/skills
```

对于**其他智能体**（仅技能）：

```bash
# 将 <skills-path> 替换为您的智能体对应的全局技能路径（见下表）
cp -r src/skills <skills-path>
```

<a id="支持的智能体及其全局技能路径"></a>

**支持的智能体及其全局技能路径：**

| 智能体 | 全局技能路径 |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |
| GitHub Copilot | `~/.copilot/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Cline / Warp | `~/.agents/skills/` |
| Goose | `~/.config/goose/skills/` |
| Roo Code | `~/.roo/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Codex | `~/.codex/skills/` |

> [!TIP]
> 也支持项目级安装。将 `src/skills/` 复制到工作目录根目录下的 `.claude/skills/`（或对应智能体的目录），可将技能限定在该项目范围内使用。

**4. 重启您的智能体**以加载新的智能体和技能。

**5.（可选）激活 Wolfram Engine 许可证：**

<details>
<summary>🔬 配置 Mathematica / Wolfram Engine 许可证</summary>

FeynRules 相关蓝图（`feynrules-model-validator`、`ufo-generator`）需要 Wolfram Engine 许可证。由于许可证绑定的是**容器**的机器标识而非宿主机，激活必须在容器内部进行。

1. 在 [wolfram.com/engine/free-license](https://wolfram.com/engine/free-license) 注册免费 Wolfram ID

2. 在容器内运行激活：

```bash
mkdir -p ~/.wolfram-container-license
docker run -it --rm \
  -v ~/.wolfram-container-license:/root/.WolframEngine/Licensing \
  git.pku.edu.cn/het-agi/mma-het:latest wolframscript
```

3. 按照交互式提示输入您的 Wolfram ID 和密码。

许可证文件（`mathpass`）将写入宿主机的 `~/.wolfram-container-license/`，后续所有 FeynRules 蓝图运行将自动挂载该目录。此步骤仅需执行一次。

</details>

## 快速开始

最快的体验方式是直接运行一个标准模型双轻子不变质量图——经典的部分子级验证——从命令行一键执行：

```bash
claude -p "Plot the dilepton invariant mass distribution for parton-level pp -> l+l- process at the 14 TeV LHC in the SM." --dangerously-bypass-permissions
```

此命令以非交互方式运行完整流程：MadGraph5 通过 [Magnus](https://github.com/rise-agi/magnus) 产生事例，智能体在当前工作目录生成归一化的 $m_{\ell\ell}$ 直方图。

## 使用方法

### 基本工作流程

1. 准备一个详细的 Markdown 提示词（例如 `prompt.md`），描述您想运行的对撞机分析，包括拉格朗日量、对撞过程、事例选择和参数扫描策略——就像撰写研究笔记或论文草稿一样（参见 `paper-reproduction/` 中的示例）

2. 启动智能体并提供提示词：

```bash
claude -p "Execute the analysis following prompt.md"
```

3. 系统将编排完整流程：
   - 解析拉格朗日量并生成 FeynRules 模型
   - 验证并生成 UFO 模型
   - 使用 Pythia8 / Delphes 运行 MadGraph5 模拟
   - 使用 MadAnalysis5 施加分析截断
   - 生成分析输出（运动学分布图、参数排除区域等）

### 单项子任务

智能体也可用于独立子任务，无需运行完整的唯象学流程，例如：

- 将标准 LaTeX 物理符号写成的拉格朗日量翻译为 FeynRules `.fr` 模型文件
- 基于 UFO 模型文件在 LHC 上产生某一过程的事例
- 使用 MadAnalysis5 分析蒙特卡洛事例，生成运动学分布图

### 示例提示词

`paper-reproduction/` 目录包含用于复现以下论文图像的示例提示词：

| arXiv ID | 研究主题 | 图编号 |
|---|---|---|
| [hep-ph/9909255](paper-reproduction/9909255/) | KK 引力子塔影响下的 $e^+ e^- \to \mu^+ \mu^-$ | 2 |
| [1308.2209](paper-reproduction/1308.2209/) | LHC 上的重中微子产生 | 3 |
| [1605.02910](paper-reproduction/1605.02910/) | $U(1)'$ 模型 Drell-Yan 过程的参数排除区域 | 1, 10 |
| [1701.05379](paper-reproduction/1701.05379/) | ALP 有效场论与对撞机信号 | 8 |
| [1811.07920](paper-reproduction/1811.07920/) | $U_1$ 轻子夸克模型 mono-$\tau$ 搜寻的参数排除区域 | 3 |
| [2005.06475](paper-reproduction/2005.06475/) | 使用 `LUXlep` PDF 的轻子夸克产生过程 | 2 |
| [2103.02708](paper-reproduction/2103.02708/) | SSM 和 $E_6$ 启发 $Z'$ 情景下 $pp \to Z' \to \ell^+\ell^-$ | 4 |
| [2104.05720](paper-reproduction/2104.05720/) | 未来 μ 子对撞机上通过 $\mu^+\mu^- \to b\bar{b}$ 搜寻轻子夸克 | 11, 12 |

## 项目结构

```
ColliderAgent/
├── src/
│   ├── agents/                        # 子智能体定义（Claude Code）
│   │   ├── model-generator.md
│   │   ├── collider-simulator.md
│   │   ├── event-analyzer.md
│   │   └── pheno-analyzer.md
│   └── skills/                        # 智能体技能模块（适用于所有智能体）
│       ├── feynrules-model-generator/
│       ├── feynrules-model-validator/
│       ├── ufo-generator/
│       ├── madgraph-simulator/
│       ├── madanalysis-analyzer/
│       ├── pheno-pipeline-orchestrator/
│       └── magnus/
├── python-agent/                      # 独立 ADK 智能体（Python API）
├── scripts/                           # Magnus 云端蓝图脚本
├── paper-reproduction/                # 论文复现示例提示词
│   ├── 1308.2209/
│   ├── 1605.02910/
│   └── ...
├── pyproject.toml
└── README.md
```

## 子智能体

> [!NOTE]
> 子智能体目前仅 Claude Code 支持。其他智能体的用户可直接通过各自的技能调用机制使用技能模块。

| 智能体 | 功能描述 |
| --- | --- |
| `model-generator` | LaTeX → FeynRules → UFO 完整流程 |
| `collider-simulator` | MadGraph5 事例产生（含 Pythia8 / Delphes） |
| `event-analyzer` | MadAnalysis5 截断流与直方图分析 |
| `pheno-analyzer` | 编排完整唯象学研究流程 |

## 技能模块

| 技能 | 功能描述 |
| --- | --- |
| `feynrules-model-generator` | 从 LaTeX 拉格朗日量生成 `.fr` 模型文件 |
| `feynrules-model-validator` | 通过 Mathematica 验证 `.fr` 模型 |
| `ufo-generator` | 将 FeynRules 模型导出为 UFO 格式 |
| `madgraph-simulator` | 运行 MadGraph5_aMC@NLO 事例产生 |
| `madanalysis-analyzer` | 执行截断流分析并生成直方图 |
| `pheno-pipeline-orchestrator` | 协调端到端唯象学流程 |
| `magnus` | 与 Magnus 云端 HEP 平台交互 |

## Python Agent

除基于技能的接口外，ColliderAgent 还提供一个**独立 Python ADK 智能体**和一套 **Magnus 云端蓝图脚本**，供需要直接编程访问流程的用户使用——无需借助 Claude Code 或其他 AI 编程助手。

| 模块 | 功能描述 |
|---|---|
| [`python-agent/`](python-agent/) | 接受自然语言物理任务、通过 Python API 编排完整流程的 Google ADK 智能体。包含基于 `uv` 的环境配置、交互式 `CLI.py` 以及完整测试套件。 |
| [`scripts/`](scripts/) | 由 Magnus 蓝图容器执行的入口脚本。每个脚本对应一个具名蓝图（`validate-feynrules`、`generate-ufo`、`madgraph-compile` 等），由智能体工具调用。 |

> [!NOTE]
> 若您只通过 Claude Code（或其他 AI 智能体）使用 Collider-Agent，无需关注这两个目录。它们面向编程访问、自定义集成和流程开发场景。

详细安装和使用说明请参阅各模块的 README：
- [python-agent/README.md](python-agent/README.md)
- [scripts/README.md](scripts/README.md)

## 引用

如果您在研究中使用了 Collider-Agent，请引用：

```bibtex
@article{Qiu:2026iby,
    author = "Qiu, Shi and Cai, Zeyu and Wei, Jiashen and Li, Zeyu and Yin, Yixuan and Cao, Qing-Hong and Liu, Chang and Luo, Ming-xing and Yuan, Xing-Bo and Zhu, Hua Xing",
    title = "{An End-to-end Architecture for Collider Physics and Beyond}",
    eprint = "2603.14553",
    archivePrefix = "arXiv",
    primaryClass = "hep-ph",
    reportNumber = "CPTNP-2026-012",
    month = "3",
    year = "2026",
    url = "https://github.com/HET-AGI/ColliderAgent"
}
```

同时请引用分析中使用的 HEP 工具，包括 [FeynRules](https://arxiv.org/abs/1310.1921)、[MadGraph5_aMC@NLO](https://github.com/restrepo/madgraph)、[Pythia8](https://pythia.org/)、[Delphes](https://github.com/delphes/delphes) 和 [MadAnalysis5](https://github.com/MadAnalysis/madanalysis5)。

## 致谢

感谢 [FeynRules](https://arxiv.org/abs/1310.1921)、[MadGraph5_aMC@NLO](https://github.com/restrepo/madgraph)、[Pythia8](https://pythia.org/)、[Delphes](https://github.com/delphes/delphes) 和 [MadAnalysis5](https://github.com/MadAnalysis/madanalysis5) 的开发者，正是他们出色的工具使本工作成为可能。
