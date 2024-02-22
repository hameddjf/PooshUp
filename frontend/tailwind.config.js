/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
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
    },
  },
  plugins: [],
};
