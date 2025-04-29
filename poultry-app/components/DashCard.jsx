import { View } from 'react-native';

import {
    responsiveWidth,
} from "react-native-responsive-dimensions";

import { LinearGradient } from 'expo-linear-gradient';


export default function DashCard({children, className, number}){
    let radius;
    if(number === 1){
        radius = {
            borderTopLeftRadius : 90,
            borderTopRightRadius : 10,
            borderBottomLeftRadius : 10,
            borderBottomRightRadius:10
        }
    }else if(number === 2){
        radius = {
            borderTopLeftRadius : 10,
            borderTopRightRadius : 90,
            borderBottomLeftRadius : 10,
            borderBottomRightRadius:10
        }
    }else if(number === 3){
        radius = {
            borderTopLeftRadius : 10,
            borderTopRightRadius : 10,
            borderBottomLeftRadius : 90,
            borderBottomRightRadius:10
        }
    }else if(number === 4){
        radius = {
            borderTopLeftRadius : 10,
            borderTopRightRadius : 10,
            borderBottomLeftRadius : 10,
            borderBottomRightRadius:90
        }
    }
    
    if(number === 1 || number === 2){
        return(
            <View
                className={className}
                style={{
                    width : responsiveWidth(42),
                    height: responsiveWidth(41),
                    ...radius
                }}
            >
                {children}
            </View>
        )
    }else if(number === 3 || number === 4){
        return(
            <LinearGradient
                className={className}
                colors={['#ff9800', '#e64a19']}
                locations={[0, 0.55, 1]}
                start={{ x: 0, y: 0 }}
                end={{ x: 0.5, y: 2 }}
                style={{
                    width : responsiveWidth(42),
                    height: responsiveWidth(41),
                    ...radius
                }}
            >
                {children}
            </LinearGradient>
        )
    }
}