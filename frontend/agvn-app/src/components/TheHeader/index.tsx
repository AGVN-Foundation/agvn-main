// @ts-nocheck
import React, { useState } from "react";
import { Box, Flex, Text, Image, Heading, Divider } from "@chakra-ui/react";
import { useRouter } from 'next/router';
import Cookies from 'universal-cookie';
import { NavDropdown, Container, Button, Nav, Navbar } from "react-bootstrap";
import { Gear, Person, Sun, Bell } from "react-bootstrap-icons";
import { motion } from 'framer-motion';
import LogoAnimateVariants from '../2DAnimations'

async function randomQuote() {
  const response = await fetch('https://api.quotable.io/random')
  const data = await response.json()
  console.log(`${data.content} —${data.author}`)
  return data
}

export interface BannerProps {
  title: string,
  subtitle?: string,
  quote?: string,
  author?: string,
  imgUrl?: string,
  display?: boolean,
}

const MotionHeading = (component: any) => (
  <motion.div>
    {component}
  </motion.div>
)

export function Banner({ title, subtitle, quote, author, imgUrl, display = true }: BannerProps) {
  const checkSubtitle = () => subtitle ? <Divider maxW="10rem" /> : <></>

  const checkQuoteValid = () => {
    if (!(quote && author)) {
      randomQuote().then((d) => {
        quote = d.content
        author = d.author
      })
    }
  }

  React.useEffect(() => {

  })

  return (
    <Flex className="banner" backgroundColor="#282A2B" color="#D3D3D3" p="5rem">
      <Flex className="title-pane" flexDir="column" w="50%" alignItems="center">
        <motion.div whileHover={{ color: "#782020", transition: { spring: Infinity } }}>
          <Heading>{title}</Heading>
        </motion.div>
        {checkSubtitle()}
        <motion.p whileHover={{ skew: 5, textShadow: "0 0 10px", transition: { yoyo: Infinity } }}>
          {subtitle}
        </motion.p>
      </Flex>
      <Flex className="quote-pane" flexDir="column" w="50%">
        <motion.p whileHover={{ skew: 2.5, textShadow: "0 0 10px", transition: { spring: Infinity } }}>
          <Heading fontSize="12pt">{quote}</Heading>
        </motion.p>
        <Text ml="2rem">{author ? "-" + author : null}</Text>
      </Flex>
    </Flex>
  )
}

export default function TheHeader() {
  const router = useRouter();
  const [auth, setAuth] = React.useState(false);
  const cookies = new Cookies();
  const logo = require("../../public/assets/AGVN_white_transparent.png");
  const aeros = require("../../public/assets/aeros_logo.svg");
  const [navColor, setNavColor] = React.useState('dark')
  const [isDarkMode, setIsDarkMode] = React.useState(() => false);

  function toHome(e: any) {
    e.preventDefault();
    router.push('/');
  }

  function toInitiative(e: any) {
    e.preventDefault();
    router.push('/initiatives');
  }

  function toVote(e: any) {
    e.preventDefault();
    router.push('/vote');
  }

  function toContribute(e: any) {
    e.preventDefault();
    router.push('/contribute');
  }

  function toResults(e: any) {
    e.preventDefault();
    router.push('/results');
  }

  function toSignin(e: any) {
    e.preventDefault();
    router.push('/signin');
  }

  function toSignup(e: any) {
    e.preventDefault();
    router.push('/signup');
  }

  function toProfile(e: any) {
    e.preventDefault();
    router.push('/profile');
  }

  function toAbout(e: any) {
    e.preventDefault();
    router.push('/about');
  }

  function toDepartments(e: any) {
    e.preventDefault();
    router.push('/departments');
  }

  function toSetting(e: any) {
    e.preventDefault();
    router.push('/settings')
  }

  function logout(e: any) {
    e.preventDefault();
    cookies.remove('token');
    router.push('/');
  }
  function toPoll(e: any) {
    e.preventDefault();
    router.push('/poll')
  }

  function toPolicy(e: any) {
    e.preventDefault();
    router.push('/policies')
  }

  function toActions(e: any) {
    e.preventDefault();
    router.push('/actions')
  }

  function toNotifications(e: any) {
    e.preventDefault();
    router.push('/notifications')
  }

  function toAeros(e: any) {
    e.preventDefault();
    router.push('/aeros')
  }

  function toBudget(e: any){
    e.preventDefault();
    router.push('/budget')
  }

  React.useEffect(() => {
    if (cookies.get('token') !== undefined) {
      setAuth(true);
    } else {
      setAuth(false);
    }

  });

  const [collapse, setCollapse] = React.useState()

  return (
    <header>
      <Navbar bg={navColor} variant={navColor} expand='lg' className="flex-column space-evenly">
        <Container style={{ paddingBottom: 0 }}>
          <Navbar.Brand style={{ paddingBottom: 0 }} onClick={toHome}>
            <motion.img
              src={logo}
              width='137.48'
              height='280'
              className="d-inline-block align-top"
              alt="AGVN Logo"
              style={{ cursor: 'pointer', borderRadius: "25px" }}
            />
          </Navbar.Brand>
          <Nav
            style={{ fontSize: 12, paddingBottom: 0 }}
          >
            <Nav.Link onClick={toAbout}>About</Nav.Link>
            <Nav.Link onClick={toActions}>Actions</Nav.Link>
            <Nav.Link onClick={toPolicy}>Policies</Nav.Link>
          </Nav>
        </Container>
        <Container>
          <Nav>
            <motion.div whileHover={{ skew: 20, transition: { yoyo: Infinity } }}>
              <Nav.Link onClick={toHome} style={{ fontSize: 12 }}>Auto Governing System | Australia</Nav.Link>
            </motion.div>
          </Nav>
          <Nav className="ml-auto">
            <Nav.Link><motion.img src={aeros} width='80' height='40' variants={LogoAnimateVariants}
              whileHover="hover" onClick={toAeros} />
            </Nav.Link>
            {/* TODO: make this a dropdown with a button that goes to /notifications */}
            {auth && <Nav.Link onClick={toNotifications}>
              <Bell size={25} />
            </Nav.Link>}
          </Nav>
        </Container>
        <Container>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id='responsive-navbar-nav'>
            <Nav justify style={{ width: '80%' }}>
              <Nav.Link className="navhover" onClick={toVote} style={{ backgroundColor: "#333333" }}>Vote</Nav.Link>
              <Nav.Link className="navhover" onClick={toPoll} style={{ backgroundColor: "#333333" }}>Poll</Nav.Link>
              <Nav.Link className="navhover" onClick={toContribute} style={{ backgroundColor: "#333333" }}>Contribute</Nav.Link>
              <NavDropdown title="Others" id="collaible-nav-dropdown" className="navhover" style={{ backgroundColor: "#333333" }}>
                <NavDropdown.Item onClick={toDepartments}>Departments</NavDropdown.Item>
                <NavDropdown.Item onClick={toInitiative}>Initiatives</NavDropdown.Item>
                <NavDropdown.Item onClick={toResults}>Results</NavDropdown.Item>
                <NavDropdown.Item onClick={toBudget}>Budget</NavDropdown.Item>
              </NavDropdown>
            </Nav>
            <Nav className="ms-auto">
              {!auth && (
                <Nav.Link onClick={toSignin}>Login</Nav.Link>
              )}
              {auth && (
                <Nav.Link onClick={toProfile}><Person size={25} /></Nav.Link>
              )}
              {auth && <Nav.Link onClick={toSetting}>
                <motion.div whileHover="hoverthree" variants={LogoAnimateVariants}>
                  <Gear size={25} />
                </motion.div>
              </Nav.Link>}
              <Nav.Link onClick={() => { setNavColor(navColor == 'dark' ? 'light' : 'dark') }}>
                <motion.div whileHover="hoverfive" variants={LogoAnimateVariants} style={{ borderRadius: "25px" }}>
                  <Sun size={25} />
                </motion.div>
              </Nav.Link>
              {auth && (
                <Nav.Link onClick={logout}>Logout</Nav.Link>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}