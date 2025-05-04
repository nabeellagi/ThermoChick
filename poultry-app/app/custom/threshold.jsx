import { ScrollView, View, TouchableOpacity, Vibration, Text } from 'react-native';
import { Title } from '../../components/Title';
import { BodyBold } from '../../components/Body';
import { useState } from 'react';
import { Heading2 } from '../../components/Heading';
import Slider from '@react-native-community/slider';
import { responsiveScreenWidth } from 'react-native-responsive-dimensions';
import { Small } from '../../components/Small';
import { Subtitle2 } from '../../components/Subtitle';

const StepMarkersBar = ({ min, max, step, current }) => {
    const markerCount = Math.floor((max - min) / step) + 1;
    const totalWidth = responsiveScreenWidth(80);
    const markerWidth = 2;
    const totalSpacing = totalWidth - markerCount * markerWidth;
    const spacing = totalSpacing / (markerCount - 1);

    const markers = [];

    for (let i = min; i <= max; i += step) {
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

export default function ThresholdSetting() {
    const minThreshold = 20;
    const maxThreshold = 35;
    const markerStep = 5;
    const sliderStep = 1;

    const [threshold, setThreshold] = useState(25);

    const sendThreshold = async () => {
        try {
            const url = `${process.env.EXPO_PUBLIC_API_URL}/temperature-set?device_id=${process.env.EXPO_PUBLIC_DEVICE_ID}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "temperature" : threshold }),
            });

            const json = await response.json();

            if (json.status === 'success') {
                Vibration.vibrate(100);
                console.log('Threshold updated successfully:', json);
            } else {
                console.error('Threshold update failed:', json);
            }
        } catch (error) {
            console.error('POST error:', error);
        }
    };

    return (
        <ScrollView className='py-[75px] px-[30px] bg-[#080A25]'>
            <Title className="text-center text-white">
                SETEL AMBANG BATAS
            </Title>

            <BodyBold className="text-white text-justify py-[60px]">
                Geser untuk memilih ambang batas suhu (°C) ayam yang diinginkan. Tekan enter untuk menyimpan.
            </BodyBold>

            <Heading2 className="text-center text-white">
                Ambang Batas: {threshold}°C
            </Heading2>

            <Slider
                value={threshold}
                onSlidingComplete={(value) => setThreshold(Math.round(value))}
                minimumValue={minThreshold}
                maximumValue={maxThreshold}
                step={sliderStep}
                minimumTrackTintColor="#E64A19"
                maximumTrackTintColor="#FFFFFF"
                thumbTintColor="#E64A19"
                style={{ width: responsiveScreenWidth(90), alignSelf: 'center' }}
            />

            <StepMarkersBar min={minThreshold} max={maxThreshold} step={markerStep} current={threshold} />
            <View className="flex flex-row justify-between w-full">
                <Heading2 className="text-white">{minThreshold}</Heading2>
                <Heading2 className="text-white">{maxThreshold}</Heading2>
            </View>

            <TouchableOpacity
                onPress={sendThreshold}
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

            <Subtitle2 className="text-white pt-8">
                *Nilai ambang batas ini akan digunakan oleh sistem untuk menyalakan atau mematikan pemanas secara otomatis.
            </Subtitle2>

            <Small className="text-[#FBFF00] pt-4">
                *Pastikan nilai sesuai dengan kondisi ayam dan suhu ruangan.
            </Small>
            <BodyBold className="text-[#FBFF00] pb-2">
                *Jika ada masalah, periksa koneksi atau tunggu sistem memproses data
            </BodyBold>
            <View className='mb-[100px]'></View>
        </ScrollView>
    );
}
