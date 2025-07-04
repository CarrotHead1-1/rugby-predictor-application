"use client"
import React from "react"

const EloGraph = () => {
    return (
        <div className='p-4'>
            <h1 className='text-2xl font-bold mb-4'> Elo Rating Graph </h1>
            <img
                src='http://localhost:8000/static/eloGraph.png'
                alt="elo rating graph of all teams"
                width="800"
                height="500"
                className='w-full max-w-4xl mx-auto border shadow-lg rounded'
            />

        </div>

    )
}

export default EloGraph