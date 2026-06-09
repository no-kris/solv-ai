import { useState } from "react";

const problemCategories = [
  { name: "Arrays", id: 1, color: "#FF6B6B" }, // Red
  { name: "Hash Maps", id: 2, color: "#4ECDC4" }, // Teal
  { name: "Linked Lists", id: 3, color: "#FFD93D" }, // Yellow
  { name: "Trees", id: 4, color: "#A78BFA" }, // Purple
  { name: "Graphs", id: 5, color: "#34D399" }, // Green
];

const problemDifficulties = [
  { name: "Easy", id: 1, color: "#06B6D4" }, // Cyan
  { name: "Medium", id: 2, color: "#F97316" }, // Orange
  { name: "Hard", id: 3, color: "#EC4899" }, // Pink
];

function App() {
  const [problemCategory, setProblemCategory] = useState("Arrays");
  const [problemDifficulty, setProblemDifficulty] = useState("Easy");
  const [showApiKeyModal, setShowApiKeyModal] = useState(false);
  const [apiKey, setApiKey] = useState(() => {
    return sessionStorage.getItem("apiKey") || "";
  });
  const [codingProblem, setCodingProblem] = useState({
    isSet: true,
    description:
      "Given an array of integers, return the indecis of the two numbers that add up to a target sum.",
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

  const handleProblemCategoryChange = (category) => {
    setProblemCategory(category);
  };

  const handleProblemDifficultyChange = (difficulty) => {
    setProblemDifficulty(difficulty);
  };

  const handleApiKeyChange = (e) => {
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

function CodingBlock() {
  return (
    <div className="coding-block">
      <label className="coding-block-label">Your Solution</label>
      <textarea placeholder="Write your code here..." />
      <button className="run-tests-btn">Run Tests</button>
    </div>
  );
}

function ProblemBlock({ problem }) {
  return (
    <div className="problem">
      <h2>{problem.description}</h2>
      <div className="problem-examples">
        {problem.examples.map((item, idx) => {
          return (
            <div className="problem-example" key={idx}>
              <div className="problem-example-label">Example {idx + 1}</div>
              <div className="problem-example-label">Input:</div>
              <div className="problem-example-content">{item.input}</div>
              <div className="problem-example-label">Output:</div>
              <div className="problem-example-content">{item.output}</div>
              <div className="problem-example-explanation">
                {item.explanation}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function Modal({ onClose, children }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {children}
        <button className="modal-close" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
}

function List({ list, onChange }) {
  const handleClick = (item) => {
    onChange(item.name);
  };

  return (
    <>
      <ul className="list">
        {list.map((item) => {
          return (
            <Item item={item} key={item.id} onClick={() => handleClick(item)} />
          );
        })}
      </ul>
    </>
  );
}

function Item({ item, onClick }) {
  return (
    <button
      className="item-btn"
      style={{ backgroundColor: item.color }}
      onClick={onClick}
    >
      {item.name}
    </button>
  );
}

export default App;
