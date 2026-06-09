import type { JSX } from "react/jsx-runtime";
import type { ItemProps } from "../types/types";

function Item({ item, onClick }: ItemProps): JSX.Element {
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

export default Item;
