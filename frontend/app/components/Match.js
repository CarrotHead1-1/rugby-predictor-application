
"use client"

import React, { useEffect, useState } from 'react'
import MatchCard from './MatchCard';

const Matches = ({ season }) => {
    const [matches, setMatches] = useState([]);
    const [elo, setElo] = useState({}); // Ensure elo is an object with keys

    useEffect(() => {
        if (!season) return;

        fetch(`http://localhost:8000/matches?season=${season}`)
            .then(res => res.json())
            .then(data => {
                const fetchedMatches = data.matches || [];
                setMatches(fetchedMatches);
                console.log('Fetched Matches', fetchedMatches);

                fetchedMatches.forEach(match => {
                    fetch(`http://localhost:8000/elo?home=${match.HomeTeam}&away=${match.AwayTeam}&season=${season}&round=${match.Round}`)
                        .then(res => res.json())
                        .then(eloData => {
                            setElo(prev => ({
                                ...prev,
                                [`${match.HomeTeam}-${match.AwayTeam}-${match.Round}`]: eloData
                            }));
                        });
                });
            });
    }, [season]);

    return (

        <div className='w-full max-w-4xl mx-auto px-4 py-6 space-y-4'>
            {matches.length === 0 ? (
                <p className='text-center'> No available matches for this season</p>
            ) : (
                matches.map((match) => {
                    const matchKey = `${match.HomeTeam}-${match.AwayTeam}-${match.Round}`;
                    const matchElo = elo[matchKey];

                    return (
                        <MatchCard
                            key={matchKey}
                            match={match}
                            elo={matchElo}
                        />
                    );
                })
            )}
        </div>

    );
}

export default Matches;
