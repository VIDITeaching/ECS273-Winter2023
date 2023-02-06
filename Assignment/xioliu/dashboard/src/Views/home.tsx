import React from "react";
import './home.css'
// @ts-ignore
import csvPath from '../data/test.csv';

import * as d3 from "d3";
import Histogram from "../charts/histogram";
import Piechart from "../charts/piechart";
import Parallel from "../charts/parallel";
import {log} from "util";

function Home() {
    const [data, setData] = React.useState(null);

    React.useEffect(() => {
        fetch('http://127.0.0.1:3100/fetchExample')
            .then(response=>{
                if (response.ok) {
                    console.log(response);
                    return response.json();
                }
            })
            .then(json=>{
                setData(json.data);
                console.log(json);
            })
    }, [])

    // @ts-ignore
    if (data !== null){
        console.log(data[0]);
    }

    return (
        <div className={'background'}>
            <div className={'title_txt'}>
                <text> Analysis of Airline Passenger Satisfaction</text>
            </div>
            <div className={'overall'}>
                <Histogram data={data}/>
            </div>

            <div className={'contexts'}>
                {/*<div className={'left'}>*/}
                {/*    <Piechart data={data} />*/}
                {/*</div>*/}

                <div className={'right'}>
                    <Parallel data={data} />
                </div>
            </div>

        </div>
    )
}

export default Home
