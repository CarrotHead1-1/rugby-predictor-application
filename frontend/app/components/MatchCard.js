
"use client";

import React, { useEffect, useState } from "react";

const MatchCard = ({ match, elo }) => {
    const [prediction, setPrediction] = useState(null);

    useEffect(() => {
        if (!match) return;

        fetch(
            `http://localhost:8000/predictions?home=${match.HomeTeam}&away=${match.AwayTeam}&season=${match.Season}&round=${match.Round}`
        )
            .then((res) => res.json())
            .then((data) => setPrediction(data.prediction))
            .catch((err) => {
                console.error("Prediction fetch error:", err);
                setPrediction(null); // Handle the error case
            });
    }, [match]);

    const homeElo = elo?.homeElo ?? "N/A";
    const awayElo = elo?.awayElo ?? "N/A";
    const eloDiff = elo?.eloDiff ?? "N/A";

    return (
        <div className="w-full max-w-6xl p-5 mb-5 rounded-lg shadow-md flex flex-col gap-4">
            {/* Match Information */}
            <div className="absolute top-2 left-2 text-lg font-bold">
                {match.Round}
            </div>
            <div className="flex justify-between items-center">
                {/* Home Section */}
                <div className="text-center flex-1">
                    <div className="text-sm">
                        <p className="font-semibold">{match.HomeTeam}</p>
                        <p className="text-xs">Elo: {homeElo}</p>
                    </div>
                </div>

                {/* Score Section */}
                <div className="flex flex-col items-center justify-center gap-2 font-semibold text-lg">
                    <p className="text-2xl">
                        {match.HomeScore} : {match.AwayScore}
                    </p>
                    <p className="text-xs">Elo Diff: {eloDiff}</p>
                </div>

                {/* Away Section */}
                <div className="text-center flex-1">
                    <div className="text-sm">
                        <p className="font-semibold">{match.AwayTeam}</p>
                        <p className="text-xs">Elo: {awayElo}</p>
                    </div>
                </div>
            </div>

            {/* Prediction */}
            <div className="flex justify-center items-center mt-4">
                {prediction ? (
                    <div className="w-full max-w-xs bg-blue-100 p-4 rounded-lg shadow-lg text-center">
                        <p className="font-semibold text-lg">Model Prediction</p>
                        <p className="text-xl text-bold">{prediction[4]}</p>
                    </div>
                ) : (
                    <div className="w-full max-w-xs bg-gray-200 p-4 rounded-lg shadow-lg text-center">
                        <p className="font-semibold text-lg">Loading Prediction...</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MatchCard;
