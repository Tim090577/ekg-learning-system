# EKG Learning System - 心电图学习系统

<div align="center">

![EKG Learning System](https://img.shields.io/badge/EKG-Learning%20System-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![React](https://img.shields.io/badge/React-18.0+-61DAFB)
![License](https://img.shields.io/badge/License-MIT-yellow)

一个基于 AI 的心电图分析与学习平台，帮助医学生和医生学习心电图诊断

</div>

## 📋 项目简介

EKG Learning System 是一个综合性的心电图学习平台，结合了先进的信号处理技术和交互式可视化，为用户提供：

- 🔬 **智能分析**：使用 NeuroKit2 和 scipy 进行专业的心电图信号分析
- 📊 **3D可视化**：基于 Three.js 的交互式 3D 心脏模型
- 🎯 **诊断辅助**：支持多种心电图异常的自动识别（AFIB、STEMI、NSTEMI、房室传导阻滞等）
- 📚 **知识库**：内置丰富的心电图诊断规则和疾病症状数据库
- 🔄 **复习系统**：间隔重复学习算法，帮助巩固知识

## 🏗️ 技术栈

### 后端
- **FastAPI**: 现代、快速的 Python Web 框架
- **NeuroKit2**: 神经生理信号分析库
- **SciPy & NumPy**: 科学计算和信号处理
- **PyPDF2**: PDF 文档解析
- **PostgreSQL**: 数据持久化

### 前端
- **React 18**: 现代化的 UI 框架
- **Ant Design**: 企业级 UI 组件库
- **Three.js**: 3D 图形渲染
- **Recharts**: 数据可视化
- **Vite**: 快速的前端构建工具

### DevOps
- **Docker & Docker Compose**: 容器化部署
- **Nginx**: 反向代理和静态文件服务

## 🚀 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 1.29+
- 或者：Python 3.9+, Node.js 16+

### 使用 Docker Compose（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd ＥＫＧ
```

2. **配置环境变量**
```bash
# 后端环境变量
cp backend/.env.example backend/.env

# 前端环境变量
cp frontend/.env.example frontend/.env
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **访问应用**
- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 本地开发

#### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn app.main:app --reload --port 8000
```

#### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

## 📖 功能特性

### 1. EKG 信号分析
- 上传心电图数据（支持 CSV、PDF 格式）
- 自动检测 P 波、QRS 波群、T 波
- 计算心率、PR 间期、QT 间期、QRS 时长
- 识别心律失常和传导异常

### 2. 诊断辅助
支持以下心电图异常的识别：
- **心律失常**: 房颤（AFIB）、室性心动过速（VT）
- **缺血性改变**: ST 段抬高型心梗（STEMI）、非 ST 段抬高型心梗（NSTEMI）
- **传导阻滞**: 房室传导阻滞（AVB）、左束支传导阻滞（LBBB）、右束支传导阻滞（RBBB）
- **其他**: 长 QT 综合征、Brugada 综合征

### 3. 3D 可视化
- 交互式 3D 心脏模型
- 心脏电活动动画演示
- 异常区域高亮显示

### 4. 智能复习系统
- 基于艾宾浩斯遗忘曲线的间隔重复算法
- 个性化学习路径
- 知识点掌握度追踪

## 📁 项目结构

```
ＥＫＧ/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── ekg.py      # 心电图分析接口
│   │   │   └── review.py   # 复习系统接口
│   │   ├── core/           # 核心功能
│   │   │   ├── ekg_analyzer.py    # 心电图分析引擎
│   │   │   ├── pdf_parser.py      # PDF 解析器
│   │   │   └── diagnosis.py       # 诊断引擎
│   │   ├── database/       # 数据库
│   │   │   └── knowledge_base.py  # 知识库
│   │   ├── models/         # 数据模型
│   │   │   └── schemas.py
│   │   └── main.py         # FastAPI 应用入口
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # React 组件
│   │   │   ├── EKGUploader.jsx
│   │   │   ├── EKGVisualization.jsx
│   │   │   ├── DiagnosisPanel.jsx
│   │   │   ├── Heart3DVisualization.jsx
│   │   │   └── ReviewPanel.jsx
│   │   ├── utils/          # 工具函数
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env.example
├── data/                   # 数据文件
│   ├── diagnosis_rules.json      # 诊断规则
│   └── disease_symptoms.json     # 疾病症状数据库
├── docker-compose.yml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## 🔬 使用示例

### 分析心电图数据

```python
# Python 示例
import requests

# 上传心电图数据
with open('ekg_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/ekg/analyze',
        files={'file': f}
    )

result = response.json()
print(f"心率: {result['heart_rate']} bpm")
print(f"诊断: {result['diagnosis']}")
```

### 前端集成

```javascript
// React 示例
import { analyzeEKG } from './utils/api';

const handleUpload = async (file) => {
  const result = await analyzeEKG(file);
  console.log('分析结果:', result);
};
```

## 🧪 测试

### 后端测试
```bash
cd backend
pytest tests/
```

### 前端测试
```bash
cd frontend
npm test
```

## 📚 API 文档

启动后端服务后，访问以下地址查看完整的 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要 API 端点

#### EKG 分析
- `POST /api/ekg/analyze` - 分析上传的心电图数据
- `GET /api/ekg/history` - 获取分析历史记录
- `GET /api/ekg/{id}` - 获取特定分析结果

#### 复习系统
- `GET /api/review/next` - 获取下一个复习项目
- `POST /api/review/submit` - 提交复习结果
- `GET /api/review/statistics` - 获取学习统计

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献指南。

### 开发流程

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 医疗免责声明

**重要提示**: 本系统仅供教育和学习目的使用，不应用于实际的临床诊断。所有诊断建议仅供参考，最终诊断应由有资质的医疗专业人员做出。

## 🔗 相关资源

- [NeuroKit2 文档](https://neuropsychology.github.io/NeuroKit/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [React 文档](https://react.dev/)
- [Three.js 文档](https://threejs.org/docs/)

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至: [your-email@example.com]

## 🙏 致谢

感谢以下开源项目：
- NeuroKit2 团队
- FastAPI 社区
- React 和 Three.js 社区
- 所有贡献者

---

<div align="center">
Made with ❤️ for medical education
</div>
