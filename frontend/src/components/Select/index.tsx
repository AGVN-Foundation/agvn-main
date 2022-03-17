import React from 'react'
import { Flex, Text, Select, Box } from '@chakra-ui/react'

interface CustomSelectProps {
    position: number
    label: string
    options: {
        label: string
        value: string
    }[]
    onClick?: (value: string) => void
}

const CustomSelect = (props: CustomSelectProps) => {
    return (
        <Box>
            <Text>
                {props.position}. {props.label}
            </Text>
            <Select onSelect={(x) => console.log({ x })}>
                {props.options.map((opt) => (
                    <option
                        value={opt.value}
                        label={opt.label}
                        key={opt.value}
                    />
                ))}
            </Select>
        </Box>
    )
}

export default CustomSelect
