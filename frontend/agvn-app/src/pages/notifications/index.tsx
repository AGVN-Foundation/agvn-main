import { Box, Button, Divider, Flex, Heading, Image, Text, useDisclosure } from '@chakra-ui/react'
import { motion } from 'framer-motion'
import { remove } from 'lodash'
import React from 'react'
import styled from 'styled-components'
import { Banner } from '../../components/TheHeader'
import administrative from '../../public/assets/Occupation_icons/administrative.png'
import financial from '../../public/assets/Occupation_icons/financial.png'
import { CheckLg, PatchExclamationFill } from 'react-bootstrap-icons'

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
  },
  focus: {
    scale: 1.5,
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

interface NotificationCardProps {
  title: string,
  subtitle?: string,
  content?: string,
  imageUrl?: string,
  backgroundColor?: string,
  moreContent?: string
}

export const assignCards = (cardData: Array<NotificationCardProps>) => {
  const [cards, setCards] = React.useState()
  const handleAccept = (title: string) => {
    // make the box disappear and put 'TICK' in its place
    setCards(cards)
  }

  return (
    <Flex justifyContent="center" flexDirection="column" alignItems="center" p="0.5rem">
      {cardData.map((c) => (
        <React.Fragment key={c.title}>
          <NotificationCard {...c} />
          <Box h="3.5rem" />
        </React.Fragment>
      ))}
    </Flex>
  )
}

// NOTE: if accepted a new position, all the promotion offers are set to false

function NotificationCard({ title, subtitle, content, imageUrl, moreContent }: NotificationCardProps) {
  const handleClick = (type: boolean) => {
    setIconB(type ? <CheckLg size={35} color="green" /> : <Text>That's unfortunate. We hope you consider us again next time.</Text>)
    setShowButtons(false)
  }
  const [showButtons, setShowButtons] = React.useState(true)
  const [iconB, setIconB] = React.useState<any>("")

  return (
    <Card className="card" whileFocus="focus" whileHover="hover" animate="rest" variants={cardMotion}>
      <Flex justifyContent='space-between' p="2.2rem">
        <Image src={imageUrl} maxW='50%' h="15rem" />
        <Box rounded="false" justifyContent="center">
          <Heading textAlign="left" mb="2rem" maxW="25rem">{title}</Heading>
          <Text fontSize="0.75rem" pl="5rem" pb="1rem">
            {subtitle ? subtitle : ""}
          </Text>
          <Box pl="5rem">
            <LineDivider variants={lineExpansion} />
          </Box>
          <Box className="card-contents" maxW="25rem" pt="2.5rem" pl="5rem" pr="5rem">
            {content ? (content + (content?.length === 200 ? "..." : "")) : ""}
          </Box>
        </Box>
      </Flex>
      {
        showButtons ?
          <Flex alignItems="center" justifyContent="center">
            <Button colorScheme="green" m="1rem" onClick={() => handleClick(true)}>Accept</Button>
            <Button colorScheme="red" m="1rem" onClick={() => handleClick(false)}>Reject</Button>
          </Flex>
          :
          iconB
      }
    </Card>
  )
}


function NotificationPage() {
  const NOTIFICATION_SAMPLES: NotificationCardProps[] = [
    {
      title: "Promotion Available!",
      subtitle: "You have a new promotion for your Administrative position!",
      imageUrl: administrative
    },
    {
      title: "Position Available!",
      subtitle: "A position as a government financial analyst is available based on your skills!",
      imageUrl: financial
    }
  ]
  return (
    <>
      <Banner {...{ title: "Notifications" }} />
      <Flex flexDir="column" p="5rem">
        {assignCards(NOTIFICATION_SAMPLES)}
      </Flex>
    </>
  )
}

export default NotificationPage
