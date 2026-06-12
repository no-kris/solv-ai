import { useState } from "react";
import type { FilterOption } from "../types/types";
import List from "../components/List";
import ProblemBlock from "../components/ProblemBlock";
import CodingBlock from "../components/CodingBlock";
import { useProblem } from "../hooks/useProblem";
import { handleGenerateProblem } from "../services/handleGenerateProblem";

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
  const { state: problemState, dispatch } = useProblem();

  const handleGenerateProblemClick = () => {
    handleGenerateProblem({
      dispatch,
      problemMetadata: {
        problemCategory,
        problemDifficulty,
      },
    });
  };
  const handleProblemCategoryChange = (category: string): void => {
    setProblemCategory(category);
  };

  const handleProblemDifficultyChange = (difficulty: string): void => {
    setProblemDifficulty(difficulty);
  };

  return (
    <div className="center-container">
      <h1 className="main-title">Solv.AI</h1>

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
          onClick={handleGenerateProblemClick}
        >
          {problemState.loading ? "Generating..." : "Generate"}
        </button>
      </p>

      {problemState.hasError && (
        <div className="problem-error-message">{problemState.errorMessage}</div>
      )}

      {problemState.content.isSet && (
        <div className="problem-code-display">
          <ProblemBlock problem={problemState.content} />
          <CodingBlock problem={problemState.content} />
        </div>
      )}
    </div>
  );
}

export default App;
