"use client"
import React, { useEffect, useState } from 'react'

const ModelPredictionCount = ({ }) => {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    fetch(`http://localhost:8000/modelCount`)
      .then(res => res.json())
      .then(data => setStats(data))
  }, [])

  if (!stats) {
    return (<div className='fixed top-24 right-4 bg-white border shadow-md rounded-lg px-4 py-3 text-sm'> Loading Prediction Stats </div>)
  }

  return (
    <div className='fixed top-24 right-4 bg-white border shadow-md rounded-lg px-4 py-3 text-sm'>
      <h2 className='text-base font-semibold mb-2'>Model Prediction Stats</h2>
      <div className='space-y-2'>
        <p><span className='font-medium'>Correct: </span> {stats.correctPredictions}</p>
        <p><span className='font-medium'>Incorrect: </span> {stats.incorrectPredictions}</p>
        <p><span className='font-medium'>Total Predictions: </span> {stats.totalPredictions}</p>
        <p><span className='font-medium'>Accuracy: </span> {stats.Accuracy} %</p>
        <p><span className='font-xs'>*Model Accuracy may not be a true reflection of Accuracy</span></p>
      </div>
    </div>
  )
}

export default ModelPredictionCount;
