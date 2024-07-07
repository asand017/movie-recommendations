"use client";

import { useRouter } from "next/navigation";
import {
  getConfiguration,
  getMovies,
  getTmdbMovies,
  searchTmdbMovies,
} from "@/utils/api";
import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";

// if the first login, enter an initial preferences module to get preferences and should use to filter returned movies accordingly
// TODO: add search feature/api
const Movies = () => {
  const router = useRouter();
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [totalResults, setTotalResults] = useState(0);
  const [nextPage, setNextPage] = useState(2);
  const [previousPage, setPreviousPage] = useState(1);
  const [count_per_page, setCountPerPage] = useState(20);
  const [tmdbConfig, setTmdbConfig] = useState<any>({});
  const [searchTerm, setSearchTerm] = useState("");
  const [movies, setMovies] = useState<
    {
      adult: Boolean;
      overview: string;
      backdrop_path: string;
      id: Number;
      genre_ids: number[];
      original_language: string;
      original_title: string;
      popularity: number;
      release_date: string;
      title: string;
      video: Boolean;
      vote_average: string;
      vote_count: number;
      poster_path: string;
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
      const response = await getTmdbMovies(); //await getMovies(page, count_per_page, searchTerm);
      console.log("response: ", response);
      setTotalPages(response.total_pages);
      setMovies(response.results);
      setTotalResults(response.total_results);
      // setHasNext(response.has_next);
      // setHasPrevious(response.has_prev);
      // setNextPage(response.next_page);
      // setPreviousPage(response.prev_page);
    } catch (error) {
      console.log("problem fetching movies: ", error);
    }
  };

  const searchMovies = async () => {
    try {
      const response = await searchTmdbMovies(searchTerm);
      setTotalPages(response.total_pages);
      setMovies(response.results);
      setTotalResults(response.total_results);
    } catch (error) {
      console.log("problem fetching searched movies: ", error);
    }
  };

  useEffect(() => {
    fetchConfiguration();
    fetchMovies();
  }, []);

  useEffect(() => {
    fetchMovies();
  }, [page]); // [page, count_per_page]);

  useEffect(() => {
    if (searchTerm === "") {
      fetchMovies();
    } else {
      searchMovies();
    }
  }, [searchTerm]);

  useEffect(() => {
    console.log("fresh movies: ", movies);
  }),
    [movies];

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  // TODO: fix overflow issues, also fix layout/reload animations
  return (
    <div className="p-4 text-black overflow-auto flex flex-col justify-center space-y-3">
      <div className="mb-4 flex">
        <input
          type="text"
          placeholder="Search movies..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div className="flex flex-wrap justify-center overflow-auto">
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
                    onClick={() => router.push(`/movies/${movie.id}`)} // tmdb movie id
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
        <button
          className={`${!(page > 1) ? "text-gray-500 " : ""}`}
          disabled={!hasPrevious}
          onClick={() => {
            if (page > 1) setPage(page - 1);
          }}
        >
          Previous
        </button>
        <input
          type="number"
          value={page}
          onChange={(e) => setPage(parseInt(e.target.value))}
          className="text-black text-center w-10"
        />
        <span>/</span>
        <div>{totalPages}</div>
        <button
          className={`${!(page < totalPages) ? "text-gray-500 " : ""}`}
          disabled={!hasNext}
          onClick={() => {
            if (page < totalPages) setPage(page + 1);
          }}
        >
          Next
        </button>
      </div>
      {/* <div className="per-page-selection-container flex justify-center space-x-4">
        <label htmlFor="per-page" className="text-white">
          per page
        </label>
        <select
          id="per-page"
          value={count_per_page}
          onChange={(e) => setCountPerPage(parseInt(e.target.value))}
        >
          <option value={20}>20</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
        </select>
      </div> */}
    </div>
  );
};

export default Movies;
