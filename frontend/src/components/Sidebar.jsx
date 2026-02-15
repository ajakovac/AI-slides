import React from "react";

export default function Sidebar({ keys = [], onSelectKey }) {
  return (
    <div className="sidebar-inner">
      <h2>Sidebar</h2>
      <div className="nav-list">
        {keys.map((k) => (
          <button key={k} className="nav-btn" onClick={() => onSelectKey(k)}>
            {k}
          </button>
        ))}
      </div>
    </div>
  );
}
