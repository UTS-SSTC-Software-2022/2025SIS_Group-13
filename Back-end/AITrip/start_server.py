#!/usr/bin/env python
"""
AITrip 后端服务器启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path


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
        print("👤 创建超级用户...")
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
        print("⚠️ 超级用户可能已存在，跳过创建")
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


def main():
    """主函数"""
    print("AITrip 后端服务器启动脚本")
    print("=" * 40)

    # 检查当前目录
    if not Path("manage.py").exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)

    # 1. 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请先安装缺少的依赖后再运行程序")
        sys.exit(1)

    # 2. 执行数据库迁移
    if not run_migrations():
        print("❌ 数据库迁移失败，程序退出")
        sys.exit(1)

    # 3. 创建超级用户
    create_superuser()

    print("\n" + "=" * 40)
    print("✅ 初始化完成！")
    print("=" * 40)

    # 4. 启动服务器
    start_server()


if __name__ == "__main__":
    main()