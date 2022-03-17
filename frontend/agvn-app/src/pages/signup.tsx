import React from 'react';
import { Button, Text, Box, Flex } from '@chakra-ui/react';
import Link from 'next/link';
import Cookies from 'universal-cookie';
import { useRouter } from 'next/router';
import Popups from '../components/Popup';
import Head from 'next/head'
import PageTitle from '../components/PageTitle';
import { MDBCol, MDBContainer, MDBInput, MDBRow } from 'mdbreact';
import { Form } from 'react-bootstrap';
import { Banner } from '../components/TheHeader';

const host = 'http://127.0.0.1:8000/api/v1';

function SignupPage() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirmPass, setConfirmPass] = React.useState('');
  const [driverLicense, setDriverLicense] = React.useState('');
  const [medicare, setMedicare] = React.useState('');
  const [irn, setIrn] = React.useState('');
  const [term, setTerm] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState('');
  const cookies = new Cookies();
  const router = useRouter();

  async function register(e: any) {
    e.preventDefault()
    if (term === false) {
      setErrorMsg("You need to accept the terms of user and privacy");
      setDefault();

    } else if (password !== confirmPass) {
      setErrorMsg("You have entered different passwords");
      setDefault();
    } else {
      try {
        const req = {
          method: 'POST',
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(
            {
              "email": email,
              "password": password,
              "medicare": medicare,
              "irn": irn,
              "driver_license": driverLicense,
            }
          )
        };

        const response = await fetch(`${host}/register`, req);
        if (response.status === 201) {
          const data = await response.json();
          cookies.set('token', data.token, { path: '/' });
          router.push('/');
        } else {
          const data = await response.json();
          setErrorMsg(data.error);
          console.log(data.error);
          setDefault();
        }

      } catch (error) {
        setErrorMsg('Please Try again.');
        setDefault();
      }
    }
  }


  React.useEffect(() => {
    if (cookies.get('token') !== undefined) {
      router.push('/');
    }
  })

  function setDefault() {
    setEmail('');
    setPassword('');
    setConfirmPass('');
    setDriverLicense('');
    setMedicare('');
    setIrn('');
  }

  function recordEmail(e: any) {
    e.preventDefault();
    setEmail(e.target.value);
    setErrorMsg('');
  }

  function recordPassword(e: any) {
    e.preventDefault();
    setPassword(e.target.value);
    setErrorMsg('');
  }

  function recordConfirmPass(e: any) {
    e.preventDefault();
    setConfirmPass(e.target.value);
    setErrorMsg('');
  }

  function recordDriverLicense(e: any) {
    e.preventDefault();
    setDriverLicense(e.target.value);
    setErrorMsg('');
  }

  function recordMedicare(e: any) {
    e.preventDefault();
    setMedicare(e.target.value);
    setErrorMsg('');
  }

  function recordIrn(e: any) {
    e.preventDefault();
    setIrn(e.target.value);
    setErrorMsg('');
  }

  function recordTerm(e: any) {
    setTerm(e.target.checked);
    setErrorMsg('');
  }

  return (
    <>
      {Banner({ title: "Sign Up", quote: "Sign up today, and be part of something greater", author: "AGVN" })}
      <Head>
        <title>A-GVN System - Signup</title>
      </Head>
      <Flex my={75} h='2rem' alignItems="center" justifyContent="center" >
        <PageTitle title="Create Account" />
      </Flex>
      <Box
        as="form"
        onSubmit={register}
        h="100%"
      >
        <MDBContainer>
          <MDBRow>
            <MDBCol md='6'>
              <MDBInput
                label="E-mail address"
                outline
                icon="envelope"
                value={email}
                onChange={recordEmail}
                required
              />
              <MDBInput
                label="Password"
                outline
                type="password"
                icon="lock"
                value={password}
                onChange={recordPassword}
                required
              />
              <MDBInput
                label="Confirm Password"
                outline
                type="password"
                icon="exclamation-triangle"
                value={confirmPass}
                onChange={recordConfirmPass}
                required
              />


            </MDBCol>
            <MDBCol md='6'>
              <MDBInput
                label="Driver License"
                outline
                far
                icon="id-card"
                value={driverLicense}
                onChange={recordDriverLicense}
                required
              />
              <MDBInput
                label="Medicare Number"
                outline
                icon="id-card"
                value={medicare}
                onChange={recordMedicare}
                required
              />
              <MDBInput
                label="IRN"
                outline
                icon="id-card"
                value={irn}
                onChange={recordIrn}
                required
              />
            </MDBCol>
            <MDBRow start>
              <MDBCol size="4"></MDBCol>
              <MDBCol md="6" size="4">
                <Form.Check
                  inline
                  label="I agree with terms of user and privacy"
                  type="checkbox"
                  checked={term}
                  onChange={recordTerm}
                  required
                />
              </MDBCol>
            </MDBRow>
            <MDBRow start>
              <MDBCol size="4"></MDBCol>
              <MDBCol md="3" size="4">
                <Button textTransform="uppercase" type="submit">Sign up </Button>
              </MDBCol>
            </MDBRow>

          </MDBRow>

        </MDBContainer>

        <Box mb="2rem"/>
        <Text textAlign="center">
          Already have an account?{' '}
          <Text as="span" fontWeight="bold">
            <Link href="/signin">Sign in.</Link>
          </Text>
        </Text>
      </Box>
      <Popups type="error" message={errorMsg} />
    </>
  )
}

export default SignupPage
