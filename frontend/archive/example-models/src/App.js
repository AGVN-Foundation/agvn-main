import React, { useEffect } from 'react'
import { Box, Grid, Flex, Modal, ModalOverlay, ModalContent, ModalCloseButton, ModalFooter } from '@chakra-ui/react'
import axios from "axios"
import { ChatDotsFill } from 'react-bootstrap-icons'

const chatbotUrl = 'http://localhost:1337/message/'

function App() {
  useEffect(() => {

    // axios.get()
  })

  return (
    <>
      <header></header>
      <Flex className="main">


      </Flex>
      <>
        <Button onClick={onOpen}>Trigger modal</Button>

        <Modal onClose={onClose} isOpen={isOpen} isCentered>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Modal Title</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Lorem count={2} />
            </ModalBody>
            <ModalFooter>
              <Button onClick={onClose}>Close</Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
      <Box className="chatbot-container" pos="fixed" bottom="4rem" right="4rem">
        <ChatDotsFill size={35} />
      </Box>
      <footer></footer>
    </>
  )
}

export default App
