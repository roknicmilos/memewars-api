import React from "react";

export function CloseSVG({ color = "#480000" }) {
  return (
    <svg
      style={ { width: "100%", height: "100%" } }
      width="800px"
      height="800px"
      viewBox="0 0 1024 1024"
      xmlns="http://www.w3.org/2000/svg">
      <path
        fill={ color }
        d={
          `M764.288 214.592 512 466.88 259.712 214.592a31.936 31.936 0 0 0-45.12
           45.12L466.752 512 214.528 764.224a31.936 31.936 0 1 0 45.12 45.184L512
           557.184l252.288 252.288a31.936 31.936 0 0 0 45.12-45.12L557.12
           512.064l252.288-252.352a31.936 31.936 0 1 0-45.12-45.184z`
        }
      />
    </svg>
  );
}
