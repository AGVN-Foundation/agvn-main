// @ts-nocheck

import React from 'react'
import { Doughnut } from 'react-chartjs-2'
import { Text, Box, Flex, Spinner } from '@chakra-ui/react'
import axios from 'axios'

import Banner from '../components/Banner'

interface ResultsType {
    initiative: string
    n_votes: number
}

// return type -> [{n_votes_initiatives: [8]}]
const resultsUrl = 'http://localhost:8000/api/v1/election-results'

const ResultsPage = () => {
    const [isLoading, setIsLoading] = React.useState(true)
    const [data, setData] = React.useState<ResultsType[]>([])
    const [errors, setError] = React.useState<any>(null)

    const initiativeIndices = [
        "Convervative",
        "Progressive",
        "Libertarian",
        "Activist",
        "Left Libertarian",
        "Social Democratic",
        "Statist",
        "Authoritarian"
    ]

    React.useEffect(() => {
        ;(async function() {
            const response = await axios.get(resultsUrl)
            let _data = response.data[0].n_votes_initiatives
            let i = 0
            _data = _data.map(d => (
                {initiative: initiativeIndices[i++], n_votes: d}
            ))

            setData(_data as ResultsType[])
            setIsLoading(false)
        })()
    }, [])

    const { labels, votes } = data.reduce(
        (acc, cur) => {
            return {
                labels: [...acc.labels, cur.initiative],
                votes: [...acc.votes, cur.n_votes],
            }
        },
        {
            labels: [] as string[],
            votes: [] as number[],
        }
    )

    if (isLoading)
        return (
            <Flex h="50vh" justify="center" alignItems="center">
                <Spinner size="lg" />
            </Flex>
        )
    else if (errors) return errors

    return (
        <>
            <Banner
                title="Results"
                subtitle="The results from the previous stage"
                quote="If the only thing a man does is to sleep and eat, he's not better than an animal"
                author="Shakespeare"
            />
            <Flex
                flexDir="column"
                alignItems="center"
                p="0 25%"
                mt="75px"
                mb="60px"
            >
                <Text
                    mx="10%"
                    fontSize="36px"
                    fontWeight="bold"
                    lineHeight="auto"
                >
                    Election Results
                </Text>
                <Box mt="24px" mb="112px" h="2px" w="100%" bg="#404040" />
                <Flex
                    flexDir="column"
                    alignItems="center"
                    border="1px solid"
                    w="100%"
                >
                    <Text fontSize="20px" fontWeight="bold" my="50px">
                        Voting Stage 15th March 2021 - 22nd March 2021
                    </Text>
                    <Box h="500px" w="100%" maxW="500px">
                        <Doughnut
                            data={{
                                labels: labels,
                                datasets: [
                                    {
                                        label: 'My First Dataset',
                                        data: votes,
                                        backgroundColor: [
                                            'rgb(255, 99, 132)',
                                            'rgb(54, 162, 235)',
                                            'rgb(255, 205, 86)',
                                            '#4287f5',
                                            '#b28af2',
                                            '#c2a23a',
                                            '#9e371b',
                                            '#291d1a'
                                        ],
                                        hoverOffset: 4,
                                    },
                                ],
                            }}
                        />
                    </Box>
                    <Text fontSize="28px" fontWeight="bold" mt="50px" mb="64px">
                        The breakdown
                    </Text>
                </Flex>
            </Flex>
        </>
    )
}

export default ResultsPage
