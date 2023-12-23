import React from "react";
import Logo from "../assets/crown.png"; // Tell webpack this JS file uses this image

export default function Home() {
  return (
    <div className="flex flex-col justify-center items-center mt-[50px]">
      <img src={Logo} className="h-32 w-32"/>
      <h1 className="text-3xl font-bold text-pink-500">Hello world!</h1>
    </div>
  );
}
