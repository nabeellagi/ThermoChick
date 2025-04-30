import { ScrollView, View, TextInput, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Heading1 } from '../../components/Heading';
import { Title } from '../../components/Title';
import { Subtitle2 } from '../../components/Subtitle';
import { useEffect, useState } from 'react';
import { responsiveWidth } from "react-native-responsive-dimensions";
import Markdown from 'react-native-markdown-display';
import { Image } from 'expo-image';
import { Audio } from 'expo-av';  // Import expo-av for recording
import * as FileSystem from 'expo-file-system';  // For handling file URIs

export default function AI() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false); // Track if recording
  const [recording, setRecording] = useState(null); // Store the recording instance
  const [audioUri, setAudioUri] = useState(null); // Store the recorded audio file URI

  const [audio, setAudio] = useState(null);

  const [permissionResponse, requestPermission] = Audio.usePermissions();

  // Start recording function
  const startRecording = async () => {
    try {
      if (permissionResponse.status !== 'granted') {
        console.log('Requesting permission..');
        await requestPermission();
      }
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      if(audio){
        audio.stopAsync();
      }

      console.log('Starting recording..');
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      setIsRecording(true); // Set recording state to true
      console.log('Recording started');
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  // Stop recording function and post file to /vtt/text-questions
  const stopRecording = async () => {
    try {
      console.log('Stopping recording..');
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setAudioUri(uri); // Save the recorded file URI
      setRecording(null);
      setIsRecording(false); // Set recording state to false
      console.log('Recording stopped and stored at', uri);

      // Upload the recorded audio to the server
      await uploadAudio(uri);
    } catch (err) {
      console.error('Failed to stop recording', err);
    }
  };

  // Handle button press to toggle between recording and stopping recording
  const handleRecordPress = async () => {
    if (isRecording) {
      await stopRecording();
    } else {
      await startRecording();
    }
  };

  // Upload the audio file to the server
  const uploadAudio = async (uri) => {
    try {
      setLoading(true);

      // Read the audio file into base64 or binary data
      const fileInfo = await FileSystem.readAsStringAsync(uri, {
        encoding: FileSystem.EncodingType.Base64,
      });

      const formData = new FormData();
      formData.append('file', {
        uri,
        type: 'audio/m4a',  // Change this if you're using a different format
        name: 'audio.m4a',
      });

      const res = await fetch(`${process.env.EXPO_PUBLIC_API_URL}/vtt/text-questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      });

      const data = await res.json();

      if (data?.text) {
        setResponse(data.text);
        if (data.audio_url) {
          playAudio(data.audio_url);
        }
      } else {
        setResponse('Tidak ada jawaban ditemukan.');
      }

      console.log('Audio uploaded and response received');
    } catch (error) {
      setResponse('Gagal mengunggah audio atau mendapatkan jawaban.');
      console.error('Upload error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle query submission
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
      setResponse(data.answer || "Tidak ada jawaban ditemukan.");
    } catch (error) {
      setResponse("Gagal mengambil jawaban. Pastikan server berjalan.");
    } finally {
      setLoading(false);
    }
  };

  const playAudio = async (audioPath) => {
    try {
      const sound = new Audio.Sound();
      const fullUrl = `${process.env.EXPO_PUBLIC_API_URL}${audioPath}`;
      await sound.loadAsync({ uri: fullUrl });
      await sound.playAsync();
      setAudio(sound); // Save for cleanup
    } catch (error) {
      console.error("Failed to play audio:", error);
    }
  };
  
  
  useEffect(() => {
    return () => {
      if (audio) {
        audio.unloadAsync();
      }
    };
  }, [audio]);

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

          {/* New Button for recording */}
          <TouchableOpacity
            onPress={handleRecordPress}
            style={{
              marginTop: 16,
              backgroundColor: '#E64A19',
              padding: 12,
              borderRadius: 20,
              alignItems: 'center',
            }}
          >
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <Image
                source={require('../../assets/pixel-emoji/darkmic.png')}
                style={{
                  width: 40,
                  height: 40,
                  marginRight: 8,
                }}
              />
              <Text style={{ color: '#fff', fontFamily: 'Montserrat_600SemiBold' }}>
                {isRecording ? "Sedang Mendengarkan..." : "Berbicara Langsung?"}
              </Text>
            </View>
          </TouchableOpacity>

        </View>

        <View className='pt-[32px] mb-[128px]'>
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
