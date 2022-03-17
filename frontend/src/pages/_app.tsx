import type { AppProps } from 'next/app'
import { ChakraProvider, extendTheme } from '@chakra-ui/react'
import React from 'react'
import { motion } from 'framer-motion'

import Layout from '../components/TheLayout'

import '../styles/globals.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbreact/dist/css/mdb.css'
import { SSRProvider } from 'react-bootstrap'

const colors = {
    text: '#999999',
    darkestBlue: '#254F90',
    darkBlue: '#4569A0',
}

const theme = extendTheme({ colors })

// Note: specify key={router.route} in motion.div to fade away as you go to different routes

function MyApp({ Component, pageProps }: AppProps) {

    return (
        <SSRProvider>
            <motion.div initial="pageInitial" animate="pageAnimate" variants={{
                pageInitial: {
                    opacity: 0
                },
                pageAnimate: {
                    opacity: 1
                }
            }}>
                <ChakraProvider theme={theme}>
                    <Layout>
                        <Component {...pageProps} />
                    </Layout>
                </ChakraProvider>
            </motion.div>
        </SSRProvider>
    )
}
export default MyApp
