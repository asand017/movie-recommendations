"use client";

import MovieList from "@/components/MovieList";
import { getPopularMovies } from "@/utils/api";
import { useRouter } from "next/navigation";

const FavoritesPreferences = () => {
  const router = useRouter();


  return (
    <div className="flex flex-col justify-center items-center content-center overflow-auto">
      <div className="text-lg">What are some of your favorite movies?</div>
      <MovieList api={getPopularMovies}/>
      <button
        className="bg-blue-500 w-1/4 grow-0 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => {
          router.push("/preferences/genres");
        }}
      >
        next
      </button>
    </div>
  );
};

export default FavoritesPreferences;
