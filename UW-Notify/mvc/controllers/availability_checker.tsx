import { View, Text } from "react-native";
import React, { useEffect, useState } from "react";

const POLL_RATE_MS = 5_000;

enum AvailabilityStatus {
  Pending,
  Available,
  Full,
}

export default function availability_checker() {
  const [status, setStatus] = useState("pending");

  // poll availability every 5 seconds
  useEffect(() => {
    const intervalId = setInterval(() => {
      console.log("This runs every second!");
    }, POLL_RATE_MS);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <View>
      <Text>availability_checker</Text>
    </View>
  );
}
