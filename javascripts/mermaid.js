import mermaid from "https://unpkg.com/mermaid@10/dist/mermaid.esm.min.mjs";

mermaid.initialize({ startOnLoad: false });

const elementCode = ".mermaid";

const loadMermaid = function () {
  const scheme = document.body.getAttribute("data-md-color-scheme");
  const theme = scheme === "slate" ? "dark" : "default";
  
  mermaid.initialize({ theme: theme });
  mermaid.run({
    querySelector: elementCode
  });
};

// Initialize on load
document.addEventListener("DOMContentLoaded", () => {
    // Check if there are any mermaid diagrams to render
    if (document.querySelector(elementCode)) {
        loadMermaid();
    }
});

// Re-render on instant navigation (if enabled)
// This handles the case where the page content changes via AJAX
if (typeof window !== "undefined") {
  window.document.addEventListener("DOMContentSwitch", () => {
     if (document.querySelector(elementCode)) {
        loadMermaid();
     }
  });
}
