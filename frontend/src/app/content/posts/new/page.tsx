"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import toast from 'react-hot-toast';
import ApiSelect from '@/components/forms/ApiSelect';

const NewPostPage = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    body: '',
    campaign: '',
    platform: '',
    post_type: '',
    status: '',
  });
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { id, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const newPostData = {
      ...formData,
      campaign: Number(formData.campaign),
      platform: Number(formData.platform),
      post_type: Number(formData.post_type),
      status: Number(formData.status),
    };

    try {
      await axios.post('/api/content/posts/', newPostData);
      toast.success('Post created successfully!');
      router.push('/content');
    } catch (err) {
      toast.error('Failed to create post. Please check the form and try again.');
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Create New Post</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md">
        <div className="mb-4">
          <label htmlFor="title" className="block text-gray-700 font-bold mb-2">
            Title
          </label>
          <input
            type="text"
            id="title"
            value={formData.title}
            onChange={handleChange}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>

        <ApiSelect
          endpoint="/api/content/campaigns/"
          value={formData.campaign}
          onChange={handleChange}
          label="Campaign"
          id="campaign"
        />

        <ApiSelect
          endpoint="/api/content/platforms/"
          value={formData.platform}
          onChange={handleChange}
          label="Platform"
          id="platform"
        />

        <ApiSelect
          endpoint="/api/content/post-types/"
          value={formData.post_type}
          onChange={handleChange}
          label="Post Type"
          id="post_type"
        />

        <ApiSelect
          endpoint="/api/content/post-statuses/"
          value={formData.status}
          onChange={handleChange}
          label="Status"
          id="status"
        />

        <div className="mb-6">
          <label htmlFor="body" className="block text-gray-700 font-bold mb-2">
            Body
          </label>
          <textarea
            id="body"
            value={formData.body}
            onChange={handleChange}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-32"
            required
          />
        </div>

        <div className="flex items-center justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:bg-gray-400"
          >
            {isSubmitting ? 'Creating...' : 'Create Post'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewPostPage;