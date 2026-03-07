import { useState } from 'react'
import { Layout, Menu, Typography, Alert, Space, Tag } from 'antd'
import {
  HeartOutlined,
  UploadOutlined,
  HistoryOutlined,
  ReadOutlined,
  BarChartOutlined,
  SettingOutlined,
} from '@ant-design/icons'
import EKGUploader from './components/EKGUploader'
import EKGVisualization from './components/EKGVisualization'
import DiagnosisPanel from './components/DiagnosisPanel'
import Heart3DVisualization from './components/Heart3DVisualization'
import ReviewPanel from './components/ReviewPanel'

const { Header, Content, Sider } = Layout
const { Title, Text } = Typography

function App() {
  const [currentView, setCurrentView] = useState('upload')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result)
    setCurrentView('results')
  }

  const menuItems = [
    {
      key: 'upload',
      icon: <UploadOutlined />,
      label: '上传分析',
    },
    {
      key: 'results',
      icon: <BarChartOutlined />,
      label: '分析结果',
      disabled: !analysisResult,
    },
    {
      key: 'review',
      icon: <ReadOutlined />,
      label: '复习系统',
    },
    {
      key: 'history',
      icon: <HistoryOutlined />,
      label: '历史记录',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '设置',
    },
  ]

  const renderContent = () => {
    switch (currentView) {
      case 'upload':
        return (
          <div>
            <Alert
              message="⚠️ 医疗免责声明"
              description="本系统仅供教育和学习目的使用，不得用于临床诊断。所有分析结果仅供参考，最终诊断应由有资质的医疗专业人员做出。"
              type="warning"
              showIcon
              style={{ marginBottom: 24 }}
            />
            <EKGUploader 
              onAnalysisComplete={handleAnalysisComplete}
              onLoadingChange={setLoading}
            />
          </div>
        )
      
      case 'results':
        return analysisResult ? (
          <div>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <DiagnosisPanel data={analysisResult} />
              <EKGVisualization data={analysisResult} />
              <Heart3DVisualization diagnosis={analysisResult.diagnosis} />
            </Space>
          </div>
        ) : (
          <Alert
            message="暂无分析结果"
            description="请先上传心电图文件进行分析"
            type="info"
          />
        )
      
      case 'review':
        return <ReviewPanel />
      
      case 'history':
        return (
          <Alert
            message="功能开发中"
            description="历史记录功能正在开发中，敬请期待"
            type="info"
          />
        )
      
      case 'settings':
        return (
          <Alert
            message="功能开发中"
            description="设置功能正在开发中，敬请期待"
            type="info"
          />
        )
      
      default:
        return null
    }
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        display: 'flex', 
        alignItems: 'center', 
        background: '#001529',
        padding: '0 24px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', flex: 1 }}>
          <HeartOutlined style={{ fontSize: 32, color: '#ff4d4f', marginRight: 16 }} />
          <div>
            <Title level={3} style={{ color: 'white', margin: 0 }}>
              EKG Learning System
            </Title>
            <Text style={{ color: 'rgba(255,255,255,0.65)', fontSize: 12 }}>
              心电图学习系统
            </Text>
          </div>
        </div>
        <Space>
          <Tag color="blue">v1.0.0</Tag>
          <Tag color="green">教育版</Tag>
        </Space>
      </Header>
      
      <Layout>
        <Sider width={200} theme="light" style={{ background: '#fff' }}>
          <Menu
            mode="inline"
            selectedKeys={[currentView]}
            onClick={({ key }) => setCurrentView(key)}
            items={menuItems}
            style={{ height: '100%', borderRight: 0 }}
          />
        </Sider>
        
        <Layout style={{ padding: '24px' }}>
          <Content
            style={{
              background: '#fff',
              padding: 24,
              margin: 0,
              minHeight: 280,
              borderRadius: 8,
            }}
          >
            {renderContent()}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  )
}

export default App
