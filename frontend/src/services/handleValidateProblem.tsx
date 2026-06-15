import type { ValidateProblemProps } from "../types/types";

const MAX_CODE_LENGTH = 2000;

export const handleValidateProblem = async ({
  code,
  problem,
  dispatch,
}: ValidateProblemProps) => {
  if (code.length > MAX_CODE_LENGTH) {
    dispatch({
      type: "ERROR",
      payload: `Your code is too long (${code.length}/${MAX_CODE_LENGTH} characters). Please simplify it.`,
    });
    return;
  }

  dispatch({ type: "RESET" });
  dispatch({ type: "LOADING" });
  try {
    const response = await fetch(import.meta.env.VITE_API_ROUTE_VALIDATE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code,
        tests: problem.tests,
        paramNames: problem.paramNames,
      }),
    });

    if (!response.ok) {
      let errorMessage = "Oops. The LLM had a hiccup.";
      try {
        await response.json();
      } catch {
        if (response.status === 400) {
          errorMessage +=
            "Your code has syntax errors or can't be parsed. Check your Python!.";
        } else if (response.status === 500) {
          errorMessage =
            "The validation server is having issues. Try again in a moment!";
        } else if (response.status === 408) {
          errorMessage =
            "Validation took too long. Your code might be stuck in an infinite loop!";
        }
      }
      dispatch({ type: "ERROR", payload: errorMessage });
      return;
    }

    const data = await response.json();
    dispatch({ type: "SUCCESS", payload: data });
  } catch {
    const errorMessage = "Can't reach the validation server.";
    dispatch({
      type: "ERROR",
      payload: errorMessage,
    });
  }
};
