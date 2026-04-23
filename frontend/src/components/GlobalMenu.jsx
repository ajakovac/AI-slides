import React, { useState } from "react";

const DEFAULT_THEME_OPTIONS = [
  { value: "pastel", label: "Pastel" },
  { value: "metal", label: "Metal" },
];

export default function GlobalMenu({
  theme,
  onThemeChange,
  themeOptions = DEFAULT_THEME_OPTIONS,
}) {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isThemeDropdownOpen, setIsThemeDropdownOpen] = useState(false);

  const toggleSettings = () => {
    setIsSettingsOpen(!isSettingsOpen);
    if (!isSettingsOpen) {
      setIsThemeDropdownOpen(false); // Close theme dropdown when closing settings
    }
  };

  const toggleThemeDropdown = () => {
    setIsThemeDropdownOpen(!isThemeDropdownOpen);
  };

  const selectTheme = (newTheme) => {
    onThemeChange?.(newTheme);
    setIsThemeDropdownOpen(false);
  };

  const currentThemeLabel = themeOptions.find(opt => opt.value === theme)?.label || theme;

  return (
    <nav className="global-menu" aria-label="Global application menu">
      <div className="menu-right">
        <button className="menu-icon" aria-label="File menu">
          📁
        </button>
        <div className="settings-container">
          <button
            className="menu-icon"
            onClick={toggleSettings}
            aria-label="Settings menu"
            aria-expanded={isSettingsOpen}
          >
            ⚙️
          </button>
          {isSettingsOpen && (
            <div className="settings-dropdown">
              <div className="theme-selector-custom">
                <span className="theme-label">Theme</span>
                <button
                  className="theme-current"
                  onClick={toggleThemeDropdown}
                  aria-expanded={isThemeDropdownOpen}
                >
                  {currentThemeLabel}
                  <span className="arrow">{isThemeDropdownOpen ? '▲' : '▶'}</span>
                </button>
                {isThemeDropdownOpen && (
                  <div className="theme-options">
                    {themeOptions.map((option) => (
                      <button
                        key={option.value}
                        className={`theme-option ${option.value === theme ? 'selected' : ''}`}
                        onClick={() => selectTheme(option.value)}
                      >
                        {option.value === theme && <span className="checkmark">✓</span>}
                        {option.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        <button className="menu-icon" aria-label="Search">
          🔍
        </button>
      </div>
    </nav>
  );
}