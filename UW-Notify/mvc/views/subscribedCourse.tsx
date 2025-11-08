import { Text, View, StyleSheet } from "react-native";
import React from "react";
import { StyledButton } from "./styledButton";
import { Course, removeCourse } from "../models/courseStore";
import { useGlobalContext } from "../models/context";
import { term_to_str } from "../controllers/get_term";

export default function SubscribedCourse({
  course,
  onChanged,
}: {
  course: Course;
  onChanged: () => void;
}) {
  const { apiHost, token } = useGlobalContext();

  function unsubscribeCourse(course: Course, expoToken: string): void {
    fetch(apiHost + "/unsubscribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        course: course.code,
        push_token: expoToken,
        term: course.term,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          alert("Something went wrong. Please try again.");
          console.log(response);
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(async () => {
        console.log(`successfuly unsubbed ${course.code} - ${course.term}!`);
        await removeCourse(course);
        await onChanged();
      });
  }

  return (
    <View style={styles.container}>
      <View style={[styles.courseView, styles.box]}>
        <Text>
          {course.code} - {term_to_str(course.term)}
        </Text>
      </View>
      <StyledButton
        onPress={() => {
          console.log(
            `pressed unsub button for ${course.code} - ${course.term}`
          );
          unsubscribeCourse(course, token || "");
        }}
        text="☒"
        disabled={!token}
        fontSize={35}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 0,
    flexDirection: "row",
    gap: 10,
    alignItems: "center",
  },
  courseView: {
    width: 175,
    height: 35,
    justifyContent: "center",
    paddingLeft: 4,
  },
  box: {
    borderWidth: 1,
    borderColor: "grey",
    borderStyle: "solid",
    padding: 2,
  },
  button: {
    color: "grey",
    fontSize: 35,
  },
});
