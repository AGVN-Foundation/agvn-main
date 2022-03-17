// @ts-nocheck

import React from 'react';
import { useRouter } from 'next/router';
import Cookies from 'universal-cookie';
import ContributeChart from '../../components/ContributeChart';
import { Box, Text, Flex, Heading, Divider, Grid } from "@chakra-ui/react";
import PageTitle from "../../components/PageTitle";
import Popups from '../../components/Popup';
import { Container, Row, Col } from 'react-bootstrap';
import { Button } from '@chakra-ui/button';
import { Spacer } from '@chakra-ui/layout';
import { Checkbox } from '@chakra-ui/checkbox';
import { MDBCol, MDBContainer, MDBRow } from 'mdbreact';

const host = 'http://127.0.0.1:8000/api/v1';

const policyTypeValueSample = [
  {
    policyType: 'Taxation',
    favorability: 'High'
  },
  {
    policyType: 'Health',
    favorability: 'Neutral'
  }
]

const PoliticalInterests = (policyTypesValues: any) => {
  return (
    <Container>
      <Row>
        <Col style={{ fontWeight: 'bold' }}>Policy Types</Col>
        <Col style={{ fontWeight: 'bold' }}>Favorableness</Col>
      </Row>
      {policyTypeValueSample.map((p) => (
        <Row>
          <Col>{p.policyType}</Col>
          <Col color={p.favorability == 'High' ? "#82b884" : "#82b5b8"}>{p.favorability}</Col>
        </Row>
      ))}
    </Container>
  )
}

function Profile() {
  const [email, setEmail] = React.useState('');
  const [name, setName] = React.useState('');
  const [sex, setSex] = React.useState('');
  const [age, setAge] = React.useState('');
  const [driverLicense, setDriverLicense] = React.useState('');
  const [medicare, setMedicare] = React.useState('');
  const [irn, setIrn] = React.useState('');
  const [family, setFamily] = React.useState('');
  const [education, setEducation] = React.useState('');
  const [residence, setResidence] = React.useState('');
  const [country, setCountry] = React.useState('');
  const [occupation, setOccupation] = React.useState('');
  const [oRank, setORank] = React.useState('');
  const [income, setIncome] = React.useState('');
  const [isGov, setIsGov] = React.useState(false);
  const [interests, setInterests] = React.useState('')
  const [skills, setSkills] = React.useState('')
  const [contributions, setContributions] = React.useState([])
  const [political, setPolitical] = React.useState('')
  const [errorMsg, setErrorMsg] = React.useState('');
  const [loaded, setLoaded] = React.useState(false);
  const [toSignin, setToSignin] = React.useState(false);
  const [wWidth, setWWidth] = React.useState(0);
  const [contribWidth, setContribWidth] = React.useState(0);
  const cookies = new Cookies();
  const router = useRouter()

  async function getProfile() {
    try {
      const req = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          Authorization: cookies.get('token'),
        }
      };
      const response = await fetch(`${host}/profile`, req);
      if (response.status === 401) {
        setErrorMsg('Invalid Token, please sign in again.');
        setToSignin(true);
      } else if (response.status === 500) {
        setErrorMsg("Please try again later.")
      } else {
        const data = await response.json();
        setEmail(data.email);
        setName(data.name);
        getSex(data.sex);
        setAge(data.age);
        setDriverLicense(data.driver_license);
        setMedicare(data.medicare.card_number);
        setIrn(data.medicare.IRN);
        setFamily(data.family);
        setEducation(data.education);
        setResidence(data.residence);
        setCountry(data.country);
        setOccupation(data.current_occupation);
        setORank(data.occupation_rank);
        setIncome(data.income);
        setIsGov(data.government_employee);
        getInterests(data.interests);
        getSkills(data.skills);
        setContributions(data.contribution);
        setErrorMsg('');
        setToSignin(false);
      }
    } catch (error) {
      setErrorMsg('Please try again.');
      setToSignin(true);
      console.log(errorMsg);
    }
  }

  function getSex(gender: number) {
    if (gender === 1) {
      setSex('Male');
    } else if (gender === 2) {
      setSex('Female');
    } else {
      setSex('Indeterminte/Intersex/Unspecific');
    }
  }

  function getInterests(arr: [string]) {
    var newString = arr.join(", ");
    setInterests(newString);
  }

  function getSkills(arr: [string]) {
    var newString = arr.join(", ");
    setSkills(newString);
  }

  function toEditProfile(e: any) {
    e.preventDefault();
    router.push('/profile/edit');
  }

  function getPolitical(arr: any) {
    var newString = arr.join(", ");
    setPolitical(newString);
  }

  React.useEffect(() => {
    if (cookies.get('token') === undefined) {
      router.push('/signin');
    } else if (loaded === false) {
      getProfile();
      setLoaded(true);
    }
  })

  React.useEffect(() => {
    window.addEventListener('resize', () => setWWidth(window.innerWidth))
    setContribWidth(document.getElementById('contrib-box')?.offsetWidth - 100);
  }, [wWidth])

  function Feature({ title, desc, ...rest }: FeatureProps) {
    return (
      <MDBCol md="6">
        <Box w="100%" shadow="md" borderWidth="1px" p="6" {...rest}>
          <Heading fontSize="xl">{title}</Heading>
          <Divider style={{ color: "#d3d3d3", width: "30%" }} />
          <Text mt={4}>{desc}</Text>
        </Box>
      </MDBCol>
    )
  }

  interface FeatureProps {
    title: string;
    desc: string;
  }

  // return (
  //   <Flex flexDir="column" alignItems="center" justifyContent="center">
  //     <Flex my={75} h='2rem'>
  //       <PageTitle title='Profile' />
  //       <Spacer mr="1rem" />
  //       <Box>
  //         <Button
  //           colorScheme='blackAlpha'
  //           variant='outline'
  //           size='sm'
  //           onClick={toEditProfile}
  //         >
  //           Edit
  //         </Button>
  //       </Box>
  //     </Flex>

  //     <Box minW="60%" gridColumn="7/13" gridRow="3/20">
  //       <MDBContainer>
  //         <MDBRow>
  //           <Feature
  //             title="Email Address"
  //             desc={email}
  //           />
  //           <Feature
  //             title="Legal Name"
  //             desc={name}
  //           />
  //         </MDBRow><br/>
  //         <MDBRow>
  //           <Feature
  //             title="Sex"
  //             desc={sex}
  //           />
  //           <Feature
  //             title="Age"
  //             desc={age}
  //           />
  //         </MDBRow><br/>
  //         <MDBRow>
  //           <Feature
  //             title="Driver License"
  //             desc={driverLicense}
  //           />
  //           <MDBCol md="6">
  //             <Grid templateColumns="repeat(5, 1fr)" gap={6} w="100%" shadow="md" borderWidth="1px" p="6">
  //               <Box h={50}>
  //                 <Heading fontSize="xl">Medicare</Heading>
  //                 <Divider style={{ color: "#d3d3d3", width: "30%" }} />
  //                 <Text mt={4} mb="1rem">{medicare}</Text>
  //               </Box>
  //               <Box/>
  //               <Box >
  //                 <Heading fontSize="xl">IRN</Heading>
  //                 <Divider style={{ color: "#d3d3d3", width: "30%" }} />
  //                 <Text mt={4}>{irn}</Text>
  //               </Box>
  //             </Grid>
  //           </MDBCol>
  //         </MDBRow><br/>
  //         <MDBRow>
  //           <Feature
  //             title="Number of Family Members"
  //             desc={family}
  //           />
  //           <Feature
  //             title="Education Level"
  //             desc={education}
  //           />
  //         </MDBRow><br/>
  //         <MDBRow>
  //           <Feature
  //             title="Home address"
  //             desc={residence}
  //           />
  //           <Feature
  //             title="Current Citizenship"
  //             desc={country}
  //           />
  //         </MDBRow><br/>
  //         <MDBRow>
  //           <MDBCol>
  //             <Flex w="100%" shadow="md" borderWidth="1px" p="2rem" flexDir="column">
  //               <Heading fontSize="xl">Current Occupation:</Heading>
  //               <Divider style={{ color: "#d3d3d3", width: "30%" }} />
  //               <Text mt={4} mb="1rem">Occupation: {occupation}</Text>
  //               <Checkbox colorScheme='green' isChecked={isGov} isReadOnly style={{ cursor: 'auto' }}>Government Employee</Checkbox>
  //             </Flex>
  //          </MDBCol>
  //         </MDBRow><br/>
  //       <MDBRow>
  //         <Feature
  //           title="Current Occupation Rank"
  //           desc={oRank}
  //         />
  //         <Feature
  //           title="Anual Income"
  //           desc={income}
  //         />
  //       </MDBRow><br/>
  //       <MDBRow>
  //         <Feature
  //           title="Interests"
  //           desc={interests}
  //         />
  //         <Feature
  //           title="Skills"
  //           desc={skills}
  //         />
  //       </MDBRow><br/>
  //       <MDBRow>
  //         <MDBCol>
  //           <Flex w="100%" shadow="md" borderWidth="1px" flexDir="column" p="2rem">
  //             <Heading fontSize="xl">Political Interests</Heading>
  //             <Divider style={{ color: "#d3d3d3", width: "30%" }} mb="1rem" />
  //             <PoliticalInterests />
  //           </Flex>
  //         </MDBCol>
  //       </MDBRow><br/>
  //       <MDBRow>
  //         <MDBCol>
  //           <Flex w="100%" shadow="md" borderWidth="1px" flexDir="column" p="2rem" id="contrib-box">
  //             <Heading fontSize="xl">Contribution (past 30 days)</Heading>
  //             <Divider style={{ color: "#d3d3d3", width: "30%" }} />
  //             <br />
  //             <ContributeChart data={contributions} width={contribWidth}/>
  //           </Flex>
  //         </MDBCol>
  //       </MDBRow>
  //       </MDBContainer>
  //     </Box>

  //     <Popups type="error" message={errorMsg} toSignin={toSignin} />
  //   </Flex>
  // );

  return (
    <></>
  )
}

export default Profile;
