import { useReducer } from "react";

export type ValidationAction =
  | { type: "LOADING" }
  | { type: "SUCCESS"; payload: ValidationResult }
  | { type: "ERROR"; payload: string }
  | { type: "RESET" };

export type ValidationResult = {
  passed: number;
  total: number;
};

export type ValidationState = {
  loading: boolean;
  hasError: boolean;
  errorMessage: string;
  results: ValidationResult | null;
};

const initialState: ValidationState = {
  loading: false,
  hasError: false,
  errorMessage: "",
  results: null,
};

export const validationReducer = (
  state: ValidationState,
  action: ValidationAction,
): ValidationState => {
  switch (action.type) {
    case "LOADING":
      return { ...state, loading: true, hasError: false, errorMessage: "" };
    case "SUCCESS":
      return {
        ...state,
        loading: false,
        hasError: false,
        results: action.payload,
      };
    case "ERROR":
      return {
        ...state,
        loading: false,
        hasError: true,
        errorMessage: action.payload,
        results: null,
      };
    case "RESET":
      return initialState;
    default:
      return state;
  }
};

export const useValidation = () => {
  const [state, dispatch] = useReducer(validationReducer, initialState);
  return { state, dispatch };
};
