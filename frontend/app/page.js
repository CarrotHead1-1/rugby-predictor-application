import React from 'react'
import Matches from './components/Match'
import Seasons from './components/Seasons'
import ModelPredictionCount from './components/predictionCountCard'
import ModelReportCard from './components/modelReportCard'

export default async function Home() {

  return (

    <section className='px-4 md:px-6 max-w-4xl mx-auto py-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='test-md md:text-xl font-bold'> Matches </h1>
        <div className='"px-4 py-0 md:py-1 bg-green-200 rounded-md font-medium'>

        </div>
      </div>
      <Seasons />
      <div className='mt-6'>
        <ModelPredictionCount />
        <ModelReportCard />
      </div>
    </section >

  )
}
