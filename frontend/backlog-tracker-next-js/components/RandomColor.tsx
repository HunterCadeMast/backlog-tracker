"use client";
import { useState, isValidElement, cloneElement, ReactNode, ReactElement } from "react";

const colors = ["var(--text1)", "var(--text2)", "var(--text3)", "var(--text4)",];

type RandomColorProps = {
  children: ReactElement<React.HTMLAttributes<HTMLElement>> | string;
  constant?: boolean;
  element?: "text" | "bg";
};

const RandomColor = ({children, constant = false, element = "text"}: RandomColorProps)  => {
  const [color, setColor] = useState<string | undefined>();
  const randomizeColor = () => {
    const availableColors = colors.filter((c) => c !== color);
    const nextColor = availableColors[Math.floor(Math.random() * availableColors.length)];
    setColor(nextColor);
  };
  const resetColor = () => {
    if (!constant) setColor(undefined);
  };
  const changeElement = element === "bg" ? {backgroundColor: color} : {color: color};
  const animation = "transition-colors duration-150";
  if (isValidElement(children)) {
    return cloneElement(children, {style: { ...children.props.style, ...changeElement }, className: [children.props.className, animation].filter(Boolean).join(" "), onMouseEnter: randomizeColor, onMouseLeave: resetColor,});
  }
  return (
    <span onMouseEnter ={ randomizeColor} onMouseLeave = {resetColor} style = {changeElement} className = {`${animation} cursor-pointer`}>{children}</span>
  );
};

export default RandomColor;