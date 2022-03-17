// @ts-nocheck

import React from "react"
import { Doughnut, Bar } from "react-chartjs-2"
import { Text, Box, Flex, Spinner } from "@chakra-ui/react"
import axios from "axios"

import Banner from "../components/Banner"

interface BudgetType {
  policy_type: string
  policy_cost: number
}

const electedInitiativeURL = "http://localhost:8000/api/v1/elected-initiative/"
const policyURL = "http://localhost:8000/api/v1/policy"

const PolicyTypeMapping = [
  "Taxation",
  "Lifestyle and Culture",
  "Community",
  "Infrastructure and Transport",
  "Foreign Relations",
  "Health",
  "Education and Employment",
  "National Security",
  "Safety",
  "Industry",
  "Science and Technology",
  "Environment",
  "Energy",
  "Assets",
  "Economy",
  "Foreign Trade",
  "Natural Resources",
]

const BudgetPage = () => {
  const [isLoading, setIsLoading] = React.useState(true)
  const [error, setError] = React.useState<any>(null)
  const [data, setData] = React.useState<BudgetType[]>([])
  const [electedInitiative, setElectedInitiative] = React.useState(0)

  React.useEffect(() => {
    ;(async function () {
      // first get the elected initiative
      axios
        .get(electedInitiativeURL)
        .then((res) => {
          let eInit = res.data[0].elected_initiative
          console.log(eInit)
          setElectedInitiative(eInit)
          // call axios on policy
          return eInit
        })
        .then((e) =>
          axios.get(policyURL).then((res) => {
            let _data = res.data
            console.log(_data, e)
            // filter the policies by initiative
            _data = _data.filter((policy) => policy.initiative == e)
            console.log("after filtering", _data)
            _data = _data.map((d) => ({
              policy_type: PolicyTypeMapping[d.policy_type],
              policy_cost: d.policy_cost,
            }))
            console.log("after mapping", _data)
            setData(_data)
            console.log(data)
          })
        )
      setIsLoading(false)
    })()
  }, [])
  if (isLoading)
    return (
      <Flex w="100%" h="50vh" justify="center" alignItems="center">
        <Spinner size="lg" />
      </Flex>
    )
  else if (error) return error

  const labels = data.map(({ policy_type }) => policy_type)
  const amounts = data.map(({ policy_cost }) => policy_cost)

  return (
    <>
      <Banner
        title="Budget"
        subtitle="Learn about this year's federal budget"
        quote="Money, if it does not bring you happiness, will at least help you be miserable in comfort"
        author="Helen Brown"
      />
      <Flex flexDir="column" alignItems="center" p="0 25%" mt="75px" mb="60px">
        <Text mx="10%" fontSize="36px" fontWeight="bold" lineHeight="auto">
          Budget Views
        </Text>
        <Box mt="24px" mb="112px" h="2px" w="100%" bg="#404040" />
        <Flex flexDir="column" alignItems="center" border="1px solid" w="100%">
          <Box h="500px" w="100%" maxW="500px">
            <Doughnut
              data={{
                labels,
                datasets: [
                  {
                    label: "My First Dataset",
                    data: amounts,
                    backgroundColor: [
                      "rgb(255, 99, 132)",
                      "rgb(54, 162, 235)",
                      "rgb(255, 205, 86)",
                    ],
                    hoverOffset: 4,
                  },
                ],
              }}
            />
          </Box>
          <Text fontSize="28px" mt="50px" mb="64px">
            2021 Budget Proportions
          </Text>
        </Flex>
        <Flex
          flexDir="column"
          justify="center"
          alignItems="center"
          border="1px solid"
          w="100%"
          mt="106px"
          p="50px"
        >
          <Bar
            data={{
              labels,
              datasets: [
                {
                  data: amounts,
                  backgroundColor: [],
                  borderColor: [],
                  borderWidth: 1,
                },
              ],
            }}
            options={{
              indexAxis: "y",
              elements: {
                bar: {
                  borderWidth: 2,
                },
              },
              responsive: true,
              plugins: {
                legend: {
                  position: "right",
                },
              },
            }}
          />
          <Text fontSize="28px" mt="64px">
            2021 Revenue Expenses
          </Text>
        </Flex>
      </Flex>
    </>
  )
}

export default BudgetPage
