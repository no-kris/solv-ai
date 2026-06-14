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

    if (!response.ok) {
      let errorMessage = "Oops. The LLM had a hiccup.";
      try {
        await response.json();
      } catch {
        if (response.status === 400) {
          errorMessage += "Hmm, something about your request didn't compute.";
        } else if (response.status === 500) {
          errorMessage = "Server took a coffee break. Try again in a moment.";
        }
      }
      dispatch({ type: "ERROR", payload: errorMessage });
      return;
    }

    const data = await response.json();
    dispatch({ type: "SUCCESS", payload: data });
  } catch {
    const errorMessage =
      "Lost connection. Looks like you lost some data over the network.";
    dispatch({
      type: "ERROR",
      payload: errorMessage,
    });
  }
};
