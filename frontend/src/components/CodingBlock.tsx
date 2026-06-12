import type { JSX } from "react/jsx-runtime";
import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { useState } from "react";
import type { ProblemProps, NodeStructure } from "../types/types";

const buildNodeStructure = (node: NodeStructure): string => {
  const params = node.fields.map((f) => `${f.name}=${f.default}`).join(", ");

  const body = node.fields
    .map((f) => `\tself.${f.name} = ${f.name}`)
    .join("\n");

  return `class ${node.className}:
  def __init__(self, ${params}):
${body}`;
};

const buildSignature = (paramNames: string[]): string => {
  const params = paramNames.join(", ");
  return `# ============================================
# DO NOT modify the function signature below
# ============================================
def solution(${params}):
  # Write your code here
  pass
# ============================================`;
};

function CodingBlock({ problem }: ProblemProps): JSX.Element {
  const [code, setCode] = useState<string>(() => {
    const signature = buildSignature(problem.paramNames);
    if (problem.nodeStructure) {
      return buildNodeStructure(problem.nodeStructure) + "\n\n" + signature;
    }
    return signature;
  });

  return (
    <div className="coding-block">
      <label className="coding-block-label">Your Solution</label>
      <CodeMirror
        value={code}
        onChange={setCode}
        height="100%"
        extensions={[python()]}
        className="code-editor"
      />
      <button className="run-tests-btn">Run Tests</button>
    </div>
  );
}

export default CodingBlock;
