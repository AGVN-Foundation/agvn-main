import React from "react"
import { Text, Flex, Image, Heading, Divider } from "@chakra-ui/react"
import calendar from '../public/assets/Images/calendar.png'
import { assignCards, DownCardProps } from "../components/InfoCard/down_card"
import actions from "../public/assets/HomeScreen_icons/Actions.png"
import department from "../public/assets/HomeScreen_icons/Department.png"
import policy from "../public/assets/HomeScreen_icons/Policy.png"
import aeros from "../public/assets/aeros_logo.png"
import { Banner } from "../components/TheHeader"


const HOME_CARDS: Array<DownCardProps> = [
  {
    title: "Current Policies",
    imageUrl: policy,
    directUrl: '/policies'
  },
  {
    title: "Actions we're taking",
    imageUrl: actions,
    directUrl: '/actions'
  },
  {
    title: "Our Departments",
    imageUrl: department,
    directUrl: '/departments'
  },
  {
    title: "Aeros (G-Coin)",
    imageUrl: aeros,
    directUrl: '/aeros'
  },
]

const Home = () => {
  return (
    <>
      {Banner({ title: "Home", subtitle: "There's no place like home" })}
      <Flex m="4rem" flexDir="column">
        <Flex className="voting-container" justifyContent="center" alignItems="center" flexDir="column" mb="5rem">
          <Heading textAlign="center" >Next Voting Stage</Heading>
          <Text>September, 2021</Text>
          <Divider width='50%' />
          <Flex alignItems="center" justifyContent="center" mb="1rem">
            <Text m="2.5rem" maxW="25rem">
              Welcome to the Automatic Governing System (A-GVN)!
              <br />
              Here you can browse our initiatives that are generated based on everyone's interests.
              Vote for initiatives, grow your contribution and complete polls to enhance the system.
              Learn about what AGVN is doing for you!
              <br />
              Visit our About page for more information.
            </Text>
            <Image src={calendar}></Image>
          </Flex>
          <Text ml="10rem" className="Note" fontSize="10pt">Note: to vote you must have an account with A-GVN Services.</Text>
        </Flex>

        <Flex className="home-cards" justifyContent="center" alignItems="center" flexDir="column">
          <Heading textAlign="center" mb="1rem">New to AGVN?</Heading>
          <Divider width='50%' />
          <Flex ml="5rem" mr="5rem">
            {assignCards(HOME_CARDS)}
          </Flex>
        </Flex>
      </Flex>
    </>
  )

}
export default Home
