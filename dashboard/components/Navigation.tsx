import Link from "next/link";

export default function Navigation() {
  return (
    <nav style={{ padding: "1rem 0", borderBottom: "1px solid #eee", marginBottom: 24 }}>
      <ul style={{ display: "flex", gap: 24, listStyle: "none", margin: 0, padding: 0 }}>
        <li><Link href="/">Home</Link></li>
        <li><Link href="/agents">Agents</Link></li>
        <li><Link href="/audits">Audits</Link></li>
        <li><Link href="/content">Content</Link></li>
        <li><Link href="/backlinks">Backlinks</Link></li>
        <li><Link href="/settings">Settings</Link></li>
      </ul>
    </nav>
  );
} 