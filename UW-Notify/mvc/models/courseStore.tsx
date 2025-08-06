import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY = "subscribedCourses";

export async function getCourses(): Promise<string[]> {
  const json = await AsyncStorage.getItem(KEY);
  return json ? JSON.parse(json) : [];
}

export async function addCourse(code: string) {
  const list = await getCourses();
  if (list.includes(code)) return;
  list.push(code);
  await AsyncStorage.setItem(KEY, JSON.stringify(list));
}

export async function removeCourse(code: string) {
  const list = (await getCourses()).filter((c) => c !== code);
  await AsyncStorage.setItem(KEY, JSON.stringify(list));
}
