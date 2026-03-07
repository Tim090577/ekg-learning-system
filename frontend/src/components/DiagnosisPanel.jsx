import { Card, Descriptions, Tag, Alert, Space, Typography, Divider, Collapse } from 'antd'
import { 
  CheckCircleOutlined, 
  WarningOutlined, 
  InfoCircleOutlined,
  HeartOutlined 
} from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography
const { Panel } = Collapse

function DiagnosisPanel({ data }) {
  if (!data) {
    return null
  }

  const { heart_rate, intervals, hrv, diagnosis } = data

  // 严重程度颜色映射
  const severityColors = {
    normal: 'success',
    mild: 'warning',
    moderate: 'orange',
    high: 'error',
    critical: 'error',
  }

  // 严重程度图标
  const severityIcons = {
    normal: <CheckCircleOutlined />,
    mild: <InfoCircleOutlined />,
    moderate: <WarningOutlined />,
    high: <WarningOutlined />,
    critical: <WarningOutlined />,
  }

  const primaryDiagnosis = diagnosis?.primary_diagnosis
  const secondaryDiagnoses = diagnosis?.secondary_diagnoses || []
  const alerts = diagnosis?.alerts || []
  const clinicalNotes = diagnosis?.clinical_notes || []

  return (
    <Card title="诊断分析结果" className="custom-card">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        
        {/* 主要诊断 */}
        {primaryDiagnosis && (
          <div>
            <Title level={4}>
              <HeartOutlined /> 主要诊断
            </Title>
            <Alert
              message={
                <Space>
                  {severityIcons[primaryDiagnosis.severity]}
                  <Text strong style={{ fontSize: 16 }}>
                    {primaryDiagnosis.name}
                  </Text>
                  {primaryDiagnosis.name_en && (
                    <Text type="secondary">({primaryDiagnosis.name_en})</Text>
                  )}
                  <Tag color={severityColors[primaryDiagnosis.severity]}>
                    {primaryDiagnosis.severity.toUpperCase()}
                  </Tag>
                </Space>
              }
              description={
                <div style={{ marginTop: 12 }}>
                  <Text>置信度: {(primaryDiagnosis.confidence * 100).toFixed(0)}%</Text>
                  {primaryDiagnosis.recommendations?.length > 0 && (
                    <div style={{ marginTop: 12 }}>
                      <Text strong>建议措施:</Text>
                      <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                        {primaryDiagnosis.recommendations.map((rec, index) => (
                          <li key={index}><Text>{rec}</Text></li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              }
              type={primaryDiagnosis.severity === 'normal' ? 'success' : 'warning'}
              showIcon
            />
          </div>
        )}

        {/* 次要诊断 */}
        {secondaryDiagnoses.length > 0 && (
          <div>
            <Title level={4}>次要诊断</Title>
            <Space direction="vertical" style={{ width: '100%' }}>
              {secondaryDiagnoses.map((diag, index) => (
                <Alert
                  key={index}
                  message={
                    <Space>
                      <Text>{diag.name}</Text>
                      {diag.name_en && <Text type="secondary">({diag.name_en})</Text>}
                      <Tag color={severityColors[diag.severity]}>{diag.severity}</Tag>
                    </Space>
                  }
                  description={`置信度: ${(diag.confidence * 100).toFixed(0)}%`}
                  type="info"
                  showIcon
                />
              ))}
            </Space>
          </div>
        )}

        {/* 警报 */}
        {alerts.length > 0 && (
          <div>
            <Title level={4}>
              <WarningOutlined style={{ color: '#ff4d4f' }} /> 异常警报
            </Title>
            <Space direction="vertical" style={{ width: '100%' }}>
              {alerts.map((alert, index) => (
                <Alert
                  key={index}
                  message={alert.message}
                  description={alert.recommendation}
                  type={alert.severity === 'high' ? 'error' : 'warning'}
                  showIcon
                />
              ))}
            </Space>
          </div>
        )}

        <Divider />

        {/* 心电图参数 */}
        <div>
          <Title level={4}>心电图参数</Title>
          <Descriptions bordered column={2} size="small">
            <Descriptions.Item label="心率">
              <Text strong style={{ fontSize: 16, color: heart_rate < 60 || heart_rate > 100 ? '#ff4d4f' : '#52c41a' }}>
                {heart_rate} bpm
              </Text>
            </Descriptions.Item>
            
            <Descriptions.Item label="PR 间期">
              <Text strong>{intervals?.pr_interval || 0} ms</Text>
              {intervals?.pr_interval > 200 && <Tag color="orange" style={{ marginLeft: 8 }}>延长</Tag>}
            </Descriptions.Item>
            
            <Descriptions.Item label="QRS 时限">
              <Text strong>{intervals?.qrs_duration || 0} ms</Text>
              {intervals?.qrs_duration > 120 && <Tag color="orange" style={{ marginLeft: 8 }}>增宽</Tag>}
            </Descriptions.Item>
            
            <Descriptions.Item label="QT 间期">
              <Text strong>{intervals?.qt_interval || 0} ms</Text>
            </Descriptions.Item>
            
            <Descriptions.Item label="QTc 间期">
              <Text strong>{intervals?.qtc_interval || 0} ms</Text>
              {intervals?.qtc_interval > 450 && <Tag color="red" style={{ marginLeft: 8 }}>延长</Tag>}
            </Descriptions.Item>
            
            <Descriptions.Item label="R 峰计数">
              <Text strong>{data.r_peak_count} 个</Text>
            </Descriptions.Item>
          </Descriptions>
        </div>

        {/* 心率变异性 */}
        {hrv && (
          <div>
            <Title level={4}>心率变异性 (HRV)</Title>
            <Descriptions bordered column={3} size="small">
              <Descriptions.Item label="SDNN">
                <Text strong>{hrv.sdnn} ms</Text>
              </Descriptions.Item>
              <Descriptions.Item label="RMSSD">
                <Text strong>{hrv.rmssd} ms</Text>
              </Descriptions.Item>
              <Descriptions.Item label="pNN50">
                <Text strong>{hrv.pnn50}%</Text>
              </Descriptions.Item>
            </Descriptions>
          </div>
        )}

        {/* 临床备注 */}
        {clinicalNotes.length > 0 && (
          <div>
            <Collapse>
              <Panel header="临床备注" key="1">
                <ul style={{ paddingLeft: 20 }}>
                  {clinicalNotes.map((note, index) => (
                    <li key={index}><Text>{note}</Text></li>
                  ))}
                </ul>
              </Panel>
            </Collapse>
          </div>
        )}

        {/* 总结 */}
        {diagnosis?.summary && (
          <div style={{ background: '#f0f2f5', padding: 16, borderRadius: 8 }}>
            <Title level={5}>诊断总结</Title>
            <Paragraph>{diagnosis.summary}</Paragraph>
          </div>
        )}

        {/* 医疗免责声明 */}
        <Alert
          message="⚠️ 医疗免责声明"
          description="本分析结果仅供教育和学习参考，不得用于临床诊断。所有诊断建议应由有资质的医疗专业人员确认。"
          type="warning"
          showIcon
        />
      </Space>
    </Card>
  )
}

export default DiagnosisPanel
