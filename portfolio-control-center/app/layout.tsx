import type { Metadata } from "next";
import "./globals.css";

const title = "AI Product Portfolio Control Center";
const description = "A governed portfolio workspace for project evidence, lifecycle gates and balanced KPI results across 18 AI products.";

export const metadata: Metadata = {
  title,
  description,
  openGraph: { title, description, images: [{ url: "/og.jpg", width: 1200, height: 630, alt: title }] },
  twitter: { card: "summary_large_image", title, description, images: ["/og.jpg"] },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en"><body>{children}</body></html>
  );
}
