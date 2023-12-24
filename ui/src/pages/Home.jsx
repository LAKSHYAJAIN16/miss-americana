import React from "react";
import Logo from "../assets/crown.png"; // Tell webpack this JS file uses this image

export default function Home() {
  return (
    <div className="center flex flex-col justify-center items-center">
      <img src={Logo} className="h-20 w-20" />
      <h1 className="-mt-10 text-8xl font-bold text-pink-500 text-center font-dancing ">
        miss americana
      </h1>
      <p className="text-lg text-white text-center font-dancing">
        'because spotify sucks'
      </p>

      <a href="/onboard">
        <button className="text-2xl bg-white mt-10 transition-all pl-9 pr-9 pt-1 pb-1 rounded-xl hover:scale-110 font-josepfin">
          start vibing
        </button>
      </a>
    </div>
  );
}
