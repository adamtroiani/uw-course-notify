import { Image } from 'expo-image';
import { ActivityIndicator, Platform, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';
import { AppState, Platform } from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

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

export default function HomeScreen() {
  const [data, setData]   = useState<Availability | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const fetchAvailability = async () => {
      try {
        if (AppState.currentState !== 'active') return; // skip if app in background
        const res = await fetch(
          `${API_HOST}/availability/${encodeURIComponent('CLAS 202')}`,
        );
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
        const json: Availability = await res.json();
        setData(json);
        setError(null);
      } catch (e) {
        setError((e as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchAvailability();

    intervalId = setInterval(fetchAvailability, POLL_EVERY_MS);

    return () => clearInterval(intervalId);
  }, []);

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
