import { Box, Heading, Image, Text, Flex } from '@chakra-ui/react'
import React, { useState } from 'react'

export interface ActionProp {
    heading: string
    content: string
    imgUrl?: string
    current?: boolean
}

function Action({ heading, content, imgUrl, current = true }: ActionProp) {
    const [isCurrent, setCurrent] = useState(true)

    return (
        <Flex mb="10rem" flexDir="column" justifyContent="center" alignItems="center">
            <Heading mb="2rem" textAlign="center">{heading}</Heading>
            <Image src={imgUrl} mb="1rem" />
            <Box className="social-media"></Box>
            <Box>
                <Text textAlign="center" fontSize="1rem" mb="2rem" color={current ? "red" : "green"}>{current ? "Action being undertaken" : "Action has been taken"}</Text>
                <Text textAlign="left" fontSize="1.5rem" pl="4rem" pr="4rem">
                    {content}
                </Text>
            </Box>
        </Flex>
    )
}

export function assignActions(actions: Array<ActionProp>) {
    return (
        <Flex m="4rem" flexDir="column" p="4rem">
            {actions.map((a) => (
                <Action {...a} key={a.heading} />
            ))}
        </Flex>
    )
}

export default assignActions
