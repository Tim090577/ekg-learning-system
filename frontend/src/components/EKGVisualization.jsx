import { Card, Typography, Space } from 'antd'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Scatter, ScatterChart } from 'recharts'

const { Title, Text } = Typography

function EKGVisualization({ data }) {
  if (!data || !data.processed_signal) {
    return null
  }

  // 准备图表数据
  const signalData = data.processed_signal.map((value, index) => ({
    time: index / data.sampling_rate,
    signal: value,
  }))

  // 准备 R 峰数据
  const rPeakData = (data.peaks?.r_peaks || []).map(peak => ({
    time: peak / data.sampling_rate,
    signal: data.processed_signal[peak] || 0,
  }))

  // 准备 P 峰数据
  const pPeakData = (data.peaks?.p_peaks || []).map(peak => ({
    time: peak / data.sampling_rate,
    signal: data.processed_signal[peak] || 0,
  }))

  // 准备 T 峰数据
  const tPeakData = (data.peaks?.t_peaks || []).map(peak => ({
    time: peak / data.sampling_rate,
    signal: data.processed_signal[peak] || 0,
  }))

  return (
    <Card title="心电图波形" className="custom-card">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 主波形图 */}
        <div>
          <Title level={4}>信号波形（前 2 秒）</Title>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={signalData.slice(0, 1000)} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="time" 
                label={{ value: '时间 (秒)', position: 'insideBottom', offset: -5 }}
                tickFormatter={(value) => value.toFixed(2)}
              />
              <YAxis 
                label={{ value: '电压 (mV)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                formatter={(value) => [value.toFixed(3), '电压']}
                labelFormatter={(label) => `时间: ${label}秒`}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="signal" 
                stroke="#1890ff" 
                strokeWidth={2} 
                dot={false}
                name="心电信号"
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* 峰值标注图 */}
        {(rPeakData.length > 0 || pPeakData.length > 0 || tPeakData.length > 0) && (
          <div>
            <Title level={4}>波峰标注</Title>
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  type="number" 
                  dataKey="time" 
                  name="时间" 
                  label={{ value: '时间 (秒)', position: 'insideBottom', offset: -5 }}
                  domain={[0, Math.max(...signalData.map(d => d.time))]}
                />
                <YAxis 
                  type="number" 
                  dataKey="signal" 
                  name="电压"
                  label={{ value: '电压 (mV)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Legend />
                
                {/* 背景信号线 */}
                <Line 
                  data={signalData.slice(0, 1000)} 
                  type="monotone" 
                  dataKey="signal" 
                  stroke="#d9d9d9" 
                  strokeWidth={1} 
                  dot={false}
                  name="信号"
                />
                
                {/* R 峰 */}
                {rPeakData.length > 0 && (
                  <Scatter 
                    data={rPeakData.slice(0, 10)} 
                    fill="#ff4d4f" 
                    name="R 峰"
                    shape="circle"
                  />
                )}
                
                {/* P 峰 */}
                {pPeakData.length > 0 && (
                  <Scatter 
                    data={pPeakData.slice(0, 10)} 
                    fill="#52c41a" 
                    name="P 峰"
                    shape="triangle"
                  />
                )}
                
                {/* T 峰 */}
                {tPeakData.length > 0 && (
                  <Scatter 
                    data={tPeakData.slice(0, 10)} 
                    fill="#1890ff" 
                    name="T 峰"
                    shape="square"
                  />
                )}
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* 信号质量指标 */}
        <div style={{ background: '#f0f2f5', padding: 16, borderRadius: 8 }}>
          <Title level={5}>信号质量评估</Title>
          <Space direction="vertical" style={{ width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>质量等级:</Text>
              <Text strong className={`severity-${data.signal_quality?.quality_level || 'unknown'}`}>
                {data.signal_quality?.quality_level?.toUpperCase() || 'UNKNOWN'}
              </Text>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>质量评分:</Text>
              <Text strong>{((data.signal_quality?.quality_score || 0) * 100).toFixed(0)}%</Text>
            </div>
            {data.signal_quality?.issues?.length > 0 && (
              <div>
                <Text type="warning">检测到的问题:</Text>
                <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                  {data.signal_quality.issues.map((issue, index) => (
                    <li key={index}><Text type="warning">{issue}</Text></li>
                  ))}
                </ul>
              </div>
            )}
          </Space>
        </div>

        {/* 检测统计 */}
        <div style={{ background: '#f0f2f5', padding: 16, borderRadius: 8 }}>
          <Title level={5}>波峰检测统计</Title>
          <Space direction="vertical" style={{ width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>R 峰数量:</Text>
              <Text strong>{data.r_peak_count || 0} 个</Text>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>P 峰数量:</Text>
              <Text strong>{data.peaks?.p_peaks?.length || 0} 个</Text>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>T 峰数量:</Text>
              <Text strong>{data.peaks?.t_peaks?.length || 0} 个</Text>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text>采样率:</Text>
              <Text strong>{data.sampling_rate} Hz</Text>
            </div>
          </Space>
        </div>
      </Space>
    </Card>
  )
}

export default EKGVisualization
