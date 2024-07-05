"use client";

import { useRouter } from "next/navigation";
import { getConfiguration, getMovies } from "@/utils/api";
import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";

// if the first login, enter an initial preferences module to get preferences and should use to filter returned movies accordingly

const Movies = () => {
  const router = useRouter();
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [nextPage, setNextPage] = useState(2);
  const [previousPage, setPreviousPage] = useState(1);
  const [count_per_page, setCountPerPage] = useState(20);
  const [tmdbConfig, setTmdbConfig] = useState<any>({});
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

  const fetchConfiguration = async () => {
    try {
      const response = await getConfiguration();
      const data = await response;
      console.log("config: ", data);
      setTmdbConfig(data);
    } catch (error) {
      console.log("problem fetching config: ", error);
    }
  };

  const fetchMovies = async () => {
    try {
      const response = await getMovies(page, count_per_page);
      console.log("response: ", response);
      setTotalPages(response.pages);
      setMovies(response.data);
      setHasNext(response.has_next);
      setHasPrevious(response.has_prev);
      setNextPage(response.next_page);
      setPreviousPage(response.prev_page);
    } catch (error) {
      console.log("problem fetching movies: ", error);
    }
  };

  useEffect(() => {
    fetchConfiguration();
    fetchMovies();
  }, []);

  useEffect(() => {
      fetchMovies();
  }, [page, count_per_page]);

  useEffect(() => {
    console.log("fresh movies: ", movies);
  }),
    [movies];

  return (
    <div className="p-4 text-black overflow-auto flex flex-col justify-center space-y-3">
      <div className="flex flex-wrap justify-center">
        {movies.map((movie, index) => (
          <div key={index} className="w-auto px-2 mb-4">
            <div className="bg-gray-100 p-4 rounded-lg shadow-md">
              {tmdbConfig.images && tmdbConfig.images.base_url && (
                <div className="flex flex-col justify-center">
                  <img
                    src={`${tmdbConfig.images.base_url}w185${movie.poster_path}`}
                    alt={movie.title}
                    className="w-full h-64 object-cover mb-4"
                    width={185}
                  />
                  <button
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    onClick={() => router.push(`/movies/${movie.tmdb_id}`)}
                  >
                    View Details
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      <div className="page-buttons flex justify-center space-x-4 text-white">
        <button className={`${!hasPrevious ? "text-gray-500 " : ""}`} disabled={!hasPrevious} onClick={() => setPage(previousPage)}>Previous</button>
        <input type="number" value={page} onChange={(e) => setPage(parseInt(e.target.value))} className="text-black text-center w-10"/><span>/</span><div>{totalPages}</div>
        <button className={`${!hasNext ? "text-gray-500 " : ""}`} disabled={!hasNext} onClick={() => setPage(nextPage)}>Next</button>
      </div>
      <div className="per-page-selection-container flex justify-center space-x-4">
        <label htmlFor="per-page" className="text-white">per page</label>
        <select
          id="per-page"
          value={count_per_page}
          onChange={(e) => setCountPerPage(parseInt(e.target.value))}
        >
          <option value={20}>20</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
        </select>
      </div>
    </div>
  );
};

export default Movies;
