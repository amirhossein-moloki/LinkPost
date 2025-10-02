"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import axios from "axios"
import { PlusCircle } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { columns, Tag } from "./columns"
import { DataTable } from "./data-table"

const TagsPage = () => {
  const [data, setData] = useState<Tag[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const [isAlertOpen, setIsAlertOpen] = useState(false)
  const [itemToDelete, setItemToDelete] = useState<number | null>(null)

  const fetchData = async () => {
    setLoading(true)
    try {
      const response = await axios.get("/api/content/tags/")
      setData(response.data)
    } catch (err) {
      setError("Failed to fetch tags.")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const promptDelete = (id: number) => {
    setItemToDelete(id)
    setIsAlertOpen(true)
  }

  const confirmDelete = async () => {
    if (itemToDelete === null) return

    try {
      await axios.delete(`/api/content/tags/${itemToDelete}/`)
      fetchData()
    } catch (err) {
      setError("Failed to delete the tag.")
      console.error(err)
    } finally {
      setIsAlertOpen(false)
      setItemToDelete(null)
    }
  }

  if (loading) {
    return <div>Loading tags...</div>
  }

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  return (
    <div className="container mx-auto py-10">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Manage Tags</h1>
        <Button asChild>
          <Link href="/content/tags/new">
            <PlusCircle className="mr-2 h-4 w-4" />
            New Tag
          </Link>
        </Button>
      </div>

      <DataTable
        columns={columns}
        data={data}
        onDelete={(tag) => promptDelete(tag.id)}
      />

      <AlertDialog open={isAlertOpen} onOpenChange={setIsAlertOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>
              Are you sure you want to delete this tag?
            </AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the tag.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setItemToDelete(null)}>
              Cancel
            </AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete}>Continue</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

export default TagsPage
