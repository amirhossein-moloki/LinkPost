"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';

// Interface for the Post data based on the Django model
interface Post {
  id: number;
  title: string;
  body: string;
  status: number; // Assuming we'll get the ID of the status
  platform: number; // Assuming we'll get the ID of the platform
  created_at: string;
  updated_at: string;
}

const ContentPage = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/content/posts/');
      setPosts(response.data);
    } catch (err) {
      setError('Failed to fetch posts. Make sure the backend server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handleDelete = async (postId: number) => {
    if (confirm('Are you sure you want to delete this post?')) {
      try {
        await axios.delete(`/api/content/posts/${postId}/`);
        // Refresh the posts list after deletion
        fetchPosts();
      } catch (err) {
        setError('Failed to delete the post.');
        console.error(err);
      }
    }
  };

  if (loading) {
    return <div>Loading posts...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Posts</h1>
        <Link href="/content/posts/new" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          New Post
        </Link>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border">
          <thead className="bg-gray-800 text-white">
            <tr>
              <th className="py-2 px-4 text-left">ID</th>
              <th className="py-2 px-4 text-left">Title</th>
              <th className="py-2 px-4 text-left">Created At</th>
              <th className="py-2 px-4 text-left">Updated At</th>
              <th className="py-2 px-4 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {posts.length > 0 ? (
              posts.map((post) => (
                <tr key={post.id} className="border-t hover:bg-gray-100">
                  <td className="py-2 px-4">{post.id}</td>
                  <td className="py-2 px-4">{post.title}</td>
                  <td className="py-2 px-4">{new Date(post.created_at).toLocaleString()}</td>
                  <td className="py-2 px-4">{new Date(post.updated_at).toLocaleString()}</td>
                  <td className="py-2 px-4">
                    <Link href={`/content/posts/edit/${post.id}`} className="text-blue-600 hover:underline mr-4">
                      Edit
                    </Link>
                    <button
                      onClick={() => handleDelete(post.id)}
                      className="text-red-600 hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="py-4 px-4 text-center">No posts found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ContentPage;