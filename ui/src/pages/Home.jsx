import React from "react";
import Logo from "../assets/crown.png"; // Tell webpack this JS file uses this image

export default function Home() {
  return (
    <div className="center flex flex-col justify-center items-center">
      <img src={Logo} className="h-24 w-24" />
      <h1 className="-mt-10 text-8xl font-bold text-pink-500 text-center font-dancing ">
        miss americana
      </h1>
      <p className="text-lg text-white text-center font-dancing">
        'because spotify sucks'
      </p>

      <button className="text-2xl bg-white mt-10 transition-all pl-10 pr-10 pt-3 pb-3 rounded-xl hover:scale-110 font-josepfin">
        start vibing
      </button>
    </div>
  );
}
