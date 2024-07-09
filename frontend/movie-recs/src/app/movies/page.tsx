"use client";

import {
  getTmdbMovies,
} from "@/utils/api";
import MovieList from "@/components/MovieList";

// if the first login, enter an initial preferences module to get preferences and should use to filter returned movies accordingly
const Movies = () => {
  return (
    <>
      <MovieList api={getTmdbMovies}/>
    </>
  );
};

export default Movies;
