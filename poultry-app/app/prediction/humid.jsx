import { ScrollView, View, TouchableOpacity, Vibration, Text } from 'react-native';
import { Title } from '../../components/Title';
import { BodyBold } from '../../components/Body';
import { useState } from 'react';
import { Heading2 } from '../../components/Heading';
import Slider from '@react-native-community/slider';
import { responsiveScreenWidth } from 'react-native-responsive-dimensions';
import { Small } from '../../components/Small';
import { Subtitle2 } from '../../components/Subtitle';

const StepMarkersBar = ({ max, step, current }) => {
    const markerCount = Math.floor(max / step) + 1;
    const totalWidth = responsiveScreenWidth(80);
    const markerWidth = 2;
    const totalSpacing = totalWidth - markerCount * markerWidth;
    const spacing = totalSpacing / (markerCount - 1);

    const markers = [];

    for (let i = 0; i <= max; i += step) {
        const selected = i === current;

        markers.push(
            <View
                key={i}
                style={{
                    width: markerWidth,
                    height: 20,
                    backgroundColor: selected ? '#E64A19' : '#FFFFFF90',
                    marginRight: i === max ? 0 : spacing,
                    borderRadius: 1,
                }}
            />
        );
    }

    return (
        <View
            style={{
                flexDirection: 'row',
                justifyContent: 'flex-start',
                alignItems: 'flex-end',
                width: totalWidth,
                alignSelf: 'center',
                marginTop: 10,
                marginBottom: 20,
            }}
        >
            {markers}
        </View>
    );
};

export default function Humidpredict() {
    const [second, setSecond] = useState(1);
    const [humidity, setHumidity] = useState(null); // for storing API result
    const maxSecond = 120;
    const markerStep = 10;
    const sliderStep = 5;

    const fetchPrediction = async () => {
        try {
            const url = `${process.env.EXPO_PUBLIC_API_URL}/predict?device_id=${process.env.EXPO_PUBLIC_DEVICE_ID}&seconds_ahead=${second}`;
            const response = await fetch(url);
            const json = await response.json();

            if (json.status === 'success') {
                setHumidity(json.data.humidity);
                Vibration.vibrate(100);
            } else {
                console.error('Prediction failed:', json);
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    };

    return (
        <ScrollView className='py-[75px] px-[30px] bg-[#080A25]'>
            <Title className="text-center text-white">
                PREDIKSI KELEMBAPAN
            </Title>

            <BodyBold className="text-white text-justify py-[60px]">
                Gerakkan penggeser hingga detik yang diinginkan. Lalu tekan enter 
            </BodyBold>

            <Heading2 className="text-center text-white">
                Dalam {second} detik
            </Heading2>

            <Slider
                value={second}
                onSlidingComplete={(value) => setSecond(Math.round(value))}
                minimumValue={0}
                maximumValue={maxSecond}
                step={sliderStep}
                minimumTrackTintColor="#E64A19"
                maximumTrackTintColor="#FFFFFF"
                thumbTintColor="#E64A19"
                style={{ width: responsiveScreenWidth(90), alignSelf: 'center' }}
            />

            <StepMarkersBar max={maxSecond} step={markerStep} current={second} />
            <View className="flex flex-row justify-between w-full">
                <Heading2 className="text-white">0</Heading2>
                <Heading2 className="text-white">{maxSecond}</Heading2>
            </View>

            <TouchableOpacity
                onPress={fetchPrediction}
                style={{
                    marginTop: 16,
                    backgroundColor: '#E64A19',
                    padding: 12,
                    borderRadius: 30,
                    alignItems: 'center',
                }}
            >
                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                    <Heading2 className="text-white">Enter</Heading2>
                </View>
            </TouchableOpacity>

            {humidity !== null ? (
                <>
                    <Heading2 className="text-center text-white mt-6">
                        Prediksi Kelembapan
                    </Heading2>
                    <Text
                        className="text-[#3E2723] text-center text-white"
                        style={{
                            fontFamily: 'Montserrat_700Bold',
                            fontSize: 90,
                        }}
                    >
                        {humidity.toFixed(1)}%
                    </Text>
                </>
            ) : (
                <>
                    <Heading2 className="text-center text-white mt-6">
                        Coba klik enter.
                    </Heading2>
                </>
            )}

            <Subtitle2 className="text-white pb-8">
                {second >= 60 && (
                    <>
                        *{second} detik adalah{' '}
                        {Math.floor(second / 60)} menit
                        {second % 60 !== 0 && ` ${second % 60} detik`}
                    </>
                )}
            </Subtitle2>


            <Small className="text-[#FBFF00] pt-[32px] pb-2">
                *JIKA HASIL DIRASA BELUM AKURAT, TUNGGU BEBERAPA SAAT DIKARENAKAN ALAT SEDANG MENGUMPULKAN DATA
            </Small>
            <BodyBold className="text-[#FBFF00] pb-2">
                *Ini hanyalah model prediksi, bukan kelembapan asli
            </BodyBold>
            <View className='mb-[100px]'></View>
        </ScrollView>
    );
}
