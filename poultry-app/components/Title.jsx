import React from 'react';
import { Text } from 'react-native';

import {
  responsiveScreenFontSize
} from 'react-native-responsive-dimensions';

function Title({ children, className }) {
  return (
    <Text
      className={`text-[#3E2723] leading-[40px] ${className}`}
      style={{
        fontFamily: 'Montserrat_700Bold',
        fontSize: responsiveScreenFontSize(4),
      }}
    >
      {children}
    </Text>
  );
}

export { Title };
