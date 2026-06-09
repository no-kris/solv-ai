import type { JSX } from "react/jsx-runtime";
import type { FilterOption, ListProps } from "../types/types";
import Item from "./Item";

function List({ list, onChange }: ListProps): JSX.Element {
  const handleClick = (item: FilterOption): void => {
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

export default List;
