import React from 'react'
import { Text, Box, Textarea, BoxProps } from '@chakra-ui/react'

interface PollTextAreaProps extends BoxProps {
    number: number
    label: string
}

const PollTextArea: React.FC<PollTextAreaProps> = ({
    number,
    label,
    ...props
}) => {
    return (
        <Box {...props}>
            <Text>
                {number}. {label}
            </Text>
            <Textarea />
        </Box>
    )
}

export default PollTextArea
