import React from 'react'
import { Box, Flex, Text, Radio, RadioGroup } from '@chakra-ui/react'
import { range } from 'lodash'

interface Props {
    position: number
    label: string
    options: string[]
}

const HowMuch = (props: Props) => {
    return (
        <Box>
            <Text>
                {props.position}. {props.label}
            </Text>
            <Flex justify="space-between" w="80%" ml="20%">
                <Text>Not at All</Text>
                <Text>Not</Text>
                <Text>Neither</Text>
                <Text>Somewhat</Text>
                <Text>Very Much</Text>
            </Flex>
            {props.options.map((opt) => (
                <Flex justify="space-between">
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

export default HowMuch
