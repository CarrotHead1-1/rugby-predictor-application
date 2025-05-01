import React from 'react'
import Matches from './components/Match'
import Seasons from './components/Seasons'



export default async function Home() {

  return (
    <>
      <section className='px-2 md:px-4 md:w-[600px]'>
        <div className='flex justify-between items-center mb-4 md:md-2'>
          <h1 className='test-md md:text-xl font-bold'> Matches </h1>
          <div className='"px-4 py-0 md:py-1 bg-green-200 rounded-md test-testPrimary test-sm'>
            <p> Season : 23/34 </p>
          </div>
        </div>
        <Seasons />
      </section>
    </>
  )
}
