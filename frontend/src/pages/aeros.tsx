import React, { useState } from "react"
import {
  Box,
  Button,
  Flex,
  Heading,
  Divider,
  Text,
  Input,
  Spinner,
  useDisclosure,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  Modal,
} from "@chakra-ui/react"
import axios from "axios"
import Cookies from "universal-cookie"
import { motion } from "framer-motion"
import { CheckCircleFill, X } from "react-bootstrap-icons"
import GenericModal from "../components/GenericModal"
import GCoinChart from "../components/GCoinChart"

interface GCoinCardProps {
  address: string
  value: number
}

const GCoinCard = (props: GCoinCardProps) => {
  return (
    <motion.div
      whileHover={{ scale: 1.05, boxShadow: "0 0 50px #D2CEAF" }}
      style={{ borderRadius: "25px" }}
    >
      <Flex
        justifyContent="space-between"
        minW="20rem"
        boxShadow="2xl"
        cursor="pointer"
        borderRadius="25px"
      >
        <Box backgroundColor="#D2CEAF" mr="20rem" borderRadius="25px" p="2rem">
          <Text fontWeight="semibold">Address</Text>
          {/* cut off address at 20 */}
          <Text>{props.address.substr(0, 20)}...</Text>
        </Box>
        <Box>
          <Text fontSize="2xl" fontWeight="semibold" p="2rem">
            {props.value}
          </Text>
        </Box>
      </Flex>
    </motion.div>
  )
}

function AerosPage() {
  const cookies = new Cookies()
  const [auth, setAuth] = React.useState(false)

  const [totalGCoin, setTotalGCoin] = React.useState(0)

  const { isOpen, onOpen, onClose } = useDisclosure()

  const [gcoinAddressInfo, setGCoinAddressInfo] = useState<
    Array<GCoinCardProps>
  >([{ address: "21fsafas", value: 25 }])

  const noLoginContainer = (
    <Flex
      className="contribution-container"
      justifyContent="center"
      alignItems="center"
      flexDir="column"
      mb="5rem"
    >
      <Heading textAlign="center" mb="1rem" mt="10" size="2xl">
        Login to access Aeros!
      </Heading>
      <Text className="Note" fontSize="10pt">
        With Aeros you can register your wallet, access your accounts, and send
        GCoin to other addresses.
      </Text>
    </Flex>
  )

  React.useEffect(() => {
    setAuth(cookies.get("token") ? true : false)
    // set total gcoin to the sum of gcoin addresses
    gcoinAddressInfo.forEach((g) => {
      setTotalGCoin(g.value + totalGCoin)
    })
    handleGetStatistics()
  }, [gcoinAddressInfo])

  const handleAddAddress = () => {
    // add an address, create a random value
    let addr = "asfasv"
    setGCoinAddressInfo([...gcoinAddressInfo, { address: addr, value: 0 }])
  }

  const handlePay = () => {
    // first, check if the user has enough money in their wallet
    if (totalGCoin < payValue || payValue <= 0) {
      setPayStatus(3)
    } else {
      setPayStatus(1)
      const transactionPayURL = "http://localhost:4200/send/"
      // pay the address
      let data = {
        from_addr: "",
        to_addr: recipientAddr,
        amount: payValue,
        fee: 1,
      }
      setRecipientAddr("")
      setPayValue(0)

      // subtract from each address until you get the right amount
      let total = payValue
      gcoinAddressInfo.forEach((g) => {
        if (total != 0) {
          let can_pay = Math.min(g.value, payValue)
          total -= can_pay
          g.value -= can_pay
        }
      })

      axios
        .post(transactionPayURL, data)
        .then((res) => {
          if (res.data.is_success) {
            setTotalGCoin(totalGCoin - payValue)
            // reset inputs
            setPayStatus(2)
          } else {
            setPayStatus(3)
          }
        })
        .catch((err) => console.log(err))
    }
  }

  // NEED To fetch from /account/address to check the balance of an address
  // Aeros stores the amount for each address
  //

  const [recipientAddr, setRecipientAddr] = useState("")
  const [payValue, setPayValue] = useState(0)
  // 0 -> nothing, 1 -> loading, 2 -> success, 3 -> fail
  const [payStatus, setPayStatus] = useState(0)

  const statusIcon =
    payStatus == 1 ? (
      <Spinner />
    ) : payStatus == 2 ? (
      <Flex>
        <CheckCircleFill size={35} color="green" />
        <Text ml="1rem">Paid.</Text>
      </Flex>
    ) : payStatus == 0 ? null : (
      <Flex>
        <X size={35} color="red" />
        <Text ml="1rem">Sorry, you don't have enough funds.</Text>
      </Flex>
    )

  const paySomeone = (
    <Modal
      onClose={onClose}
      isOpen={isOpen}
      isCentered
      size="xl"
      scrollBehavior="inside"
    >
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Pay Someone</ModalHeader>
        <ModalBody p="2rem">
          <Flex flexDir="column">
            <Input
              placeholder="Recipient Address"
              onChange={(event: any) => {
                setRecipientAddr(event.target.value)
              }}
              mb="1rem"
            />
            <Input
              placeholder="Value"
              onChange={(event: any) => {
                setPayValue(event.target.value)
              }}
              mb="1rem"
            />
            <Button onClick={handlePay}>Pay</Button>
            {
              // on success, render green tick
              statusIcon
            }
          </Flex>
        </ModalBody>
      </ModalContent>
    </Modal>
  )

  const [statistics, setStatistics] = useState([])
  const [days, setDays] = useState([
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29,
  ])

  const handleGetStatistics = () => {
    const statisticsUrl = "http://localhost:4200/statistics/"
    axios
      .get(statisticsUrl)
      .then((res) => {
        setStatistics(res.data.values)
      })
      .catch((err) => console.log(err))
  }

  const statisticsContent = (
    <Flex>
      {/* Chart */}
      <GCoinChart data={statistics} width={500} />
    </Flex>
  )

  const loginContainer = (
    <Flex
      className="contribution-container"
      justifyContent="center"
      alignItems="center"
      flexDir="column"
      mb="5rem"
      minW="30rem"
    >
      {paySomeone}
      <Flex
        flexDir="column"
        className="gcoin-widget"
        alignItems="center"
        justifyContent="center"
        mb="2.5rem"
      >
        <Text textAlign="center" mb="0.5rem" color="#676565">
          GCoin<sup>TM</sup>
        </Text>
        <Divider width="100%" mb="0.2rem" />
        <Flex justifyContent="space-between">
          <Button colorScheme="blackAlpha" mr="2rem" onClick={handleAddAddress}>
            Add Address
          </Button>
          <Box mr="2rem">
            {/* Need to define content */}
            <GenericModal
              title="GCoin Value"
              buttonText="Statistics"
              content={statisticsContent}
            />
          </Box>
          <Button colorScheme="blackAlpha" onClick={onOpen}>
            Pay Someone
          </Button>
        </Flex>
      </Flex>
      <Heading textAlign="center" mb="1rem">
        Your GCOIN Wallet
      </Heading>
      <Flex justifyContent="space-between" minW="35rem">
        <Flex>
          <Text mr="1rem">View</Text>
          <Text>History</Text>
        </Flex>
        <Flex>
          <Text>Total: {totalGCoin}</Text>
        </Flex>
      </Flex>
      <Divider width="100%" mb="2rem" />
      <Flex flexDir="column" p="2rem">
        {gcoinAddressInfo.map((g) => (
          <>
            <GCoinCard address={g.address} value={g.value} key={g.address} />
            <Box mb="2rem" />
          </>
        ))}
      </Flex>
    </Flex>
  )

  return (
    <Flex
      flexDir="column"
      p="4rem"
      justifyContent="center"
      alignItems="center"
      minH="600px"
    >
      {auth ? loginContainer : noLoginContainer}
    </Flex>
  )
}

export default AerosPage
