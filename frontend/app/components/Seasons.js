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
                    setSelectedSeason([data.seasons.length - 1]);
                }
            })
    }, [])

    return (
        <div>
            <h2 className='text-lg font-semibold mb-2'> Season: </h2>
            <div className='flex space-x-4 mb-2 md:mb-4'>
                {seasons.map((season, index) => (
                    <button
                        key={index}
                        onClick={() => setSelectedSeason(season)}
                        className={`px-3 py-1 rounded ${selectedSeason === season
                            ? "bg-blue-400 text-white"
                            : "bg-grey-200 text-black"}`}
                    >
                        {season}
                    </button>

                ))}
            </div>
            <div>
                <Matches season={selectedSeason} />
            </div>
        </div>
    )


}

export default Seasons