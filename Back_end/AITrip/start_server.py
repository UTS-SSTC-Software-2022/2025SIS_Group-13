#!/usr/bin/env python
"""
AITrip 后端服务器启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path


def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 50)
    print("🚀 AITrip 后端服务器启动脚本")
    print("=" * 50)
    print("请选择启动方式：")
    print("1. 🔄 完整启动流程（检查依赖 + 迁移 + 超级用户 + 启动服务器）")
    print("2. ⚡ 直接启动服务器（跳过所有检查）")
    print("3. ❌ 退出")
    print("-" * 50)

    while True:
        try:
            choice = input("请输入选项 (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                return choice
            else:
                print("❌ 无效选项，请输入 1、2 或 3")
        except KeyboardInterrupt:
            print("\n\n🛑 用户取消操作")
            sys.exit(0)


def check_dependencies():
    """检查依赖是否安装"""
    print("📦 检查依赖...")
    missing_deps = []

    # Check Django
    try:
        import django
    except ImportError:
        missing_deps.append("django")

    # Check Django REST framework
    try:
        import rest_framework
    except ImportError:
        missing_deps.append("djangorestframework")

    # Check JWT
    try:
        import rest_framework_simplejwt
    except ImportError:
        missing_deps.append("djangorestframework-simplejwt")

    # Check Django filters
    try:
        import django_filters
    except ImportError:
        missing_deps.append("django-filter")

    # Check CORS headers
    try:
        import corsheaders
    except ImportError:
        missing_deps.append("django-cors-headers")

    # Check MySQL driver
    try:
        import MySQLdb
    except ImportError:
        missing_deps.append("mysqlclient")

    if missing_deps:
        print("❌ 检测到缺少以下依赖:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n📋 请运行以下命令安装依赖:")
        print(f"   pip install -r requirements.txt")
        print("   或者单独安装:")
        for dep in missing_deps:
            print(f"   pip install {dep}")
        return False
    else:
        print("✅ 所有依赖已安装")
        return True


def check_migrations_needed():
    """检查是否需要执行数据库迁移"""
    try:
        print("🔍 检查数据库迁移状态...")
        # 检查是否有待应用的迁移
        result = subprocess.run(
            [sys.executable, "manage.py", "showmigrations", "--list"],
            capture_output=True,
            text=True,
            check=True,
        )

        # 检查输出中是否有 [ ] 标记的未应用迁移
        if "[ ]" in result.stdout:
            print("⚠️ 检测到未应用的数据库迁移")
            return True
        else:
            print("✅ 数据库迁移已是最新状态")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 检查迁移状态失败: {e}")
        return True  # 如果检查失败，为了安全起见，建议执行迁移


def run_migrations():
    """运行数据库迁移"""
    try:
        print("🔄 执行数据库迁移...")
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ 数据库迁移完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False


def create_superuser():
    """创建超级用户"""
    try:
        print("👤 检查超级用户...")
        # 设置环境变量
        os.environ.setdefault("DJANGO_SUPERUSER_USERNAME", "admin")
        os.environ.setdefault("DJANGO_SUPERUSER_EMAIL", "admin@aitrip.com")
        os.environ.setdefault("DJANGO_SUPERUSER_PASSWORD", "admin123")

        subprocess.run(
            [sys.executable, "manage.py", "createsuperuser", "--noinput"], check=True
        )
        print("✅ 超级用户创建完成")
        print("   用户名: admin")
        print("   密码: admin123")
        return True
    except subprocess.CalledProcessError:
        print("✅ 超级用户已存在")
        return True


def start_server():
    """启动开发服务器"""
    try:
        print("🚀 启动Django开发服务器...")
        print("🌐 服务器地址: http://localhost:8080")
        print("🔧 管理后台: http://localhost:8080/admin")
        print("📡 API接口: http://localhost:8080/api/")
        print("按 Ctrl+C 停止服务器")
        print("-" * 50)

        subprocess.run([sys.executable, "manage.py", "runserver", "8080"])
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")


def full_startup_process():
    """完整的启动流程"""
    print("\n🔄 开始完整启动流程...")
    print("=" * 40)

    # 1. 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请先安装缺少的依赖后再运行程序")
        return False

    # 2. 检查是否需要执行数据库迁移
    if check_migrations_needed():
        if not run_migrations():
            print("❌ 数据库迁移失败，程序退出")
            return False
    else:
        print("⏭️ 跳过数据库迁移")

    # 3. 创建超级用户（仅在首次运行时）
    create_superuser()

    print("\n" + "=" * 40)
    print("✅ 初始化完成！")
    print("=" * 40)

    # 4. 启动服务器
    start_server()
    return True


def direct_startup():
    """直接启动服务器"""
    print("\n⚡ 直接启动服务器...")
    print("⚠️ 注意：跳过所有检查，如果系统未正确配置可能会启动失败")
    print("=" * 40)

    # 检查当前目录
    if not Path("manage.py").exists():
        print("❌ 请在项目根目录运行此脚本")
        return False

    start_server()
    return True


def main():
    """主函数"""
    # 检查当前目录
    if not Path("manage.py").exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)

    while True:
        choice = show_menu()

        if choice == "1":
            # 完整启动流程
            full_startup_process()
            break
        elif choice == "2":
            # 直接启动服务器
            direct_startup()
            break
        elif choice == "3":
            # 退出
            print("👋 再见！")
            sys.exit(0)


if __name__ == "__main__":
    main()
