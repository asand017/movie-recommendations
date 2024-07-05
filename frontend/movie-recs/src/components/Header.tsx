"use client";

import { useAuth } from "@/context/AuthContext";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

const Header = ({ className = "" }: { className?: string }) => {
  const { isAuthenticated, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    console.log("header rendered");
    console.log("isAuthenticated: ", isAuthenticated);
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, []);

  return (
    <header className={`bg-gray-800 text-white ${className} w-screen flex`}>
      <div className="grow-0 container mx-auto p-2">
        <p className="text-center" onClick={() => router.push("/")}>Movie Recs</p>
      </div>
      {isAuthenticated && (
        <div className="logout-container ">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={() => logout()}>
            Logout
          </button>
        </div>
      )}
    </header>
  );
};

export default Header;
