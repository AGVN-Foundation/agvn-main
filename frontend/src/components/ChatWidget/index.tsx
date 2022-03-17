//@ts-nocheck
import React from 'react'
import dynamic from 'next/dynamic'

const ChatWidget = dynamic(
    () => import('react-chat-widget').then((mod) => mod.Widget),
    { ssr: false }
)

export default ChatWidget
