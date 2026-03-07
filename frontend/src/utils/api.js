import axios from 'axios'

// API 基础 URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 统一错误处理
    const message = error.response?.data?.message || error.message || '请求失败'
    console.error('API Error:', message)
    return Promise.reject(new Error(message))
  }
)

// ========== EKG 分析 API ==========

/**
 * 分析上传的心电图文件
 * @param {File} file - 心电图文件
 * @returns {Promise} 分析结果
 */
export const analyzeEKG = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('sampling_rate', '500')

  const response = await apiClient.post('/api/ekg/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response
}

/**
 * 获取分析历史记录
 * @param {number} limit - 返回记录数
 * @param {number} offset - 偏移量
 * @returns {Promise} 历史记录列表
 */
export const getAnalysisHistory = async (limit = 10, offset = 0) => {
  return await apiClient.get('/api/ekg/history', {
    params: { limit, offset },
  })
}

/**
 * 获取特定分析结果详情
 * @param {string} analysisId - 分析记录 ID
 * @returns {Promise} 分析详情
 */
export const getAnalysisDetail = async (analysisId) => {
  return await apiClient.get(`/api/ekg/${analysisId}`)
}

/**
 * 删除分析记录
 * @param {string} analysisId - 分析记录 ID
 * @returns {Promise} 删除结果
 */
export const deleteAnalysis = async (analysisId) => {
  return await apiClient.delete(`/api/ekg/${analysisId}`)
}

/**
 * 获取统计数据
 * @returns {Promise} 统计数据
 */
export const getStatistics = async () => {
  return await apiClient.get('/api/ekg/stats/overview')
}

// ========== 复习系统 API ==========

/**
 * 获取下一个复习项目
 * @param {string} category - 类别（可选）
 * @returns {Promise} 复习项目
 */
export const getNextReviewItem = async (category = null) => {
  return await apiClient.get('/api/review/next', {
    params: category ? { category } : {},
  })
}

/**
 * 提交复习答案
 * @param {Object} submission - 提交数据
 * @returns {Promise} 提交结果
 */
export const submitReview = async (submission) => {
  return await apiClient.post('/api/review/submit', submission)
}

/**
 * 获取复习统计数据
 * @param {string} userId - 用户 ID（可选）
 * @returns {Promise} 统计数据
 */
export const getReviewStatistics = async (userId = null) => {
  return await apiClient.get('/api/review/statistics', {
    params: userId ? { user_id: userId } : {},
  })
}

/**
 * 获取复习类别列表
 * @returns {Promise} 类别列表
 */
export const getReviewCategories = async () => {
  return await apiClient.get('/api/review/categories')
}

/**
 * 重置学习进度
 * @param {string} userId - 用户 ID
 * @param {string} category - 类别（可选）
 * @returns {Promise} 重置结果
 */
export const resetProgress = async (userId, category = null) => {
  return await apiClient.post('/api/review/reset-progress', null, {
    params: {
      user_id: userId,
      ...(category && { category }),
    },
  })
}

// ========== 通用 API ==========

/**
 * 获取 API 信息
 * @returns {Promise} API 信息
 */
export const getAPIInfo = async () => {
  return await apiClient.get('/api/info')
}

/**
 * 健康检查
 * @returns {Promise} 健康状态
 */
export const healthCheck = async () => {
  return await apiClient.get('/health')
}

export default apiClient
