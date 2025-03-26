"use client";
import { cn } from "@/lib/utils";
import React, { ReactNode } from "react";

interface AuroraBackgroundProps extends React.HTMLProps<HTMLDivElement> {
  children: ReactNode;
  showRadialGradient?: boolean;
}

export const AuroraBackground = ({
  className,
  children,
  showRadialGradient = true,
  ...props
}: AuroraBackgroundProps) => {
  return (
    <div
      className={cn(
        "relative flex flex-col min-h-screen items-center justify-center bg-black text-slate-50 transition-bg overflow-hidden",
        className
      )}
      {...props}
    >
      {/* Aurora Blur Layer */}
      <div className="absolute inset-0 z-0 overflow-hidden">
        <div
          className={cn(
            `
            [--aurora:repeating-linear-gradient(100deg,var(--blue-900)_10%,var(--blue-700)_20%,var(--blue-500)_30%,var(--blue-400)_40%,var(--blue-300)_50%)]
            [background-image:var(--aurora)]
            [background-size:300%,_200%]
            [background-position:50%_50%,50%_50%]
            filter blur-[20px] opacity-80
            after:content-[""] after:absolute after:inset-0 after:[background-image:var(--aurora)] 
            after:[background-size:200%,_100%] 
            after:animate-aurora after:[background-attachment:fixed] after:mix-blend-screen
            pointer-events-none absolute inset-0 opacity-50 will-change-transform`,

            showRadialGradient &&
              `[mask-image:radial-gradient(ellipse_at_50%_50%,black_10%,var(--transparent)_80%)]`
          )}
        />
      </div>

      {/* Main Content */}
      <div className="z-10 w-full">{children}</div>
    </div>
  );
};
