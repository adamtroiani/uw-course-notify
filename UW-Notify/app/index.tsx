import React, {
  useState,
  useEffect,
  createContext,
  useContext,
  useCallback,
} from "react";
import { Text, TextInput, View, StyleSheet } from "react-native";
import * as Notifications from "expo-notifications";
import { usePushNotifications } from "@/mvc/controllers/notifications";
import { getCourses } from "@/mvc/models/courseStore";
import SubscribeButton from "@/mvc/views/subscribeButton";
import SubscribedCourse from "@/mvc/views/subscribedCourse";
import { GlobalProvider } from "@/mvc/models/context";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
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
  const API_HOST = "https://api.adamtroiani.com";

  const [course, setCourse] = useState("");
  const { token, permission } = usePushNotifications(course, API_HOST);

  const [subs, setSubs] = useState<string[]>([]);

  const refreshSubs = useCallback(async (resetCourse: boolean) => {
    const list = await getCourses();
    setSubs(list);
    if (resetCourse) setCourse("");
  }, []);

  let term: string | null = null;

  useEffect(() => {
    refreshSubs(false);
  }, [refreshSubs]);

  return (
    <GlobalProvider value={{ apiHost: API_HOST, token: token }}>
      <View style={styles.container}>
        <View style={styles.container}>
          <Text style={styles.heading}>Welcome to UW Notify 🌐</Text>
          {permission !== "granted" || !token ? (
            <View style={styles.noticeWrap}>
              <Text style={styles.noticeText}>
                Please enable notifications to begin adding courses ‼️
              </Text>
            </View>
          ) : (
            <>
              <View style={styles.courseInput}>
                <Text>Please enter a course:</Text>
                <TextInput
                  placeholder="e.g. CLAS 202"
                  maxLength={10}
                  style={[styles.box, { minWidth: 80, maxWidth: 100 }]}
                  value={course}
                  onChangeText={setCourse}
                  autoCapitalize="characters"
                />
                <View style={[styles.courseInput, styles.box, { width: 22 }]}>
                  <SubscribeButton
                    course={course}
                    onSub={() => refreshSubs(true)}
                  />
                </View>
              </View>
            </>
          )}
        </View>
        {permission === "granted" && token && (
          <View style={styles.watchlist}>
            {subs.length === 0 ? (
              <>
                <Text>Your watchlist is empty!</Text>
                <Text>Get started by adding a course 📚</Text>
              </>
            ) : (
              <>
                <Text style={styles.heading}>My Watchlist</Text>
                {subs.map((course) => (
                  <SubscribedCourse
                    key={`${course}-${term}`}
                    course={course}
                    termCode={1259}
                    onChanged={() => refreshSubs(false)}
                  />
                ))}
              </>
            )}
          </View>
        )}
      </View>
    </GlobalProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
  },
  watchlist: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 10,
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
  heading: { fontSize: 16, fontWeight: "bold" },
  noticeWrap: {
    width: "80%",
    alignSelf: "stretch", // make wrapper full width
    marginTop: 8,
  },
  noticeText: {
    fontSize: 14,
    fontWeight: "bold",
    textAlign: "center", // center multi-line text
  },
});
