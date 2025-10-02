"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';
import { PlusCircle } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { columns, Campaign } from './columns';
import { DataTable } from './data-table';

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // State for the delete confirmation dialog
  const [isAlertOpen, setIsAlertOpen] = useState(false);
  const [campaignToDelete, setCampaignToDelete] = useState<number | null>(null);

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

  // Opens the confirmation dialog
  const promptDelete = (campaignId: number) => {
    setCampaignToDelete(campaignId);
    setIsAlertOpen(true);
  };

  // Performs the deletion after confirmation
  const confirmDelete = async () => {
    if (campaignToDelete === null) return;

    try {
      await axios.delete(`/api/content/campaigns/${campaignToDelete}/`);
      fetchCampaigns(); // Refresh the list
    } catch (err) {
      setError('Failed to delete the campaign.');
      console.error(err);
    } finally {
      setIsAlertOpen(false);
      setCampaignToDelete(null);
    }
  };

  if (loading) {
    return <div>Loading campaigns...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Campaigns</h1>
        <Button asChild>
          <Link href="/content/campaigns/new">
            <PlusCircle className="mr-2 h-4 w-4" />
            New Campaign
          </Link>
        </Button>
      </div>

      <DataTable columns={columns} data={campaigns} deleteCampaign={promptDelete} />

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isAlertOpen} onOpenChange={setIsAlertOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the campaign
              and remove its data from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setCampaignToDelete(null)}>
              Cancel
            </AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete}>
              Continue
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default CampaignsPage;