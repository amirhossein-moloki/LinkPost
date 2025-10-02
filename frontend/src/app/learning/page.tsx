"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';

interface Topic {
  id: number;
  title: string;
  description: string;
}

const LearningPage = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await axios.get('/api/learning/topics/');
        setTopics(response.data);
      } catch (err) {
        setError('Failed to fetch topics.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTopics();
  }, []);

  if (loading) {
    return <div>Loading topics...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Learning Topics</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {topics.length > 0 ? (
          topics.map((topic) => (
            <Link key={topic.id} href={`/learning/topics/${topic.id}`} className="block p-6 bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100">
              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">{topic.title}</h5>
              <p className="font-normal text-gray-700">{topic.description}</p>
            </Link>
          ))
        ) : (
          <p>No topics found.</p>
        )}
      </div>
    </div>
  );
};

export default LearningPage;