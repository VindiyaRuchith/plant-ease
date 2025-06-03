"use client";

import React, { useEffect, useId, useRef, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "motion/react";
import { useOutsideClick } from "@/hooks/use-outside-click";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { CloseIcon } from "@/components/ui/Close-Icon";

export default function AuroraBackgroundDemo() {
  const [active, setActive] = useState<(typeof cards)[number] | boolean | null>(null);
  const id = useId();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setActive(false);
      }
    }

    if (active && typeof active === "object") {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [active]);

  useOutsideClick(ref, () => setActive(null));

  return (
    <AuroraBackground>
      <h1 className="text-4xl font-bold text-green-600 text-center mb-10">PLANT-EASE</h1>

      <AnimatePresence>
        {active && typeof active === "object" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/20 h-full w-full z-10"
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {active && typeof active === "object" ? (
          <div className="fixed inset-0 grid place-items-center z-[100]">
            <motion.button
              key={`button-${active.title}-${id}`}
              layout
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, transition: { duration: 0.05 } }}
              className="flex absolute top-2 right-2 lg:hidden items-center justify-center bg-white rounded-full h-6 w-6"
              onClick={() => setActive(null)}
            >
              <CloseIcon />
            </motion.button>
            <motion.div
              layoutId={`card-${active.title}-${id}`}
              ref={ref}
              className="w-full max-w-[500px] h-full md:h-fit md:max-h-[90%] flex flex-col bg-white dark:bg-neutral-900 sm:rounded-3xl overflow-hidden"
            >
              <motion.div layoutId={`image-${active.title}-${id}`}>
                <img
                  width={200}
                  height={200}
                  src="/cinnamon.jpg"
                  alt={active.title}
                  className="w-full h-80 lg:h-80 sm:rounded-tr-lg sm:rounded-tl-lg object-cover object-top"
                />
              </motion.div>

              <div>
                <div className="flex justify-between items-start p-4">
                  <div>
                    <motion.h3
                      layoutId={`title-${active.title}-${id}`}
                      className="font-medium text-neutral-700 dark:text-neutral-200 text-base"
                    >
                      {active.title}
                    </motion.h3>
                    <motion.p
                      layoutId={`description-${active.description}-${id}`}
                      className="text-neutral-600 dark:text-neutral-400 text-base"
                    >
                      {active.description}
                    </motion.p>
                  </div>

                  <motion.div
                    layout
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="px-4 py-3 text-sm rounded-full font-bold bg-green-500 text-white cursor-pointer"
                  >
                    <Link href={active.link}>{active.button}</Link>
                  </motion.div>
                </div>
                <div className="pt-4 relative px-4 pb-4">
                  <motion.div
                    layout
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="text-neutral-600 text-xs md:text-sm lg:text-base h-40 md:h-fit flex flex-col items-start gap-4 overflow-auto dark:text-neutral-400 [mask:linear-gradient(to_bottom,white,white,transparent)] [scrollbar-width:none] [-ms-overflow-style:none] [-webkit-overflow-scrolling:touch]"
                  >
                    {active.content}
                  </motion.div>
                </div>
              </div>
            </motion.div>
          </div>
        ) : null}
      </AnimatePresence>

      <ul className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
        {cards.map((card, index) => (
          <motion.div
            layoutId={`card-${card.title}-${id}`}
            key={card.title}
            onClick={() => setActive(card)}
            className="relative group bg-cover bg-center rounded-xl shadow-lg overflow-hidden cursor-pointer transition-transform duration-500 hover:scale-105"
            style={{ backgroundImage: `url("/cinnamon.jpg")` }}
          >
            <div className="absolute inset-0 bg-black/50 group-hover:bg-black/30 transition duration-500"></div>
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500">
              <div className="w-full h-full bg-gradient-to-tr from-blue-400/20 to-purple-400/20 blur-2xl"></div>
            </div>
            <div className="relative z-10 flex flex-col justify-center items-center h-full p-8 text-white text-center">
              <motion.h3 layoutId={`title-${card.title}-${id}`} className="text-2xl font-semibold mb-2 drop-shadow-lg">
                {card.title}
              </motion.h3>
              <motion.p layoutId={`description-${card.description}-${id}`} className="mb-2 drop-shadow-md">
                {card.description}
              </motion.p>
              <motion.div
                layout
                className="px-6 py-3 bg-blue-500 hover:bg-blue-700 rounded-full shadow-md text-white transition-all transform hover:scale-110 hover:shadow-lg"
              >
                {card.button}
              </motion.div>
            </div>
          </motion.div>
        ))}
      </ul>
    </AuroraBackground>
  );
}

const cards = [
  {
    title: "Scan Your Image",
    description: "Instantly check your cinnamon plant&apos;s health with AI-powered image scanning.",
    button: "Scan Now",
    link: "/scan",
    content: (
      <p>
        Upload a photo of your cinnamon plant leaf, and our advanced AI model will quickly analyze it to provide insights on potential diseases, along with a confidence score.
      </p>
    ),
  },
  {
    title: "About Us",
    description: "Learn more about how PLANT-EASE supports sustainable farming with cutting-edge technology.",
    button: "Learn More",
    link: "/about",
    content: (
      <p>
        PLANT-EASE is dedicated to helping farmers maintain healthy crops using AI-powered plant disease detection and clear explanations. Our mission is to support sustainable farming practices worldwide.
      </p>
    ),
  },
  {
    title: "Terms of Service",
    description: "Understand how we ensure responsible use and data protection in PLANT-EASE.",
    button: "Read Terms",
    link: "/terms",
    content: (
      <p>
        Review our terms of service to understand your rights, data privacy, and how we maintain a safe and reliable experience for all users of PLANT-EASE.
      </p>
    ),
  },
  {
    title: "Get Support",
    description: "Need help using the app? Check out our comprehensive guides and resources.",
    button: "View Help",
    link: "/howto",
    content: (
      <p>
        Explore our support section for tutorials, troubleshooting tips, and answers to common questions. We are here to help you get the most out of PLANT-EASE.
      </p>
    ),
  },
];
