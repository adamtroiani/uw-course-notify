import { useEffect, useState } from "react";
import { addCourse, Course, getCourses } from "../models/courseStore";
import React from "react";
import { StyledButton } from "./styledButton";
import { useGlobalContext } from "../models/context";
import { get_term, term_to_str } from "../controllers/get_term";

export default function SubscribeButton({
  code,
  onSub,
}: {
  code: string;
  onSub: () => void;
}) {
  const { apiHost, token } = useGlobalContext();
  const [subbed, setSubbed] = useState(false);

  useEffect(() => {
    const loadCourses = async () => {
      const courses = await getCourses();
      setSubbed(
        code === "" ||
          courses.some((c) => c.code === code || courses.length == 5)
      );
    };

    loadCourses();
  }, [code]);

  const handlePress = async () => {
    const course = new Course(code, get_term());
    console.log(
      `button pressed - subscribing to ${course.code} - ${course.term}`
    );
    if (!course.code) {
      return;
    }

    await fetch(`${apiHost}/subscribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course: course.code,
        push_token: token,
        term: course.term,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          alert(
            `${
              course.code
            } does not exist or is not being offered this term (${term_to_str(
              course.term
            )}), or add period has not begun!`
          );
          console.log(
            "Course does not exist or is not being offered this term!"
          );
          throw new Error("Subscription failed");
        }
      })
      .then(async () => {
        console.log("Successfuly subscribed!");
        await addCourse(course);
        await onSub();
      });
  };

  return (
    <StyledButton
      text="＋"
      fontSize={14}
      onPress={handlePress}
      disabled={subbed}
    />
  );
}
