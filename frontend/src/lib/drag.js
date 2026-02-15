export const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

export function startDrag(onMove, onEnd) {
  return (event) => {
    event.preventDefault();
    const handleMove = (e) => onMove(e);
    const handleUp = () => {
      window.removeEventListener("pointermove", handleMove);
      window.removeEventListener("pointerup", handleUp);
      onEnd?.();
    };
    window.addEventListener("pointermove", handleMove);
    window.addEventListener("pointerup", handleUp);
  };
}
