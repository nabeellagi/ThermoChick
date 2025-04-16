import React from 'react';
import { Text } from 'react-native';
import { responsiveScreenFontSize } from 'react-native-responsive-dimensions';

function Subtitle2({ children, className }) {
  return (
    <Text
      className={`text-[#3E2723] leading-[24px] ${className}`}
      style={{
        fontFamily: 'Montserrat_500Medium',
        fontSize: responsiveScreenFontSize(2.2), // ~18px depending on screen
      }}
    >
      {children}
    </Text>
  );
}

export { Subtitle2 };
