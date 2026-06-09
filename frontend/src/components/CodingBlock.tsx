import type { JSX } from "react/jsx-runtime";

function CodingBlock(): JSX.Element {
  return (
    <div className="coding-block">
      <label className="coding-block-label">Your Solution</label>
      <textarea placeholder="Write your code here..." />
      <button className="run-tests-btn">Run Tests</button>
    </div>
  );
}

export default CodingBlock;
