"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';

interface Campaign {
  id: number;
  name: string;
  description: string;
}

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCampaigns = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/content/campaigns/');
      setCampaigns(response.data);
    } catch (err) {
      setError('Failed to fetch campaigns.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const handleDelete = async (campaignId: number) => {
    if (confirm('Are you sure you want to delete this campaign?')) {
      try {
        await axios.delete(`/api/content/campaigns/${campaignId}/`);
        fetchCampaigns(); // Refresh the list
      } catch (err) {
        setError('Failed to delete the campaign.');
        console.error(err);
      }
    }
  };

  if (loading) {
    return <div>Loading campaigns...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Campaigns</h1>
        <Link href="/content/campaigns/new" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          New Campaign
        </Link>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border">
          <thead className="bg-gray-800 text-white">
            <tr>
              <th className="py-2 px-4 text-left">ID</th>
              <th className="py-2 px-4 text-left">Name</th>
              <th className="py-2 px-4 text-left">Description</th>
              <th className="py-2 px-4 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {campaigns.length > 0 ? (
              campaigns.map((campaign) => (
                <tr key={campaign.id} className="border-t hover:bg-gray-100">
                  <td className="py-2 px-4">{campaign.id}</td>
                  <td className="py-2 px-4">{campaign.name}</td>
                  <td className="py-2 px-4 truncate max-w-xs">{campaign.description}</td>
                  <td className="py-2 px-4">
                    <Link href={`/content/campaigns/edit/${campaign.id}`} className="text-blue-600 hover:underline mr-4">
                      Edit
                    </Link>
                    <button
                      onClick={() => handleDelete(campaign.id)}
                      className="text-red-600 hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="py-4 px-4 text-center">No campaigns found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CampaignsPage;