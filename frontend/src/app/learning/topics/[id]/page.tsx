"use client";

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import axios from 'axios';

interface Topic {
  id: number;
  title: string;
  description: string;
}

interface Chapter {
  id: number;
  title: string;
  content: string;
  topic: number;
}

const TopicDetailPage = () => {
  const params = useParams();
  const { id } = params;

  const [topic, setTopic] = useState<Topic | null>(null);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      const fetchData = async () => {
        try {
          const topicResponse = axios.get(`/api/learning/topics/${id}/`);
          const chaptersResponse = axios.get(`/api/learning/chapters/?topic=${id}`);

          const [topicResult, chaptersResult] = await Promise.all([topicResponse, chaptersResponse]);

          setTopic(topicResult.data);
          setChapters(chaptersResult.data);
        } catch (err) {
          setError('Failed to fetch topic details.');
          console.error(err);
        } finally {
          setLoading(false);
        }
      };
      fetchData();
    }
  }, [id]);

  if (loading) {
    return <div>Loading topic details...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  if (!topic) {
    return <div>Topic not found.</div>;
  }

  return (
    <div>
      <h1 className="text-4xl font-bold mb-2">{topic.title}</h1>
      <p className="text-lg text-gray-600 mb-8">{topic.description}</p>

      <h2 className="text-2xl font-semibold mb-4">Chapters</h2>
      <div className="space-y-4">
        {chapters.length > 0 ? (
          chapters.map((chapter) => (
            <div key={chapter.id} className="p-4 bg-white rounded-lg border border-gray-200 shadow-sm">
              <h3 className="font-bold text-xl">{chapter.title}</h3>
              {/* This will eventually link to a lesson page */}
              {/* <Link href={`/learning/chapters/${chapter.id}`}>View Lessons</Link> */}
            </div>
          ))
        ) : (
          <p>No chapters found for this topic.</p>
        )}
      </div>
    </div>
  );
};

export default TopicDetailPage;