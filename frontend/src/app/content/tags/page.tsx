"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';
import { MoreHorizontal, PlusCircle } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
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
import { columns, Tag } from './columns';
import { DataTable } from './data-table';

const TagsPage = () => {
  const [data, setData] = useState<Tag[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // State for the delete confirmation dialog
  const [isAlertOpen, setIsAlertOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/content/tags/');
      setData(response.data);
    } catch (err) {
      setError('Failed to fetch tags.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Opens the confirmation dialog
  const promptDelete = (id: number) => {
    setItemToDelete(id);
    setIsAlertOpen(true);
  };

  // Performs the deletion after confirmation
  const confirmDelete = async () => {
    if (itemToDelete === null) return;

    try {
      await axios.delete(`/api/content/tags/${itemToDelete}/`);
      fetchData(); // Refresh the list
    } catch (err) {
      setError('Failed to delete the tag.');
      console.error(err);
    } finally {
      setIsAlertOpen(false);
      setItemToDelete(null);
    }
  };

  const tableColumns = columns.map(col => {
      if (col.id === 'actions') {
          return {
              ...col,
              cell: ({ row }) => {
                  const tag = row.original
                  return (
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <span className="sr-only">Open menu</span>
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem
                          onClick={() => navigator.clipboard.writeText(String(tag.id))}
                        >
                          Copy Tag ID
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>
                            <Link href={`/content/tags/edit/${tag.id}`}>Edit</Link>
                        </DropdownMenuItem>
                        <DropdownMenuItem
                            onClick={() => promptDelete(tag.id)}
                            className="text-red-500"
                        >
                            Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  )
              }
          }
          return col
      }
  )

  if (loading) {
    return <div>Loading tags...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Tags</h1>
        <Button asChild>
          <Link href="/content/tags/new">
            <PlusCircle className="mr-2 h-4 w-4" />
            New Tag
          </Link>
        </Button>
      </div>

      <DataTable columns={tableColumns} data={data} />

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isAlertOpen} onOpenChange={setIsAlertOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure you want to delete this tag?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the tag.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setItemToDelete(null)}>
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

export default TagsPage;