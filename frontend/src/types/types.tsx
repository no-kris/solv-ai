import type { Dispatch } from "react";
import type { ProblemAction } from "../hooks/useProblem";
import type { ValidationAction } from "../hooks/useValidation";

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
export interface GenericTestCase {
  params: Record<string, unknown | string | number>;
  expectedOutput: string | number | boolean | unknown;
}

export interface LinkedListTestCase {
  head: Record<string, unknown> | null;
  expectedOutput: string | number | boolean | unknown;
}

export interface TreeTestCase {
  root: Record<string, unknown> | null;
  expectedOutput: string | number | boolean | unknown;
}

export interface GraphTestCase {
  edges: Record<string, number[]>;
  start: string;
  target: string;
  expectedOutput: string | number | boolean | unknown;
}

export type TestCase =
  | GenericTestCase
  | LinkedListTestCase
  | TreeTestCase
  | GraphTestCase;

/**
 * Represents a node data structure
 */
type NodeField = { name: string; default: string };
export type NodeStructure = { className: string; fields: NodeField[] };

/**
 * Represents a complete coding problem
 */
export interface CodingProblem {
  isSet: boolean;
  description: string;
  paramNames: string[];
  examples: ProblemExample[];
  tests: TestCase[];
  nodeStructure?: NodeStructure;
}

/**
 * Props for the ProblemBlock component
 */
export interface ProblemProps {
  problem: CodingProblem;
  onValidateProblem?: (code: string, problem: CodingProblem) => Promise<void>;
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

export interface ValidateProblemProps {
  code: string;
  problem: CodingProblem;
  dispatch: Dispatch<ValidationAction>;
}
