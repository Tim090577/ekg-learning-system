import { useState } from 'react'
import { Upload, Button, Card, message, Space, Typography, Progress } from 'antd'
import { InboxOutlined, FileTextOutlined } from '@ant-design/icons'
import { analyzeEKG } from '../utils/api'

const { Dragger } = Upload
const { Title, Text } = Typography

function EKGUploader({ onAnalysisComplete, onLoadingChange }) {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)

  const handleUpload = async (file) => {
    // 检查文件类型
    const validTypes = ['text/csv', 'application/pdf', 'application/vnd.ms-excel']
    const isValidType = validTypes.includes(file.type) || 
                        file.name.endsWith('.csv') || 
                        file.name.endsWith('.pdf')
    
    if (!isValidType) {
      message.error('仅支持 CSV 和 PDF 格式的文件')
      return false
    }

    // 检查文件大小 (10MB)
    const maxSize = 10 * 1024 * 1024
    if (file.size > maxSize) {
      message.error('文件大小不能超过 10MB')
      return false
    }

    // 开始上传分析
    setUploading(true)
    setProgress(0)
    onLoadingChange?.(true)

    // 模拟进度
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 200)

    try {
      const result = await analyzeEKG(file)
      
      clearInterval(progressInterval)
      setProgress(100)
      
      message.success('分析完成！')
      
      setTimeout(() => {
        onAnalysisComplete(result)
        setUploading(false)
        setProgress(0)
        onLoadingChange?.(false)
      }, 500)
      
    } catch (error) {
      clearInterval(progressInterval)
      message.error(error.message || '分析失败，请稍后重试')
      setUploading(false)
      setProgress(0)
      onLoadingChange?.(false)
    }

    return false // 阻止默认上传行为
  }

  const uploadProps = {
    name: 'file',
    multiple: false,
    accept: '.csv,.pdf',
    beforeUpload: handleUpload,
    showUploadList: false,
    disabled: uploading,
  }

  return (
    <Card title="上传心电图数据" className="custom-card">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div>
          <Title level={4}>支持的文件格式</Title>
          <Space>
            <FileTextOutlined /> CSV 格式（心电图信号数据）
          </Space>
          <br />
          <Space style={{ marginTop: 8 }}>
            <FileTextOutlined /> PDF 格式（心电图报告）
          </Space>
        </div>

        <Dragger {...uploadProps} style={{ padding: '20px 0' }}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined style={{ color: uploading ? '#1890ff' : undefined }} />
          </p>
          <p className="ant-upload-text">
            {uploading ? '正在分析中...' : '点击或拖拽文件到此区域上传'}
          </p>
          <p className="ant-upload-hint">
            支持单个文件上传，文件大小限制为 10MB
          </p>
        </Dragger>

        {uploading && (
          <div>
            <Text type="secondary">分析进度</Text>
            <Progress 
              percent={progress} 
              status="active"
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
            />
          </div>
        )}

        <div style={{ background: '#f0f2f5', padding: 16, borderRadius: 8 }}>
          <Title level={5}>快速开始</Title>
          <ol style={{ paddingLeft: 20 }}>
            <li>准备您的心电图数据文件（CSV 或 PDF 格式）</li>
            <li>点击上传区域或拖拽文件到此处</li>
            <li>等待系统自动分析（通常需要 5-10 秒）</li>
            <li>查看详细的分析结果和诊断建议</li>
          </ol>
        </div>

        <div style={{ background: '#fffbe6', padding: 16, borderRadius: 8, borderLeft: '4px solid #faad14' }}>
          <Text strong>💡 提示</Text>
          <ul style={{ paddingLeft: 20, marginTop: 8, marginBottom: 0 }}>
            <li>CSV 文件应包含心电图信号的数值数据</li>
            <li>PDF 文件可以是扫描的心电图报告</li>
            <li>确保数据质量良好以获得准确的分析结果</li>
            <li>系统会自动检测 P 波、QRS 波群和 T 波</li>
          </ul>
        </div>
      </Space>
    </Card>
  )
}

export default EKGUploader
