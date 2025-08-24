import { Text, View, StyleSheet } from "react-native";
import React from "react";
import { StyledButton } from "./styledButton";
import { removeCourse } from "../models/courseStore";
import { useGlobalContext } from "../models/context";

export default function SubscribedCourse({
  course,
  termCode,
  onChanged,
}: {
  course: string;
  termCode: Number;
  onChanged: () => void;
}) {
  const { apiHost, token } = useGlobalContext();

  function unsubscribeCourse(
    course: string,
    expoToken: string,
    term: Number
  ): void {
    fetch(apiHost + "/unsubscribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        course: course,
        push_token: expoToken,
        term: term,
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
        console.log(`successfuly unsubbed ${course}!`);
        await removeCourse(course);
        await onChanged();
      });
  }

  return (
    <View style={styles.container}>
      <View style={[styles.courseView, styles.box]}>
        <Text>{course}</Text>
      </View>
      <StyledButton
        onPress={() => {
          console.log(`pressed unsub button for ${course}`);
          unsubscribeCourse(course, token || "", termCode);
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
    width: 120,
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
