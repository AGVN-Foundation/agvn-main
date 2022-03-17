// @ts-nocheck
import assignActions, { ActionProp } from "../components/Actions"
import flood from "../public/assets/Images/victoria_flooding_jumbo_img.png"
import cyclone from "../public/assets/Action_images/cyclone.jpg"
import bushfire from "../public/assets/Action_images/bushfire.jpg"
import drought from "../public/assets/Action_images/drought.jpg"
import war from "../public/assets/Action_images/war.png"
import citizen_hostage from "../public/assets/Action_images/hostage.jpg"
import terrorism from "../public/assets/Action_images/terrorism.png"
import pandemic from "../public/assets/Action_images/pandemic.jpg"
import nuclear_meltdown from "../public/assets/Action_images/nuclear_meltdown.jpg"
import mass_revolt from "../public/assets/Action_images/mass_revolt.jpg"
import corporate_abuse from "../public/assets/Action_images/corporate_abuse.png"

import React from "react"
import { Banner } from "../components/TheHeader"
import { Box, Button, Flex, Input } from "@chakra-ui/react"
import axios from "axios"
import { Radio, RadioGroup } from "@chakra-ui/react"
import { CodeSlash } from "react-bootstrap-icons"

/**
 * Image types reqiured
 *  flooding
 *  cyclone
 *  earthquake
 *  diplomatic emergency
 *  war
 *  terrorist activity
 *  pandemic
 *  nuclear meltdown
 *  riots
 */

const ACTION_MAP = {
  flood: flood,
  cyclone: cyclone,
  bushfire: bushfire,
  drought: drought,
  war: war,
  citizen_hostage: citizen_hostage,
  terrorism: terrorism,
  pandemic: pandemic,
  nuclear_meltdown: nuclear_meltdown,
  mass_revolt: mass_revolt,
  corporate_abuse: corporate_abuse,
}

const SAMPLE_ACTIONS: Array<ActionProp> = [
  {
    heading: `Responding to the recent flooding in Victoria`,
    content: `Flooding is natural and cannot be stopped and can have both positive and negative impacts.

    The positive impacts of flooding, for example, include water for wetland ecosystems and replenishing soil moisture and nutrients.

    The negative impacts can bring substantial damages to homes and businesses, critical infrastructure and to farming, such as agriculture and crops. However, the negative effects of floods can be reduced with good planning and the right actions.

    Flood planning and action is a shared community responsibility. Local, state and federal governments all have a role to play in reducing the damage from floods in Victoria but so do you and your neighbours.`,
    imgUrl: flood,
    current: true,
  },
]

const actionsUrl = "http://localhost:8200/action/"

function ActionPage() {
  const [actions, setActions] = React.useState<Array<ActionProp>>([
    {
      heading: `Responding to the recent flooding in Victoria`,
      content: `Flooding is natural and cannot be stopped and can have both positive and negative impacts.

    The positive impacts of flooding, for example, include water for wetland ecosystems and replenishing soil moisture and nutrients.

    The negative impacts can bring substantial damages to homes and businesses, critical infrastructure and to farming, such as agriculture and crops. However, the negative effects of floods can be reduced with good planning and the right actions.

    Flood planning and action is a shared community responsibility. Local, state and federal governments all have a role to play in reducing the damage from floods in Victoria but so do you and your neighbours.`,
      imgUrl: flood,
      current: true,
    },
  ])
  const [prompt, setPrompt] = React.useState<string>("")
  const [value, setValue] = React.useState(cyclone)

  const [devMode, setDevMode] = React.useState(false)

  const getAction = (prompt: string, callback: any) => {
    axios
      .get(actionsUrl, { params: { action: prompt } })
      .then((res) =>
        setActions([
          ...actions,
          {
            heading: prompt,
            content: res.data["text"],
            imgUrl: ACTION_MAP[value],
          },
        ])
      )
      .then(callback())
      .catch((err) => console.log(err))
  }

  const handleChange = (event: any) => {
    setPrompt(event.target.value)
  }

  const handleClick = () => {
    getAction(prompt, () => {
      setPrompt("")
      console.log(value)
    })
  }

  return (
    <>
      {Banner({
        title: "Actions",
        subtitle: "AGVN is prepared to take action",
        quote: "The most effective way to do it, is to do it.",
        author: "Amelia Earhart",
      })}
      <Box>{assignActions(actions)}</Box>
      <Flex className="ctl-panel" p="5rem" flexDir="column">
        <CodeSlash
          size={35}
          onClick={() => {
            setDevMode(!devMode)
          }}
          cursor="pointer"
        />
        {devMode && (
          <>
            <Input value={prompt} onChange={handleChange} />
            <RadioGroup onChange={setValue} value={value}>
              <Flex flexDir="row" p="2rem" flexWrap="wrap">
                {Object.keys(ACTION_MAP).map((key, val) => (
                  <Radio key={key} value={key} m="1rem">
                    {key}
                  </Radio>
                ))}
              </Flex>
            </RadioGroup>
            <Button onClick={handleClick}>Submit</Button>
          </>
        )}
      </Flex>
    </>
  )
}

export default ActionPage
