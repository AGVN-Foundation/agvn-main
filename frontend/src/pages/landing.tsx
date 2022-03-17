import React from "react"
import { Flex } from "@chakra-ui/react"
import styled from "styled-components"
import MeshCanvas from "../components/3D"
import { Banner } from "../components/TheHeader"

const FlexWrapper = styled(Flex)`
  html {
    scroll-snap-type: y mandatory;
    overflow-y: scroll;
    height: 100vh;
  }
`

const Section = styled(Flex)`
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #000;
  color: #e3dddc;
  scroll-snap-align: start;
`

function LandingPagePrev() {
  return (
    <>
      {Banner({ title: "", display: false })}
      <FlexWrapper gridColumn="4/12" colSpan="4">
        <Section gridColumn="4/12" colSpan="4">
          Welcome
        </Section>
        <Section gridColumn="4/12" colSpan="4">
          Section 2
        </Section>
      </FlexWrapper>
    </>
  )
}

function LandingPage() {
  return (
    <>
      <MeshCanvas />
    </>
  )
}

export default LandingPage
