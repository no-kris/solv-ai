import { useReducer } from "react";
import type { CodingProblem, ProblemState } from "../types/types";

export type ProblemAction =
  | { type: "LOADING" }
  | { type: "SUCCESS"; payload: CodingProblem }
  | { type: "ERROR"; payload: string }
  | { type: "RESET" };

const initialProblem: CodingProblem = {
  isSet: false,
  description: "",
  paramNames: [],
  examples: [],
  tests: [],
};

const initialState: ProblemState = {
  problem: initialProblem,
  loading: false,
  hasError: false,
  errorMessage: "",
};

export const problemReducer = (
  state: ProblemState,
  action: ProblemAction,
): ProblemState => {
  switch (action.type) {
    case "LOADING":
      return { ...state, loading: true, hasError: false, errorMessage: "" };
    case "SUCCESS":
      return {
        problem: action.payload,
        loading: false,
        hasError: false,
        errorMessage: "",
      };
    case "ERROR":
      return {
        ...state,
        loading: false,
        hasError: true,
        errorMessage: action.payload,
      };
    case "RESET":
      return initialState;
    default:
      return state;
  }
};

export const useProblem = () => {
  const [state, dispatch] = useReducer(problemReducer, initialState);

  return { state, dispatch };
};
