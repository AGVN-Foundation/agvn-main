import React, { Component } from "react";
import { Box, Text } from "@chakra-ui/react";

interface PageTitleProps {
  title: string;
  subtitle?: string;
}

const PageTitle = ({ title, subtitle }: PageTitleProps) => {
  return (
    <Box color='text' gridColumn='3/end'>
      <Text align="center" as='h3' fontSize='36px' color='black'>
        {title}
      </Text>
      <Text align="center" fontSize='28px' mt='1rem'>
        {subtitle}
      </Text>
    </Box>
  );
};

export default PageTitle;
