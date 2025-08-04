import { Image } from 'expo-image';
import { ActivityIndicator, Platform, StyleSheet, AppState } from 'react-native';
import { useEffect, useState } from 'react';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import * as Notifications from "expo-notifications"
import Constants from "expo-constants"

// ---------- API helpers ----------
const API_HOST = Platform.select({
  ios: 'http://localhost:8000',
  android: 'http://10.0.2.2:8000',
  default: 'http://localhost:8000',
});

type Availability = {
  course: string;
  available_sections: string[];
};
// ---------------------------------

const POLL_EVERY_MS = 5_000;
const COURSE_CODE   = 'CLAS 202';                                   //  NEW

export default function HomeScreen() {
  const [data, setData]   = useState<Availability | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  /* ───────── 1. SUBSCRIBE FOR PUSHES ONCE ───────── */
  useEffect(() => {
    (async () => {
      // Ask user permission
      const { status } = await Notifications.requestPermissionsAsync();
      if (status !== 'granted') {
        console.warn('Push permission not granted');
        return;
      }

      // Get Expo push token
      const { data: token } = await Notifications.getExpoPushTokenAsync({
        projectId: Constants.expoConfig?.extra?.eas?.projectId,
      });

      // Send token to your FastAPI backend
      await fetch(`${API_HOST}/subscribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ course: COURSE_CODE, push_token: token }),
      });
      console.log('✔ Subscribed for pushes:', token);
    })().catch(console.error);
  }, []);
  /* ──────────────────────────────────────────────── */

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
          style={styles.reactLogo}
        />
      }>
      {/* --- Stock welcome content --- */}
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Welcome!</ThemedText>
        <HelloWave />
      </ThemedView>

      {/* --- Availability results --- */}
      <ThemedView style={styles.stepContainer}>
        <ThemedText type="subtitle">CLAS 202 seat tracker</ThemedText>

        {loading && <ActivityIndicator size="small" />}

        {error && (
          <ThemedText type="error">
            Couldn’t fetch availability – {error}
          </ThemedText>
        )}

        {data && (
          <>
            <ThemedText>
              {data.available_sections.length
                ? 'Open section codes:'
                : 'No open seats right now.'}
            </ThemedText>

            {data.available_sections.map((sec) => (
              <ThemedText key={sec} type="defaultSemiBold">
                • {sec}
              </ThemedText>
            ))}
          </>
        )}
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
});
