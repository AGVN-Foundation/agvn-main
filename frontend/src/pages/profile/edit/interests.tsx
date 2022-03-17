import React from "react"
import Head from "next/head"
import { Box, Flex, Button } from "@chakra-ui/react"
import PageTitle from "../../../components/PageTitle"
import Cookies from "universal-cookie"
import Select from "react-select"
import { MDBCol, MDBRow } from "mdbreact"
import { useRouter } from "next/router"
import Popups from "../../../components/Popup"

const host = "http://127.0.0.1:8000/api/v1"

export default function Interests() {
  const [options, setOptions] = React.useState([{}])
  const [hasInterest, setHasInterest] = React.useState(false)
  const [defaultValues, setDefaultValues] = React.useState([{}])
  const [values, setValues] = React.useState([{}])
  const [errorMsg, setErrorMsg] = React.useState("")
  const [successMsg, setSuccessMsg] = React.useState("")
  const cookies = new Cookies()
  const router = useRouter()

  async function getOptions() {
    try {
      const req = {
        method: "GET",
        headers: {
          "Content-type": "application/json",
        },
      }
      const response = await fetch(`${host}/interests/`, req)
      if (response.status === 200) {
        const data = await response.json()
        createOptions(data)
      } else {
        setErrorMsg("An error has occured, please try again.")
      }
    } catch (error) {
      setErrorMsg("An error has occured, please try again.")
    }
  }

  function setDefault() {
    setValues(defaultValues)
  }

  async function getInterests() {
    try {
      const req = {
        method: "GET",
        headers: {
          "Content-type": "application/json",
          Authorization: cookies.get("token"),
        },
      }
      const response = await fetch(`${host}/user/interests`, req)
      if (response.status === 200) {
        const data = await response.json()
        setDefaultValues(data.interests)
        setValues(data.interests)
        if (data.interests.length > 0) {
          setHasInterest(true)
        }
      } else {
        setErrorMsg("An error has occured, please try again.")
      }
    } catch (error) {
      setErrorMsg("An error has occured, please try again.")
    }
  }

  function createOptions(
    choices: [{ type: number; description: string; type_name: string }]
  ) {
    var newOptions = []
    var newOption = {}
    for (var choice of choices) {
      newOption = { value: choice.type, label: choice.type_name }
      newOptions.push(newOption)
    }
    setOptions(newOptions)
  }

  function recordValues(e: any) {
    setValues(e)
    setErrorMsg("")
  }

  async function updateInterests() {
    try {
      const req = {
        method: "PUT",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: cookies.get("token"),
        },
        body: JSON.stringify({
          interests: values,
        }),
      }
      const response = await fetch(`${host}/user/interests/update`, req)
      if (response.status === 200) {
        setSuccessMsg("Your interests has been updated.")
      } else {
        setErrorMsg("An error has occured, please try again.")
        setDefault()
      }
    } catch (error) {
      setErrorMsg("An error has occured, please try again.")
    }
  }

  function toEdit(e: any) {
    e.preventDefault()
    router.push("/profile/edit")
  }

  React.useEffect(() => {
    if (cookies.get("token") !== undefined) {
      getOptions()
      getInterests()
    } else {
      setErrorMsg("Invalid token, please try again")
    }
  }, [])

  return (
    <Flex
      flexDir="column"
      justifyContent="center"
      alignItems="center"
      minH="600px"
    >
      <Head>
        <title>Update Interests</title>
      </Head>
      <Flex my={75} h="2rem" mb="10rem">
        <PageTitle title="Edit Profile" subtitle="Update Interests" />
      </Flex>
      <Box as="form" h="100%" w="30%">
        <MDBRow>
          {hasInterest && (
            <Select
              closeMenuOnSelect={false}
              isMulti
              options={options}
              defaultValue={values}
              values={values}
              onChange={recordValues}
            />
          )}
          {!hasInterest && (
            <Select
              closeMenuOnSelect={false}
              isMulti
              options={options}
              values={values}
              onChange={recordValues}
            />
          )}
        </MDBRow>
        <br />
        <MDBRow center>
          <MDBCol size="auto">
            <Button textTransform="uppercase" onClick={updateInterests}>
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
