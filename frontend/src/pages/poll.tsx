// @ts-nocheck

import React, { useState } from "react"
import {
  Flex,
  Box,
  Button,
  Grid,
  Heading,
  Radio,
  RadioGroup,
  Text,
  Textarea,
} from "@chakra-ui/react"
import axios from "axios"
import { Banner } from "../components/TheHeader"
import Cookies from "universal-cookie"
import Select from "react-select"
import { MDBCol, MDBContainer, MDBRow } from "mdbreact"
import Slider from "@material-ui/core/Slider"
import Popups from "../components/Popup"
import { CodeSlash } from "react-bootstrap-icons"

const DividerLine = () => <Box w="100%" h="1px" bg="gray" my="24px" />

const pollUrl = "http://localhost:8000/api/v1/polls/"
const host = "http://localhost:8000/api/v1"
const PolicyTypes = [
  "taxation",
  "lifestyle",
  "community",
  "infrastructure",
  "foreign relations",
  "health",
  "education",
  "national security",
  "safety",
  "industry",
  "science",
  "environment",
  "energy",
  "assets",
  "economy",
  "foreign trade",
  "natural resources",
]

interface PollsProps {
  type: number
  pollQuestion: string
  pollAnswers: string
  question_id: number
}

const PollPage = () => {
  const [pollAvailable, setAvailable] = useState(false)
  const [polls, setPolls] = useState<
    {
      id: number
      question: string
      ongoing: boolean
      type: number
      end_date: string
      possible_answers: string
      subject: number
    }[]
  >([])
  const [isRetrived, setIsRetrived] = useState(false)
  const [authorised, setAuthorised] = useState(false)
  const [successMsg, setSuccessMsg] = useState("")
  const [errorMsg, setErrorMsg] = useState("")
  const [devMode, setDevMode] = useState(false)
  const cookies = new Cookies()

  async function sendPoll(id: number) {
    setErrorMsg("")
    setSuccessMsg("")
    var e = document.getElementById(String(id)) as HTMLInputElement
    console.log(e.value)
    const data = {
      answer: e.value,
      poll_id: id,
    }
    const config = {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: cookies.get("token"),
      },
    }
    axios
      .post(`${host}/polls/submit`, data, config)
      .then(function (response) {
        if (response.status === 200) {
          setSuccessMsg("You have succesfully submitted the poll.")
        }
      })
      .catch(function (error) {
        if (error.response.status === 400) {
          setErrorMsg(
            "You have already voted, please contact admin if you want to revote."
          )
        }
      })
  }

  const generatePoll = () => {
    const url = "http://localhost:8200/poll/generate"
    axios
      .get(url, { params: { policy_type: PolicyTypes[radioValue] } })
      .then((res) => {
        let _data = res.data
        console.log(_data)
        setPolls([...polls, _data])
      })
      .catch((err) => console.log(err))
  }

  const [radioValue, setRadioValue] = useState(0)

  const loginProp = (
    <Flex as="form" flexDirection="column">
      <Heading mt="10" mb="10" size="2xl" textAlign="center">
        {pollAvailable ? "Polls Available!" : "No polls available"}
      </Heading>
      {
        // map poll questions
        polls.map((p, index) => (
          //Poll(p.type, 1, p.question, p.possible_answers, p.id)
          <MDBContainer>
            <MDBRow center between>
              <MDBCol size="4">
                <Text>
                  <b>Question {index + 1}</b>: {p.question}
                </Text>
              </MDBCol>
              <MDBCol md="5">
                <Poll
                  type={p.type}
                  pollQuestion={p.question}
                  pollAnswers={p.possible_answers}
                  question_id={p.id}
                />
              </MDBCol>
              <MDBCol size="auto">
                <Button
                  bg="darkestBlue"
                  color="white"
                  onClick={() => sendPoll(p.id)}
                >
                  Submit
                </Button>
              </MDBCol>
            </MDBRow>
            <br />
          </MDBContainer>
        ))
      }
      <Box mt="10rem" />
      <CodeSlash
        size={35}
        onClick={() => {
          setDevMode(!devMode)
        }}
        cursor="pointer"
      />
      {devMode && (
        <>
          <RadioGroup mt="2rem" onChange={setRadioValue}>
            <Flex flexDir="row" p="2rem" flexWrap="wrap">
              {Object.keys(PolicyTypes).map((key) => (
                <Radio key={key} value={key} m="1rem">
                  {PolicyTypes[key]}
                </Radio>
              ))}
            </Flex>
          </RadioGroup>
          <Button onClick={generatePoll}>Submit</Button>
        </>
      )}
    </Flex>
  )
  const logoutProp = (
    <Flex as="form" flexDirection="column">
      <Heading mt="10" mb="10" size="2xl" textAlign="center">
        Login to do polls!
      </Heading>
    </Flex>
  )

  const effectFn = async () => {
    let response = await axios.get(`${pollUrl}`)
    if (response.data.length > 0) {
      setAvailable(true)
    }

    // extract all polls -> JSON array
    let retrievedPolls = response.data

    // set polls
    setPolls(retrievedPolls)
    setIsRetrived(true)
  }

  React.useEffect(() => {
    if (cookies.get("token") !== undefined) {
      effectFn()
      setAuthorised(true)
    }
    if (isRetrived) {
      console.log(polls)
    }
    setErrorMsg("")
    setSuccessMsg("")
  }, [])

  function Poll({ type, pollQuestion, pollAnswers, question_id }: PollsProps) {
    // comma separated values
    const shortAnswer = () => {
      return <Textarea label={pollQuestion} id={String(question_id)} />
    }

    const scaleQuestion = () => {
      const [value, setValue] = useState(1)
      const [min, setMin] = useState(0)
      const [max, setMax] = useState(1)
      const [answerArr, setAnswerArr] = useState(pollAnswers.split(","))
      const marks = [
        {
          value: Number(answerArr[0]),
          label: "Not at all Likely",
        },
        {
          value: Number(answerArr[1]),
          label: "Extremely Likely",
        },
      ]
      const handleChange = (event: any, newValue: any) => {
        setValue(newValue)
      }

      function valuetext(value: any) {
        return `${value}`
      }

      React.useEffect(() => {
        setAnswerArr(pollAnswers.split(","))
        setValue(Number(answerArr[0]))
        setMin(Number(answerArr[0]))
        setMax(Number(answerArr[1]))
        console.log()
      }, [])

      return (
        <>
          <Slider
            value={value}
            getAriaValueText={valuetext}
            aria-labelledby="discrete-slider-custom"
            step={1}
            min={min}
            max={max}
            valueLabelDisplay="auto"
            marks={marks}
            onChange={handleChange}
          />
          <input value={value} id={String(question_id)} hidden={true} />
        </>
      )
    }

    function multiChoice() {
      const [options, setOptions] = React.useState([{}])
      const [values, setValues] = React.useState([{}])
      const [value, setValue] = React.useState("")

      React.useEffect(() => {
        getAnswer()
      }, [])

      function recordValues(e: any) {
        setValues(e)
        setValue(e.value)
      }

      function getAnswer() {
        var newOptions = []
        var newOption = {}
        const answerArr = pollAnswers.split(",")
        for (let ans of answerArr) {
          newOption = { value: ans, label: ans }
          newOptions.push(newOption)
        }
        setOptions(newOptions)
      }

      return (
        <>
          <Select options={options} values={values} onChange={recordValues} />
          <input hidden={true} id={String(question_id)} value={value} />
        </>
      )
    }

    const checkBox = () => {
      const [options, setOptions] = useState([{}])
      const [values, setValues] = useState([{}])
      const [endValues, setEndValues] = useState<string[]>([])

      React.useEffect(() => {
        getAnswer()
      }, [])

      function getAnswer() {
        var newOptions = []
        var newOption = {}
        const answerArr = pollAnswers.split(",")
        for (let ans of answerArr) {
          newOption = { value: ans, label: ans }
          newOptions.push(newOption)
        }
        setOptions(newOptions)
      }

      function recordValues(e: any) {
        setValues(e)
        var newValues = []
        for (var v of values) {
          newValues.push(v.value)
        }
        setEndValues(newValues)
      }

      return (
        <>
          <Select
            closeMenuOnSelect={false}
            isMulti
            options={options}
            values={values}
            onChange={recordValues}
          />
          <input hidden={true} id={String(question_id)} value={endValues} />
        </>
      )
    }
    return (
      <>
        {type === 1 && multiChoice()}
        {type === 2 && scaleQuestion()}
        {type === 3 && shortAnswer()}
        {type === 4 && checkBox()}
        {type === 5 && multiChoice()}
      </>
    )
  }

  return (
    <>
      {Banner({
        title: "Poll",
        subtitle: "Boost your contribution by completing polls",
        quote:
          "We are of different opinions at different hours, but we always may be said to be at heart on the side of truth",
        author: "Ralph Emerson",
      })}
      <Flex
        m="5rem"
        flexDir="column"
        alignItems="center"
        justifyContent="center"
      >
        {authorised ? loginProp : logoutProp}
      </Flex>
      <Popups type="error" message={errorMsg} />
      <Popups type="success" message={successMsg} />
    </>
  )
}

export default PollPage
