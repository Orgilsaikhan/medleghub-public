"use client"

import * as React from "react"
import { cn } from "cn"
import { Slider as SliderPrimitive } from "radix-ui"

/** Нэг бариултай слайдер. Бариулын a11y шинжийг (`aria-labelledby`, `aria-valuetext`) `thumbProps`-оор өгнө. */
function Slider({
  className,
  thumbProps,
  ...props
}: React.ComponentProps<typeof SliderPrimitive.Root> & {
  thumbProps?: React.ComponentProps<typeof SliderPrimitive.Thumb>
}) {
  return (
    <SliderPrimitive.Root
      data-slot="slider"
      className={cn(
        "relative flex w-full touch-none items-center select-none data-disabled:opacity-50",
        className
      )}
      {...props}
    >
      <SliderPrimitive.Track
        data-slot="slider-track"
        className="relative h-1.5 w-full grow overflow-hidden rounded-full bg-muted"
      >
        <SliderPrimitive.Range data-slot="slider-range" className="absolute h-full bg-primary" />
      </SliderPrimitive.Track>
      <SliderPrimitive.Thumb
        data-slot="slider-thumb"
        className="block size-5 shrink-0 cursor-grab rounded-full border-2 border-primary bg-background shadow-sm transition-[box-shadow] outline-none hover:ring-4 hover:ring-ring/30 focus-visible:ring-4 focus-visible:ring-ring/50 active:cursor-grabbing"
        {...thumbProps}
      />
    </SliderPrimitive.Root>
  )
}

export { Slider }
