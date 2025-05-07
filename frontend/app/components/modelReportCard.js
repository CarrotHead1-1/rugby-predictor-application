
"use client"
import React, { useEffect, useState } from 'react'

const ModelReportCard = ({ }) => {

    const [report, setReport] = useState(null)

    useEffect(() => {
        fetch(`http://localhost:8000/modelReport`)
            .then(res => res.json())
            .then(data => setReport(data))
    }, [])

    if (!report) {
        return (<div className='fixed top-60 right-4 bg-white border shadow-md rounded-lg px-4 py-3 text-sm'> Loading Model Report</div>)
    }
    return (
        <div className='fixed top-75 right-8 bg-white border shadow-md rounded-lg px-4 py-3 text-sm'>
            <h2 className='text-xl font-bond mb-2'> Model Testing Report </h2>
            <div className='space-y-2 text-sm'>
                <p><span className='font-medium'> Accuracy: {report.modelAccuracy} </span></p>
                <p><span className='font-medium'> Classification Report</span></p>
                <div>
                    <p><span className='font-xs'> Home Win - Precision: {report.classificationReport.HomeWin.precision}</span></p>
                    <p><span className='font-xs'> Home Win - Recall: {report.classificationReport.HomeWin.recall}</span></p>
                    <p><span className='font-xs'> Home Win - F1 Score: {report.classificationReport.HomeWin.f1Score}</span></p>
                    <p><span className='font-xs'> Home Win - Support: {report.classificationReport.HomeWin.support}</span></p>
                    <p><span className='font-xs'> Away Win - Precision: {report.classificationReport.AwayWin.precision}</span></p>
                    <p><span className='font-xs'> Away Win - Recall: {report.classificationReport.AwayWin.recall}</span></p>
                    <p><span className='font-xs'> Away Win - F1 Score: {report.classificationReport.AwayWin.f1Score}</span></p>
                    <p><span className='font-xs'> Away Win - Support: {report.classificationReport.AwayWin.support}</span></p>
                    <p><span className='font-xs'> Accuracy - F1 Score: {report.classificationReport.AwayWin.f1Score}</span></p>
                    <p><span className='font-xs'> Accuracy - Support: {report.classificationReport.accuracy.support}</span></p>
                    <p><span className='font-xs'> Macro Avg - Precision: {report.classificationReport.macro_avg.precision}</span></p>
                    <p><span className='font-xs'> Macro Avg - Recall: {report.classificationReport.macro_avg.recall}</span></p>
                    <p><span className='font-xs'> Macro Avg - F1-Score: {report.classificationReport.macro_avg.f1Score}</span></p>
                    <p><span className='font-xs'> Macro Avg- Support: {report.classificationReport.macro_avg.support}</span></p>
                    <p><span className='font-xs'> Weighted Avg - Precision: {report.classificationReport.weighted_avg.precision}</span></p>
                    <p><span className='font-xs'> Weighted Avg - Recall: {report.classificationReport.weighted_avg.recall}</span></p>
                    <p><span className='font-xs'> Weighted Avg - F1-Score: {report.classificationReport.weighted_avg.f1Score}</span></p>
                    <p><span className='font-xs'> Weighted Avg - Support: {report.classificationReport.weighted_avg.support}</span></p>


                </div>
            </div>
        </div>
    )
}

export default ModelReportCard