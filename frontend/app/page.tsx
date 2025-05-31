'use client';

import {useEffect, useState} from 'react';

type Dog = {
  id: number;
  name: string;
  breed: string;
  location: string;
  distance: string;
  age: string;
  img_url: string;
  source_url: string;
};

export default function HomePage() {
  const [dog, setDog] = useState<Dog | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchDog = async (lat?: number, lon?: number): Promise<void> => {
    setLoading(true);
    try {
      const url = new URL('http://localhost:8000/dogs');
      url.searchParams.append('limit', '1');
      if (lat && lon) {
        url.searchParams.append('lat', lat.toString());
        url.searchParams.append('lon', lon.toString());
      }

      const res = await fetch(url.toString());
      const data: Dog[] = await res.json();
      if (data.length > 0) setDog(data[0]);
    } catch (err) {
      console.error('Error fetching dog:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const storedCoords = localStorage.getItem("coords");

    const loadDog = async () => {
      if (storedCoords) {
        const {lat, lon} = JSON.parse(storedCoords);
        await fetchDog(lat, lon);
      } else if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const {latitude, longitude} = position.coords;
            await fetchDog(latitude, longitude);
          },
          async (error) => {
            console.warn('Geolocation error:', error.message);
            await fetchDog();  // fallback
          }
        );
      } else {
        console.warn('Geolocation not available');
        await fetchDog(); // fallback
      }
    };
    
  void loadDog();
}, []);


return (
  <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-100 text-gray-800">
    <h1 className="text-4xl font-bold mb-8">🐶 DogRoulette</h1>

    {loading && <p className="text-lg">Loading a good doggo...</p>}

    {!loading && dog && (
      <div className="bg-white rounded-xl shadow-md p-6 max-w-sm w-full text-center">
        <h2 className="text-2xl font-semibold mb-4">{dog.name}</h2>
        <img
          src={dog.img_url}
          alt={dog.name}
          className="rounded-lg w-full mb-4"
        />
        <p className="mb-2"><strong>Breed:</strong> {dog.breed}</p>
        <p className="mb-2"><strong>Age:</strong> {dog.age}</p>
        <p className="mb-4"><strong>Location:</strong> {dog.location}</p>
        <p className="mb-4"><strong>Distance:</strong> {dog.distance} miles</p>
        <a
          href={dog.source_url}
          target="_blank"
          rel="noreferrer"
          className="mt-6 bg-amber-700 hover:bg-amber-600 text-white px-4 py-2 rounded transition mr-4"
        >
          🐾 Adopt me
        </a>
        <button
          onClick={() => fetchDog()}
          className="mt-6 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition"
        >
          Show Another Dog
        </button>
      </div>
    )}
  </main>
);
}
