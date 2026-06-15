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
        param_names: problem.paramNames,
      }),
    });

    if (!response.ok) {
      let errorMessage = "Validation failed";
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        // If response isn't valid JSON, use a generic message
        errorMessage = `Validation failed (Status: ${response.status})`;
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
