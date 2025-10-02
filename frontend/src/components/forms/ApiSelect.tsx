"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';

interface SelectOption {
  id: number;
  name: string;
}

interface ApiSelectProps {
  endpoint: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  label: string;
  id: string;
}

const ApiSelect = ({ endpoint, value, onChange, label, id }: ApiSelectProps) => {
  const [options, setOptions] = useState<SelectOption[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const response = await axios.get(endpoint);
        setOptions(response.data);
      } catch (err) {
        setError(`Failed to load ${label.toLowerCase()}.`);
        console.error(`Error fetching from ${endpoint}:`, err);
      } finally {
        setLoading(false);
      }
    };
    fetchOptions();
  }, [endpoint, label]);

  return (
    <div className="mb-4">
      <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
        {label}
      </label>
      <select
        id={id}
        value={value}
        onChange={onChange}
        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        disabled={loading || error !== null}
        required
      >
        {loading && <option>Loading...</option>}
        {error && <option>{error}</option>}
        {!loading && !error && (
          <>
            <option value="" disabled>Select a {label.toLowerCase()}</option>
            {options.map((option) => (
              <option key={option.id} value={option.id}>
                {option.name}
              </option>
            ))}
          </>
        )}
      </select>
    </div>
  );
};

export default ApiSelect;