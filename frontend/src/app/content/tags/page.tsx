"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';

interface Tag {
  id: number;
  name: string;
}

const TagsPage = () => {
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTags = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/content/tags/');
      setTags(response.data);
    } catch (err) {
      setError('Failed to fetch tags.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTags();
  }, []);

  const handleDelete = async (tagId: number) => {
    if (confirm('Are you sure you want to delete this tag?')) {
      try {
        await axios.delete(`/api/content/tags/${tagId}/`);
        fetchTags(); // Refresh the list
      } catch (err) {
        setError('Failed to delete the tag.');
        console.error(err);
      }
    }
  };

  if (loading) {
    return <div>Loading tags...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Tags</h1>
        <Link href="/content/tags/new" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          New Tag
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
            {tags.length > 0 ? (
              tags.map((tag) => (
                <tr key={tag.id} className="border-t hover:bg-gray-100">
                  <td className="py-2 px-4">{tag.id}</td>
                  <td className="py-2 px-4">{tag.name}</td>
                  <td className="py-2 px-4">
                    <Link href={`/content/tags/edit/${tag.id}`} className="text-blue-600 hover:underline mr-4">
                      Edit
                    </Link>
                    <button
                      onClick={() => handleDelete(tag.id)}
                      className="text-red-600 hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={3} className="py-4 px-4 text-center">No tags found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TagsPage;