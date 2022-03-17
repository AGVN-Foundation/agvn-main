import React, { useState } from "react"
import {
  Box,
  Button,
  Flex,
  Heading,
  Divider,
  Text,
  Image,
  FormControl,
  Input,
  FormLabel,
  IconButton,
  Spinner,
} from "@chakra-ui/react"
import { AiFillQuestionCircle } from "react-icons/ai"
import assignCards, {
  BenefitCardProps,
} from "../components/InfoCard/benefit_card"
import axios from "axios"
import Cookies from "universal-cookie"
import { Modal } from "react-bootstrap"

import grant from "../public/assets/ContributionScreen_icons/grant.png"
import localCandidate from "../public/assets/ContributionScreen_icons/local_candidate.jpg"
import sponsorship from "../public/assets/ContributionScreen_icons/sponsorship.png"
import subsidy from "../public/assets/ContributionScreen_icons/subsidy.png"
import stateCandidate from "../public/assets/ContributionScreen_icons/state_candidate.jpg"
import { Banner } from "../components/TheHeader"
import Form from "react-bootstrap/Form"
import {
  CheckCircleFill,
  X,
  ExclamationCircleFill,
} from "react-bootstrap-icons"
import {
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  CloseButton,
} from "@chakra-ui/react"

const behavioralUrl = "http://localhost:8200/behavioral/"

function VContributionDialog(props: any) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          <Flex alignItems="center">
            <Text mr="1rem">What is my Contribution Index?</Text>
            <ExclamationCircleFill />
          </Flex>
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Text>
          Your contribution index shows how much you've taken part in your
          community. Contribution is a benefit-only scheme that allows you, an
          outstanding citizen, to easily apply for government benefits like
          subsidies and tax breaks because you've have contributed to the
          greater public good.
        </Text>
      </Modal.Body>
    </Modal>
  )
}

const CONTRIBUTE_CARDS: Array<BenefitCardProps> = [
  {
    title: "Grants & Sponsorships",
    threshold: 2000,
    imageUrl: grant,
    imageUrl2: sponsorship,
  },
  {
    title: "Subsidies & Run for Local Government",
    threshold: 10000,
    imageUrl: subsidy,
    imageUrl2: localCandidate,
  },
  {
    title: "Run for State Government",
    threshold: 20000,
    imageUrl: stateCandidate,
  },
]

interface ErrorInterface {
  title: string
  body?: string
}

const goodLabels = [
  "fun",
  "giving blood",
  "helping others",
  "teamwork",
  "volunteering",
]

const badLabels = ["assault", "bullying", "riots", "stealing", "vandalism"]

const ContributePage = () => {
  const cookies = new Cookies()
  const [contributionScore, setContributionScore] = useState(500)
  const [contributionTier, setContributionTier] = useState(1)
  const [auth, setAuth] = React.useState(false)
  const [show, setShow] = React.useState(false)
  const [analyzed, setAnalyzed] = React.useState(0)
  const [encodedFile, setEncodedFile] = React.useState<
    string | null | ArrayBuffer
  >(null)
  const [errorMsg, setErrorMsg] = React.useState<ErrorInterface>({
    title: "",
    body: "",
  })
  const [showErrDialog, setShowErrDialog] = React.useState(false)

  function handleShowContribution() {
    setShow(true)
  }

  function handleShowErrDialog() {
    setShowErrDialog(true)
  }

  async function handleSubmit() {
    if (encodedFile) {
      setAnalyzed(1)
      axios
        .post(
          behavioralUrl,
          { image: encodedFile },
          { headers: { "Content-Type": "application/json" } }
        )
        .then((res) => {
          let x = res.data.label
          console.log(x)
          setAnalyzed(goodLabels.includes(x) ? 2 : 3)
          // pop a modal up, green background, congratulating the user.
        })
        .catch((err) => console.log(err))
    } else {
      setErrorMsg({ title: "Please specify an image." })
      handleShowErrDialog()
    }
  }

  const noLoginContainer = (
    <Flex
      className="contribution-container"
      justifyContent="center"
      alignItems="center"
      flexDir="column"
      mb="5rem"
    >
      <Heading textAlign="center" mb="1rem" mt="10" size="2xl">
        Login to see your contribution!
      </Heading>
      <Text className="Note" fontSize="10pt">
        Note: Contribution is a benefit only scheme, meaning you will only gain
        benefits by participating!
      </Text>
    </Flex>
  )

  const loginContainer = (
    <Flex
      className="contribution-container"
      justifyContent="center"
      alignItems="center"
      flexDir="column"
      mb="5rem"
    >
      <VContributionDialog show={show} onHide={() => setShow(false)} />
      <Heading textAlign="center" mb="1rem">
        Your Contribution
      </Heading>
      <Divider width="50%" mb="2rem" />
      <Flex
        flexDir="row"
        className="contribution-items"
        alignItems="center"
        justifyContent="center"
        mb="1rem"
        backgroundColor="#bdbdbd"
      >
        <Flex className="score-tier" flexDir="column" m="2rem">
          <FormControl id="score" mb="1.2rem">
            <FormLabel>Your Contribution</FormLabel>
            <Input type="" value={contributionScore}></Input>
          </FormControl>
          <FormControl id="tier">
            <FormLabel>Your Contribution Tier</FormLabel>
            <Input type="" value={contributionTier}></Input>
          </FormControl>
        </Flex>
        <IconButton
          onClick={handleShowContribution}
          ml="10rem"
          mr="2rem"
          icon={<AiFillQuestionCircle />}
          aria-label="What is this"
          colorScheme="blue"
          size="2xl"
          fontSize="40px"
        />
      </Flex>
      <Text className="Note" fontSize="10pt">
        Note: Contribution is a benefit only scheme, meaning you will only gain
        benefits by participating!
      </Text>
    </Flex>
  )

  function recordFile(e: any) {
    const file = e.target.files[0]
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = function () {
      setEncodedFile(reader.result)
      console.log(encodedFile)
    }
    reader.onerror = function (error) {
      console.log("error")
    }
  }

  const retrieveContribution = async () => {
    const url = "http://localhost:8000/api/v1/profile"
    const token = cookies.get("token")
    let response = await axios.get(url, { headers: { Authorization: token } })
    console.log(response)

    let contriFull = response.data["contribution"].pop()

    setContributionScore(contriFull)
    // tier 1 -> 1000
    // tier 2 -> 10000
    // tier 3 -> 20000
    let tierC = 3
    if (contriFull < 20000) {
      tierC = 2
    }
    if (contriFull < 1000) {
      tierC = 1
    }
    setContributionTier(tierC)
  }

  React.useEffect(() => {
    setAuth(cookies.get("token") ? true : false)
    retrieveContribution()
  })

  // const formData = new FormData()

  // const [selectedFile, setSelectedFile] = React.useState(null)

  return (
    <>
      {Banner({
        title: "Contribution",
        subtitle:
          "View your hard efforts in contributing to societal development",
        quote:
          "If the only thing a man does is to sleep and eat, he's not better than an animal",
        author: "Shakespeare",
      })}
      <Flex
        flexDir="column"
        m="4rem"
        justifyContent="center"
        alignItems="center"
      >
        {auth ? loginContainer : noLoginContainer}
        <Flex
          className="benefits-container"
          justifyContent="center"
          alignItems="center"
          flexDir="column"
          mb="5rem"
        >
          {assignCards(CONTRIBUTE_CARDS)}
        </Flex>
        <Flex
          maxW="50rem"
          flexDir="column"
          justifyContent="center"
          alignItems="center"
        >
          <Heading mb="3rem">Did something good for the community?</Heading>
          <Text mb="2rem">
            With behavioral analysis, we can detect you doing the right thing in
            the community. Whether that's helping out with cleaning up your
            neighborhood, volunteering your time, checking up on people in need.
          </Text>
          <Form.Group
            className="mb-3"
            style={{ marginBottom: "2rem", minWidth: "30rem" }}
          >
            <Form.Control
              type="file"
              onInput={recordFile}
              accept=".jpg, .jpeg, .png, .svg"
              style={{
                minWidth: "100%",
              }}
            />
          </Form.Group>
          <Button
            className="submit"
            onClick={handleSubmit}
            backgroundColor="black"
            color="white"
            mb="1rem"
          >
            Submit
          </Button>
          {analyzed == 1 ? (
            <Spinner />
          ) : analyzed == 2 ? (
            <Flex>
              <CheckCircleFill size={35} color="green" />
              <Text ml="1rem">
                Nice! We think you did something positive for the community.
              </Text>
            </Flex>
          ) : analyzed == 0 ? null : (
            <Flex>
              <X size={35} color="red" />
              <Text ml="1rem">
                Sorry, we don't think you did something good in this image.
              </Text>
            </Flex>
          )}
          <Box mb="1rem" />
          {showErrDialog && (
            <Alert status="error">
              <AlertIcon />
              <AlertTitle mr={2}>{errorMsg.title}</AlertTitle>
              <AlertDescription>{errorMsg.body}</AlertDescription>
              <CloseButton
                position="absolute"
                right="8px"
                top="8px"
                onClick={() => {
                  setShowErrDialog(false)
                }}
              />
            </Alert>
          )}
        </Flex>
      </Flex>
    </>
  )
}

export default ContributePage
