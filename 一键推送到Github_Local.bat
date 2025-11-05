@echo off
chcp 65001 >nul
echo ==========================================
echo   一键推送 simple-servlet-form 项目
echo ==========================================
echo.

REM 1. 克隆包含项目的仓库
echo 📥 正在下载项目...
git clone -b claude/update-master-to-maven-011CUox8ErAXfQVMepRqg7cG https://github.com/wangsi001/Wangci_-.git temp_download
cd temp_download\simple-servlet-form

echo.
echo ✅ 项目下载完成！
echo.

REM 2. 初始化为新的Git仓库
echo 🔧 正在初始化Git仓库...
rmdir /s /q .git 2>nul
git init
git add .
git commit -m "初始提交：超简单Servlet表单项目"

echo.
echo ✅ Git仓库初始化完成！
echo.

REM 3. 推送到新仓库
echo 🚀 正在推送到 Github_Local 仓库...
git remote add origin https://github.com/wangsi001/Github_Local.git
git branch -M master
git push -u origin master

echo.
echo ==========================================
echo   🎉 完成！
echo ==========================================
echo.
echo 访问你的新仓库：
echo https://github.com/wangsi001/Github_Local
echo.
echo 项目已成功推送！
pause
