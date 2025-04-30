import './global.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Rugby Prediction App',
  description: 'Description',
}

export default function RootLayout({
  children, }
  : {
    children: React.ReactNode
  }) {
  return (
    <html lang='eng'>
      <body className={inter.className} >
        <main className='px-2 md:px-16 md:py-2 text-textPrimary'>
          {/*nav bar */}
          <section className='flex space-x-4'>
            {/*side bar */}
            {children}
            {/* other */}

          </section>
        </main>
        {children}</body>
    </html>
  )
}
