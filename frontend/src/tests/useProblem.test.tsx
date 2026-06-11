// frontend/src/hooks/useProblem.test.ts

import { describe, it, expect } from "vitest";
import type { ProblemState } from "../types/types";
import { problemReducer, type ProblemAction } from "../hooks/useProblem";

const mockProblem = {
  isSet: true,
  description: "Test problem",
  paramNames: ["nums", "target"],
  examples: [
    {
      input: "nums = [1, 2], target = 3",
      output: "[0, 1]",
      explanation: "Test explanation",
    },
  ],
  tests: [
    {
      params: { nums: [1, 2], target: 3 },
      expectedOutput: "[0, 1]",
    },
  ],
};

const initialState: ProblemState = {
  content: {
    isSet: false,
    description: "",
    paramNames: [],
    examples: [],
    tests: [],
  },
  loading: false,
  hasError: false,
  errorMessage: "",
};

describe("problemReducer", () => {
  it("should handle LOADING action", () => {
    const action: ProblemAction = { type: "LOADING" };
    const newState = problemReducer(initialState, action);

    expect(newState.loading).toBe(true);
    expect(newState.hasError).toBe(false);
    expect(newState.errorMessage).toBe("");
  });

  it("should handle SUCCESS action", () => {
    const action: ProblemAction = {
      type: "SUCCESS",
      payload: mockProblem,
    };
    const newState = problemReducer(initialState, action);

    expect(newState.content).toEqual(mockProblem);
    expect(newState.loading).toBe(false);
    expect(newState.hasError).toBe(false);
    expect(newState.errorMessage).toBe("");
  });

  it("should handle ERROR action", () => {
    const errorMsg = "Failed to generate problem";
    const action: ProblemAction = {
      type: "ERROR",
      payload: errorMsg,
    };
    const newState = problemReducer(initialState, action);

    expect(newState.hasError).toBe(true);
    expect(newState.errorMessage).toBe(errorMsg);
    expect(newState.loading).toBe(false);
  });

  it("should handle RESET action", () => {
    const loadedState: ProblemState = {
      content: mockProblem,
      loading: false,
      hasError: false,
      errorMessage: "",
    };

    const action: ProblemAction = { type: "RESET" };
    const newState = problemReducer(loadedState, action);

    expect(newState).toEqual(initialState);
  });

  it("should preserve problem on ERROR action", () => {
    const stateWithProblem: ProblemState = {
      content: mockProblem,
      loading: false,
      hasError: false,
      errorMessage: "",
    };

    const action: ProblemAction = {
      type: "ERROR",
      payload: "New error",
    };
    const newState = problemReducer(stateWithProblem, action);

    expect(newState.content).toEqual(mockProblem);
    expect(newState.hasError).toBe(true);
  });
});
