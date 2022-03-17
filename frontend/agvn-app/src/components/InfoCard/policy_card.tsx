import React from 'react'
import { Divider, Flex, Box, Heading, Text } from '@chakra-ui/layout'
import { Image } from '@chakra-ui/image'
import { motion } from 'framer-motion'
import styled from 'styled-components'
import { Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useDisclosure } from "@chakra-ui/react"

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
    padding: 2rem;
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

export interface PolicyCardProps {
    title: string,
    subtitle?: string,
    content?: string,
    imageUrl?: string,
    moreContent?: string
}

export const assignCards = (cardData: Array<PolicyCardProps>) => {
    const checkMoreContent = (cardData: Array<PolicyCardProps>) => {
        cardData.forEach(c => {
            if (c.content && c.content.length > 200) {
                c.moreContent = c.content.substr(200)
                c.content = c.content.slice(0, 200)
            }
        })
        return cardData
    }

    return (
        <Flex justifyContent="center" flexDirection="row" alignItems="center" flexWrap="wrap">
            {
                checkMoreContent(cardData).map((c) => (
                    <Box key={c.title} m="2.5rem">
                        <PolicyCard {...c} />
                    </Box>
                ))}
        </Flex>
    )
}

function PolicyCard({ title, subtitle, content, imageUrl, moreContent }: PolicyCardProps) {
    const { isOpen, onOpen, onClose } = useDisclosure()

    const expandCard = () => {
        // set content to content + moreContent
        // moreContent? content = content?.substr(200) + moreContent : content?.substr(200)
        onOpen()
    }
    return (
        <Card onClick={expandCard} className="card" whileHover="hover" animate="rest" variants={cardMotion}>
            <Modal onClose={onClose} isOpen={isOpen} isCentered size="xl" scrollBehavior="inside">
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>{title}</ModalHeader>
                    <ModalBody>{content + (moreContent ? moreContent : "")}</ModalBody>
                </ModalContent>
            </Modal>
            <Box rounded="false" justifyContent="center" p="5rem 0" h="25rem">
                <Heading textAlign="center" mb="2rem">{title}</Heading>
                <Text fontSize="14px" pl="5rem" pb="1rem">
                    {subtitle}
                </Text>
                <Box pl="5rem">
                    <LineDivider variants={lineExpansion} />
                </Box>
                <Image src={imageUrl} maxW='50%' mt="-1.5rem" mb="0.5rem" ml="27rem" maxHeight="3rem" />
                <Box className="card-contents" width="40rem" pt="2.5rem" pl="5rem" pr="5rem">
                    {content + (content?.length === 200 ? "..." : "")}
                </Box>
            </Box>
        </Card>
    )
}

export default PolicyCard
