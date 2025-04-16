import { ScrollView, View, Text } from 'react-native';
import { Heading1 } from '../../components/Heading';
import { Title } from '../../components/Title';
import { Subtitle2 } from '../../components/Subtitle';
import DashCard from '../../components/DashCard';
import { useEffect, useState } from 'react';
import { Image } from 'expo-image';
import Animated, { withRepeat, withSpring, useAnimatedStyle, useSharedValue, ReduceMotion } from 'react-native-reanimated';
import {
  responsiveWidth,
} from "react-native-responsive-dimensions";

export default function App() {
  let [lastUpdated, setLastUpdated] = useState('');

  let [temp, setTemp] = useState(0);
  let [humid, setHumid] = useState(0);
  let [predict_temp, setPredict_temp] = useState(0);
  let [predict_humid, setPredict_humid] = useState(0);

  const chick_translateX = useSharedValue(0);
  const egg_translateY = useSharedValue(0);

  useEffect(() => {
    fetchSensorData();       // Fetch real-time data
    fetchPredictData();      // Fetch predicted data

    const intervalId = setInterval(() => {
      fetchSensorData();
      fetchPredictData();
    }, 5000);

    chick_translateX.value = withRepeat(
      withSpring(10, {
        mass: 1,
        damping: 10,
        stiffness: 100,
        overshootClamping: false,
        restDisplacementThreshold: 0.01,
        restSpeedThreshold: 2,
        reduceMotion: ReduceMotion.System,
      }),
      -1,
      true
    );

    egg_translateY.value = withRepeat(
      withSpring(25, {
        mass: 1,
        damping: 10,
        stiffness: 100,
        overshootClamping: false,
        restDisplacementThreshold: 0.01,
        restSpeedThreshold: 2,
        reduceMotion: ReduceMotion.System,
      }),
      -1,
      true
    );
  }, []);

  const chick_animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ translateX: chick_translateX.value }],
    };
  });

  const egg_animatedStyle = useAnimatedStyle(()=>{
    return {
      transform: [{ translateY: egg_translateY.value }],
    };
  })

  async function fetchSensorData() {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/sensor`);
      const data = await response.json();
      if (data.status === 'success') {
        const sensorData = data.data;
        setTemp(sensorData.temperature || 0);
        setHumid(sensorData.humidity || 0);
        setLastUpdated(new Date().toLocaleString());
      } else {
        console.log('Failed to fetch data');
      }
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  }

  async function fetchPredictData() {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/predict?seconds_ahead=10`);
      const data = await response.json();
      if (data.status === 'success') {
        const prediction = data.data;
        setPredict_temp(prediction.temperature || 0);
        setPredict_humid(prediction.humidity || 0);
      } else {
        console.log('Failed to fetch prediction data');
      }
    } catch (error) {
      console.error('Error fetching prediction data: ', error);
    }
  }  

  return (
    <ScrollView className='py-8 px-4 bg-[#FFF3F0]'>
      <View className='pb-[64px]'>
        <Heading1>
          Thermochick
        </Heading1>
        <View
          style={{
            flexDirection:'row'
          }}
          className="pt-[32px]"
        >
          <Title>
            Halo, Pengguna!
          </Title>
          <Animated.View style={chick_animatedStyle}>
            <Image
              source={require('../../assets/pixel-emoji/em_outline_6.png')}
              style={
              {
                width:35,
                height:35,
              }}
            />
          </Animated.View>
        </View>
        <Subtitle2 className="pt-[32px]"> 
          Yuk cek kondisi kandang anak ayam kamu!!
        </Subtitle2>
        {/* Primary Dashboard */}
        <View className='mt-[40px] bg-[#FEF7A8]'
        style={{
          width : responsiveWidth(94),
          height: responsiveWidth(94),
          flexDirection: 'column',
          borderTopLeftRadius: 90,
          borderTopRightRadius: 90,
          borderBottomLeftRadius: 90,
          borderBottomRightRadius: 90,
        }}>
        {/* Real Data */}
          <View
            className='m-[8px]'
            style={{
              flexDirection : 'row',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <DashCard number={1}
            className="bg-[#795548] flex justify-center items-center">
              <Subtitle2 className="text-[#FBE9E7]">
                Suhu Terkini
              </Subtitle2>
              <Title className="text-white">{temp} °C</Title>
              <Animated.Image
                source={require('../../assets/pixel-emoji/egg_1.png')}
                style={[
                  egg_animatedStyle,
                  {
                    width:52,
                    height:52,
                    position: 'absolute',
                    top: 80,
                    right: -1, 
                    transform: [{ rotate: '10deg' }],
                  }
                ]}
              />
            </DashCard>

            <DashCard number={2}
            className="bg-[#795548] flex justify-center items-center">
              <Subtitle2 className="text-[#FBE9E7]">
                Kelembapan
              </Subtitle2>
              <Title className="text-white">{humid}%</Title>
            </DashCard>
          </View>
        {/* Predict Data  */}
        <View
            className='m-[8px]'
            style={{
              flexDirection : 'row',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <DashCard number={3}
            className="bg-[#FF9800] flex justify-center items-center">
              <Subtitle2 className="text-[#FBE9E7]">
                Prediksi Suhu
              </Subtitle2>
              <Title className="text-white">{predict_temp} °C</Title>
            </DashCard>

            <DashCard number={4}
            className="bg-[#FF9800] flex justify-center items-center">
              <Subtitle2 className="text-[#FBE9E7]">
                Prediksi Kelembapan
              </Subtitle2>
              <Title className="text-white">{predict_humid}%</Title>
            </DashCard>
          </View>
        </View>
        <Subtitle2 className="pt-[32px] text-center">Terkahir diperbarui : {lastUpdated}</Subtitle2>
        <Heading1 className="pt-[32px]">
            Perbandingan
        </Heading1>
      </View>
    </ScrollView>
  );
}