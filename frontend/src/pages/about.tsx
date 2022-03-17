import React from "react"
import { Text, Flex, Image, Divider, Heading } from "@chakra-ui/react"
import { Banner } from "../components/TheHeader"
import agvn from "../public/assets/AGVN_logos/AGVN.png"
import voteInitiatives from "../public/assets/voteInitiatives.png"

interface Props {}

const AboutPage = (props: Props) => {
  React.useEffect(() => {})

  return (
    <>
      <Banner
        {...{
          title: "About A-GVN",
          quote: "Don't call us, we'll call you",
          author: "Hollywood Principle",
        }}
      />
      <Flex m="4rem" flexDir="column">
        <Flex
          className="voting-container"
          justifyContent="center"
          alignItems="center"
          flexDir="column"
          mb="5rem"
        >
          <Heading textAlign="center" mb="1rem">
            A-GVN System
          </Heading>
          <Divider width="50%" />
          <Flex
            alignItems="center"
            justifyContent="center"
            mb="1rem"
            maxW="70%"
          >
            <Text m="2.5rem" w="65%">
              The Automatic Governing System (A-GVN) is the next step in
              governing our society. Moving on from poor, inefficient and
              outdated methods of leadership and evaluation of your desires, we
              are presenting an answer to these problems in the form of a highly
              efficient, highly scalable, extensible and portable software
              system.
            </Text>
            <Image src={agvn} w="35%"></Image>
          </Flex>
        </Flex>
        <Flex
          className="contribution-container"
          justifyContent="center"
          alignItems="center"
          flexDir="column"
          mb="5rem"
        >
          <Flex
            alignItems="center"
            justifyContent="center"
            mb="1rem"
            maxW="70%"
          >
            <Text m="2.5rem" w="65%">
              Using A-GVN you can learn about the various initiatives you may
              choose to support, vote for your chose initiative, boost your
              Contribution Score by completing surveys, view the results from a
              previous voting cycle and more.
            </Text>
            <Image src={voteInitiatives} w="35%"></Image>
          </Flex>
          <Text ml="10rem" className="Note" fontSize="10pt">
            If you wish to learn more, feel free to talk to our chatbot on the
            bottom right. It will answer all of your concerns. If you still have
            more questions, contact us at admin@agvn.info.
          </Text>
        </Flex>
      </Flex>
    </>
  )
}

export default AboutPage
