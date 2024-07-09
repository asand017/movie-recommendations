'use client';
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

const Preferences = () => {
    const router = useRouter();
    const { isAuthenticated } = useAuth();

    return(
        <div className="flex flex-col justify-center items-center content-center space-y-2">
            <h1>We need a some starting data to start recommending you movies</h1>
            <button className="bg-blue-500 w-1/4 grow-0 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={() => router.push("/preferences/favorites")}>get started</button>
        </div>
    );
}

export default Preferences;