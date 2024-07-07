import axios from 'axios';

const BASE_URL = 'http://localhost:5001/api';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
});

export const login = async (formData: any) => {
  const response = await api.post('/login', formData);
  console.log(JSON.stringify(response.data));
  return response?.data;
};

export const register = async (username: string, password: string) => { // TODO: add register flow to login route
  const response = await api.post('/register', { username, password });
  return response?.data;
};

export const getConfiguration = async () => {
  const response = await api.get('/configuration');
  return response.data;
};

export const getTmdbMovies = async () => {
  const response = await api.get('/tmdb/movies');
  return response?.data;
};

export const searchTmdbMovies = async (query: string) => {
  const response = await api.get('/tmdb/search', {
    params: {
        "search": query
    }
  });
  return response?.data;
}

export const getMovies = async (page_number: number = 1, per_page: number = 10, search: string = "") => {
  console.log("fetching movies: ", page_number, per_page);
  const response = await api.get('/movies', {
    params: {
        "page": page_number,
        "per_page": per_page,
        "search": search
    }
  }).catch((error) => {
    console.log(error.toJSON());
  });
  return response?.data;
};

export const fetchProtectedData = async (token: string) => { // TODO: rating api/recommendation apis
  const response = await api.get('/protected', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response?.data;
};