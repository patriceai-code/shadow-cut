import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SHADOW CUT — Film Continuity Command Center",
  description: "Autonomous real-time film script supervisor powered by Gemini & IBM",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-bg-primary text-text-primary antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
