import React from 'react'
import { Divider, Flex, Box, Heading, Text } from '@chakra-ui/layout'
import { Image } from '@chakra-ui/image'
import { motion } from 'framer-motion'
import styled from 'styled-components'
import Link from 'next/link'

const cardMotion = {
    rest: {
        color: "grey",
        transition: {
            duration: 2,
        }
    },
    hover: {
        color: "#97abb8",
        scale: 1.05,
        transition: {
            duration: 0.4,
        }
    }
}

const LineDivider = styled(motion(Divider))`
`
const Card = styled(motion.div)`
    cursor: pointer;
`

const lineExpansion = {
    rest: {
        width: "10rem",
        duration: 0.2
    },
    hover: {
        width: "20rem",
        transition: {
            duration: 0.2
        }
    }
}

export interface DownCardProps {
    title: string,
    subtitle?: string,
    content?: string,
    imageUrl?: string,
    directUrl?: string,
    externalUrl?: string,
}

export const assignCards = (cardData: Array<DownCardProps>) => {
    return (
        <Flex justifyContent="center" flexDirection="row" alignItems="center" flexWrap="wrap">
            {cardData.map((c) => (
                <Box key={c.title} m="2.5rem" minW="30rem">
                    <DownCard {...c} />
                </Box>
            ))}
        </Flex>
    )
}

// TODO? how to make the images take up the entire space?
// Maybe have to use a grid with equal column and row sizes (1/2 col span, 2 rows)

function DownCard({ title, subtitle, content, imageUrl, directUrl, externalUrl }: DownCardProps) {
    return (
        <Card className="card" whileHover="hover" animate="rest" variants={cardMotion}>
            <Link href={((directUrl? directUrl: "") || (externalUrl? externalUrl: ""))}>
            <Box rounded="false" justifyContent="center" p="5rem 0">
                <Heading textAlign="center" mb="2rem">{title}</Heading>
                <Text fontSize="14px" pl="5rem" pb="1rem">
                    {subtitle}
                </Text>
                <Box pl="5rem">
                    <LineDivider variants={lineExpansion} />
                    <Flex alignItems="center" justifyContent="center">
                        <Image src={imageUrl} maxW='50%' mt="1.5rem" mb="1.5rem" ml="1.5rem" h="5rem" />
                    </Flex>

                </Box>
            </Box>
            </Link>
        </Card>
    )
}

export default DownCard
