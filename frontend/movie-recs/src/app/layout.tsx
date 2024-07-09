import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { AuthProvider } from '../context/AuthContext';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <title>Movie Recommendations</title>
      </head>
      <body className={`${inter.className} min-h-screen flex flex-col`}>
        <AuthProvider>
          <Header className="bg-gray-600 text-white p-1"/>
          <main className="flex-1 p-4 overflow-auto h-full w-full flex flex-col justify-center items-center content-center">
            {children}
          </main>
          <Footer className="bg-gray-600 text-white p-1"/>
        </AuthProvider>
      </body>
    </html>
  );
}
