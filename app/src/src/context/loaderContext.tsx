import { createContext, ReactNode, useContext, useState } from "react";
import { Loader } from "../ui/components/loader/Loader";

interface LoaderContextValues {
  isLoading: boolean;

  setIsLoading(isLoading: boolean): void;
}

const LoaderContext = createContext<LoaderContextValues>({
  isLoading: false,
  setIsLoading: () => {
    throw new Error("Not implemented");
  },
});

export function LoaderContextProvider({ children }: { children: ReactNode }) {
  const [ isLoading, setIsLoading ] = useState<boolean>(false);

  return (
    <LoaderContext.Provider value={ { isLoading, setIsLoading } }>
      <>
        { children }
        { isLoading && <Loader/> }
      </>
    </LoaderContext.Provider>
  );
}

export function useLoader() {
  return useContext(LoaderContext);
}

// TODO: Check if this context is necessary! If not, REMOVE it!
