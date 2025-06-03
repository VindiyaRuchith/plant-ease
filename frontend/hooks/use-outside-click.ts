import React, { useEffect } from "react";

export const useOutsideClick = (
  ref: React.RefObject<HTMLElement | null>, // 🟩 Note: explicitly allow `null`
  callback: (event: MouseEvent | TouchEvent) => void // 🟩 typed event
) => {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      // If ref is null or click is inside, do nothing
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return;
      }
      callback(event);
    };

    document.addEventListener("mousedown", listener);
    document.addEventListener("touchstart", listener);

    return () => {
      document.removeEventListener("mousedown", listener);
      document.removeEventListener("touchstart", listener);
    };
  }, [ref, callback]);
};
