import React from "react"
import { Flex, Heading, Divider, Text, Box } from "@chakra-ui/layout"
import Modal from "react-bootstrap/Modal"
import { FormControl, FormLabel, Input, Button, Switch } from "@chakra-ui/react"
import LogoAnimateVariants from "../components/2DAnimations"
import { motion } from "framer-motion"

interface Props {}

function PopupMenu(props: any) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {props.title}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body style={{ padding: "3rem" }}>{props.content}</Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  )
}

const Option = (title: string, subtitle: string, content?: any) => {
  const [show, setShow] = React.useState(false)
  const handleShow = () => {
    setShow(true)
  }
  const handleClose = () => {
    setShow(false)
  }
  return (
    <Flex flexDir="column">
      <PopupMenu
        show={show}
        {...{ title: title, content: content, onHide: handleClose }}
      />
      <Text textAlign="center" mb="1rem" color="#152154" fontSize="1.5rem">
        {title}
      </Text>
      <motion.div
        onClick={handleShow}
        style={{ cursor: "pointer" }}
        whileHover="hoverfour"
        variants={LogoAnimateVariants}
      >
        <Text textAlign="center" mb="1rem">
          {subtitle}
        </Text>
      </motion.div>
    </Flex>
  )
}

const SettingsPage = (props: Props) => {
  const passwordContent = (props?: any) => (
    <>
      <Text>
        Want to change your password?
        <br />
        Thats easy! Just enter your new password here.
      </Text>
      <FormControl id="password">
        <FormLabel>Current Password</FormLabel>
        <Input type="password" />
        <FormLabel>New Password</FormLabel>
        <Input type="password" />
        <FormLabel>Confirm Password</FormLabel>
        <Input type="password" />
        <Button
          mt={4}
          colorScheme="teal"
          isLoading={props.isSubmitting}
          type="submit"
        >
          Submit
        </Button>
      </FormControl>
    </>
  )

  return (
    <Flex m="4rem" flexDir="column">
      <Flex
        className="heading-container"
        justifyContent="center"
        alignItems="center"
        flexDir="column"
        mb="1rem"
      >
        <Heading textAlign="center" mb="1rem">
          Settings
        </Heading>
        <Divider width="50%" />
      </Flex>

      <Flex
        className="home-cards"
        justifyContent="center"
        alignItems="center"
        flexDir="column"
      >
        {Option(
          "Password",
          "Change your password",
          <>
            <Text mb="2.5rem">
              Want to change your password?
              <br />
              Thats easy! Just enter your new password here.
            </Text>
            <FormControl id="password" display="flex" alignItems="center">
              <Box>
                <FormLabel>Current Password</FormLabel>
                <Input type="password" />
                <FormLabel>New Password</FormLabel>
                <Input type="password" />
                <FormLabel>Confirm Password</FormLabel>
                <Input type="password" />
              </Box>
              <Button ml="2rem" mt={4} colorScheme="teal" type="submit">
                Submit
              </Button>
            </FormControl>
          </>
        )}
        <Divider width="50%" />
        {Option(
          "Email Address",
          "Change the email address linked to your account",
          <>
            <Text mb="0.5rem">Changing your email?</Text>
            <Text mb="2.5rem">Enter your new email below.</Text>
            <FormControl id="email">
              <FormLabel>New Email</FormLabel>
              <Input type="email" />
              <Button mt={4} colorScheme="teal" type="submit">
                Submit
              </Button>
            </FormControl>
          </>
        )}
        <Divider width="50%" />
        {Option(
          "Email Notifications",
          "Customize what information and updates you recieve",
          <>
            <Text mb="0.5rem">Want notifications?</Text>
            <Text mb="2.5rem">Toggle your options below.</Text>
            {/* Doesn't actually have state right now */}
            <FormControl display="flex" alignItems="left" flexDir="column">
              <FormLabel htmlFor="email-alerts" mb="0">
                Enable alerts?
              </FormLabel>
              <Switch id="email-alerts" />
              <FormLabel htmlFor="email-promtions" mb="0">
                Enable promotions?
              </FormLabel>
              <Switch id="email-alerts" />
              <FormLabel htmlFor="email-transcend" mb="0">
                Transcend your humanity to be part of AI?
              </FormLabel>
              <Switch id="email-alerts" />
            </FormControl>
          </>
        )}
        <Divider width="50%" />
        {Option(
          "Dark Mode",
          "Change to Light or Dark Mode depending on your preferences"
        )}
      </Flex>
    </Flex>
  )
}

export default SettingsPage
