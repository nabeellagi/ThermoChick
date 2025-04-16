import FontAwesome from '@expo/vector-icons/FontAwesome';
import { Tabs } from 'expo-router';
import { Image } from 'expo-image';

export default function TabLayout() {
  return (
    <Tabs screenOptions={
        {
          tabBarActiveTintColor: 'white',
          tabBarStyle: {
            backgroundColor: '#795548',
          },
        }
      }
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: () => (
            <Image 
              source={require('../../assets/pixel-emoji/home.png')} 
              style={{ width:32, height:32 }}
            />
          ),
          headerShown : false
        }}
      />

      <Tabs.Screen
        name="ai"
        options={{
          title: 'AI Assistant',
          tabBarIcon: () => (
            <Image 
              source={require('../../assets/pixel-emoji/star.png')} 
              style={{ width:32, height:32 }}
            />
          ),
          headerShown : false
        }}
      />

      <Tabs.Screen
        name="graph"
        options={{
          title: 'Lihat Grafik',
          tabBarIcon: () => (
            <Image 
              source={require('../../assets/pixel-emoji/arrow-up.png')} 
              style={{ width:32, height:32 }}
            />
          ),
          headerShown : false
        }}
      />
    </Tabs>
  );
}
