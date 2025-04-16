import '../global.css';
import { Stack } from 'expo-router/stack';
import { useFonts } from '@expo-google-fonts/montserrat/useFonts';
import { Montserrat_400Regular } from '@expo-google-fonts/montserrat/400Regular';
import { Montserrat_500Medium } from '@expo-google-fonts/montserrat/500Medium';
import { Montserrat_600SemiBold } from '@expo-google-fonts/montserrat/600SemiBold';
import { Montserrat_700Bold } from '@expo-google-fonts/montserrat/700Bold';
import { Montserrat_800ExtraBold } from '@expo-google-fonts/montserrat/800ExtraBold';
import { Montserrat_400Regular_Italic } from '@expo-google-fonts/montserrat/400Regular_Italic';
import { Montserrat_600SemiBold_Italic } from '@expo-google-fonts/montserrat/600SemiBold_Italic';
import { Montserrat_700Bold_Italic } from '@expo-google-fonts/montserrat/700Bold_Italic';

export default function Layout() {

  let [fontsLoaded] = useFonts({
    Montserrat_400Regular, 
    Montserrat_500Medium, 
    Montserrat_600SemiBold, 
    Montserrat_700Bold, 
    Montserrat_800ExtraBold, 
    Montserrat_400Regular_Italic, 
    Montserrat_600SemiBold_Italic, 
    Montserrat_700Bold_Italic, 
  });

  if (!fontsLoaded) {
    return null;
  }

  return (
    <Stack screenOptions={{
        header: () => null
      }}
    >
      <Stack.Screen name="(tabs)" options={{ header: () => null }} />
    </Stack>
  );
}
