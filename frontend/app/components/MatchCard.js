"use client"

import React, { useEffect, useState } from 'react'
import Matches from './Match'

const MatchCard = ({ match, elo }) => {
    const [prediction, SetPrediction] = useState(null)

    if (!match) return
    useEffect(() => {
        fetch(`http://localhost:8000/prediction?home=${match.HomeTeam}&away=${match.AwayTeam}
            &season=${match.Season}&round=${match.Round}`)
            .then((res) => res.json()
                .then((data) => SetPrediction(data.match)))
    }, [match])

    const homeElo = elo[match.HomeTeam]?.["HomeElo"] ?? "N/A";
    const awayElo = elo[match.AwayTeam]?.["AwayElo"] ?? "N/A";

    return (
        <div>
            <p> {match.HomeTeam} </p>
            <p> {homeElo} </p>
            <p> {match.HomeScore} : {match.AwayScore} </p>
            <p> {match.AwayTeam} </p>
            <p> {awayElo} </p>
        </div>
    )

}

export default MatchCard