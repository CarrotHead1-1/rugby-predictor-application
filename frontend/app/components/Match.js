"use client"
import React, { useEffect, useState } from 'react'

const Matches = ({ season }) => {
    const [matches, setMatches] = useState([]);
    const [elo, setElo] = useState([]);


    useEffect(() => {

        if (!season) return

        fetch(`http://localhost:8000/matches?season=${season}`)
            .then((res) => res.json().then((data) => setMatches(data.matches || [])))

        matches.forEach((match) => {
            fetch(`http://localhost:8000/elo/?home=${match.HomeTeam}&?away=${match.AwayTeam}
                &?season=${season}&?round=${match.Round}`)
                .then((res) => res.json())
                .then((eloData) => {
                    setElo(prev => ({
                        ...prev,
                        [`${match.HomeTeam}-${match.AwayTeam}-${match.Round}`]: eloData
                    }))
                })
        })
    }, [season]);

    return (
        <>
            <div className='grid grid-cols-1 md:grid-cols-3 items-center gap-4'>
                {matches.map((match, index) => (
                    <div key={index} className='flex items-center'>
                        <div className=''>
                            <p className='text-sm'> {match.HomeTeam} </p>
                        </div>
                        <div>
                            <p> {match.HomeScore} : {match.AwayScore} </p>
                        </div>
                        <div className=''>
                            <p className='text-sm'> {match.AwayTeam} </p>
                        </div>
                    </div>
                ))
                }
            </div>


        </>
    )
}

export default Matches


//
// return (
//     <div className='rid grid-cols-1 md:grid-cols-3 items-center gap-4'>
//         {matches.map((match, index) => (
//             <div key={index} className='p-4 rounded-xl shadow-md bg-white border'>
//                 <div className='w-full flex items-center'>

//                     <p className='text-sm'> {match.HomeTeam}</p>
//                 </div>
//                 <div className='px-2 m-auto flex justify-center items-center rounded-2xl'>
//                     <p className='py-1 text-textPrimary text-xs'> {match.HomeScore} : {match.AwayScore} </p>
//                 </div>
//                 <div className='w-full flex items-center justify-end'>
//                     <p className='text-sm text-right'> {match.AwayTeam} </p>

//                 </div>
//             </div>
//         ))}
//     </div>
// )