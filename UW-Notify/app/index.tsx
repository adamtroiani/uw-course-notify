import React, { useState, createContext, useContext } from "react";
import { Text, TextInput, View, StyleSheet } from "react-native";
import * as Notifications from "expo-notifications";
import Constants from "expo-constants";
import { usePushNotifications } from "@/mvc/controllers/notifications";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
    shouldShowBanner: true,
    shouldShowList: true,
  }),
});

type GlobalContext = {
  apiHost: string;
  token: string | null;
};
export const Context = createContext<GlobalContext | null>(null);
export const useGlobalContext = () => {
  const ctx = useContext(Context);
  if (!ctx) throw new Error("Wrap tree in <PushProvider>");
  return ctx;
};

export default function Index() {
  const API_HOST = __DEV__
    ? `http://${Constants.expoConfig!.hostUri!.split(":")[0]}:8000`
    : "#TODO";

  const [course, setCourse] = useState("");
  const { token, permission } = usePushNotifications(course, API_HOST);

  return (
    <Context.Provider value={{ apiHost: API_HOST, token: token }}>
      <View style={styles.container}>
        <Text style={styles.heading}>Welcome to UW Notify 🌐</Text>
        <View style={styles.courseInput}>
          <Text>Please enter a course:</Text>
          <TextInput
            placeholder="e.g. CLAS 202"
            maxLength={10}
            style={styles.box}
            value={course}
            onChangeText={setCourse}
            autoCapitalize="characters"
          />
        </View>
      </View>
      <View style={styles.container}>
        // change to get courses from storage
        {course && (
          <>
            <Text>Checking availability for {course}...</Text>
          </>
        )}
      </View>
    </Context.Provider>
  );
}

const styles = StyleSheet.create({
  body: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
  },
  courseInput: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
  },
  box: {
    borderWidth: 1,
    borderColor: "grey",
    borderStyle: "solid",
    padding: 2,
  },
  heading: {
    fontSize: 16,
    fontWeight: "bold",
  },
});
