import React, { useState} from 'react';
import * as d3 from 'd3';
import '../App.css'
import { Dropdown } from './DropDown';
import FetchInteractiveData from '../fetchData/FetchInteractiveData';
const lists=[
    {value:'price',label:'Rent(in $)'},
    {value:'beds',label:'Bedroom per Home'},
    {value: 'sqft', label:'Square Ft per Home'}
];
const label={
    "price":"Rent(in $)",
    "beds":"Bedrooms Per House",
    "sqft":"House Area in Square Ft"
}

const w=1200;
const h=600;

const margin={top:40,
      right:50,
      bottom:50,
      left:100
    };

const ScatterPlot=() => {
  const {data}=FetchInteractiveData();

  const initialxV = 'price';
  const[xV,setX]=useState(initialxV);

  const initialyV = 'beds';
  const[yV,setY]=useState(initialyV);
  
  if(!data){
    return <h3>Visualization not available due to no data availability</h3>;
  }

  const yScale = d3.scaleLinear()
    .domain(d3.extent(data, d => d[yV]))
    .range([40, h-150]);

  const xScale = d3.scaleLinear()
    .domain(d3.extent(data, d => d[xV]))
    .range([80,w]);

  return (
    <>
      <label for="x-select">X:</label>

      <Dropdown
        options={lists}
        id="x-select"
        selectedValue={xV}
        onSelectedValueChange={setX}/>

      <label for="y-select"> Y:</label>

      <Dropdown
        options={lists}
        id="y-select"
        selectedValue={yV}
        onSelectedValueChange={setY}/> 

    <svg width={w} height={h}>
      <g transform={`translate(${margin.left},${margin.top})`}>
        {
          xScale.ticks().map(tickValue => (
              <g 
                key={tickValue} 
                transform={`translate(${xScale(tickValue)},0)`}>
                
                <line 
                  y2={h-120} 
                  stroke="lightgrey" 
                />
                
                <text
                  style={{ textAnchor: 'middle' }}
                  dy="16px"
                  y={h-100}>
                  {tickValue}
                </text>

              </g>
            )
          )
        }

        {
          yScale.ticks().map(tickValue => (
              <g>
                <line 
                  x2={w}
                  y1= {yScale(tickValue)}
                  y2= {yScale(tickValue)}
                  stroke="grey" />
                
                <text
                  key={tickValue}
                  style={{ textAnchor: 'end' }}
                  x={-3}
                  dy="8px"
                  y={yScale(tickValue)}>
                  {tickValue}
                </text>
              </g>
            )
          )
        }
        <line 
          x2={w} 
          stroke="lightgrey"/>

        <text className="text-label" x={w/2.4} y={h-55}>
          {label[xV]}
        </text>
        <text className="text-label" x={-250} y={h-650} transform='rotate(-90)'>
        {label[yV]}
        </text>
        {
          data.map(d => (
            <circle
                cx={xScale(d[xV])}
                cy={yScale(d[yV])} 
                r={4}
            />
          ))
        }
      </g>
    </svg>
    </>
    
  );
};
export default ScatterPlot
