import React, { useRef, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'


const Cube = (props: any) => {
    const mesh = useRef()
    const [hovered, setHover] = useState(false)
    const [active, setActive] = useState(false)
    // @ts-ignore
    useFrame((state, delta) => (mesh.current.rotation.x += 0.01))
    return (
        <mesh
            {...props}
            ref={mesh}
            scale={active ? 1.5 : 1}
            onClick={(event) => setActive(!active)}
            onPointerOver={(event) => setHover(true)}
            onPointerOut={(event) => setHover(false)}>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color={hovered ? 'black' : 'blue'} />
        </mesh>
    )
}

function CubeCanvas() {
    return (
        <Canvas>
            <ambientLight />
            <pointLight position={[10, 10, 10]} />
            <Cube position={[0, 1.4, 0]} />
        </Canvas>
    )
}

export default CubeCanvas
