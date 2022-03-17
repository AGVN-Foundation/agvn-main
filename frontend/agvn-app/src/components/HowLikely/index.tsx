import React from 'react'
import { Box, Text, Flex, Button } from '@chakra-ui/react'
import { range } from 'lodash'

interface HowLikelyProps {
    position: number
    label: string
    onClick: (value: number) => void
    start: number
    end: number
}

const HowLikely: React.FC<HowLikelyProps> = ({
    position,
    label,
    onClick,
    start,
    end,
    ...props
}) => {
    return (
        <Box>
            <Flex justify="space-between" w="calc(40px * 10)">
                <Text>Not at all Likely</Text>
                <Text>Extremely Likely</Text>
            </Flex>
            <Flex>
                {range(start, end).map((num) => (
                    <Button
                        onClick={() => onClick(num)}
                        key={num}
                        borderRadius="0"
                        border="1px solid black"
                        bg="none"
                    >
                        {num}
                    </Button>
                ))}
            </Flex>
        </Box>
    )
}

export default HowLikely
