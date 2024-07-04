'use client';
 
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  return (
    <div className="flex flex-col justify-center p-4 h-full space-y-16">
      <div className="flex flex-col space-y-2 text-2xl">
        <h1 className="text-5xl">Don't know what to watch?</h1>
        <h2 className="text-4xl">Suffering from choice paraylsis?</h2>
        <h3 className="text-3xl">Let us give you some recs!</h3>
      </div>
      <div className="flex justify-center w-full space-x-2">
        <button className="p-1 bg-white w-36 rounded-lg text-black" type="button" onClick={() => router.push('/login')}>Login</button>
        <button className="p-1 bg-green-800 w-36 rounded-lg" type="button" onClick={() => router.push('/preferences')}>Get a quick rec</button>
      </div>
    </div>
  );
}
