// @ts-nocheck

import React from 'react'
import { Flex, Box, Button, Grid, GridItem, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useDisclosure, FormControl, Input, Text } from '@chakra-ui/react'
import Header from '../TheHeader'
import Footer from '../TheFooter'
import axios from "axios";
import { ChatDotsFill } from 'react-bootstrap-icons'
import { motion } from 'framer-motion'
import { useRef } from 'react';

interface TheLayoutProps { }

const TheLayout: React.FC<TheLayoutProps> = ({ children }) => {
    let [message, setMessage] = React.useState<string>('')
    let [chatbotReply, setChatbotReply] = React.useState<string>('')
    React.useEffect(async (): void => {
        try {
            async function chatBotReply(userMessage: string): Promise<string> {
                let response = await axios.get(
                    'http://localhost:1337/message?' + `message=${userMessage}`
                )
                setChatbotReply(() => (chatbotReply = response.data.message))
                return 'done'
            }
            await chatBotReply(message)
        } catch (error) {
            console.log({ chatError: error })
        }

    }, [])

    const chatbotUrl = 'http://localhost:1337/message/'

    const getReply = (input: string, userMessage: MessageHistory, callBack: any) => {
        // get the input value and place into message history
        setInputValue("")
        setMessageHistory([...messageHistory, userMessage])

        axios.get(chatbotUrl, { params: { message: input } })
            .then(res => {
                console.log(res.data.message)
                console.log(messageHistory)
                setMessageHistory([...messageHistory, userMessage, { by: 1, message: res.data.message, id: currId + 2 }])
                currId = currId + 2
                console.log(messageHistory)
            })
            .then(callBack)
            .catch(err => console.log(err))
        console.log(messageHistory)
    }

    interface MessageHistory {
        // 0 -> user, 1 -> AI
        by: number,
        message: string
        id: number,
    }

    const [messageHistory, setMessageHistory] = React.useState<Array<MessageHistory>>([{ by: 1, message: "Welcome to AGVN!", id: 1 }])

    const messageEvent = useRef(null)

    const { isOpen, onOpen, onClose } = useDisclosure()
    const [inputValue, setInputValue] = React.useState("")
    const handleInputChange = (event) => setInputValue(event.target.value)
    var currId = 1

    const handleKeyPressChatbot = (event: any) => {
        if (event.key === 'Enter') {
            console.log("pressed Enter!")
            getReply(inputValue, { by: 0, message: inputValue, id: currId + 1 })
        }
    }

    // @ts-ignore
    return (
        <>
            <Modal onClose={onClose} isOpen={isOpen} isCentered>
                <ModalOverlay />
                <ModalContent style={{ height: "50rem" }}>
                    <ModalHeader>Chat with AGVN Bot</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody style={{ overflowY: 'scroll' }}>
                        <Flex flexDir="column" w="100%" ref={messageEvent}>
                            {
                                messageHistory.map((m) => (
                                    <Flex marginLeft={m.by === 0 ? "auto" : ""} key={m.id} backgroundColor={m.by === 0 ? "#4287f5" : "#e6e6e6"} color={m.by === 0 ? "#f0f0f0" : "#3d3c3c"} fontWeight="semibold" borderRadius="25px" w="50%" mb="1rem">
                                        <motion.div whileHover={{ scale: 1.1 }}>
                                            <Flex m="1rem">
                                                <Text pl="1.5rem">
                                                    {(m.by === 1 ? "Bot: " : "You: ")}
                                                </Text>
                                                <Text ml=".5rem">
                                                    {m.message}
                                                </Text>
                                            </Flex>
                                        </motion.div>
                                    </Flex>
                                ))
                            }
                        </Flex>
                    </ModalBody>
                    <ModalFooter>
                        {/* Form to send messages */}
                        <FormControl id="input">
                            <Input value={inputValue} onChange={handleInputChange} variant="filled" placeholder="Send a message" onKeyPress={handleKeyPressChatbot} />
                            <Button
                                mt={4}
                                colorScheme="teal"
                                type="submit"
                                onClick={() => {
                                    getReply(inputValue, { by: 0, message: inputValue, id: currId + 1 })
                                }}
                            >
                                Send
                            </Button>
                        </FormControl>
                    </ModalFooter>
                </ModalContent>
            </Modal>
            <Box className="chatbot-container" pos="fixed" bottom="4rem" right="4rem" style={{ cursor: "pointer" }} zIndex="3">
                <motion.div whileHover={{ scale: 1.1 }}>
                    <ChatDotsFill onClick={onOpen} size={35} />
                </motion.div>
            </Box>

            <Header />
            <Box>
                {children}
            </Box>
            <Footer />
        </>
    )
}

export default TheLayout
