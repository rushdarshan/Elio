import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ELIO App Dashboard",
  description: "Evidence-gated catalog intelligence — live ops dashboard.",
};

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      {children}
    </div>
  );
}
