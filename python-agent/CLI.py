#!/usr/bin/env python3
"""
Collider-Agent CLI Tool
自动配置和管理项目环境的命令行工具
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Optional, Dict, List


class Colors:
    """终端颜色类"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'

    @classmethod
    def section(cls, title: str) -> str:
        """生成步骤标题"""
        line = "═" * 60
        return f"\n{Colors.OKBLUE}{line}{Colors.ENDC}\n{Colors.BOLD}{Colors.HEADER}  {title}{Colors.ENDC}\n{Colors.OKBLUE}{line}{Colors.ENDC}\n"

    @classmethod
    def step(cls, num: int, total: int, title: str) -> str:
        """生成步骤指示器"""
        return f"{Colors.BOLD}{Colors.OKCYAN}[{num}/{total}] {title}{Colors.ENDC}"


class ColliderAgentCLI:
    """Collider-Agent CLI主类"""

    def __init__(self):
        self.project_root = Path(__file__).parent.resolve()
        self.env_file = self.project_root / ".env"
        self.venv_path = self.project_root / ".venv"

    def print_success(self, message: str):
        """打印成功消息"""
        print(f"  {Colors.OKGREEN}✓{Colors.ENDC} {message}")

    def print_error(self, message: str):
        """打印错误消息"""
        print(f"  {Colors.FAIL}✗{Colors.ENDC} {message}")

    def print_warning(self, message: str):
        """打印警告消息"""
        print(f"  {Colors.WARNING}⚠{Colors.ENDC} {message}")

    def print_info(self, message: str):
        """打印信息消息"""
        print(f"  {Colors.OKCYAN}ℹ{Colors.ENDC} {message}")

    def check_uv_installed(self) -> bool:
        """检查uv是否已安装"""
        return shutil.which("uv") is not None

    def install_uv(self) -> bool:
        """安装uv包管理器"""
        system = platform.system()

        self.print_info("正在安装uv包管理器...")

        try:
            if system == "Darwin" or system == "Linux":
                # macOS/Linux
                install_cmd = 'curl -LsSf https://astral.sh/uv/install.sh | sh'
                subprocess.run(install_cmd, shell=True, check=True)
            elif system == "Windows":
                # Windows
                install_cmd = 'powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
                subprocess.run(install_cmd, shell=True, check=True)
            else:
                self.print_error(f"不支持的操作系统: {system}")
                return False

            # 刷新PATH环境变量
            self.print_info("请重新启动终端或运行以下命令刷新PATH:")
            if system == "Windows":
                print("    $env:Path = [System.Environment]::GetEnvironmentVariable(\"Path\",\"Machine\") + \";\" + [System.Environment]::GetEnvironmentVariable(\"Path\",\"User\")")
            else:
                print("    source $HOME/.cargo/env")
                print("    或者")
                print("    source $HOME/.local/bin/env")

            self.print_success("uv安装完成！")
            return True

        except subprocess.CalledProcessError as e:
            self.print_error(f"uv安装失败: {e}")
            return False
        except Exception as e:
            self.print_error(f"安装过程中出现错误: {e}")
            return False

    def ask_user(self, question: str, default: bool = False) -> bool:
        """询问用户是/否问题"""
        default_str = "Y/n" if default else "y/N"
        response = input(f"{question} [{default_str}]: ").strip().lower()

        if not response:
            return default

        return response in ['y', 'yes', '是']

    def check_venv_configured(self) -> bool:
        """检查虚拟环境是否正确配置"""
        # 检查.venv目录是否存在
        if not self.venv_path.exists():
            return False

        # 检查python可执行文件是否存在
        if platform.system() == "Windows":
            python_path = self.venv_path / "Scripts" / "python.exe"
        else:
            python_path = self.venv_path / "bin" / "python"

        if not python_path.exists():
            return False

        # 检查关键依赖是否安装
        try:
            result = subprocess.run(
                [str(python_path), "-c", "import google_adk, litellm, sympy"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def setup_venv(self) -> bool:
        """使用uv sync配置虚拟环境"""
        self.print_info("正在配置虚拟环境...")

        try:
            result = subprocess.run(
                ["uv", "sync"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                self.print_success("虚拟环境配置完成！")
                return True
            else:
                self.print_error(f"虚拟环境配置失败: {result.stderr}")
                return False

        except Exception as e:
            self.print_error(f"配置虚拟环境时出错: {e}")
            return False

    def get_current_env_vars(self) -> Dict[str, str]:
        """获取当前环境变量配置"""
        env_vars = {}

        # 从系统环境变量读取
        system_vars = [
            "COLLIDER_AGENT_MODEL",
            "OPENAI_API_KEY",
            "OPENAI_BASE_URL",
            "DEFAULT_NEVENTS",
            "DEFAULT_EBEAM1",
            "DEFAULT_EBEAM2",
            "MG5_PATH",
            "FEYNRULES_PATH",
            "MAGNUS_ADDRESS",
            "MAGNUS_TOKEN",
            "MAGNUS_RESULT"
        ]

        for var in system_vars:
            if var in os.environ:
                env_vars[var] = os.environ[var]

        # 从.env文件读取
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()

        return env_vars

    def get_mg5_path(self) -> Optional[str]:
        """通过which命令获取MG5路径"""
        try:
            result = subprocess.run(
                ["which", "mg5_aMC"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                full_path = result.stdout.strip()
                # 过滤到bin结束
                if "/bin/" in full_path:
                    bin_index = full_path.index("/bin/")
                    return full_path[:bin_index + 4]  # 包含/bin
                return full_path
            return None

        except Exception:
            return None

    def format_model_name(self, model: str) -> str:
        """格式化模型名称，如果不是openai/开头则添加"""
        model = model.strip()
        if model.startswith("openai/"):
            return model
        else:
            return f"openai/{model}"

    def auto_configure_env(self) -> bool:
        """自动配置环境变量"""
        self.print_info("开始自动配置环境变量...\n")

        current_env = self.get_current_env_vars()
        new_env_vars = []

        # === AI配置部分 ===
        print(f"{Colors.BOLD}{Colors.OKCYAN}📊 AI 配置{Colors.ENDC}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.ENDC}")

        # COLLIDER_AGENT_MODEL
        if "COLLIDER_AGENT_MODEL" not in current_env:
            self.print_warning("未检测到 COLLIDER_AGENT_MODEL")
            model_input = input("  请输入模型名称 (例如: gemini-3-pro 或 gpt-4): ").strip()
            if model_input:
                formatted_model = self.format_model_name(model_input)
                new_env_vars.append(f"COLLIDER_AGENT_MODEL={formatted_model}")
                self.print_success(f"模型配置为: {formatted_model}")
        else:
            self.print_success(f"COLLIDER_AGENT_MODEL 已配置: {current_env['COLLIDER_AGENT_MODEL']}")

        # OPENAI_API_KEY
        if "OPENAI_API_KEY" not in current_env:
            self.print_warning("未检测到 OPENAI_API_KEY")
            api_key = input("  请输入 OpenAI API Key: ").strip()
            if api_key:
                new_env_vars.append(f"OPENAI_API_KEY={api_key}")
                self.print_success("API Key 已配置")
        else:
            self.print_success("OPENAI_API_KEY 已配置")

        # OPENAI_BASE_URL
        if "OPENAI_BASE_URL" not in current_env:
            self.print_warning("未检测到 OPENAI_BASE_URL")
            base_url = input("  请输入 Base URL (例如: https://yunwu.ai/v1): ").strip()
            if base_url:
                new_env_vars.append(f"OPENAI_BASE_URL={base_url}")
                self.print_success(f"Base URL 已配置: {base_url}")
        else:
            self.print_success(f"OPENAI_BASE_URL 已配置: {current_env['OPENAI_BASE_URL']}")

        # === 物理参数配置 ===
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}⚛️  物理参数配置{Colors.ENDC}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.ENDC}")

        # 添加默认值变量（直接写入，不询问用户）
        new_env_vars.extend([
            "DEFAULT_NEVENTS=10000",
            "DEFAULT_EBEAM1=6500",
            "DEFAULT_EBEAM2=6500"
        ])
        self.print_success("默认物理参数已添加 (NEVENTS=10000, EBEAM1=6500, EBEAM2=6500)")

        # === MadGraph5配置 ===
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}🔬 MadGraph5 配置{Colors.ENDC}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.ENDC}")

        if "MG5_PATH" not in current_env:
            mg5_path = self.get_mg5_path()
            if mg5_path:
                new_env_vars.append(f"MG5_PATH={mg5_path}")
                self.print_success(f"检测到 MG5_PATH: {mg5_path}")
            else:
                self.print_warning("未检测到 MadGraph5，跳过 MG5_PATH 配置")
        else:
            self.print_success(f"MG5_PATH 已配置: {current_env['MG5_PATH']}")

        # === MAGNUS云服务配置 ===
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}☁️  MAGNUS 云服务配置{Colors.ENDC}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.ENDC}")
        self.print_info("MAGNUS 用于在云端运行 FeynRules 验证")

        # 检查是否有任何MAGNUS变量缺失
        magnus_vars_missing = [
            var for var in ["MAGNUS_ADDRESS", "MAGNUS_TOKEN", "MAGNUS_RESULT"]
            if var not in current_env
        ]

        if magnus_vars_missing:
            self.print_warning(f"未检测到 MAGNUS 配置: {', '.join(magnus_vars_missing)}")
            should_configure = self.ask_user("是否配置 MAGNUS 云服务?", default=False)

            if should_configure:
                # 按顺序配置所有MAGNUS变量
                magnus_vars_config = [
                    ("MAGNUS_ADDRESS", "MAGNUS服务器地址 (例如: https://magnus.example.com)"),
                    ("MAGNUS_TOKEN", "MAGNUS认证令牌"),
                    ("MAGNUS_RESULT", "结果存储路径 (例如: /data/magnus/results.json)")
                ]

                for var, description in magnus_vars_config:
                    if var not in current_env:
                        user_input = input(f"  请输入 {description}: ").strip()
                        if user_input:
                            new_env_vars.append(f"{var}={user_input}")
                            self.print_success(f"{var} 已配置")
                        else:
                            self.print_warning(f"跳过 {var} 配置")
                    else:
                        self.print_success(f"{var} 已配置")
            else:
                self.print_info("跳过 MAGNUS 配置")
        else:
            self.print_success("所有 MAGNUS 变量已配置")

        # 写入.env文件
        print(f"\n{Colors.DIM}{'═' * 60}{Colors.ENDC}")
        if new_env_vars:
            self.write_env_file(new_env_vars, current_env)
            return True
        else:
            self.print_info("所有环境变量已配置，无需更新")
            return True

    def write_env_file(self, new_vars: List[str], existing_vars: Dict[str, str]):
        """写入.env文件"""
        self.print_info("\n正在写入 .env 文件...")

        try:
            # 读取现有内容
            existing_lines = []
            if self.env_file.exists():
                with open(self.env_file, 'r') as f:
                    existing_lines = f.readlines()

            # 解析新变量
            new_config = {}
            for var in new_vars:
                if '=' in var:
                    key, value = var.split('=', 1)
                    new_config[key.strip()] = value.strip()

            # 更新现有配置
            updated_lines = []
            processed_keys = set()

            for line in existing_lines:
                line_stripped = line.strip()
                if line_stripped and not line_stripped.startswith('#') and '=' in line_stripped:
                    key, _ = line_stripped.split('=', 1)
                    key = key.strip()
                    if key in new_config:
                        # 更新现有变量
                        updated_lines.append(f"{key}={new_config[key]}\n")
                        processed_keys.add(key)
                    else:
                        # 保留原有变量
                        updated_lines.append(line)
                else:
                    # 保留注释和空行
                    updated_lines.append(line)

            # 添加新变量
            for key, value in new_config.items():
                if key not in processed_keys:
                    updated_lines.append(f"{key}={value}\n")

            # 写入文件
            with open(self.env_file, 'w') as f:
                f.writelines(updated_lines)

            self.print_success(f".env 文件已更新，添加了 {len(new_vars)} 个变量")

        except Exception as e:
            self.print_error(f"写入 .env 文件时出错: {e}")

    def check_env_configured(self) -> bool:
        """检查必需的环境变量是否已配置"""
        required_vars = [
            "COLLIDER_AGENT_MODEL",
            "OPENAI_API_KEY"
        ]

        current_env = self.get_current_env_vars()

        missing_vars = [var for var in required_vars if var not in current_env]

        if missing_vars:
            self.print_warning(f"缺少必需的环境变量: {', '.join(missing_vars)}")
            return False

        self.print_success("所有必需的环境变量已配置")
        return True

    def run(self):
        """运行CLI主流程"""
        total_steps = 3

        # 标题
        print(f"\n{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║          Collider-Agent 环境配置工具                        ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}╚════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        print(f"{Colors.DIM}项目根目录: {self.project_root}{Colors.ENDC}\n")

        # 步骤1: 检测uv
        print(Colors.step(1, total_steps, "检查 uv 包管理器"))
        if not self.check_uv_installed():
            self.print_warning("未检测到 uv 包管理器")

            if self.ask_user("是否安装 uv?", default=True):
                if not self.install_uv():
                    self.print_error("uv 安装失败，无法继续")
                    sys.exit(1)
            else:
                self.print_error("需要 uv 才能继续配置环境")
                sys.exit(1)
        else:
            self.print_success("uv 已安装")

        # 步骤2: 检测虚拟环境
        print(Colors.step(2, total_steps, "检查虚拟环境"))
        if not self.check_venv_configured():
            self.print_warning("虚拟环境未正确配置")

            if self.ask_user("是否使用 uv sync 配置虚拟环境?", default=True):
                if not self.setup_venv():
                    self.print_error("虚拟环境配置失败")
                    sys.exit(1)
            else:
                self.print_error("需要正确配置的虚拟环境才能运行项目")
                sys.exit(1)
        else:
            self.print_success("虚拟环境已正确配置")

        # 步骤3: 检测环境变量
        print(Colors.step(3, total_steps, "检查环境变量配置"))
        if not self.check_env_configured():
            self.print_warning("环境变量未完全配置")

            if self.ask_user("是否运行自动配置?", default=True):
                if not self.auto_configure_env():
                    self.print_error("环境变量配置失败")
                    sys.exit(1)
            else:
                self.print_warning("部分功能可能无法正常使用")
        else:
            self.print_success("所有环境变量已正确配置")

        # 完成
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}╔════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{Colors.BOLD}║                   ✓ 环境配置完成！                          ║{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{Colors.BOLD}╚════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
        self.print_info("你现在可以运行项目了")


def main():
    """主函数"""
    cli = ColliderAgentCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}配置已取消{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}错误: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
