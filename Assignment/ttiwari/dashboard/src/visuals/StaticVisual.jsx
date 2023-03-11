import React from 'react'
import ScatterPlot from './ScatterPlot'
import BarChart from '../visuals/BarChart'
import '../index.css';
function SystemInbox() {
  return (
//     <div class='parent'>
//   <div class='child'><BarChart/></div>
//   <div class='child'><ScatterPlot/></div>
// </div>
//     <React.Fragment>
//       <BarChart/>
//       <ScatterPlot/>
//     </React.Fragment>
    <div className='sidebyside'>
      <div><BarChart/></div>
      <div><ScatterPlot/></div>
    </div>
  )
}

export default SystemInbox