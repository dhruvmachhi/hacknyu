import type { Metadata } from "next";
import "./globals.css";
import { Lato } from 'next/font/google'

export const metadata: Metadata = {
  title: "HackNYU 2025",
  description: "Generate 3D printable models of glasses for your face.",
};

const lato = Lato({weight: "400", subsets: ["latin"]});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={lato.className}>
      <body>{children}</body>
    </html>
  );
}
