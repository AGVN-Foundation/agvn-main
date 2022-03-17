import React from 'react'
import { Box, Flex, Text, Radio, RadioGroup } from '@chakra-ui/react'
import { range } from 'lodash'

interface Props {
    position: number
    label: string
    options: string[]
}

const PoorToGood = (props: Props) => {
    return (
        <Box>
            <Text mb="1rem" fontWeight="semibold">
                {props.position}. {props.label}
            </Text>
            <Flex justify="space-between" w="80%" ml="20%" mb="0.5rem">
                <Text>Highly Unfavorable</Text>
                <Text>Unfavorable</Text>
                <Text>Neutral</Text>
                <Text>Favorable</Text>
                <Text>Highly Favorable</Text>
            </Flex>
            {props.options.map((opt, index) => (
                <Flex justify="space-between" key={index}>
                    <Text>{opt}</Text>
                    <RadioGroup name={opt} w="80%">
                        <Flex justify="space-between">
                            {range(1, 6).map((num) => (
                                <Radio value={num - 4} />
                            ))}
                        </Flex>
                    </RadioGroup>
                </Flex>
            ))}
        </Box>
    )
}

export default PoorToGood
