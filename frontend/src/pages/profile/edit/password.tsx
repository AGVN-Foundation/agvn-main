import React from "react"
import Head from "next/head"
import { Box, Button, Flex } from "@chakra-ui/react"
import PageTitle from "../../../components/PageTitle"
import Cookies from "universal-cookie"
import { useRouter } from "next/router"
import { MDBCol, MDBInput, MDBRow } from "mdbreact"
import Popups from "../../../components/Popup"

const host = "http://127.0.0.1:8000/api/v1"

export default function Password() {
  const [oPass, setOPass] = React.useState("")
  const [password, setPassword] = React.useState("")
  const [confirmPass, setConfirmPass] = React.useState("")
  const [errorMsg, setErrorMsg] = React.useState("")
  const [successMsg, setSuccessMsg] = React.useState("")
  const cookies = new Cookies()
  const router = useRouter()

  function recordOPass(e: any) {
    e.preventDefault()
    setOPass(e.target.value)
    setErrorMsg("")
  }

  function recordPassword(e: any) {
    e.preventDefault()
    setPassword(e.target.value)
    setErrorMsg("")
  }

  function recordConfirmPass(e: any) {
    e.preventDefault()
    setConfirmPass(e.target.value)
    setErrorMsg("")
  }

  function toEdit(e: any) {
    e.preventDefault()
    router.push("/profile/edit")
  }

  function setDefault() {
    setPassword("")
    setConfirmPass("")
    setOPass("")
  }

  async function changePass(e: any) {
    e.preventDefault()
    if (password !== confirmPass) {
      setErrorMsg("Passwords does not match")
      setDefault()
    }

    if (password === oPass) {
      setErrorMsg(
        "Please enter a password that is different to the original password."
      )
    }

    try {
      const req = {
        method: "PUT",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: cookies.get("token"),
        },
        body: JSON.stringify({
          o_password: oPass,
          n_password: password,
        }),
      }
      const response = await fetch(`${host}/change/password`, req)
      if (response.status === 401) {
        setErrorMsg("Invalid Token, please try again.")
        setDefault()
      } else if (response.status === 400) {
        setErrorMsg("Please enter the correct current password")
        setDefault()
      } else if (response.status === 200) {
        setSuccessMsg("Your password has been updated.")
      } else {
        setErrorMsg("An error has occurred, please try again.")
        setDefault()
      }
    } catch (error) {
      setErrorMsg("Please try again.")
      setDefault()
    }
  }

  React.useEffect(() => {
    if (cookies.get("token") === undefined) {
      router.push("/")
    }
  })

  return (
    <Flex flexDir="column" justifyContent="center" alignItems="center">
      <Head>
        <title>Change Password</title>
      </Head>
      <Flex my={75} h="2rem">
        <PageTitle title="Edit Profile" subtitle="Change Password" />
      </Flex>
      <Box as="form" h="100%">
        <MDBRow>
          <MDBInput
            label="Enter your old password"
            outline
            size="lg"
            type="password"
            icon="lock"
            value={oPass}
            onChange={recordOPass}
            required
            style={{ width: "80%" }}
          />
        </MDBRow>
        <MDBRow>
          <MDBInput
            label="Enter your new password"
            outline
            size="lg"
            type="password"
            icon="lock"
            value={password}
            onChange={recordPassword}
            required
            style={{ width: "80%" }}
          />
        </MDBRow>
        <MDBRow>
          <MDBInput
            label="Confirm your new password"
            outline
            size="lg"
            type="password"
            icon="lock"
            value={confirmPass}
            onChange={recordConfirmPass}
            required
            style={{ width: "80%" }}
          />
        </MDBRow>
        <br />
        <MDBRow center>
          <MDBCol size="auto">
            <Button textTransform="uppercase" onClick={changePass}>
              Confirm
            </Button>
          </MDBCol>
          <MDBCol size="auto">
            <Button textTransform="uppercase" onClick={toEdit}>
              Cancel
            </Button>
          </MDBCol>
        </MDBRow>
      </Box>
      <Popups type="error" message={errorMsg} />
      <Popups type="success" message={successMsg} toEdit={true} />
    </Flex>
  )
}
