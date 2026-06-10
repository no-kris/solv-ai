import type { JSX } from "react/jsx-runtime";
import { Editor } from "@monaco-editor/react";
import { useState } from "react";

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

function CodingBlock({ paramNames }: { paramNames: string[] }): JSX.Element {
  const [code, setCode] = useState<string>(() => buildSignature(paramNames));

  return (
    <div className="coding-block">
      <label className="coding-block-label">Your Solution</label>
      <Editor
        height="100%"
        language="python"
        value={code}
        onChange={(value) => setCode(value || "")}
        theme="light"
        className="monaco-editor"
      />
      <button className="run-tests-btn">Run Tests</button>
    </div>
  );
}

export default CodingBlock;
