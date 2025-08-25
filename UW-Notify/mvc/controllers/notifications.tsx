import { useEffect, useState } from "react";
import * as Notifications from "expo-notifications";
import * as Device from "expo-device";
import Constants from "expo-constants";

export function usePushNotifications(courseCode: string, apiHost: string) {
  const [token, setToken] = useState<string | null>(null);
  const [permission, setPerm] = useState<"granted" | "denied" | "undetermined">(
    "undetermined"
  );

  useEffect(() => {
    let isMounted = true;

    (async () => {
      /* 1️⃣ Only try on real devices */
      if (!Device.isDevice) return;

      /* 2️⃣ Check / request permission */
      const { status: existing } = await Notifications.getPermissionsAsync();
      let status = existing;
      if (existing !== "granted") {
        ({ status } = await Notifications.requestPermissionsAsync());
      }
      if (!isMounted) return;
      setPerm(status);

      if (status !== "granted") return; // user said “Don’t Allow”

      /* 3️⃣ Get Expo push token */
      const projectId =
        Constants.easConfig?.projectId ?? // prod
        Constants.expoConfig?.extra?.projectId; // dev

      const { data } = await Notifications.getExpoPushTokenAsync({});
      if (!isMounted) return;
      setToken(data);
    })();

    return () => {
      isMounted = false;
    };
  }, [courseCode, apiHost]);

  return { token, permission };
}
