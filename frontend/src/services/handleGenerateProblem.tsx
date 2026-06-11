import type { GenerateProblemProps } from "../types/types";

export const handleGenerateProblem = async ({
  dispatch,
  problemMetadata,
}: GenerateProblemProps) => {
  dispatch({ type: "RESET" });
  dispatch({ type: "LOADING" });

  try {
    const response = await fetch("http://127.0.0.1:8000/api/generate-problem", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category: problemMetadata.problemCategory,
        difficulty: problemMetadata.problemDifficulty,
      }),
    });

    const data = await response.json();

    if (!data.success) {
      dispatch({ type: "ERROR", payload: data.error });
      return;
    }

    dispatch({ type: "SUCCESS", payload: data.content });
  } catch (err) {
    dispatch({
      type: "ERROR",
      payload: err,
    });
  }
};
