import { useRef, useEffect, useState } from 'react'
import { Card, Typography, Space, Switch, Slider, Tag } from 'antd'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'

const { Title, Text } = Typography

// 简化的 3D 心脏模型
function HeartModel({ diagnosis, animate, rotationSpeed }) {
  const meshRef = useRef()
  const [hue, setHue] = useState(0)

  // 根据诊断确定颜色
  const getColorBySeverity = (severity) => {
    switch (severity) {
      case 'normal':
        return 0x52c41a // 绿色
      case 'mild':
        return 0xfaad14 // 黄色
      case 'moderate':
        return 0xfa8c16 // 橙色
      case 'high':
      case 'critical':
        return 0xff4d4f // 红色
      default:
        return 0xff6b9d // 粉红色
    }
  }

  const severity = diagnosis?.primary_diagnosis?.severity || 'normal'
  const baseColor = getColorBySeverity(severity)

  useFrame((state, delta) => {
    if (meshRef.current) {
      // 旋转
      if (animate) {
        meshRef.current.rotation.y += delta * rotationSpeed
      }
      
      // 心跳动画（缩放）
      if (animate) {
        const scale = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1
        meshRef.current.scale.set(scale, scale, scale)
      }

      // 颜色脉冲效果
      if (animate && severity !== 'normal') {
        const pulse = Math.sin(state.clock.elapsedTime * 3) * 0.5 + 0.5
        meshRef.current.material.emissive.setHex(baseColor)
        meshRef.current.material.emissiveIntensity = pulse * 0.3
      }
    }
  })

  return (
    <mesh ref={meshRef}>
      {/* 使用简化的心脏形状（组合球体） */}
      <group>
        {/* 主体 */}
        <mesh position={[0, 0, 0]}>
          <sphereGeometry args={[1, 32, 32]} />
          <meshStandardMaterial 
            color={baseColor} 
            roughness={0.3} 
            metalness={0.6}
            emissive={baseColor}
            emissiveIntensity={0.1}
          />
        </mesh>
        
        {/* 左心室 */}
        <mesh position={[-0.5, -0.3, 0.2]}>
          <sphereGeometry args={[0.6, 32, 32]} />
          <meshStandardMaterial 
            color={baseColor} 
            roughness={0.3} 
            metalness={0.6}
            emissive={baseColor}
            emissiveIntensity={0.1}
          />
        </mesh>
        
        {/* 右心室 */}
        <mesh position={[0.5, -0.3, 0.2]}>
          <sphereGeometry args={[0.55, 32, 32]} />
          <meshStandardMaterial 
            color={baseColor} 
            roughness={0.3} 
            metalness={0.6}
            emissive={baseColor}
            emissiveIntensity={0.1}
          />
        </mesh>
        
        {/* 左心房 */}
        <mesh position={[-0.4, 0.6, 0]}>
          <sphereGeometry args={[0.4, 32, 32]} />
          <meshStandardMaterial 
            color={baseColor} 
            roughness={0.3} 
            metalness={0.6}
            emissive={baseColor}
            emissiveIntensity={0.1}
          />
        </mesh>
        
        {/* 右心房 */}
        <mesh position={[0.4, 0.6, 0]}>
          <sphereGeometry args={[0.4, 32, 32]} />
          <meshStandardMaterial 
            color={baseColor} 
            roughness={0.3} 
            metalness={0.6}
            emissive={baseColor}
            emissiveIntensity={0.1}
          />
        </mesh>
      </group>
    </mesh>
  )
}

// 电活动可视化（表示心脏传导）
function ElectricalActivity({ animate }) {
  const particlesRef = useRef()
  const particleCount = 50

  useEffect(() => {
    if (particlesRef.current) {
      const positions = new Float32Array(particleCount * 3)
      
      for (let i = 0; i < particleCount; i++) {
        // 随机分布在心脏周围
        const angle = (i / particleCount) * Math.PI * 2
        const radius = 1.5 + Math.random() * 0.5
        positions[i * 3] = Math.cos(angle) * radius
        positions[i * 3 + 1] = (Math.random() - 0.5) * 2
        positions[i * 3 + 2] = Math.sin(angle) * radius
      }
      
      particlesRef.current.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    }
  }, [])

  useFrame((state) => {
    if (particlesRef.current && animate) {
      const positions = particlesRef.current.attributes.position.array
      
      for (let i = 0; i < particleCount; i++) {
        // 粒子向心脏中心移动
        const x = positions[i * 3]
        const y = positions[i * 3 + 1]
        const z = positions[i * 3 + 2]
        
        const distance = Math.sqrt(x * x + y * y + z * z)
        
        if (distance < 0.5) {
          // 重置到外围
          const angle = Math.random() * Math.PI * 2
          const radius = 1.5 + Math.random() * 0.5
          positions[i * 3] = Math.cos(angle) * radius
          positions[i * 3 + 1] = (Math.random() - 0.5) * 2
          positions[i * 3 + 2] = Math.sin(angle) * radius
        } else {
          // 向中心移动
          positions[i * 3] *= 0.98
          positions[i * 3 + 1] *= 0.98
          positions[i * 3 + 2] *= 0.98
        }
      }
      
      particlesRef.current.attributes.position.needsUpdate = true
    }
  })

  return (
    <points>
      <bufferGeometry ref={particlesRef}>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={new Float32Array(particleCount * 3)}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.05} color="#1890ff" transparent opacity={0.6} />
    </points>
  )
}

function Heart3DVisualization({ diagnosis }) {
  const [animate, setAnimate] = useState(true)
  const [rotationSpeed, setRotationSpeed] = useState(0.5)
  const [showElectrical, setShowElectrical] = useState(true)

  const severity = diagnosis?.primary_diagnosis?.severity || 'normal'

  return (
    <Card title="3D 心脏可视化" className="custom-card">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        
        {/* 控制面板 */}
        <Space wrap>
          <Space>
            <Text>心跳动画:</Text>
            <Switch checked={animate} onChange={setAnimate} />
          </Space>
          
          <Space>
            <Text>电活动:</Text>
            <Switch checked={showElectrical} onChange={setShowElectrical} />
          </Space>
          
          <div style={{ width: 200 }}>
            <Text>旋转速度:</Text>
            <Slider
              min={0}
              max={2}
              step={0.1}
              value={rotationSpeed}
              onChange={setRotationSpeed}
              disabled={!animate}
            />
          </div>
        </Space>

        {/* 状态指示 */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: 16 }}>
          <Tag color={severity === 'normal' ? 'success' : 'warning'}>
            心脏状态: {diagnosis?.primary_diagnosis?.name || '未知'}
          </Tag>
        </div>

        {/* 3D Canvas */}
        <div 
          className="canvas-container" 
          style={{ 
            width: '100%', 
            height: 500, 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            position: 'relative'
          }}
        >
          <Canvas>
            <PerspectiveCamera makeDefault position={[0, 0, 5]} />
            
            {/* 灯光 */}
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} intensity={1} />
            <pointLight position={[-10, -10, -10]} intensity={0.5} />
            <spotLight position={[0, 5, 0]} angle={0.3} intensity={1} />
            
            {/* 心脏模型 */}
            <HeartModel 
              diagnosis={diagnosis} 
              animate={animate} 
              rotationSpeed={rotationSpeed}
            />
            
            {/* 电活动 */}
            {showElectrical && <ElectricalActivity animate={animate} />}
            
            {/* 控制器 */}
            <OrbitControls 
              enablePan={true}
              enableZoom={true}
              enableRotate={true}
              autoRotate={false}
            />
          </Canvas>
        </div>

        {/* 说明 */}
        <div style={{ background: '#f0f2f5', padding: 16, borderRadius: 8 }}>
          <Title level={5}>交互说明</Title>
          <ul style={{ paddingLeft: 20, marginBottom: 0 }}>
            <li>使用鼠标拖拽旋转心脏模型</li>
            <li>滚轮缩放视图</li>
            <li>心脏颜色代表诊断严重程度</li>
            <li>蓝色粒子表示心脏的电活动传导</li>
            <li>心跳动画模拟心脏收缩和舒张</li>
          </ul>
        </div>
      </Space>
    </Card>
  )
}

export default Heart3DVisualization
