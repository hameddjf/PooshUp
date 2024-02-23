/* eslint-disable no-unused-vars */
import { useEffect, useState } from "react";
import hero_1 from "../assets/images/hero/hero-1.jpg";
import hero_2 from "../assets/images/hero/hero-2.jpg";
import hero_3 from "../assets/images/hero/hero-3.jpg";

import Carousel from "../components/ui/Carousel/Carousel";

function Home() {
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/products")
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data);
      });
  }, []);

  return (
    <main>
      <Carousel />
    </main>
  );
}

export default Home;
