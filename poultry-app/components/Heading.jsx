import React from 'react';
import { Text } from 'react-native';

import {
    responsiveScreenFontSize
  } from "react-native-responsive-dimensions";

function Heading1({ children, className }) {
  return (
    <Text
      className={`text-[#795548] leading-[32px] ${className}`}
      style={{ 
        fontFamily: 'Montserrat_700Bold',
        fontSize : responsiveScreenFontSize(3)
     }}
    >
      {children}
    </Text>
  );
}

function Heading2({ children, className }) {
  return (
    <Text
      className={`text-[#795548] leading-[32px] ${className}`}
      style={{ 
        fontFamily: 'Montserrat_700Bold',
        fontSize : responsiveScreenFontSize(2.8)
     }}
    >
      {children}
    </Text>
  );
}

export { Heading1, Heading2 }