import React from 'react'
import { Divider, Flex, Box, Heading, Text } from '@chakra-ui/layout'
import { Image } from '@chakra-ui/image'
import { motion } from 'framer-motion'
import styled from 'styled-components'

const cardMotion = {
    rest: {
        color: "#1d3c4a",
        transition: {
            duration: 2,
        }
    },
    hover: {
        color: "#119911",
        scale: 1.05,
        transition: {
            duration: 0.4,
        }
    }
}

const Card = styled(motion.div)`
    cursor: pointer;
`

export interface BenefitCardProps {
    title: string,
    threshold: number,
    content?: string,
    imageUrl?: string,
    imageUrl2?: string
}

export default function assignCards(cardData: Array<BenefitCardProps>) {
    return (
        <Flex justifyContent="center" flexDirection="row" alignItems="center" flexWrap="wrap">
            {cardData.map((c) => (
                <Box key={c.title} m="2.5rem" minW="50rem">
                    <BenefitCard {...c} />
                </Box>
            ))}
        </Flex>
    )
}

/**
 * TODO -> onClick, expand the card and place 'content' into view.
 * Basically, create a box out of view with all the title, threshold, content... with custom styling
 * Then fade in from below as a dialog
 * If click out of the box, then close it
 */
function DialogBox({ title, threshold, content, imageUrl, imageUrl2 }: BenefitCardProps) {
    return (
        <Box w="90vv">
            <Text fontSize="20px" pl="5rem" pb="1rem">
                Threshold: {threshold} Contribution
            </Text>
            <Box pl="5rem">
                <Flex alignItems="center" justifyContent="center">
                    <Image src={imageUrl} maxW='50%' mt="1.5rem" mb="1.5rem" ml="1.5rem" h="5rem" />
                    <Image src={imageUrl2} maxW='50%' mt="1.5rem" mb="1.5rem" ml="1.5rem" h="5rem" />
                </Flex>
            </Box>
            <Flex p="5rem">
                <Text>{content}</Text>
            </Flex>
            <Heading textAlign="center" mb="2rem">{title}</Heading>
        </Box>
    )
}

function BenefitCard({ title, threshold, content, imageUrl, imageUrl2 }: BenefitCardProps) {
    return (
        <Card className="card" whileHover="hover" animate="rest" variants={cardMotion}>
            <Box rounded="false" justifyContent="center" pb="3rem" backgroundColor="#afc6c7">
                <Text fontSize="14px" m="1rem" textAlign="center">
                    Threshold: {threshold} Contribution
                </Text>
                <Box>
                    <Flex alignItems="center" justifyContent="center">
                        <Image src={imageUrl} maxW='50%' mt="1.5rem" mb="1.5rem" ml="1.5rem" h="5rem" />
                        <Image src={imageUrl2} maxW='50%' mt="1.5rem" mb="1.5rem" ml="1.5rem" h="5rem" />
                    </Flex>
                </Box>
                <Heading textAlign="center" mb="2rem">{title}</Heading>
            </Box>
        </Card>
    )
}
