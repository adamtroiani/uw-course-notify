import React, { createContext, useContext, useMemo } from "react";

export type GlobalContextValue = {
  apiHost: string;
  token: string | null;
};

const GlobalContext = createContext<GlobalContextValue | undefined>(undefined);

type GlobalProviderProps = {
  value: GlobalContextValue;
  children: React.ReactNode;
};

export function GlobalProvider({ value, children }: GlobalProviderProps) {
  // Memoize so consumers don't re-render if the fields are unchanged
  const memoValue = useMemo(() => value, [value.apiHost, value.token]);

  return (
    <GlobalContext.Provider value={memoValue}>
      {children}
    </GlobalContext.Provider>
  );
}

export function useGlobalContext(): GlobalContextValue {
  const ctx = useContext(GlobalContext);
  if (!ctx) {
    throw new Error("useGlobalContext must be used within <GlobalProvider>");
  }
  return ctx;
}

export default GlobalContext;
