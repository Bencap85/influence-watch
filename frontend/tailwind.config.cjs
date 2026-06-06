module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        tech: {
          // bg: "#0b0f19",
          panel: "#111827",
          border: "#1f2937",
          accent: "#00eaff",
          accent2: "#7df9ff",
          danger: "#ff3b3b",
          success: "#00ff9d",
        }
      }
    }
  },
  plugins: [require("daisyui"), require("tailwind-scrollbar")({ nocompatible: true })],
};
