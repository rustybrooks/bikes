import React from 'react';
import { Frameworks } from '../framework_client';

export type FrameworkContextType = {
  frameworks: null | Frameworks;
  setFramework: (data: FrameworkContextType) => void;
};

export const FrameworkContext = React.createContext<FrameworkContextType>({
  frameworks: null,
  setFramework: (_data: FrameworkContextType) => {},
});
