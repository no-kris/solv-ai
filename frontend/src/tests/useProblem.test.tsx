import { describe, it, expect } from "vitest";
import type { ProblemState, TestCase, CodingProblem } from "../types/types";
import { problemReducer, type ProblemAction } from "../hooks/useProblem";

const genericTestProblem: CodingProblem = {
  isSet: true,
  description: "Test problem - Arrays",
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
      params: { nums: [1], target: 3 },
      expectedOutput: "[0, 1]",
    },
  ],
};

const linkedListTestProblem: CodingProblem = {
  isSet: true,
  description: "Test problem - Linked Lists",
  paramNames: ["head"],
  examples: [
    {
      input: "head = [1, 2, 3]",
      output: "[3, 2, 1]",
      explanation: "Reverse the linked list",
    },
  ],
  tests: [
    {
      head: { val: 1, next: { val: 2, next: { val: 3, next: null } } },
      expectedOutput: "[3, 2, 1]",
    },
  ],
};

const treeTestProblem: CodingProblem = {
  isSet: true,
  description: "Test problem - Trees",
  paramNames: ["root"],
  examples: [
    {
      input: "root = [3, 9, 20, null, null, 15, 7]",
      output: "3",
      explanation: "Tree height is 3",
    },
  ],
  tests: [
    {
      root: {
        val: 3,
        left: { val: 9, left: null, right: null },
        right: {
          val: 20,
          left: { val: 15, left: null, right: null },
          right: { val: 7, left: null, right: null },
        },
      },
      expectedOutput: "3",
    } as TestCase,
  ],
};

const graphTestProblem: CodingProblem = {
  isSet: true,
  description: "Test problem - Graphs",
  paramNames: ["edges", "start", "target"],
  examples: [
    {
      input: "edges = [[0,1], [1,2]], start = 0, target = 2",
      output: "true",
      explanation: "Path exists from 0 to 2",
    },
  ],
  tests: [
    {
      edges: { "0": [1], "1": [2], "2": [] },
      start: "0",
      target: "2",
      expectedOutput: "true",
    } as TestCase,
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

  it("should handle SUCCESS action with generic test cases", () => {
    const action: ProblemAction = {
      type: "SUCCESS",
      payload: genericTestProblem,
    };
    const newState = problemReducer(initialState, action);

    expect(newState.content).toEqual(genericTestProblem);
    expect(newState.loading).toBe(false);
    expect(newState.hasError).toBe(false);
    expect(newState.errorMessage).toBe("");
  });

  it("should handle SUCCESS action with linked list test cases", () => {
    const action: ProblemAction = {
      type: "SUCCESS",
      payload: linkedListTestProblem,
    };
    const newState = problemReducer(initialState, action);

    expect(newState.content).toEqual(linkedListTestProblem);
    expect(newState.content.tests[0]).toHaveProperty("head");
    expect(newState.loading).toBe(false);
  });

  it("should handle SUCCESS action with tree test cases", () => {
    const action: ProblemAction = {
      type: "SUCCESS",
      payload: treeTestProblem,
    };
    const newState = problemReducer(initialState, action);

    expect(newState.content).toEqual(treeTestProblem);
    expect(newState.content.tests[0]).toHaveProperty("root");
    expect(newState.loading).toBe(false);
  });

  it("should handle SUCCESS action with graph test cases", () => {
    const action: ProblemAction = {
      type: "SUCCESS",
      payload: graphTestProblem,
    };
    const newState = problemReducer(initialState, action);

    expect(newState.content).toEqual(graphTestProblem);
    expect(newState.content.tests[0]).toHaveProperty("edges");
    expect(newState.content.tests[0]).toHaveProperty("start");
    expect(newState.content.tests[0]).toHaveProperty("target");
    expect(newState.loading).toBe(false);
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
      content: genericTestProblem,
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
      content: genericTestProblem,
      loading: false,
      hasError: false,
      errorMessage: "",
    };

    const action: ProblemAction = {
      type: "ERROR",
      payload: "New error",
    };
    const newState = problemReducer(stateWithProblem, action);

    expect(newState.content).toEqual(genericTestProblem);
    expect(newState.hasError).toBe(true);
  });
});
