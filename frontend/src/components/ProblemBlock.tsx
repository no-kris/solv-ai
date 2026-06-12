import type { ProblemProps } from "../types/types";

function ProblemBlock({ problem }: ProblemProps) {
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

export default ProblemBlock;
