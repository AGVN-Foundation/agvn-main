// @ts-nocheck

import React, { useState } from "react"
import {
  Text,
  Box,
  Flex,
  Button,
  Heading,
  Image,
  Divider,
} from "@chakra-ui/react"
import axios from "axios"
import { Banner } from "../components/TheHeader"
import agvn from "../public/assets/AGVN_white.svg"
import torch from "../public/assets/Initiative_logos/conservatism_logo_2.png"
import individual from "../public/assets/Initiative_logos/libertarianism_logo.png"
import triangleCircle from "../public/assets/Initiative_logos/progressivism_logo_2.png"
import fist from "../public/assets/Initiative_logos/radical_progressivism_logo.png"
import trident from "../public/assets/Initiative_logos/libertariansim_logo_2_.png"
import pidgeon from "../public/assets/Initiative_logos/progressivism_logo.png"
import lion from "../public/assets/Initiative_logos/conservatism_logo.png"
import owl from "../public/assets/Initiative_logos/neutral_logo.png"
import Cookies from "universal-cookie"

import { CheckCircleFill } from "react-bootstrap-icons"
import { motion } from "framer-motion"
import Popups from "../components/Popup"

const host = "http://localhost:8000/api/v1"

interface VotePageProps {}

const VotePage: React.FC<VotePageProps> = (props) => {
  const [endDate, setEndDate] = useState("")
  const [electId, setElectId] = useState(0)
  const [errorMsg, setErrorMsg] = useState("")
  const [authorised, setAuthorised] = React.useState(false)
  const cookies = new Cookies()

  const initiatives = [
    { type: "Conservatism", icon: torch, value: 1 },
    { type: "Progressivism", icon: triangleCircle, value: 2 },
    { type: "Libertarianism", icon: individual, value: 3 },
    { type: "Activism", icon: pidgeon, value: 4 },
    { type: "Technocratism", icon: owl, value: 5 },
    { type: "Socialism", icon: fist, value: 6 },
    { type: "Statist", icon: lion, value: 7 },
    { type: "Nationalism", icon: trident, value: 8 },
  ]
  const [items, setItems] = useState<
    { type: string; icon: any; value: number }[]
  >([])
  const [selected, setSelected] = useState<
    { type: string; icon: any; value: number }[]
  >([])
  const [submitted, setSubmitted] = React.useState(false)

  const sendVotes = async () => {
    setErrorMsg("")
    if (selected.length !== items.length) {
      setErrorMsg("Please rank all the initiatives.")
    } else {
      let list = []
      for (var i of selected) {
        list.push(i.value)
      }
      const data = {
        elect_id: electId,
        initiatives: list,
      }
      const config = {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: cookies.get("token"),
        },
      }
      axios
        .post(`${host}/vote`, data, config)
        .then(function (response) {
          setSubmitted(true)
          setErrorMsg("")
        })
        .catch(function (error) {
          if (error.response) {
            setErrorMsg("An error has occurred, please try again.")
            if (error.response.status === 500) {
              setErrorMsg("An error has occurred, please try again.")
            }
          } else if (error.request) {
            setErrorMsg("An error has occurred, please try again.")
          } else {
            setErrorMsg("An error has occurred, please try again.")
          }
        })
    }
  }

  const voteProp = (
    <>
      <Flex
        className="vote-container"
        justifyContent="center"
        alignItems="center"
        flexDir="column"
        mb="5rem"
      >
        <Heading textAlign="center" mb="1rem">
          Vote for Initiatives
        </Heading>
        <Divider width="50%" mb="2rem" />
        <Text>Current voting stage ends: {endDate}</Text>
        <Text>Rank your preferences, from most to least desirable.</Text>
      </Flex>
      <Flex>
        <Flex flexDir="column">
          <Text
            textAlign="center"
            mb="1rem"
            fontWeight="semibold"
            color="#1d2533"
            fontSize="1.5rem"
          >
            Choose from
          </Text>
          <Box minH="250px" w="25rem" border="1px solid gray">
            {items
              .filter((item) => !selected.some((x) => x === item))
              .map((item) => (
                <Flex key={item.type} justify="center">
                  <Button
                    w="95%"
                    my="8px"
                    onClick={() => {
                      setSelected([...selected, item])
                      setErrorMsg("")
                    }}
                  >
                    <Flex justifyContent="space-between" alignItems="center">
                      {item.type}
                      <Image src={item.icon} height="2rem" ml="0.5rem" />
                    </Flex>
                  </Button>
                </Flex>
              ))}
          </Box>
        </Flex>
        <Flex justify="center" alignItems="center" m="2rem">
          {">"}
        </Flex>
        <Flex flexDir="column">
          <Text
            textAlign="center"
            mb="1rem"
            fontWeight="semibold"
            color="#1d2533"
            fontSize="1.5rem"
          >
            Your choices
          </Text>
          <Box minH="250px" minW="25rem" border="1px solid gray">
            {selected.map((item) => {
              if (item.value !== 0) {
                return (
                  <Flex key={item.value} justify="center">
                    <Button
                      w="95%"
                      my="8px"
                      onClick={() => {
                        setSelected([...selected.filter((x) => x !== item)])
                        setErrorMsg("")
                      }}
                    >
                      {item.type}
                      <Image src={item.icon} height="2rem" ml="0.5rem" />
                    </Button>
                  </Flex>
                )
              }
            })}
          </Box>
        </Flex>
      </Flex>
      <Button w="50%" m="4.5rem" onClick={sendVotes}>
        Submit
      </Button>
    </>
  )

  const submittedProp = (
    <motion.div
      initial="pageInitial"
      animate="pageAnimate"
      variants={{
        pageInitial: {
          opacity: 0,
        },
        pageAnimate: {
          opacity: 1,
        },
      }}
    >
      <Flex alignItems="center">
        <Heading mt="10" mb="10" size="2xl" textAlign="center" mr="2rem">
          You voted!
        </Heading>
        <CheckCircleFill size="5rem" color="green" />
      </Flex>
    </motion.div>
  )

  const loginProp = <>{submitted ? submittedProp : voteProp}</>

  const logoutProp = (
    <>
      <Heading mt="10" mb="10" size="2xl" textAlign="center">
        Login to Vote!
      </Heading>
    </>
  )

  const effectFn = async () => {
    try {
      const req = {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
      const response = await fetch(`${host}/election/`, req)
      if (response.status === 200) {
        const data = await response.json()
        setElectId(data[0].elect_id)
      }
    } catch (error) {
      setErrorMsg("An error has occurred, please try again.")
    }
  }

  async function getInitiatives() {
    try {
      const req = {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
      const response = await fetch(
        `${host}/initiatives?elect_id=${electId}`,
        req
      )
      if (response.status === 200) {
        const data = await response.json()
        var item = []
        for (var i of data.initiatives) {
          item.push(initiatives[i - 1])
        }
        setItems(item)
      }
    } catch (error) {
      setErrorMsg("An error has occurred, please try again.")
    }
  }

  React.useEffect(() => {
    if (cookies.get("token") !== undefined) {
      setAuthorised(true)
      effectFn()
      setSelected([])
    }
    if (electId !== 0) {
      getInitiatives()
      checkVoted()
    }
  }, [electId])

  async function checkVoted() {
    const config = {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: cookies.get("token"),
      },
    }
    axios
      .get(`${host}/vote?elect_id=${electId}`, config)
      .then(function (response) {
        if (response.status === 202) {
          setSubmitted(true)
        } else {
          setSubmitted(false)
        }
        var date = new Date(response.data.end_date)
        const options = {
          day: "numeric",
          month: "long",
          year: "numeric",
          hour: "numeric",
          minute: "numeric",
          timeZoneName: "short",
        }
        setEndDate(date.toLocaleDateString("en-AU", options))
      })
      .catch(function (error) {
        setErrorMsg(
          "An error has occurred, please refresh the page to try again."
        )
      })
  }

  return (
    <>
      {Banner({
        title: "Vote",
        subtitle: "Elect the initiatives you desire",
        imgUrl: agvn,
      })}
      <Flex
        m="5rem"
        flexDir="column"
        alignItems="center"
        justifyContent="center"
      >
        {authorised ? loginProp : logoutProp}
      </Flex>
      <Popups type="error" message={errorMsg} />
    </>
  )
}

export default VotePage
