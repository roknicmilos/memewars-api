import { useState, useEffect, RefObject } from 'react';

export const useVisible = (
  ref: RefObject<HTMLDivElement>,
  options = {
    root: null,
    rootMargin: "10px",
    threshold: 1.0,
  }
) => {
  const [isVisible, setIsVisible] = useState<boolean>(false);

  useEffect(() => {
    const { current: elementRef } = ref;

    if (elementRef) {
      const observer = new IntersectionObserver(
        ([entry]) => setIsVisible(entry.isIntersecting),
        options
      );

      observer.observe(elementRef);

      return () => observer.unobserve(elementRef);
    }
  }, [ref, options]);

  return isVisible;
};
