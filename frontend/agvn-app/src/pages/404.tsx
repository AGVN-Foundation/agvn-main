import CubeCanvas from "../components/CubeMesh"
import { Flex, Box, Heading } from "@chakra-ui/layout"

const headerStyle = {
    position: 'absolute',
}

export default function Custom404() {
    return (
        <Flex alignItems='center' justifyContent='center' height='100vh'>
            <Box position="absolute"><Heading>404 - Page Not Found</Heading></Box>
            <CubeCanvas />
        </Flex>
    )
}