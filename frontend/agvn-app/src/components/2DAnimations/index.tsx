const LogoAnimateVariants = {
    hover: {
        backgroundColor: "#112126", boxShadow: "0 0 20px #1b3942", transition: { yoyo: Infinity, delay: 0.25, repeatDelay: 0.15, ease: "easeOut" }
    },
    hovertwo: {
        skew: "20", backgroundColor: "#0a1214", transition: { repeat: Infinity, delay: 0.25, repeatDelay: 1, ease: "easeIn" }
    },
    // spin
    hoverthree: {
        transform: "rotate(360deg)", transition: { repeat: Infinity }
    },
    hoverfour: { skew: 20, transition: { yoyo: Infinity } },
    hoverfive: { backgroundColor: "#bab582" }
}

export default LogoAnimateVariants