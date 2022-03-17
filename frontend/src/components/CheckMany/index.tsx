import React from 'react'
import {
    Box,
    Text,
    Checkbox,
    Flex,
    CheckboxGroup,
    CheckboxGroupProps,
} from '@chakra-ui/react'

interface Props extends CheckboxGroupProps {
    position: number
    label: string
    options: string[]
}

const index = (props: Props) => {
    return (
        <Box>
            <Text>
                {props.position}. {props.label}
            </Text>
            <CheckboxGroup {...props}>
                {props.options.map((opt) => (
                    <Flex>
                        <Text mr="30px">{opt}</Text>
                        <Checkbox name={opt} />
                    </Flex>
                ))}
            </CheckboxGroup>
        </Box>
    )
}

export default index
