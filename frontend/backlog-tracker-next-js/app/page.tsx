"use client";
import RandomColor from "./components/RandomColor";

const Home = () => {
  return (
    <>
      <div className = "base-background">
        <h1 className = "font-main-title text-[clamp(4rem,12vw,12rem)] text-white scale-y-180 origin-center pl-12 animate-fade-left"><RandomColor constant>Gaming</RandomColor></h1>
        <h1 className = "font-main-title text-[clamp(4rem,12vw,12rem)] text-white scale-y-180 origin-center pr-12 self-end animate-fade-right"><RandomColor constant>Logjam</RandomColor></h1>
      </div>
    </>
  );
};

export default Home;
