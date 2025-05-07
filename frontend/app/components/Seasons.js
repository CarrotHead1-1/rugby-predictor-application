"use client"

import React, { useEffect, useState } from 'react'
import Matches from './Match';

const Seasons = () => {

    const [seasons, setSeason] = useState([]);
    const [selectedSeason, setSelectedSeason] = useState(null);

    useEffect(() => {
        fetch('http://localhost:8000/seasons')
            .then((res) => res.json())
            .then((data) => {
                setSeason(data.seasons);
                if (data.seasons.length > 0) {
                    setSelectedSeason(data.seasons[data.seasons.length - 1]);
                }
            })
    }, [])

    return (
        <div className='w-full max-w-4xl mx-auto px-4 py-6'>

            <div className='flex flex-wrap gap-3 mb-6 border border-red-50 p-4'>
                {seasons.map((season, index) => (
                    <button
                        key={index}
                        onClick={() => setSelectedSeason(season)}
                        className={`px-3 py-1 rounded ${selectedSeason === season
                            ? "bg-blue-400 text-white"
                            : "bg-gray-200 text-black"}`}
                    >
                        {season}
                    </button>
                ))}
            </div>

            <div className='mt-4'>
                <Matches season={selectedSeason} />
            </div>
        </div>
    )


}

export default Seasons