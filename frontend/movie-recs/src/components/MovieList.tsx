"use client";

import { getConfiguration, getTmdbMovies, searchTmdbMovies } from "@/utils/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import MovieCard from "./MovieCard";

interface Props {
  api: Function;
}

const MovieList = ({ api }: Props) => {
  const router = useRouter();
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
      vote_average: number;
      vote_count: number;
      poster_path: string;
    }[]
  >([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [tmdbConfig, setTmdbConfig] = useState<any>({});
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalResults, setTotalResults] = useState(0);

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
      const response = await api(page);
      console.log("response: ", response);
      setTotalPages(response.total_pages);
      setMovies(response.results);
      setTotalResults(response.total_results);
    } catch (error) {
      console.log("problem fetching movies: ", error);
    }
  };

  const searchMovies = async () => {
    try {
      const response = await searchTmdbMovies(searchTerm, page);
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
  }, [page]);

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
          <MovieCard key={index} movie={movie} tmdbConfig={tmdbConfig} />
        ))}
      </div>
      <div className="page-buttons flex justify-center space-x-4 text-white">
        <button
          className={`${
            !(page > 1) ? "text-gray-500 " : ""
          } hover:cursor-pointer`}
          disabled={page <= 1}
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
          className={`${
            !(page < totalPages) ? "text-gray-500 " : ""
          } hover:cursor-pointer`}
          disabled={page >= totalPages}
          onClick={() => {
            if (page < totalPages) setPage(page + 1);
          }}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default MovieList;
