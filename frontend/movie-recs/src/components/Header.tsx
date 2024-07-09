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

  // TODO: add main navigation -> movies, about, recommendations dashboard, user settings, etc
  return (
    <header className={`bg-gray-800 text-white ${className} w-screen flex`}>
      <div className="z-10 absolute mx-auto p-2">
        <p
          onClick={() => router.push("/movies")}
          className={"text-center hover:cursor-pointer hover:font-extrabold"}
        >
          Movies
        </p>
      </div>
      <div className="grow-0 container mx-auto p-2 z-0">
        <p
          className="text-center hover:cursor-pointer"
          onClick={() => router.push("/")}
        >
          Movie Recs
        </p>
      </div>
      {isAuthenticated && (
        <div className="logout-container z-10 absolute right-0 px-2">
          <button
            className="bg-blue-500 hover:bg-blue-700 te
            xt-white font-bold py-2 px-4 rounded"
            onClick={() => logout()}
          >
            Logout
          </button>
        </div>
      )}
    </header>
  );
};

export default Header;
