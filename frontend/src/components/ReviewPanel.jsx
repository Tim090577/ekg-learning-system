import { useState, useEffect } from 'react'
import { Card, Button, Radio, Space, Typography, Progress, Tag, Alert, Divider, Statistic, Row, Col } from 'antd'
import { CheckCircleOutlined, CloseCircleOutlined, TrophyOutlined, FireOutlined } from '@ant-design/icons'
import { getNextReviewItem, submitReview, getReviewStatistics } from '../utils/api'

const { Title, Text, Paragraph } = Typography

function ReviewPanel() {
  const [loading, setLoading] = useState(false)
  const [currentItem, setCurrentItem] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [showResult, setShowResult] = useState(false)
  const [reviewResult, setReviewResult] = useState(null)
  const [statistics, setStatistics] = useState(null)

  useEffect(() => {
    loadStatistics()
  }, [])

  const loadStatistics = async () => {
    try {
      const stats = await getReviewStatistics()
      setStatistics(stats)
    } catch (error) {
      console.error('Failed to load statistics:', error)
    }
  }

  const loadNextItem = async () => {
    setLoading(true)
    setShowResult(false)
    setSelectedAnswer(null)
    setReviewResult(null)
    
    try {
      const item = await getNextReviewItem()
      setCurrentItem(item)
    } catch (error) {
      console.error('Failed to load review item:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    if (!selectedAnswer || !currentItem) return

    setLoading(true)
    
    try {
      const result = await submitReview({
        item_id: currentItem.id,
        selected_answer: selectedAnswer,
        review_count: currentItem.review_count,
      })
      
      setReviewResult(result)
      setShowResult(true)
      loadStatistics() // 更新统计数据
    } catch (error) {
      console.error('Failed to submit review:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleNext = () => {
    loadNextItem()
  }

  // 难度标签颜色
  const difficultyColors = {
    easy: 'green',
    medium: 'orange',
    hard: 'red',
  }

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      
      {/* 统计面板 */}
      {statistics && (
        <Card title="学习统计" className="custom-card">
          <Row gutter={16}>
            <Col span={6}>
              <Statistic
                title="总题目数"
                value={statistics.total_items}
                prefix={<TrophyOutlined />}
              />
            </Col>
            <Col span={6}>
              <Statistic
                title="已掌握"
                value={statistics.mastered_items}
                valueStyle={{ color: '#52c41a' }}
                suffix={`/ ${statistics.total_items}`}
              />
            </Col>
            <Col span={6}>
              <Statistic
                title="正确率"
                value={statistics.accuracy_rate * 100}
                precision={1}
                suffix="%"
                valueStyle={{ color: statistics.accuracy_rate > 0.7 ? '#52c41a' : '#ff4d4f' }}
              />
            </Col>
            <Col span={6}>
              <Statistic
                title="连续学习"
                value={statistics.review_streak_days}
                suffix="天"
                prefix={<FireOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Col>
          </Row>

          <Divider />

          <div>
            <Text strong>学习进度</Text>
            <Progress
              percent={(statistics.mastered_items / statistics.total_items * 100).toFixed(1)}
              status="active"
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
            />
          </div>
        </Card>
      )}

      {/* 复习卡片 */}
      <Card 
        title="复习练习" 
        className="custom-card"
        extra={
          !currentItem && (
            <Button type="primary" onClick={loadNextItem} loading={loading}>
              开始复习
            </Button>
          )
        }
      >
        {!currentItem ? (
          <Alert
            message="准备好了吗？"
            description="点击"开始复习"按钮获取下一个复习项目"
            type="info"
            showIcon
          />
        ) : (
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            
            {/* 题目信息 */}
            <div>
              <Space>
                <Tag color={difficultyColors[currentItem.difficulty]}>
                  {currentItem.difficulty.toUpperCase()}
                </Tag>
                <Tag>{currentItem.category}</Tag>
                {currentItem.review_count > 0 && (
                  <Tag color="blue">已复习 {currentItem.review_count} 次</Tag>
                )}
              </Space>
            </div>

            {/* 问题 */}
            <div>
              <Title level={4}>{currentItem.question}</Title>
            </div>

            {/* 心电图预览 */}
            {currentItem.ekg_data?.image_url && (
              <div
                style={{
                  width: '100%',
                  height: 200,
                  background: '#f0f2f5',
                  borderRadius: 8,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Text type="secondary">心电图图像预览</Text>
                {/* 实际应用中这里应该显示心电图图像 */}
              </div>
            )}

            {/* 选项 */}
            {!showResult && (
              <Radio.Group
                onChange={(e) => setSelectedAnswer(e.target.value)}
                value={selectedAnswer}
                style={{ width: '100%' }}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  {currentItem.options.map((option) => (
                    <Radio
                      key={option.id}
                      value={option.id}
                      style={{
                        width: '100%',
                        padding: '12px',
                        borderRadius: 8,
                        border: selectedAnswer === option.id ? '2px solid #1890ff' : '1px solid #d9d9d9',
                        background: selectedAnswer === option.id ? '#e6f7ff' : 'white',
                      }}
                    >
                      {option.text}
                    </Radio>
                  ))}
                </Space>
              </Radio.Group>
            )}

            {/* 结果展示 */}
            {showResult && reviewResult && (
              <div>
                <Alert
                  message={
                    <Space>
                      {reviewResult.is_correct ? (
                        <>
                          <CheckCircleOutlined style={{ color: '#52c41a' }} />
                          <Text strong style={{ color: '#52c41a' }}>回答正确！</Text>
                        </>
                      ) : (
                        <>
                          <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
                          <Text strong style={{ color: '#ff4d4f' }}>回答错误</Text>
                        </>
                      )}
                    </Space>
                  }
                  description={
                    <div>
                      {!reviewResult.is_correct && (
                        <div style={{ marginTop: 8 }}>
                          <Text>您选择的答案: {selectedAnswer}</Text>
                          <br />
                          <Text strong>正确答案: {reviewResult.correct_answer}</Text>
                        </div>
                      )}
                    </div>
                  }
                  type={reviewResult.is_correct ? 'success' : 'error'}
                  showIcon
                />

                <Divider />

                {/* 详细解析 */}
                <div>
                  <Title level={5}>详细解析</Title>
                  <Paragraph>{reviewResult.explanation}</Paragraph>
                </div>

                {/* 关键点 */}
                {reviewResult.key_points?.length > 0 && (
                  <div>
                    <Title level={5}>关键点</Title>
                    <ul style={{ paddingLeft: 20 }}>
                      {reviewResult.key_points.map((point, index) => (
                        <li key={index}><Text>{point}</Text></li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* 相关主题 */}
                {reviewResult.related_topics?.length > 0 && (
                  <div>
                    <Title level={5}>相关主题</Title>
                    <Space wrap>
                      {reviewResult.related_topics.map((topic, index) => (
                        <Tag key={index} color="blue">{topic}</Tag>
                      ))}
                    </Space>
                  </div>
                )}

                {/* 下次复习时间 */}
                <div style={{ background: '#f0f2f5', padding: 16, borderRadius: 8, marginTop: 16 }}>
                  <Text type="secondary">
                    下次复习时间: {new Date(reviewResult.next_review_date).toLocaleString('zh-CN')}
                  </Text>
                </div>
              </div>
            )}

            {/* 操作按钮 */}
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              {!showResult ? (
                <>
                  <Button onClick={() => setCurrentItem(null)}>取消</Button>
                  <Button 
                    type="primary" 
                    onClick={handleSubmit}
                    disabled={!selectedAnswer}
                    loading={loading}
                  >
                    提交答案
                  </Button>
                </>
              ) : (
                <Button type="primary" onClick={handleNext} style={{ width: '100%' }}>
                  下一题
                </Button>
              )}
            </div>
          </Space>
        )}
      </Card>

      {/* 类别进度 */}
      {statistics?.category_progress && (
        <Card title="分类进度" className="custom-card">
          <Space direction="vertical" style={{ width: '100%' }} size="middle">
            {Object.entries(statistics.category_progress).map(([category, progress]) => (
              <div key={category}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <Text strong>{category}</Text>
                  <Space>
                    <Text type="secondary">
                      {progress.mastered} / {progress.total}
                    </Text>
                    <Text strong>{(progress.accuracy * 100).toFixed(0)}%</Text>
                  </Space>
                </div>
                <Progress
                  percent={(progress.mastered / progress.total * 100).toFixed(1)}
                  strokeColor={{
                    from: '#108ee9',
                    to: '#87d068',
                  }}
                  status="active"
                />
              </div>
            ))}
          </Space>
        </Card>
      )}
    </Space>
  )
}

export default ReviewPanel
