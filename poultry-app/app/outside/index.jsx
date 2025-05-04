import { ScrollView, View, ActivityIndicator } from 'react-native';
import { Heading1 } from '../../components/Heading';
import { Title } from '../../components/Title';
import { Subtitle2 } from '../../components/Subtitle';
import { useEffect, useState } from 'react';
import {
  responsiveHeight,
  responsiveWidth,
} from "react-native-responsive-dimensions";
import { BodyBold } from '../../components/Body';
import { Small } from '../../components/Small';
import Animated, { FlipInEasyX, FlipOutEasyX } from 'react-native-reanimated';
import { Image } from 'expo-image';

export default function Outside() {
  const [loading, setLoading] = useState(true);
  const [sensorData, setSensorData] = useState(null);
  
  useEffect(() => {
    const fetchSensorData = async () => {
      try {
        const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/weather?device_id=${process.env.EXPO_PUBLIC_DEVICE_ID}`);
        const data = await response.json();
        setSensorData(data);
        // console.log(data)
      } catch (error) {
        console.error("Failed to fetch sensor data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSensorData();
  }, []);

  if (loading) {
    return (
      <View className='flex-1 items-center justify-center bg-[#FFF3F0]'>
        <Image
          source={require('../../assets/oc/farma_load.png')}
          style={{
            width:200,
            height:200
          }}
        />
        <Subtitle2 className='mt-4 text-[#E64A19]'>Ditunggu yaa...</Subtitle2>
      </View>
    );
  }

  return (
    <ScrollView className='py-8 bg-[#FFF3F0]'>
      <View className='pt-[32px] mx-12'>
        <Heading1>
          Thermochick
        </Heading1>
        <Title className='mt-8'>
          Cek Kondisi Di Sekitar Kandang
        </Title>
      </View>
      <View className='flex flex-row bg-[#E64A19] w-screen h-[20vh] mt-8 justify-center px-12 items-center'>
        <Heading1 className='text-white'>
          {sensorData.name},
          {'\n'} 
          {sensorData.region}
        </Heading1>
        <Image
          source={require('../../assets/oc/search.png')}
          style={{
            width:140,
            height:150
          }}
        />
      </View>
      <View className='flex flex-col mx-12 pt-8 gap-12'>
        <Animated.View className="rounded-[15px] border border-black flex-row items-center justify-between px-8"
            style={{
                width : responsiveWidth(80),
                height : responsiveHeight(20)
            }}
            entering={FlipInEasyX} exiting={FlipOutEasyX}
        >
            <View className="flex-1">
                <BodyBold>
                    Selisih Suhu
                </BodyBold>
                <Small>
                    {sensorData.difference.interpret}
                </Small>
            </View>
            <Heading1>{sensorData.difference.amount}°C</Heading1>
        </Animated.View> 
        <Animated.View className="rounded-[15px] border border-black flex-row items-center justify-between px-8"
            style={{
                width : responsiveWidth(80),
                height : responsiveHeight(20)
            }}
            entering={FlipInEasyX} exiting={FlipOutEasyX}
        >
            <View className="flex-1">
                <BodyBold>
                    Tekanan Luar
                </BodyBold>
                <Small>
                    {sensorData.pressure.interpret}
                </Small>
            </View>
            <Heading1>{sensorData.pressure.mb}Mb</Heading1>
        </Animated.View> 
        <Animated.View className="rounded-[15px] border border-black flex-row items-center justify-between px-8"
            style={{
                width : responsiveWidth(80),
                height : responsiveHeight(20)
            }}
            entering={FlipInEasyX} exiting={FlipOutEasyX}
        >
            <View className="flex-1">
                <BodyBold>
                    GB Defra Index
                </BodyBold>
                <Small>
                {sensorData.gbdefra.interpret.level}
                {'\n'}
                {sensorData.gbdefra.interpret.pesan}
                </Small>
            </View>
            <Heading1>{sensorData.gbdefra.index}</Heading1>
        </Animated.View> 
      </View>
      <ScrollView className='flex mx-8 pt-8 mb-32'
      horizontal
      showsHorizontalScrollIndicator={false}>
        <View className='flex flex-row gap-6'>
          <Animated.View className="rounded-[15px] border border-black flex-col items-center justify-center"
              style={{
                  width : responsiveWidth(40),
                  height : responsiveHeight(20)
              }}
              entering={FlipInEasyX} exiting={FlipOutEasyX}
          >
                  
              <BodyBold>
                  Suhu Luar
              </BodyBold>
              <Heading1>{sensorData.outside_temp}°C</Heading1>
          </Animated.View> 
          <Animated.View className="rounded-[15px] border border-black flex-col items-center justify-center"
              style={{
                  width : responsiveWidth(40),
                  height : responsiveHeight(20)
              }}
              entering={FlipInEasyX} exiting={FlipOutEasyX}
          >
                  
              <BodyBold>
                  Terasa Seperti
              </BodyBold>
              <Heading1>{sensorData.outside_feelslike}°C</Heading1>
          </Animated.View> 
          <Animated.View className="rounded-[15px] border border-black flex-col items-center justify-center"
              style={{
                  width : responsiveWidth(40),
                  height : responsiveHeight(20)
              }}
              entering={FlipInEasyX} exiting={FlipOutEasyX}
          >
                  
              <BodyBold>
                  Kecepatan Angin
              </BodyBold>
              <Heading1>{sensorData.wind} km/jam</Heading1>
          </Animated.View>
        </View> 
      </ScrollView>
      
    </ScrollView>
  );
}
