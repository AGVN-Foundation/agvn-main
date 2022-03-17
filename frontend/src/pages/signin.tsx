import React from "react"
import Head from "next/head"
import { Button, Text, Box, Flex } from "@chakra-ui/react"
import Link from "next/link"
import Cookies from "universal-cookie"
import { useRouter } from "next/router"
import Popups from "../components/Popup"
import PageTitle from "../components/PageTitle"
import { MDBInput } from "mdbreact"
import { Banner } from "../components/TheHeader"

const host = "http://127.0.0.1:8000/api/v1"

function SigninPage() {
  const [email, setEmail] = React.useState("")
  const [password, setPassword] = React.useState("")
  const [errorMsg, setErrorMsg] = React.useState("")
  const cookies = new Cookies()
  const router = useRouter()

  async function login(e: any) {
    e.preventDefault()
    try {
      const req = {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      }
      const response = await fetch(`${host}/login`, req)
      if (response.status === 400) {
        setEmail("")
        setPassword("")
        setErrorMsg("Wrong password or email")
      } else {
        const data = await response.json()
        setErrorMsg("")
        cookies.set("token", data.token, { path: "/" })
        router.push("/")
      }
    } catch (error) {
      setErrorMsg("Please try again.")
      setPassword("")
    }
  }

  React.useEffect(() => {
    if (cookies.get("token") !== undefined) {
      router.push("/")
    }
  })

  function recordEmail(e: any) {
    e.preventDefault()
    setEmail(e.target.value)
    setErrorMsg("")
  }

  function recordPassword(e: any) {
    e.preventDefault()
    setPassword(e.target.value)
    setErrorMsg("")
  }

  return (
    <>
      {Banner({ title: "Login", subtitle: "Login to A-GVN System" })}
      <Flex
        flexDir="column"
        m="5rem"
        alignItems="center"
        justifyContent="center"
      >
        <Head>
          <title>A-GVN System - Signin</title>
        </Head>
        <Flex my={75} h="2rem">
          <PageTitle title="Sign in" />
        </Flex>
        <Box as="form" onSubmit={login} h="100%" pl="2.5rem">
          <MDBInput
            label="E-mail address"
            outline
            icon="envelope"
            onChange={recordEmail}
            required
            style={{ width: "60%" }}
          />
          <MDBInput
            label="Password"
            outline
            type="password"
            icon="lock"
            onChange={recordPassword}
            required
            style={{ width: "60%" }}
            mb="4rem"
          />
          <Button textTransform="uppercase" type="submit" ml="4rem" mb="2rem">
            Sign in{" "}
          </Button>
          <Text>
            Don't have an account?{" "}
            <Text as="span" fontWeight="bold">
              <Link href="/signup">Create one.</Link>
            </Text>
          </Text>
        </Box>
        <Popups type="error" message={errorMsg} />
      </Flex>
    </>
  )
}

export default SigninPage
