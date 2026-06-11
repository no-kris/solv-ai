import type { Dispatch } from "react";
import type { ProblemAction } from "../hooks/useProblem";

/**
 * Represents a problem category or difficulty option
 */
export interface FilterOption {
  id: number;
  name: string;
  color: string;
}

/**
 * Represents a single example in a coding problem
 */
export interface ProblemExample {
  input: string;
  output: string;
  explanation: string;
}

/**
 * Represents a test case for a coding problem
 */
export interface TestCase {
  params: Record<string, unknown>;
  expectedOutput: string | number | boolean | unknown;
}

/**
 * Represents a complete coding problem
 */
export interface CodingProblem {
  isSet: boolean;
  description: string;
  paramNames: string[];
  examples: ProblemExample[];
  tests: TestCase[];
}

/**
 * Props for the ProblemBlock component
 */
export interface ProblemBlockProps {
  problem: CodingProblem;
}

/**
 * Props for the List component
 */
export interface ListProps {
  list: FilterOption[];
  onChange: (name: string) => void;
}

/**
 * Props for the Item component
 */
export interface ItemProps {
  item: FilterOption;
  onClick: () => void;
}

/**
 * Props for the Modal component
 */
export interface ModalProps {
  onClose: () => void;
  children: React.ReactNode;
}

/**
 * Interface for problem state.
 */
export type ProblemState = {
  content: CodingProblem;
  loading: boolean;
  hasError: boolean;
  errorMessage: string;
};

/**
 * Interface for generate problem handler.
 */
export interface GenerateProblemProps {
  dispatch: Dispatch<ProblemAction>;
  problemMetadata: Record<string, string>;
}
