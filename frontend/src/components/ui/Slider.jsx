/* eslint-disable no-unused-vars */
/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable react/prop-types */
import { twMerge } from "tailwind-merge";
import { useEffect, useState } from "react";

function Slider({ slides, bgImage, bgColor }) {
  const [curSlide, setCurSlide] = useState(0);
  const data = slides[curSlide];

  const changeSlideInterval = useEffect(() => {
    const changeSlideInterval = setInterval(nextSlide, 6000);
    return () => {
      clearInterval(changeSlideInterval);
    };
  }, [nextSlide]);

  function nextSlide() {
    if (curSlide < slides.length - 1) {
      setCurSlide(curSlide + 1);
    } else {
      setCurSlide(0);
    }
    clearInterval(changeSlideInterval);
  }

  function prevSlide() {
    if (curSlide > 0) {
      setCurSlide(curSlide - 1);
    } else {
      setCurSlide(slides.length - 1);
    }
    clearInterval(changeSlideInterval);
  }

  function Content() {
    return (
      <div
        className={`relative h-[120vw] sm:h-[350px] md:h-[480px] lg:h-[600px] xl:h-[680px] ${bgColor} overflow-hidden sm:p-4 md:p-6`}
      >
        <div className="absolute bottom-4 left-1/2 z-10 flex -translate-x-1/2 cursor-pointer gap-2 sm:bottom-8">
          {slides.map((slide, index) => (
            <div
              className="h-1 w-20 rounded-full bg-white"
              key={slide.id}
              onClick={() => setCurSlide(index)}
            >
              <span
                className={twMerge(
                  `transition-width z-40 block h-1 w-0 animate-[slideIn_0.7s_forwards] rounded-full ${
                    curSlide === slide.id - 1 ? "w-20 bg-black" : "w-20"
                  }`,
                )}
              ></span>
            </div>
          ))}
        </div>
        {bgImage && <img src={bgImage} className="m-auto w-10/12" />}
        <div className="absolute left-4 top-1/2 z-10 -translate-y-1/2 ">
          {/* <ArrowButton
            direction="left"
            action={prevSlide}
            outlineColor="dark"
            color="rgb(71, 85, 105)"
            offset="far"
          /> */}
        </div>
        <div className="absolute right-4 top-1/2 z-10 -translate-y-1/2">
          {/* <ArrowButton
            direction="right"
            action={nextSlide}
            outlineColor="dark"
            color="rgb(71, 85, 105)"
            offset="far"
          /> */}
        </div>
        <div className={"absolute top-0 h-full w-full py-6 lg:p-16"}>
          <div className="container relative h-full">
            <div className="grid h-full w-full content-center justify-items-center gap-4 sm:w-[60%] sm:justify-items-start sm:gap-8">
              {/* <h4 className="animate-[fadeInRight_0.7s_forwards] text-lg font-thin opacity-0 sm:text-xl sm:font-medium">
                {data.subtitle}
              </h4>
              <h1
                className="mb-0 animate-[fadeInRight_0.7s_0.2s_forwards] text-xl font-bold leading-[1.1]
               opacity-0 sm:text-3xl md:mb-6 md:text-4xl lg:mb-8 lg:text-5xl xl:text-7xl"
              >
                {data.title}
              </h1> */}

              <div
                className={` relative origin-top-left animate-[fadeIn_0.7s_forwards] opacity-0`}
              >
                <img className=" h-[500px]" src={data.image} />
              </div>

              {/* <Button
                animation="animate-[fadeInRight_0.7s_0.4s_forwards] opacity-0"
                mt="8"
                color="black"
                size="big"
              >
                Explore more
              </Button> */}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <Content />;
}

export default Slider;
