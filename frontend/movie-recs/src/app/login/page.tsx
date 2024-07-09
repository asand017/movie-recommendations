"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { login as apiLogin } from "@/utils/api";
import { useAuth } from '@/context/AuthContext';


const LoginPage = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const { login } = useAuth();
  const router = useRouter();

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await apiLogin(formData);
      console.log("fetching jwt token: ", response.access_token);
      login(response.access_token);
      router.push("/preferences");
      
    } catch (error) {
      console.error("Error logging in", error);
    }
  };

  useEffect(() => {
    if (localStorage.getItem("auth_token")) {
      router.push("/movies");
    }
  }, []);

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-lg h-96 mx-auto p-6 bg-white rounded-lg shadow-md text-black"
      autoComplete="off"
    >
      <h2 className="text-2xl font-bold mb-6 underline">Login</h2>
      <div className="mb-4">
        <label
          htmlFor="name"
          className="block text-gray-700 font-semibold mb-2"
        >
          Username:
        </label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Your username"
          autoComplete="off"
          required
        />
      </div>
      <div className="mb-4">
        <label
          htmlFor="password"
          className="block text-gray-700 font-semibold mb-2"
        >
          Password
        </label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Your password"
          autoComplete="off"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full bg-blue-500 text-white p-3 rounded-lg font-semibold shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
      >
        Login
      </button>
    </form>
  );
};

export default LoginPage;
