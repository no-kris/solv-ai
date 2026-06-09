import type { JSX } from "react/jsx-runtime";
import type { ModalProps } from "../types/types";

function Modal({ onClose, children }: ModalProps): JSX.Element {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {children}
        <button className="modal-close" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
}

export default Modal;
