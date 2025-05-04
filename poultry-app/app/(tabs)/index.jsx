import { ScrollView, View, Text, Switch, TouchableOpacity } from 'react-native';
import { Heading1 } from '../../components/Heading';
import { Title } from '../../components/Title';
import { Subtitle2 } from '../../components/Subtitle';
import DashCard from '../../components/DashCard';
import { useEffect, useState, useRef } from 'react';
import { Image } from 'expo-image';
import Animated, { withRepeat, withSpring, useAnimatedStyle, useSharedValue, ReduceMotion } from 'react-native-reanimated';
import {
  responsiveHeight,
  responsiveWidth,
} from "react-native-responsive-dimensions";
import { useRouter } from 'expo-router';
import { BodyBold } from '../../components/Body';
import { Small } from '../../components/Small';

export default function App() {
  const router = useRouter();
  let [lastUpdated, setLastUpdated] = useState('');

  let [temp, setTemp] = useState(0);
  let [humid, setHumid] = useState(0);
  let [predict_temp, setPredict_temp] = useState(0);
  let [predict_humid, setPredict_humid] = useState(0);
  let [lampState, setLampState] = useState(false);

  const chick_translateX = useSharedValue(0);
  const egg_translateY = useSharedValue(0);

  const [isRealTime, setIsRealTime] = useState(true);
  const intervalRef = useRef(null); 


  useEffect(() => {
    fetchSensorData();       // Fetch real-time data
    fetchPredictData();      // Fetch predicted data

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

  useEffect(() => {
    if (isRealTime) {
      intervalRef.current = setInterval(() => {
        fetchSensorData();
        fetchPredictData();
        fetchLampState();
      }, 5000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
  
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRealTime]);

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
      const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/sensor?device_id=${process.env.EXPO_PUBLIC_DEVICE_ID}`);
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
      const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/predict?device_id=${process.env.EXPO_PUBLIC_DEVICE_ID}&seconds_ahead=10`);
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

  async function fetchLampState() {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/sensor/lamp?device_id=${process.env.EXPO_PUBLIC_DEVICE_ID}`);
      const data = await response.json();
      if (data.status === 'success') {
        setLampState(data.data.lamp_state);
      } else {
        console.log('Failed to fetch lamp state');
      }
    } catch (error) {
      console.error('Error fetching lamp state: ', error);
    }
  }
  

  return (
    <ScrollView className='py-8 px-8 bg-[#FFF3F0]'>
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
        <View className="flex-row items-center justify-between mt-4">
          <Subtitle2>Real Time Detection</Subtitle2>
          <Switch
            value={isRealTime}
            onValueChange={setIsRealTime}
            thumbColor={isRealTime ? "#FF9800" : "#ccc"}
            trackColor={{ false: "#ccc", true: "#FFCC80" }}
          />
        </View>
        <View className='flex flex-row justify-center items-center w-[50vw] ml-[80px]'>
          <Subtitle2 className="pt-[32px]"> 
            Yuk cek kondisi kandang anak ayam kamu!!
          </Subtitle2>
          <Image
          source={require('../../assets/oc/greet.png')}
          style={{
            width:140,
            height:150
          }}
        />
        </View>
        {/* Primary Dashboard */}
        <View className='mt-[40px] bg-[#FEF7A8]'
        style={{
          width : responsiveWidth(90),
          height: responsiveWidth(90),
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
            <TouchableOpacity onPress={()=>router.navigate('/prediction/temp')}>
              <DashCard number={3}
              className="bg-[#FF9800] flex justify-center items-center">
                <Subtitle2 className="text-[#FBE9E7]">
                  Prediksi Suhu
                </Subtitle2>
                <Title className="text-white">{predict_temp} °C</Title>
              </DashCard>
            </TouchableOpacity>

            <TouchableOpacity onPress={()=>router.navigate('/prediction/humid')}>
              <DashCard number={4}
              className="bg-[#FF9800] flex justify-center items-center">
                <Subtitle2 className="text-[#FBE9E7]">
                  Prediksi Kelembapan
                </Subtitle2>
                <Title className="text-white">{predict_humid}%</Title>
              </DashCard>
            </TouchableOpacity>

          </View>
        </View>
        <View className="flex flex-col items-center justify-center mt-8">
          <Animated.View className="border bg-[#795548] flex-col items-center justify-center"
              style={{
                  width : responsiveWidth(40),
                  height : responsiveHeight(20),
                    borderTopLeftRadius : 10,
                    borderTopRightRadius : 90,
                    borderBottomLeftRadius : 90,
                    borderBottomRightRadius:10
              }}
          >
                  
              <BodyBold className="text-white">
                  Kondisi Lampu
              </BodyBold>
              <Heading1 className="text-white">{lampState ? 'ON' : 'OFF'}</Heading1>
          </Animated.View>
        </View>
        <Subtitle2 className="pt-[32px] text-center">Terkahir diperbarui : {lastUpdated}</Subtitle2>
        <View className='my-8'>
          <Subtitle2 className="pt-[32px] text-center">
              Perbandingan Suhu
          </Subtitle2>
          <View>
            <Title className="text-center">{(((predict_temp - temp)/temp) * 100).toFixed(2)}%</Title>
          </View>
          <Subtitle2 className="pt-[32px] text-center">
              Perbandingan Kelembapan
          </Subtitle2>
          <View>
            <Title className="text-center">{(((predict_humid - humid)/humid) * 100).toFixed(2)}%</Title>
          </View>
        </View>
        <View className="flex flex-col justify-center gap-12">
            <TouchableOpacity onPress={()=>router.navigate('/custom/threshold')}>
              <View className='bg-[#E64A19] flex justify-center items-center p-8'
              style={{
                width : responsiveWidth(80),
                height : responsiveHeight(20),
                borderRadius : 30
              }}>
                <Heading1 className="text-[#FFF3F0]">
                  Ubah threshold suhu?
                </Heading1>
              </View>
            </TouchableOpacity>
            <TouchableOpacity onPress={()=>router.navigate('/outside')}>
              <View className='bg-[#E64A19] flex justify-center items-center p-8'
              style={{
                width : responsiveWidth(80),
                height : responsiveHeight(20),
                borderRadius : 30
              }}>
                <Heading1 className="text-[#FFF3F0]">
                  Lihat Kondisi Sekitar Kandang?
                </Heading1>
              </View>
            </TouchableOpacity>
        </View> 
        <View className='mb-[100px]'/>
      </View>
    </ScrollView>
  );
}