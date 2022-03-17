import React from 'react'
import { Box, Flex, Text } from '@chakra-ui/react'

interface BannerProps {
    title: string
    subtitle: string
    quote: string
    author: string
}

const Banner = (props: BannerProps) => {
    return (
        <Flex
            justify="space-between"
            alignItems="center"
            bg="#282A2B"
            w="100%"
            h="310px"
            textColor="#D3D3D3"
            px="15%"
        >
            <Flex flexDir="column" alignItems="center">
                <Text fontSize="36px">{props.title}</Text>
                <Box bg="#D3D3D3" h="1px" w="50%" my="14px" />
                <Text fontSize="20px" textAlign="center">
                    {props.subtitle}
                </Text>
            </Flex>
            <Box maxW="60%">
                <Text fontSize="28px">{props.quote}</Text>
                <Text fontSize="20px" textAlign="center">
                    -{props.author}
                </Text>
            </Box>
        </Flex>
    )
}

export default Banner
