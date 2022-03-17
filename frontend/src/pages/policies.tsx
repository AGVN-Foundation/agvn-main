// @ts-nocheck

import React from "react"
import {
  assignCards,
  PolicyCardProps,
} from "../components/InfoCard/policy_card"
import { Grid, Flex } from "@chakra-ui/layout"
import { Banner } from "../components/TheHeader"
import { Button, Input, Radio, RadioGroup, Stack, Text } from "@chakra-ui/react"

import health from "../public/assets/PolicyType_logos/health.jpg"
import community from "../public/assets/PolicyType_logos/community.jpg"
import education from "../public/assets/PolicyType_logos/education.png"
import national_security from "../public/assets/PolicyType_logos/national_security.png"
import economy from "../public/assets/PolicyType_logos/economy.jpg"
import employment from "../public/assets/PolicyType_logos/employment.png"
import energy from "../public/assets/PolicyType_logos/energy.jpg"
import foreign_affairs from "../public/assets/PolicyType_logos/foreign_affairs.png"
import foreign_trade from "../public/assets/PolicyType_logos/foreign_trade.png"
import industry from "../public/assets/PolicyType_logos/industry.jpg"
import natural_resources from "../public/assets/PolicyType_logos/natural_resources.jpg"
import environment from "../public/assets/PolicyType_logos/environment.png"
import science_and_technology from "../public/assets/PolicyType_logos/science_and_technology.png"
import taxation from "../public/assets/PolicyType_logos/taxation.png"
import axios from "axios"
import { CodeSlash } from "react-bootstrap-icons"

const PolicyTypeMap = {
  health: health,
  community: community,
  education: education,
  national_security: national_security,
  economy: economy,
  employment: employment,
  energy: energy,
  foreign_affairs: foreign_affairs,
  foreign_trade: foreign_trade,
  industry: industry,
  natural_resources: natural_resources,
  environment: environment,
  science_and_technology: science_and_technology,
  taxation: taxation,
}

const SamplePolicies: Array<PolicyCardProps> = [
  {
    title: "Better health for students",
    content:
      "A society is made up of people. A health population brings about a healthy society.",
    imageUrl: health,
  },
  {
    title: "Stronger Families",
    content:
      "The family is the smallest unit of humanity. Whether you're in a small or large family, we wish to give all the support we can.",
    imageUrl: community,
  },
  {
    title: "Higher Education",
    content:
      "Since the industrial revolution, education has been the driving force for societal advancement. To support Australia's scientific and advanced industries, we are investing as much as we can into stronger education",
    imageUrl: education,
  },
  {
    title: "Stronger Borders",
    content:
      "Security for our citizens is paramount. We wish the best for everyone, Australians and foreigners. But not everyone should be calling Australia home, especially those willing to cause harm.",
    imageUrl: national_security,
  },
]

function Policies() {
  const [policies, setPolicies] =
    React.useState<Array<PolicyCardProps>>(SamplePolicies)
  const [prompt, setPrompt] = React.useState<string>("")
  const [value, setValue] = React.useState(health)
  const [devMode, setDevMode] = React.useState(false)

  const policyUrl = "http://localhost:8200/policy/recommend/"

  const getPolicy = (prompt: string, callback: any) => {
    axios
      .get(policyUrl, { params: { policy: prompt } })
      .then((res) =>
        setPolicies([
          ...policies,
          {
            title: prompt,
            content: res.data["text"],
            imageUrl: PolicyTypeMap[value],
          },
        ])
      )
      .then(callback())
      .catch((err) => console.log(err))
  }

  const handleChange = (event: any) => {
    setPrompt(event.target.value)
  }

  const handleClick = () => {
    getPolicy(prompt, () => {
      setPrompt("")
      console.log(value)
    })
  }

  const [helpful, setHelpful] = React.useState(false)
  const handleHelpfulClick = () => {
    setHelpful(true)
  }

  return (
    <>
      <Banner
        {...{
          title: "Policies",
          subtitle: "Understand the policies we're implementing",
          quote: "If the facts don't fit the theory, change the facts",
          author: "Albert Einstein",
        }}
      />
      <Flex flexDir="column" justifyContent="center" alignItems="center">
        <Grid gridColumn="3/13" mb="10rem">
          <Flex
            justifyContent="center"
            flexDirection="column"
            alignItems="center"
          >
            {assignCards(policies)}
          </Flex>
        </Grid>
        <Flex
          flexDir="column"
          justifyContent="center"
          alignItems="center"
          mb="4rem"
        >
          <Text mb="2rem">Helpful?</Text>
          {!helpful ? (
            <Flex>
              <Button
                backgroundColor="black"
                color="white"
                mr="2rem"
                onClick={handleHelpfulClick}
              >
                Yes
              </Button>
              <Button
                backgroundColor="black"
                color="white"
                onClick={handleHelpfulClick}
              >
                No
              </Button>
            </Flex>
          ) : (
            <Text>Thanks for your feedback.</Text>
          )}
        </Flex>
        <Flex className="ctl-panel" p="5rem" flexDir="column">
          <CodeSlash
            size={35}
            onClick={() => {
              setDevMode(!devMode)
            }}
            cursor="pointer"
          />
          {devMode && (
            <>
              <Input value={prompt} onChange={handleChange} />
              <RadioGroup onChange={setValue} value={value}>
                <Flex flexDir="row" p="2rem" flexWrap="wrap">
                  {Object.keys(PolicyTypeMap).map((key, val) => (
                    <Radio key={key} value={key} m="1rem">
                      {key}
                    </Radio>
                  ))}
                </Flex>
              </RadioGroup>
              <Button onClick={handleClick}>Submit</Button>
            </>
          )}
        </Flex>
      </Flex>
    </>
  )
}

export default Policies
