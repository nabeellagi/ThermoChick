import { ScrollView, View, TextInput, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Heading1 } from '../../components/Heading';
import { Title } from '../../components/Title';
import { Subtitle2 } from '../../components/Subtitle';
import { useEffect, useState } from 'react';
import {
  responsiveWidth,
} from "react-native-responsive-dimensions";
import Markdown from 'react-native-markdown-display';

function CallButton(){
  return
}

export default function AI() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      const res = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/faq/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setResponse(data.answer || "Tidak ada jawaban ditemukan."); // Adjust if your backend response uses a different key
    } catch (error) {
      setResponse("Gagal mengambil jawaban. Pastikan server berjalan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView className='py-8 px-8 bg-[#FFF3F0]'>
      <View>
        <Heading1>
          Thermochick
        </Heading1>

        <Title className="pt-[32px]">
          {"Gunakan Asisten \nAI"}
        </Title>

        <View className='pt-[40px]'>
          <Subtitle2>
            Ketik pesan kamu disini
          </Subtitle2>

          <TextInput
            value={query}
            onChangeText={setQuery}
            style={{
              height: responsiveWidth(30),
              borderRadius: 10,
              borderColor: '#3E2723',
              borderWidth: 2,
              fontFamily: 'Montserrat_400Regular',
              paddingHorizontal: 12,
              textAlignVertical: 'top',
            }}
            placeholder='Ketik disini'
            multiline
          />

          <TouchableOpacity
            onPress={handleSubmit}
            style={{
              marginTop: 16,
              backgroundColor: '#3E2723',
              padding: 12,
              borderRadius: 8,
              alignItems: 'center',
            }}
          >
            <Text style={{ color: '#fff', fontFamily: 'Montserrat_600SemiBold' }}>
              Kirim
            </Text>
          </TouchableOpacity>
        </View>

        <View className='pt-[32px]'>
          <Subtitle2>
            Lihat Jawaban Kamu Disini
          </Subtitle2>

          {loading ? (
            <ActivityIndicator color="#3E2723" size="large" style={{ marginTop: 16 }} />
          ) : (
            <Markdown>
              {response}
            </Markdown>
          )}
        </View>
      </View>
    </ScrollView>
  );
}
