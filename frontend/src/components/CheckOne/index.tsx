import React from 'react'
import {
    Box,
    Text,
    Radio,
    Flex,
    RadioGroup,
    RadioGroupProps,
} from '@chakra-ui/react'

interface Props extends Omit<RadioGroupProps, 'position' | 'children'> {
    position: number
    label: string
    options: string[]
}

const CheckOne = ({ position, ...props }: Props) => {
    return (
        <Box>
            <Text>
                {position}. {props.label}
            </Text>
            <RadioGroup {...props}>
                {props.options.map((opt) => (
                    <Flex>
                        <Text mr="30px">{opt}</Text>
                        <Radio name={opt} />
                    </Flex>
                ))}
            </RadioGroup>
        </Box>
    )
}

export default CheckOne
