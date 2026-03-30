import React from "react";

export default function Sidebar({ keys = [], title = "Contents", onSelectKey }) {
  console.log(keys)
  return (
    <div className="sidebar-inner">
      <h2>{title}</h2>
      <div className="nav-list">
        {keys.map((entry) => {
          const [label, key] = Array.isArray(entry)
            ? [String(entry[0] ?? ""), String(entry[1] ?? "")]
            : [String(entry), String(entry)];

          return (
            <button
              key={key}
              className="nav-btn"
              onClick={() => onSelectKey(key)}
            >
              {label || key}
            </button>
          );
        })}
      </div>
    </div>
  );
}
