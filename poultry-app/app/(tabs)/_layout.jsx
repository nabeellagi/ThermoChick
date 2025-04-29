import { Tabs } from 'expo-router';
import { Image } from 'expo-image';

export default function TabLayout() {
  return (
    <Tabs screenOptions={
        {
          tabBarActiveTintColor: 'white',
          tabBarStyle: {
            position: 'absolute',
            margin: 12,
            backgroundColor: '#795548',
            borderRadius: 30,
            left: 12,
            right: 12,
            bottom: 12,
            elevation: 5, // Android shadow
            shadowColor: '#000', // iOS shadow
            shadowOffset: { width: 0, height: 3 },
            shadowOpacity: 0.2,
            shadowRadius: 4,
          }
          
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
