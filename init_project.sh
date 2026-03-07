#!/bin/bash
# EKG Learning System - 项目初始化脚本

echo "🫀 正在创建 EKG Learning System 项目..."

# 确认必须的 Python 文件已经通过 create_file 工具创建
# 检查它们是否存在于根目录
if [ -f "/README.md" ]; then
  echo "✅ 检测到文件已在根目录创建，正在复制..."
  cp /README.md ./README.md 2>/dev/null
  cp /LICENSE ./LICENSE 2>/dev/null
  cp /CONTRIBUTING.md ./CONTRIBUTING.md 2>/dev/null
  cp /.gitignore ./.gitignore 2>/dev/null
  cp /docker-compose.yml ./docker-compose.yml 2>/dev/null
  cp /start.sh ./start.sh 2>/dev/null
  cp /start.bat ./start.bat 2>/dev/null
  
  # 后端文件
  cp -r /backend/* ./backend/ 2>/dev/null
  
  # 前端文件
  cp -r /frontend/* ./frontend/ 2>/dev/null
  
  # 数据文件
  cp -r /data/* ./data/ 2>/dev/null
  
  # .github 文件
  cp -r /.github/* ./.github/ 2>/dev/null
fi

echo "✅ 项目结构已创建！"
ls -la
