import { useSwiper } from "swiper/react";
// import rightArrow from "../../../assets/icons/RightArrow-icon.svg";

function CarouselPrev() {
  const swiper = useSwiper();

  return (
    <button
      onClick={() => swiper.slidePrev()}
      className={`duration-250 3xl:w-12 3xl:h-12 3xl:text-2xl z-40 m-12 flex h-7 w-7 rotate-180 transform
    items-center justify-center rounded-full bg-white text-sm
    text-black shadow transition hover:bg-gray-900 hover:text-white focus:outline-none
    md:text-base lg:h-9 lg:w-9 lg:text-xl xl:h-10 xl:w-10 ltr:left-0 ltr:-translate-x-1/2
     rtl:right-0 rtl:translate-x-1/2`}
    >
      {/* <img src={rightArrow} /> */}
      <svg
        stroke="currentColor"
        fill="currentColor"
        strokeWidth="0"
        viewBox="0 0 512 512"
        height="1em"
        width="1em"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M217.9 256L345 129c9.4-9.4 9.4-24.6 0-33.9-9.4-9.4-24.6-9.3-34 0L167 239c-9.1 9.1-9.3 23.7-.7 33.1L310.9 417c4.7 4.7 10.9 7 17 7s12.3-2.3 17-7c9.4-9.4 9.4-24.6 0-33.9L217.9 256z"></path>
      </svg>
    </button>
  );
}

export default CarouselPrev;
