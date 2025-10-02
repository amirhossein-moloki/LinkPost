"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';

interface Platform {
  id: number;
  name: string;
}

const PlatformsPage = () => {
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPlatforms = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/content/platforms/');
      setPlatforms(response.data);
    } catch (err) {
      setError('Failed to fetch platforms.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlatforms();
  }, []);

  const handleDelete = async (platformId: number) => {
    if (confirm('Are you sure you want to delete this platform?')) {
      try {
        await axios.delete(`/api/content/platforms/${platformId}/`);
        fetchPlatforms(); // Refresh the list
      } catch (err) {
        setError('Failed to delete the platform.');
        console.error(err);
      }
    }
  };

  if (loading) {
    return <div>Loading platforms...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Platforms</h1>
        <Link href="/content/platforms/new" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          New Platform
        </Link>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border">
          <thead className="bg-gray-800 text-white">
            <tr>
              <th className="py-2 px-4 text-left">ID</th>
              <th className="py-2 px-4 text-left">Name</th>
              <th className="py-2 px-4 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {platforms.length > 0 ? (
              platforms.map((platform) => (
                <tr key={platform.id} className="border-t hover:bg-gray-100">
                  <td className="py-2 px-4">{platform.id}</td>
                  <td className="py-2 px-4">{platform.name}</td>
                  <td className="py-2 px-4">
                    <Link href={`/content/platforms/edit/${platform.id}`} className="text-blue-600 hover:underline mr-4">
                      Edit
                    </Link>
                    <button
                      onClick={() => handleDelete(platform.id)}
                      className="text-red-600 hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={3} className="py-4 px-4 text-center">No platforms found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PlatformsPage;