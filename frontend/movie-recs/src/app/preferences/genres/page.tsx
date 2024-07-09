"use client";
import { useRouter } from "next/navigation";

const GenresPreferences = () => {
  const router = useRouter();
  return (
    <div className="flex flex-col justify-center items-center content-center">
      <div className="text-lg">What are your favorite genres?</div>
      <button
        className="bg-blue-500 w-1/4 grow-0 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => {
          router.push("/preferences/runtime");
        }}
      >
        next
      </button>
    </div>
  );
};

export default GenresPreferences;
