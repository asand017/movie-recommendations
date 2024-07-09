"use client";

import { useRouter } from "next/navigation";

const RuntimePreferences = () => {
  const router = useRouter();

  const processPreferences = () => { // send initial preferences to get initial recs back from server
    router.push("/recommendations");
  };

  return (
    <div className="flex flex-col justify-center items-center content-center">
      <div className="text-lg">What is your ideal movie runtime?</div>
      <button
        className="bg-blue-500 w-1/4 grow-0 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => {
          processPreferences();
        }}
      >
        next
      </button>
    </div>
  );
};

export default RuntimePreferences;
