/* eslint-disable no-unused-vars */
import hero_1 from "../../../assets/images/hero/hero-1.jpg";
import hero_2 from "../../../assets/images/hero/hero-2.jpg";
import hero_3 from "../../../assets/images/hero/hero-3.jpg";
import hero_4 from "../../../assets/images/hero/hero-4.jpg";
import hero_5 from "../../../assets/images/hero/hero-5.jpg";
import hero_6 from "../../../assets/images/hero/hero-6.jpg";

import {
  Navigation,
  Autoplay,
  Pagination,
  Scrollbar,
  A11y,
} from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";

// Import Swiper styles
import "swiper/css";
import CarouselNext from "./CarouselNext";
import CarouselPrev from "./CarouselPrev";

function Carousel() {
  return (
    <div className="pagecontainer relative">
      <Swiper
        modules={[Navigation, Autoplay, Pagination, Scrollbar, A11y]}
        spaceBetween={50}
        slidesPerView={1}
        loop={true}
        centeredSlides={true}
        autoplay={{
          delay: 6000,
          disableOnInteraction: false,
        }}
        navigation
        pagination={{ clickable: true }}
        scrollbar={{ draggable: true }}
        // onSwiper={(swiper) => console.log(swiper)}
        // onSlideChange={() => console.log("slide change")}
      >
        <div className="absolute -left-14 top-1/2 z-30 -translate-y-16 md:-left-12 md:-translate-y-24">
          <CarouselNext />
        </div>
        <SwiperSlide>
          <img src={hero_4} alt="slider image" />
        </SwiperSlide>
        <SwiperSlide>
          <img src={hero_5} alt="slider image" />
        </SwiperSlide>
        <SwiperSlide>
          <img src={hero_6} alt="slider image" />
        </SwiperSlide>
        <div className="absolute -right-7 top-1/2 z-30 -translate-y-16 md:-right-2 md:-translate-y-24">
          <CarouselPrev />
        </div>
      </Swiper>
    </div>
  );
}

export default Carousel;
