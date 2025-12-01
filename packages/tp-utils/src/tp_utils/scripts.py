import os
import subprocess
import shlex


def _pkg_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def run_tests():
    root = _pkg_root()
    cmd = ["pytest", "-q", "tests"]
    print(f"测试根目录: {root}")
    print(f"执行测试命令: {shlex.join(cmd)}")
    r = subprocess.run(cmd, cwd=root)
    print(f"测试退出码: {r.returncode}")
    return r.returncode


def build_package():
    root = _pkg_root()
    cmd = ["poetry", "build"]
    print(f"构建根目录: {root}")
    print(f"执行构建命令: {shlex.join(cmd)}")
    r = subprocess.run(cmd, cwd=root)
    dist_dir = os.path.join(root, "dist")
    if os.path.isdir(dist_dir):
        files = sorted(os.listdir(dist_dir))
        print(f"构建产物: {', '.join(files) if files else '(空)'}")
    print(f"构建退出码: {r.returncode}")
    return r.returncode


def publish_package():
    root = _pkg_root()
    repo = "cnb"
    username = os.getenv("TWINE_USERNAME") or "cnb"
    password = os.getenv("TWINE_PASSWORD")
    repo_url = os.getenv("POETRY_REPOSITORY_URL") or os.getenv("TWINE_REPOSITORY_URL")

    cmd = ["poetry", "publish", "--build", "--skip-existing"]
    if repo:
        cmd += ["-r", repo]
    if username:
        cmd += ["-u", username]
    if password:
        cmd += ["-p", password]

    print(f"发布仓库URL: {repo_url}")
    print(f"发布根目录: {root}")
    print(f"发布仓库: {repo}")
    print(f"发布用户名: {username if username else '(未设置)'}")
    print(f"发布密码已配置: {'是' if password else '否'}")
    print(f"执行发布命令: {shlex.join(cmd)}")
    r = subprocess.run(cmd, cwd=root)
    print(f"发布退出码: {r}")
    return r.returncode
