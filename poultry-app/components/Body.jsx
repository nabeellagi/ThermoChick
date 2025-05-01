import React from 'react';
import { Text } from 'react-native';
import { responsiveScreenFontSize } from 'react-native-responsive-dimensions';

function BodyBold({ children, className }) {
  return (
    <Text
      className={`text-[#3E2723] leading-[24px] ${className}`}
      style={{
        fontFamily: 'Montserrat_600SemiBold',
        fontSize: responsiveScreenFontSize(2),
      }}
    >
      {children}
    </Text>
  );
}

export { BodyBold };
