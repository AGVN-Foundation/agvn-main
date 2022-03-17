import React from "react"
import { Box, Divider, Flex } from "@chakra-ui/react"

import { assignCards } from "../components/InfoCard"
import PageTitle from "../components/PageTitle"
import agriculture from "../public/assets/Departments_logos/Agriculture.jpg"
import defence from "../public/assets/Departments_logos/defence.png"
import edu from "../public/assets/Departments_logos/edu.png"
import finance from "../public/assets/Departments_logos/Finance.jpg"
import foreign from "../public/assets/Departments_logos/foreign-affairs.png"
import health from "../public/assets/Departments_logos/health.png"
import home_affairs from "../public/assets/Departments_logos/home-affairs.png"
import industry from "../public/assets/Departments_logos/industry-science.png"
import infrastructure from "../public/assets/Departments_logos/infrastructure.jpg"
import social from "../public/assets/Departments_logos/social-services.png"
import veterans from "../public/assets/Departments_logos/veterans.png"
import { Banner } from "../components/TheHeader"
import {
  FormControl,
  FormLabel,
  Input,
  Button,
  Heading,
} from "@chakra-ui/react"
import axios from "axios"

const DEPARTMENTS = [
  {
    title: "Defense",
    subtitle: "Defense, is superior to opulence.",
    content: `We all know that a strong country requires strong defense. 
    The Australian Defence Force (ADF) is the military organisation responsible for the defence of Australia and its national interests. It consists of the Royal Australian Navy (RAN), Australian Army, Royal Australian Air Force (RAAF) and several "tri-service" units. The ADF has a strength of just over 85,000 full-time personnel and active reservists and is supported by the Department of Defence and several other civilian agencies.

    During the first decades of the 20th century, the Australian Government established the armed services as separate organisations. Each service had an independent chain of command. In 1976, the government made a strategic change and established the ADF to place the services under a single headquarters. Over time, the degree of integration has increased and tri-service headquarters, logistics, and training institutions have supplanted many single-service establishments.

    The ADF is technologically sophisticated but relatively small. Although the ADF's 58,206 full-time active-duty personnel and 29,560 active reservists make it the largest military in Oceania, it is smaller than most Asian military forces. Nonetheless, the ADF is supported by a significant budget by worldwide standards and can deploy forces in multiple locations outside Australia. 
    `,
    imageUrl: defence,
  },
  {
    title: "Agriculture & Enviroment",
    subtitle: "The environment just got greener.",
    content:
      "Whether a bushfire or a flood, we got you covered. The environment is the basis for all life.",
    imageUrl: agriculture,
  },
  {
    title: "Infrastructure & Transport",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: infrastructure,
  },
  {
    title: "Education, Skills & Employment",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: edu,
  },
  {
    title: "Finance",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: finance,
  },
  {
    title: "Foreign Affairs",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: foreign,
  },
  {
    title: "Health",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: health,
  },
  {
    title: "Home Affairs",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: home_affairs,
  },
  {
    title: "Industry, Science, Energy & Resources",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: industry,
  },
  {
    title: "Social Services",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: social,
  },
  {
    title: "Veteran's Affairs",
    subtitle: "Learn more about the federal government's transport schemes.",
    content: "The best transport is teleportation.",
    imageUrl: veterans,
  },
]

const DepartmentsPage = () => {
  React.useEffect(() => {})

  const mapsAPIURL = "http://localhost:7200/maps/search/"
  const [iframeSrc, setiframeSrc] = React.useState<any>()
  const [formValue, setFormValue] = React.useState<string>()
  const handleSearchDepartments = () => {
    // CALL GET on scraper/maps/search
    axios.get(mapsAPIURL + `?search=${formValue}`).then((res) => {
      setiframeSrc(res.data["iframe_src"])
    })
    setFormValue("")
  }

  const [goToValue, setGoToValue] = React.useState(
    "https://www.google.com/maps/embed/v1/place?API_KEY=&q="
  )

  const handleChangeGoToValue = (event: any) => {
    // replace spaces with addition signs
    let val = event.target.value
    val.replace(" ", "+")
    setGoToValue(val)
  }

  return (
    <>
      {Banner({
        title: "Departments",
        subtitle: "Understand what the government is doing for you",
        quote: "Who deserves more credit than the wife of a coal miner?",
        author: "Merle Travis",
      })}
      <Flex flexDirection="column" justifyContent="center" alignItems="center">
        <Box m="20">
          <PageTitle title="Departments" />
          <Divider />
        </Box>

        {assignCards(DEPARTMENTS)}

        <Flex
          className="map-recommender"
          flexDir="column"
          justifyContent="center"
          alignItems="center"
        >
          <Box m="20">
            <Heading mb="1rem">Need to go somewhere?</Heading>
            <Divider mb="2rem" />
            <FormControl>
              <FormLabel>
                We'll recommend a place for you to get your things sorted.
              </FormLabel>
              <Flex
                justifyContent="center"
                alignItems="center"
                flexDir="column"
              >
                <Input
                  placeholder="Tell me where you want to go"
                  onChange={handleChangeGoToValue}
                />
                <Button mt={4} colorScheme="teal" type="submit">
                  Submit
                </Button>
              </Flex>
            </FormControl>
          </Box>
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d16687.156700646265!2d151.23325406570711!3d-33.91151570101442!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6b129838f39a743f%3A0x3017d681632a850!2sSydney%20NSW!5e0!3m2!1sen!2sau!4v1627704530940!5m2!1sen!2sau"
            width="600"
            height="450"
            style={{ border: "0" }}
            loading="lazy"
          ></iframe>
        </Flex>
      </Flex>
    </>
  )
}

export default DepartmentsPage
