# 贡献指南 / Contributing Guide

感谢您对 EKG Learning System 项目的关注！我们欢迎各种形式的贡献。

Thank you for your interest in contributing to the EKG Learning System project! We welcome all forms of contributions.

## 📋 目录 / Table of Contents

- [行为准则](#行为准则--code-of-conduct)
- [如何贡献](#如何贡献--how-to-contribute)
- [开发流程](#开发流程--development-workflow)
- [代码规范](#代码规范--coding-standards)
- [提交信息规范](#提交信息规范--commit-message-guidelines)
- [测试要求](#测试要求--testing-requirements)

## 行为准则 / Code of Conduct

### 我们的承诺 / Our Pledge

为了营造一个开放和友好的环境，我们承诺让每个参与者都能获得良好的体验，无论年龄、体型、残疾、民族、性别认同和表达、经验水平、国籍、个人外貌、种族、宗教或性认同和取向如何。

### 我们的标准 / Our Standards

**积极行为包括 / Positive behaviors include:**
- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同情

**不可接受的行为包括 / Unacceptable behaviors include:**
- 使用性化的语言或图像
- 侮辱性/贬损性评论和人身或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息
- 其他在专业环境中可能被认为不适当的行为

## 如何贡献 / How to Contribute

### 报告 Bug / Reporting Bugs

在提交 Bug 报告之前：
- 检查现有的 Issues，确保 Bug 尚未被报告
- 收集关于 Bug 的信息（操作系统、Python/Node 版本、错误消息等）

提交 Bug 时请包含：
1. **清晰的标题**：简洁描述问题
2. **重现步骤**：详细的重现步骤
3. **期望行为**：您期望发生什么
4. **实际行为**：实际发生了什么
5. **环境信息**：操作系统、版本号等
6. **截图**：如果适用

### 建议新功能 / Suggesting Features

提交功能建议时请包含：
1. **功能描述**：清晰描述建议的功能
2. **使用场景**：解释为什么需要这个功能
3. **可能的实现**：如果有想法，描述可能的实现方式
4. **替代方案**：考虑过的其他解决方案

### 提交代码 / Submitting Code

1. **Fork 项目**
   ```bash
   # 点击 GitHub 上的 Fork 按钮
   # 克隆您的 fork
   git clone https://github.com/YOUR-USERNAME/ＥＫＧ.git
   cd ＥＫＧ
   ```

2. **创建分支**
   ```bash
   # 创建并切换到新分支
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行更改**
   - 遵循代码规范
   - 添加必要的测试
   - 更新文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **推送到 GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**
   - 访问您的 fork 页面
   - 点击 "New Pull Request"
   - 填写 PR 模板

## 开发流程 / Development Workflow

### 环境设置

#### 后端开发环境
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果存在

# 运行测试
pytest

# 启动开发服务器
uvicorn app.main:app --reload
```

#### 前端开发环境
```bash
cd frontend

# 安装依赖
npm install

# 运行测试
npm test

# 启动开发服务器
npm run dev
```

### 分支命名规范

- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档更新
- `style/` - 代码格式化（不影响功能）
- `refactor/` - 代码重构
- `test/` - 测试相关
- `chore/` - 构建过程或辅助工具的变动

示例：
- `feature/add-heart-3d-animation`
- `fix/ekg-analysis-crash`
- `docs/update-api-documentation`

## 代码规范 / Coding Standards

### Python 代码规范

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范：

```python
# Good
def analyze_ekg_signal(signal_data: np.ndarray, sampling_rate: int = 500) -> dict:
    """
    分析心电图信号
    
    Args:
        signal_data: 心电图信号数组
        sampling_rate: 采样率（Hz）
    
    Returns:
        包含分析结果的字典
    """
    # 处理逻辑
    pass

# 使用类型提示
from typing import List, Dict, Optional

def process_batch(items: List[str]) -> Dict[str, Any]:
    pass
```

**工具**：
- 使用 `black` 进行代码格式化
- 使用 `flake8` 进行代码检查
- 使用 `mypy` 进行类型检查

```bash
# 运行格式化
black backend/

# 运行 linter
flake8 backend/

# 类型检查
mypy backend/
```

### JavaScript/React 代码规范

遵循 [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)：

```javascript
// Good
const analyzeEKG = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/ekg/analyze', formData);
    return response.data;
  } catch (error) {
    console.error('EKG analysis failed:', error);
    throw error;
  }
};

// React 组件
const EKGVisualization = ({ data, onAnalysisComplete }) => {
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // 副作用逻辑
  }, [data]);
  
  return (
    <div className="ekg-visualization">
      {/* 组件内容 */}
    </div>
  );
};
```

**工具**：
- 使用 `ESLint` 进行代码检查
- 使用 `Prettier` 进行代码格式化

```bash
# 运行 linter
npm run lint

# 格式化代码
npm run format
```

### 文档规范

- 所有公共函数和类都应有文档字符串
- 复杂的算法应有注释说明
- README 和 API 文档应保持更新
- 使用中英文双语文档（中文优先）

## 提交信息规范 / Commit Message Guidelines

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或工具变动
- `perf`: 性能优化

### 示例

```
feat(ekg-analyzer): add STEMI detection algorithm

实现了 ST 段抬高型心梗的自动检测算法
- 使用小波变换检测 ST 段偏移
- 添加了多导联一致性验证
- 更新了诊断规则数据库

Closes #123
```

```
fix(frontend): resolve EKG chart rendering issue

修复了在 Safari 浏览器中心电图表无法正确渲染的问题

Fixes #456
```

## 测试要求 / Testing Requirements

### 后端测试

```python
# tests/test_ekg_analyzer.py
import pytest
from app.core.ekg_analyzer import EKGAnalyzer

def test_heart_rate_calculation():
    """测试心率计算"""
    analyzer = EKGAnalyzer()
    signal = np.random.randn(5000)
    result = analyzer.calculate_heart_rate(signal, sampling_rate=500)
    
    assert 40 <= result['heart_rate'] <= 200
    assert 'r_peaks' in result

def test_afib_detection():
    """测试房颤检测"""
    analyzer = EKGAnalyzer()
    # 加载测试数据
    afib_signal = load_test_signal('afib_sample.csv')
    result = analyzer.detect_afib(afib_signal)
    
    assert result['has_afib'] == True
    assert result['confidence'] > 0.8
```

### 前端测试

```javascript
// src/components/__tests__/EKGVisualization.test.jsx
import { render, screen } from '@testing-library/react';
import EKGVisualization from '../EKGVisualization';

describe('EKGVisualization', () => {
  test('renders EKG chart with data', () => {
    const mockData = {
      signal: [1, 2, 3, 4, 5],
      peaks: [2, 4]
    };
    
    render(<EKGVisualization data={mockData} />);
    
    expect(screen.getByTestId('ekg-chart')).toBeInTheDocument();
  });
  
  test('displays loading state', () => {
    render(<EKGVisualization loading={true} />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
});
```

### 测试覆盖率要求

- 新功能必须包含测试
- 目标覆盖率：后端 > 80%，前端 > 70%
- 关键功能（诊断算法）必须 > 90%

```bash
# 后端覆盖率
pytest --cov=app --cov-report=html

# 前端覆盖率
npm run test:coverage
```

## Pull Request 检查清单

在提交 PR 之前，请确保：

- [ ] 代码遵循项目的代码规范
- [ ] 所有测试都通过
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 提交信息遵循规范
- [ ] 没有合并冲突
- [ ] CI/CD 检查通过

## 医疗数据处理注意事项

⚠️ **重要提示**：

1. **禁止使用真实患者数据**：
   - 所有测试数据必须是合成的或匿名化的
   - 不得在代码、注释或提交信息中包含真实患者信息

2. **数据隐私**：
   - 遵守 HIPAA、GDPR 等数据保护法规
   - 确保所有用户数据都经过适当的加密和保护

3. **医疗免责声明**：
   - 记住这是一个教育工具，不用于临床诊断
   - 在 UI 中明确显示免责声明

## 获取帮助

如有疑问，可以通过以下方式获取帮助：

- 📝 提交 Issue
- 💬 参与 Discussions
- 📧 发送邮件至：[your-email@example.com]

## 致谢

感谢所有为本项目做出贡献的开发者！

---

再次感谢您的贡献！🎉

Thank you for contributing! 🎉
