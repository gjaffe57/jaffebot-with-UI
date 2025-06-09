import React from "react";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header style={{ padding: "1rem", borderBottom: "1px solid #eee" }}>
        <h1 style={{ margin: 0, fontSize: 24 }}>JaffeBot Dashboard</h1>
      </header>
      <main style={{ flex: 1, padding: "2rem 1rem" }}>{children}</main>
      <footer style={{ padding: "1rem", borderTop: "1px solid #eee", textAlign: "center" }}>
        &copy; {new Date().getFullYear()} JaffeBot 3.0
      </footer>
    </div>
  );
} 