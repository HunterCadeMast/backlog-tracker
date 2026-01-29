"use client";
import RandomColor from "../components/RandomColor";

const Home = () => {
  return (
    <>
      <div className = "base-background overflow-hidden">
        <h1 className = "font-main-title text-[clamp(3rem,10vw,12rem)] text-white scale-y-125 md:scale-y-180 origin-center pl-4 md:pl-12 animate-fade-left motion-safe:animate-fade-left"><RandomColor constant>Gaming</RandomColor></h1>
        <h1 className = "font-main-title text-[clamp(3rem,10vw,12rem)] text-white scale-y-125 md:scale-y-180 origin-center pr-4 md:pr-12 self-end animate-fade-right motion-safe:animate-fade-right"><RandomColor constant>Logjam</RandomColor></h1>
      </div>
    </>
  );
};

export default Home;
