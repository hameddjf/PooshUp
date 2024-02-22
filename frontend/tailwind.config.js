/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        body: "#5A5A5A",
        heading: "#212121",
        input: "#1D1E1F",
        black: "#000",
        white: "#fff",
        linen: "#FBF1E9",
        linenSecondary: "#ECE7E3",
        olive: "#3D9970",
        maroon: "#B03060",
        brown: "#C7844B",
        placeholder: "#707070",
        borderBottom: "#f7f7f7",
        facebook: "#4267B2",
        facebookHover: "#395fad",
        google: "#4285F4",
        googleHover: "#307bf9",
        gray: {
          50: "#FBFBFB",
          100: "#F1F1F1",
          150: "#F4F4F4",
          200: "#F9F9F9",
          300: "#E6E6E6",
          350: "#E9ECEF",
          400: "#999999",
          500: "#D8D8D8",
          600: "#3A3A3A",
          700: "#292929",
          800: "#707070",
        },
      },
      height: {
        screen: "100dvh",
      },
    },

    keyframes: {
      fadeInRight: {
        "0%": { opacity: 0, transform: "translateX(-50px)" },
        "100%": { opacity: 1, transform: "translateX(0)" },
      },
      fadeIn: {
        "0%": { opacity: 0, transform: "scale(1.1)" },
        "100%": { opacity: 1, transform: "scale(1)" },
      },
      fadeInUp: {
        "0%": { opacity: 0, transform: "translateY(18px)" },
        "50%": { opacity: 0.4 },
        "100%": { opacity: 1, transform: "translateY(0)" },
      },
      slideIn: {
        "0%": {
          width: "0",
        },
        "100%": {
          width: "100%",
        },
      },
      underline: {
        "0%": {
          width: "0",
        },
        "100%": {
          width: "100%",
        },
      },
    },
  },
  plugins: [],
};
