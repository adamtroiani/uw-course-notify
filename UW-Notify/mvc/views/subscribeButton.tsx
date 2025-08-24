import { useEffect, useState } from "react";
import { addCourse, getCourses } from "../models/courseStore";
import React from "react";
import { StyledButton } from "./styledButton";
import { useGlobalContext } from "../models/context";

export default function SubscribeButton({
  course,
  onSub,
}: {
  course: string;
  onSub: () => void;
}) {
  const { apiHost, token } = useGlobalContext();
  const [subbed, setSubbed] = useState(false);

  useEffect(() => {
    const loadCourses = async () => {
      const courses = await getCourses();
      setSubbed(
        course === "" ||
          courses.some((c) => c === course || courses.length == 5)
      );
    };

    loadCourses();
  }, [course]);

  const handlePress = async () => {
    console.log(`button pressed - subscribing to ${course}`);
    if (!course) {
      return;
    }

    await fetch(`${apiHost}/subscribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course: course,
        push_token: token,
        term: 1259, // TODO: fetch term on app launch directly from UW instead of hitting my server to reduce load (i.e. useEffect in index.ts) instead of hardcoding
      }),
    })
      .then((response) => {
        if (!response.ok) {
          alert(`${course} does not exist or is not being offered this term!`);
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
