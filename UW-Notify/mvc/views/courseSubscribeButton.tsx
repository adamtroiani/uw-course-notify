import { useEffect, useState } from "react";
import { Button } from "react-native";
import { addCourse, getCourses } from "../models/courseStore";
import { useGlobalContext } from "@/app";
import React from "react";

export default function SubscribeButton({ code }: { code: string }) {
  const [subbed, setSubbed] = useState(false);
  const { apiHost, token } = useGlobalContext();

  useEffect(() => {
    getCourses().then((list) => setSubbed(list.includes(code)));
  }, [code]);

  const handlePress = async () => {
    await addCourse(code); // persist
    await fetch(`${apiHost}/subscribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ course: code, push_token: token }),
    });
    setSubbed(true);
  };

  return (
    <Button
      title={subbed ? "Already Subscribed" : "Notify me"}
      onPress={handlePress}
      disabled={subbed}
    />
  );
}
