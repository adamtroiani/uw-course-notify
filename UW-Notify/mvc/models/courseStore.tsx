import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY = "subscribedCourses";

export class Course {
  /** Normalized code (e.g., "CS451") */
  public readonly code: string;
  /** UWaterloo term code (e.g., 1261) */
  public readonly term: number;

  /** Create a Course (throws if invalid) */
  constructor(code: string, term: number) {
    this.code = code;
    this.term = term;
    Object.freeze(this);
  }
}

export async function getCourses(): Promise<Course[]> {
  const json = await AsyncStorage.getItem(KEY);
  return json ? JSON.parse(json) : [];
}

export async function addCourse(course: Course) {
  const list = await getCourses();
  if (list.includes(course)) return;
  list.push(course);
  await AsyncStorage.setItem(KEY, JSON.stringify(list));
}

export async function removeCourse(course: Course) {
  const list = (await getCourses()).filter(
    (c) => !(c.code === course.code && c.term === course.term)
  );
  await AsyncStorage.setItem(KEY, JSON.stringify(list));
}
