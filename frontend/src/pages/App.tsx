import { useState, type ChangeEvent, type JSX } from "react";
import type { CodingProblem, FilterOption } from "../types/types";
import List from "../components/List";
import Modal from "../components/Modal";
import ProblemBlock from "../components/ProblemBlock";
import CodingBlock from "../components/CodingBlock";

const problemCategories: FilterOption[] = [
  { id: 1, name: "Arrays", color: "#FF6B6B" },
  { id: 2, name: "Hash Maps", color: "#4ECDC4" },
  { id: 3, name: "Linked Lists", color: "#FFD93D" },
  { id: 4, name: "Trees", color: "#A78BFA" },
  { id: 5, name: "Graphs", color: "#34D399" },
];

const problemDifficulties: FilterOption[] = [
  { id: 1, name: "Easy", color: "#06B6D4" },
  { id: 2, name: "Medium", color: "#F97316" },
  { id: 3, name: "Hard", color: "#EC4899" },
];

function App() {
  const [problemCategory, setProblemCategory] = useState<string>("Arrays");
  const [problemDifficulty, setProblemDifficulty] = useState<string>("Easy");
  const [showApiKeyModal, setShowApiKeyModal] = useState<boolean>(false);
  const [apiKey, setApiKey] = useState<string>(() => {
    return sessionStorage.getItem("apiKey") || "";
  });
  const [codingProblem, setCodingProblem] = useState<CodingProblem>({
    isSet: true,
    description:
      "Given an array of integers, return the indices of the two numbers that add up to a target sum.",
    examples: [
      {
        input: "nums = [2, 7, 11, 15], target = 9",
        output: "[0, 1]",
        explanation: "nums[0] + nums[1] == 9, so we return [0, 1].",
      },
      {
        input: "nums = [3, 2, 4], target = 6",
        output: "[1, 2]",
        explanation: "nums[1] + nums[2] == 6, so we return [1, 2].",
      },
    ],
    tests: [
      {
        input: "[2, 7, 11, 15]",
        expectedOutput: "[0, 1]",
      },
      {
        input: "[3, 2, 4]",
        expectedOutput: "[1, 2]",
      },
      {
        input: "[3, 3]",
        expectedOutput: "[0, 1]",
      },
    ],
  });

  const handleProblemCategoryChange = (category: string): void => {
    setProblemCategory(category);
  };

  const handleProblemDifficultyChange = (difficulty: string): void => {
    setProblemDifficulty(difficulty);
  };

  const handleApiKeyChange = (e: ChangeEvent<HTMLInputElement>): void => {
    const key = e.target.value;
    setApiKey(key);
    sessionStorage.setItem("apiKey", key);
  };

  return (
    <div className="center-container">
      <h1 className="main-title">Solv.AI</h1>
      <span className="api-key">
        <button
          className="qstn-btn"
          onClick={() => setShowApiKeyModal(!showApiKeyModal)}
        >
          ?
        </button>
        {showApiKeyModal && (
          <Modal onClose={() => setShowApiKeyModal(false)}>
            <h2>Why Do You Need an API Key?</h2>
            <br />
            <p>
              This app uses large language models to generate coding problems
              dynamically. To generate problems, we need to call the LLM API,
              which requires your API key.
            </p>
            <br />
            <p>
              By providing your own API key, you maintain full control over your
              usage and costs. <strong>Your API key is never stored</strong>
              —it's only used to make the API call and then discarded when you
              leave the app.
            </p>
            <br />
            <p>
              <em>
                Note: You will have to re-enter the API key each time you visit
                the app.
              </em>
            </p>
          </Modal>
        )}
        API Key:
        <input
          type="text"
          placeholder="Paste API Key here..."
          value={apiKey}
          onChange={handleApiKeyChange}
        />
      </span>
      <div className="filters">
        <List list={problemCategories} onChange={handleProblemCategoryChange} />
        <List
          list={problemDifficulties}
          onChange={handleProblemDifficultyChange}
        />
      </div>
      <p className="info">
        Generating problem using ...
        <span className="filter-category-label">{problemCategory}</span>... with
        difficulty ...
        <span className="filter-difficulty-label">{problemDifficulty}</span>
        <button
          type="submit"
          className="item-btn generate-btn"
          disabled={!apiKey}
        >
          Generate
        </button>
      </p>

      {codingProblem.isSet && (
        <div className="problem-code-display">
          <ProblemBlock problem={codingProblem} />
          <CodingBlock />
        </div>
      )}
    </div>
  );
}

export default App;
