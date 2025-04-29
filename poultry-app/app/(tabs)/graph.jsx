import React, { useEffect, useState } from 'react';
import { ScrollView, View, Text, ActivityIndicator, Button } from 'react-native';
import { LineChart } from 'react-native-gifted-charts';
import { Heading1 } from '../../components/Heading';
import { Title } from '../../components/Title';

export default function Graph() {
  const [sensorData, setSensorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchSensorData = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/sensor/recent`);
      const data = await res.json();
      if (data.status === "success") {
        setSensorData(data.data);
        const latestTimestamp = data.data.timestamps?.slice(-1)[0];
        if (latestTimestamp) {
          setLastUpdated(new Date(latestTimestamp));
        }
      }
    } catch (error) {
      console.error("Failed to fetch sensor data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSensorData();
  }, []);

  const formatChartData = (values) => {
    return values.map((value, index) => ({
      value,
      label: index % 2 === 0 ? `#${index}` : '',
    }));
  };

  const chartConfig = {
    spacing: 30,
    color: '#5D4037',
    thickness: 3,
    hideDataPoints: false,
    showTextOnIndicators: true,
    textColor: 'black',
    xAxisLabelTextStyle: { color: '#333' },
    yAxisTextStyle: { color: '#333' },
  };

  const formatLastUpdated = (date) => {
    return new Intl.DateTimeFormat('id-ID', {
      dateStyle: 'long',
      timeStyle: 'medium',
    }).format(date);
  };

  return (
    <ScrollView className='py-12 px-8 bg-[#FFF3F0]'>
      <Heading1>Thermochick</Heading1>
      <Title className="pt-[32px]">Lihat Grafik</Title>

      <Button title="Perbarui" onPress={fetchSensorData} color="#795548" style={{
        
      }} />

      {lastUpdated && (
        <Text style={{ marginTop: 10, fontStyle: 'italic', color: '#555' }}>
          Terakhir diperbarui: {formatLastUpdated(lastUpdated)}
        </Text>
      )}

      {loading ? (
        <ActivityIndicator size="large" color="#FF7B54" className="mt-10" />
      ) : sensorData ? (
        <View style={{ marginTop: 30 }}>
          <Text style={{ fontSize: 18, marginBottom: 10 }}>Temperature (°C)</Text>
          <LineChart
            data={formatChartData(sensorData.temperatures)}
            yAxisOffset={22}
            {...chartConfig}
          />

          <Text style={{ fontSize: 18, marginTop: 30, marginBottom: 10 }}>Humidity (%)</Text>
          <LineChart
            data={formatChartData(sensorData.humidities)}
            color="#3DA5F4"
            {...chartConfig}
          />
        </View>
      ) : (
        <Text style={{ marginTop: 20 }}>Tidak ada data sensor ditemukan.</Text>
      )}
      <View className='my-[100px]' />
    </ScrollView>
  );
}
