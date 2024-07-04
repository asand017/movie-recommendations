"use client";

import { useRouter } from "next/navigation";
import { getMovies } from "@/utils/api";
import { useEffect, useState } from "react";
import { useAuth } from '@/context/AuthContext';

// if the first login, enter an initial preferences module to get preferences and should use to filter returned movies accordingly

const Movies = () => {
  const router = useRouter();
  const [page, setPage] = useState(1);
  const [count_per_page, setCountPerPage] = useState(10);
  const [movies, setMovies] = useState<
    {
      title: string;
      description: string;
      backdrop_path: string;
      imdb_id: string;
      directors: string[];
      genre: string;
      id: number;
      imdb_rating: number;
      imdb_votes: number;
      poster_path: string;
      review: string;
      runtime: number;
      tmdb_id: number;
      year: number;
    }[]
  >([]);
  const { isAuthenticated, logout } = useAuth();

  const fetchMovies = async () => {
    try {
      const response = await getMovies(page, count_per_page);
      const data = await response.data;
      setMovies(data);
    } catch (error) {
      console.log("problem fetching movies: ", error);
    }
  };

  useEffect(() => {
    fetchMovies();
  }, []);

  // useEffect(() => {
  //     fetchMovies();
  // }, [page, count_per_page]);

  useEffect(() => {
    console.log("fresh movies: ", movies);
  }),
    [movies];

  return (
    // <div className="text-lg">Movies</div>
    <div className="p-4 text-black overflow-auto h-full">
      <div className="flex flex-wrap -mx-2">
        {movies.map((movie, index) => (
          <div key={index} className="w-1/5 px-2 mb-4">
            <div className="bg-gray-100 p-4 rounded-lg shadow-md">
              <h3 className="text-lg font-bold mb-2">{movie.title}</h3>
              <p>{movie.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Movies;
