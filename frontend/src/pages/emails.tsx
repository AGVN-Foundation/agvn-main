import { Flex } from "@chakra-ui/react"
import React from "react"
import { Banner } from "../components/TheHeader"

function Emails() {
  React.useEffect(() => {})

  return (
    <>
      {Banner({
        title: "Emails",
        subtitle: "View all your emails in one place",
        quote:
          "If the only thing a man does is to sleep and eat, he's no better than an animal",
        author: "Shakespeare",
      })}
      <Flex></Flex>
    </>
  )
}

export default Emails
