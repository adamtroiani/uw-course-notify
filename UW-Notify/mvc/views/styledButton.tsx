import React, { useEffect, useRef } from "react";
import {
  Text,
  StyleSheet,
  Pressable,
  Animated,
  GestureResponderEvent,
} from "react-native";

type Props = {
  text: string;
  onPress?: (e?: GestureResponderEvent) => void;
  disabled: boolean;
  fontSize: number;
};

export function StyledButton({ text, onPress, disabled, fontSize }: Props) {
  const colorAnim = useRef(new Animated.Value(0)).current;

  const fadeTo = (toValue: number) =>
    Animated.timing(colorAnim, {
      toValue,
      duration: 150,
      useNativeDriver: false,
    }).start();

  const interpolatedColor = colorAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ["grey", "rgb(109, 172, 203)"],
  });

  return (
    <Pressable
      onPress={onPress}
      onPressIn={() => fadeTo(1)}
      onPressOut={() => fadeTo(0)}
      disabled={disabled}
    >
      <Animated.Text style={{ color: interpolatedColor, fontSize: fontSize }}>
        {text}
      </Animated.Text>
    </Pressable>
  );
}
