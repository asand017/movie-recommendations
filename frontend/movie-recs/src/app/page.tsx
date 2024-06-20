'use client';
 
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  return (
    <div className="flex justify-center p-4 h-96">
      <h1 className="">Don't know what to watch?</h1>
      <h2>Suffering from choice paraylsis?</h2>
      <h3>Let us give you some recs!</h3>
      <div className="flex justify-center w-full space-x-2">
        <button className="p-3 bg-purple text-white" type="button" onClick={() => router.push('/login')}>Login</button>
      </div>
    </div>
  );
}
