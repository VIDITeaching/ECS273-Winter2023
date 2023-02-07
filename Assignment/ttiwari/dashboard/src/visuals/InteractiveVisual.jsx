import React from 'react'
import ScatterPlot from './ScatterPlot'
function InteractiveVisual() {
  return (
    <div>
      <h1>Interactive Visual</h1>
      {/* <label for="xaxis">X Axis: </label>
      <select id="xaxis">
      <option value="rent">Rent</option>
      <option value="room">Room</option>
      </select>
      <br/>
      <label for="yaxis">Y Axis: </label>
      <select id="yaxis">
      <option value="room">Room</option>
      <option value="rent">Rent</option>
      </select> */}
      <ScatterPlot/>
    </div>
  )}
  export default InteractiveVisual