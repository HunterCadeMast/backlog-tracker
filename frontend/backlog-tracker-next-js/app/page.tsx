"use client";
import RandomColor from "./components/RandomColor";

const Home = () => {
  return (
    <>
      <div className = "container max-w-screen h-full mx-auto flex items-center justify-center bg-main-compliment">
        <h1 className = "font-main-title text-9xl text-white"><RandomColor consant>Gaming</RandomColor></h1>
        <h1 className = "pl-10 font-main-title text-9xl text-white"><RandomColor consant>Logjam</RandomColor></h1>
      </div>
    </>
  );
};

export default Home;