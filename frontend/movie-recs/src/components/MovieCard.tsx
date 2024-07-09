"use client";

import { useRouter } from "next/navigation";

interface Props {
  movie: {
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
  };
  tmdbConfig: any;
}

const MovieCard = ({ movie, tmdbConfig }: Props) => {
  const router = useRouter();

  // TODO: add logic that when clicking on movie, add to favorite movie list and save to context (if logged in, will write to db)
  return (
    <div className="w-auto px-2 mb-4">
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
  );
};

export default MovieCard;
