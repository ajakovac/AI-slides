import { createContext, useContext, useEffect, useState } from "react";
import { apiFetch } from "../api/client";

const SystemContext = createContext(null);

export function SystemProvider({ children }) {
  const [system, setSystem] = useState(null);

  useEffect(() => {
    apiFetch("/system")
      .then(setSystem)
      .catch(console.error);
  }, []);

  return (
    <SystemContext.Provider value={system}>
      {children}
    </SystemContext.Provider>
  );
}

export function useSystem() {
  return useContext(SystemContext);
}
