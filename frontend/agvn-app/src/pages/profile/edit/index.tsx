import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import PageTitle from '../../../components/PageTitle';
import { Box, Divider, Flex } from '@chakra-ui/react';
import { useRouter } from 'next/router';
import Cookies from 'universal-cookie';
import { MDBContainer, MDBRow } from 'mdbreact';

export default function Edit() {

  return (
    <Flex flexDir="column" justifyContent="center" alignItems="center">
      <Head>
        <title>Update Profile</title>
      </Head>
      <Flex my={75} h='2rem'>
        <PageTitle title='Edit Profile' />
      </Flex>

      <Box
        as="form"
        h="100%"
        width="50%"
      >
        <MDBContainer>
          <Divider /><br />
          <MDBRow>
            <p className="text-center fs-4"><Link href="/profile/edit/password">Change Password</Link></p>
          </MDBRow>
          <br /><Divider /><br />
          <MDBRow>
            <p className="text-center fs-4"><Link href="/profile/edit/interests">Update Interests</Link></p>
          </MDBRow>
          <br /><Divider /><br />
          <MDBRow>
            <p className="text-center fs-4"><Link href="/profile/edit/skills">Update Skills</Link></p>
          </MDBRow>
          <br /><Divider />
        </MDBContainer>
      </Box>

    </Flex>
  );
}