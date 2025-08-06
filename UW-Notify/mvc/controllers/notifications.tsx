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
      const { data } = await Notifications.getExpoPushTokenAsync({
        projectId: Constants.expoConfig?.extra?.projectId,
      });
      if (!isMounted) return;
      setToken(data);

      /* 4️⃣ Tell your FastAPI backend you want alerts */
      await fetch(`${apiHost}/subscribe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ course: courseCode, push_token: data }),
      });
    })();

    return () => {
      isMounted = false;
    };
  }, [courseCode, apiHost]);

  return { token, permission };
}
