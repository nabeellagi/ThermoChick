import React from 'react';
import { Text } from 'react-native';
import { responsiveScreenFontSize } from 'react-native-responsive-dimensions';

function Small({ children, className }) {
  return (
    <Text
      className={`text-[#3E2723] leading-[16px] ${className}`}
      style={{
        fontFamily: 'Montserrat_500Medium',
        fontSize: responsiveScreenFontSize(1.4), // ~18px depending on screen
      }}
    >
      {children}
    </Text>
  );
}

export { Small };
