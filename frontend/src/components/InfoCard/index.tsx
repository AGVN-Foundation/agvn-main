import React, { useState } from "react"
import { Divider, Flex, Box, Heading, Text } from "@chakra-ui/layout"
import { Image } from "@chakra-ui/image"
import { motion } from "framer-motion"
import styled from "styled-components"
import {
  Button,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  useDisclosure,
} from "@chakra-ui/react"

/**
 * rest and hover for parent-child usability
 */
const cardMotion = {
  rest: {
    color: "grey",
    transition: {
      duration: 2,
    },
  },
  hover: {
    color: "#97abb8",
    scale: 1.05,
    transition: {
      duration: 0.4,
    },
  },
  focus: {
    scale: 1.5,
    transition: {
      duration: 0.4,
    },
  },
}

const LineDivider = styled(motion(Divider))``
const Card = styled(motion.div)`
  cursor: pointer;
`

const lineExpansion = {
  rest: {
    width: "10rem",
    duration: 0.2,
  },
  hover: {
    width: "20rem",
    transition: {
      duration: 0.2,
    },
  },
}

interface LeftCardProps {
  title: string
  subtitle?: string
  content?: string
  imageUrl?: string
  backgroundColor?: string
  moreContent?: string
}

export const assignCards = (cardData: Array<LeftCardProps>) => {
  const checkMoreContent = (cardData: Array<LeftCardProps>) => {
    cardData.forEach((c) => {
      if (c.content && c.content.length > 200) {
        c.moreContent = c.content.substr(200)
        c.content = c.content.slice(0, 200)
      }
    })
    return cardData
  }
  return (
    <Flex
      justifyContent="center"
      flexDirection="column"
      alignItems="center"
      p="0.5rem"
    >
      {checkMoreContent(cardData).map((c) => (
        <React.Fragment key={c.title}>
          <LeftCard {...c} />
          <Box h="3.5rem" />
        </React.Fragment>
      ))}
    </Flex>
  )
}

/**
 * on click -> expands even more -> rest of the content fades in
 * when content > 200 characters, make 200+ chars as '...'
 * on click, those box expands and the characters come in
 */

function LeftCard({
  title,
  subtitle,
  content,
  imageUrl,
  moreContent,
}: LeftCardProps) {
  const { isOpen, onOpen, onClose } = useDisclosure()

  const expandCard = () => {
    // set content to content + moreContent
    // moreContent? content = content?.substr(200) + moreContent : content?.substr(200)
    onOpen()
  }

  return (
    <Card
      onClick={expandCard}
      className="card"
      whileFocus="focus"
      whileHover="hover"
      animate="rest"
      variants={cardMotion}
    >
      <Modal
        onClose={onClose}
        isOpen={isOpen}
        isCentered
        size="xl"
        scrollBehavior="inside"
      >
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{title}</ModalHeader>
          <ModalBody>{content + (moreContent ? moreContent : "")}</ModalBody>
        </ModalContent>
      </Modal>
      <Flex justifyContent="space-between" p="2.2rem">
        <Image src={imageUrl} maxW="50%" h="15rem" />
        <Box rounded="false" justifyContent="center">
          <Heading textAlign="center" mb="2rem" maxW="25rem">
            {title}
          </Heading>
          <Text fontSize="0.75rem" pl="5rem" pb="1rem">
            {subtitle}
          </Text>
          <Box pl="5rem">
            <LineDivider variants={lineExpansion} />
          </Box>
          <Box
            className="card-contents"
            maxW="25rem"
            pt="2.5rem"
            pl="5rem"
            pr="5rem"
          >
            {content + (content?.length === 200 ? "..." : "")}
          </Box>
        </Box>
      </Flex>
    </Card>
  )
}

export default LeftCard
