
<template>
    <!-- <div class="outer" ref="parallelContainer">
            <div class="inner"><svg id="stacked-svg"></svg></div>
        </div> -->
    <div id = "stackedcontainer" ref="parallelContainer" class="chart-container outer d-flex">

        <svg id="stacked-svg" class="inner"></svg>
    </div>
</template>
  
<script lang="ts">
import * as d3 from 'd3';
import axios from 'axios';
import { mapState, storeToRefs } from 'pinia';
import { useHousingStore } from '../stores/housingStore';

import { useYearStore } from '../stores/yearStore'
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';
import { getColors } from '../helpers/colors';

// import { setEndYear, setStartYear, setCurrentYear, getCurrentYear, getStackedCurrentYear, getStackedStartYear, getStackedEndYear, setStackedCurrentYear, setStackedEndYear, setStackedStartYear } from "../helpers/animate";
interface DataPoint {
    year: number;
    [key: string]: number;
}

export default {
    setup() {
        const store = useHousingStore();
        const { resize } = storeToRefs(store);

        const yearStore = useYearStore();


        return {
            store,
            resize,
            yearStore
        }
    },
    computed: {
        ...mapState(useHousingStore, ['selectedMethod']),
        ...mapState(useYearStore, [])
    },

    created() {
        this.store.fetchHousing(this.selectedMethod);
        this.yearStore.setYear(1990);
    },
    methods: {

        onResize() {
            let target = this.$refs.parallelContainer as HTMLElement

            if (target === undefined || target === null) return;
            this.store.size = { width: target.clientWidth, height: target.clientHeight };
        },


        initChart() {
            let svg = d3.select('#stacked-svg')

                .attr('width', this.store.size.width + this.store.margin.left + this.store.margin.right + 50)
                .attr('height', this.store.size.height + this.store.margin.top + this.store.margin.bottom)
                .append("g")
                .attr("transform", `translate(${this.store.margin.right}, ${-this.store.margin.bottom})`);

            let data: any[] = d3.csvParse(this.store.housing);

            const keys = data.columns.slice(1);

            const test = () => {
                let extent =
                    d3.extent(data, function (d: DataPoint) {

                        return d.year;
                    })

            }
            test()

            const x = d3.scaleLinear()
                .domain(d3.extent(data, function (d: DataPoint) {

                    return d.year;
                }))
                .range([this.store.margin.left, this.store.size.width - this.store.margin.right]);

            svg.append("g")
                .attr("transform", `translate(0, ${this.store.size.height})`)

                .call(d3.axisBottom(x).ticks(10).tickFormat(d3.format("")));

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", (this.store.size.width + this.store.margin.left) / 2)
                .attr("y", this.store.size.height + this.store.margin.bottom - 3)
                .text("Year");


            svg.append("text")
                .attr("text-anchor", "end")
                .attr("font-size", "24px")
                .attr("font-weight", "bold")
                .attr("x", (this.store.size.width + this.store.margin.left + 375) / 2)

                .attr("y", this.store.size.height + this.store.margin.bottom - 470)
                .text("Housing Production by County - Bay Area");

            var maxValue = d3.max(data, function (d) {
                var values = Object.values(d);
                values.shift(); // remove first element "year"
                return d3.max(values.map(Number));
            });



            function getMax(data: any) {
                if (data.length === 0) return 0;
                let maxRow = data.reduce((maxRow: any, currentRow: any) => {
                    let currentRowSum = d3.sum(Object.values(currentRow).map(Number));
                    let maxRowSum = d3.sum(Object.values(maxRow).map(Number));
                    return currentRowSum > maxRowSum ? currentRow : maxRow;
                });
                let maxValue = d3.sum(Object.values(maxRow).map(Number));
                return maxValue;
            }





            const y = d3.scaleLinear()
                .domain([0, getMax(data)])
                .range([this.store.size.height, this.store.margin.top]);

            svg.append("g")

                .call(d3.axisLeft(y))
                .attr("transform", `translate(${this.store.margin.left}, 0)`);

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", -this.store.size.height / 2 + (this.store.margin.bottom))
                .attr("y", (this.store.margin.left) - 75)
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-90)")
                .text("Number of Units Produced")

            const color = getColors(keys);



            const stackedData = d3.stack()
                // .offset(d3.stackOffsetSilhouette)
                .keys(keys)
                .value((d, key) => {

                    if (d[key] < 0) {
                    }

                    return d[key] < 0 ? 0 : d[key];
                })(data)





            const areaChart = svg
                .append('g')
                .attr('id', "myAreaChart")

                .attr("clip-path", "url(#clip)")

            areaChart.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr('id', "backgroundRect")
                .attr("width", this.store.size.width - ( this.store.margin.right))
                .attr("height", this.store.size.height - this.store.margin.top)
                .attr("transform", `translate(${0}, ${100})`)
                .attr("fill", "red")
                .attr("opacity", 0)


            areaChart
                .selectAll("mylayers")
                
                .data(stackedData)
                .join("path")
                .attr("class", function (d) {
                    return "myArea " + d.key.replaceAll(' ', '')
                })
                .attr("id", "selected")
                .style("fill", function (d) {
                    return color(d.key);
                })
                .attr("d", d3.area()
                    .x((d: any, i: any) => x(d.data.year))
                    .y0((d: any) => y(d[0]))
                    .y1((d: any) => y(d[1]))
                )

                .on("mouseover", function (event, d) {
                    
                    highlight(d.key.replaceAll(' ', ''))
                    tooltip.html(
                        `<div>County: ${d.key}</div>`
                    )
                        .style('visibility', 'visible');
                })
                .on('mousemove', function (event, d) {

                    tooltip
                        .style('top', (event.pageY - 10) + 'px')
                        .style('left', (event.pageX + 10) + 'px');

                    // get the x and y position of the mouse
                    // var x = event.clientX - chart.getBoundingClientRect().left;
                    // var y = event.clientY - chart.getBoundingClientRect().top;

                })
                .on("mouseleave", function (event, d) {
                    noHighlight(d.key.replaceAll(' ', ''))
                    tooltip.html(``).style('visibility', 'hidden');
                })
                .on("click", (event, d) => {
                })


            keys.sort((a, b) => a.localeCompare(b))



            // Add one dot in the legend for each name.
            const size = 20
            svg.selectAll("myrect")
                .data(keys)
                .join("rect")
                .attr("x", 700)
                .attr("class", function (d) {
                    return "legendRect"
                })
                .attr("id", function (d) {
                    return d.replaceAll(' ', '')
                })
                .attr("y", function (d, i) { return 350 + -i * (size + 5) }) // 100 is where the first dot appears. 25 is the distance between dots
                .attr("width", size)
                .attr("height", size)
                .style("fill", function (d) { return color(d) })
                .on("mouseover", function (event, d) {
                    highlight(d.replaceAll(' ', ''))

                })
                .on("mouseleave", function (event, d) {
                    noHighlight(d.replaceAll(' ', ''))
                })



            // Add one dot in the legend for each name.
            svg.selectAll("mylabels")
                .data(keys)
                .join("text")
                .attr("x", 700 + size * 1.2)
                .attr("y", function (d, i) { return 350 + -i * (size + 5) + (size / 2) }) // 100 is where the first dot appears. 25 is the distance between dots
                .style("fill", function (d) { return color(d) })
                .attr("class", function (d) {
                    return "legendLabel"
                })
                .attr("id", function (d) {
                    return d.replaceAll(' ', '')
                })
                .text(function (d) { return d.replaceAll(' County', '') })
                .attr("text-anchor", "left")
                .style("alignment-baseline", "middle")
                .on("mouseover", function (event, d) {
                    highlight(d.replaceAll(' ', ''))

                })
                .on("mouseleave", function (event, d) {
                    noHighlight(d.replaceAll(' ', ''))
                })

            // Add brushing
            const brush = d3.brushX()                 // Add the brush feature using the d3.brush function
                .extent([[0, 0], [this.store.size.width, this.store.size.height]])
                .on("brush", (event, d) => {

                    // var extent = brush.extent();
                    // svg.selectAll(".myArea")
                    // .on("mouseover", function(e, d) {
                    // console.log('d: ', d)
                    // let is_brushed = extent[0] <= d.index && d.index <= extent[1];
                    // return is_brushed;
                    // });
                    if (event.selection.map(x.invert)[0] < 1990 || event.selection.map(x.invert)[1] >= 2018) {
                        return;
                    }
                    else {
                        brushed(event, d)
                    }
                })
                .on("end", function (event, d) {
                    // brushended(event, d);
                }) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
            // .on("end", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

            // Create the scatter variable: where both the circles and the brush take place


            function mouseEvent(e, d, marginTop, marginBottom, height) {
                // console.log('movemouse')
                let [xCoordinate] = d3.pointer(e);
                // use a bisector to find the closest year on the x-axis
                let year = x.invert(xCoordinate);
                year = Math.round(year);

                if (year > 2018 || year < 1990) {
                    return;
                }

                bisectorRect
                    .attr("x", x(year) - 1)
                    .attr("y", marginTop)
                    .attr("width", 2)
                    .attr("height", height - (marginTop))

                // update the position of the bisector line
                // bisectorLine
                // .attr("x1", x(year))// x(year))
                // .attr("x2", x(year))
                // .attr("y1", 100)
                // .attr("y2", 500)
                // .style("display", "block");


            }
            function brushed(event, d) {
                // let interval = d3.timeYear.every(1)
                // console.log('d3.brushselection: ', d3.pointer(d))
                if (!event.sourceEvent) return; // Only transition after input.

                const d0 = event.selection.map(x.invert);

                let lower = Math.round(d0[0])
                let upper = Math.round(d0[1])
                // d1 = Math.round(d0)
                // console.log('d1', d0)
                // console.log('lower', lower)
                // console.log('upper', upper)

                setEndYear(upper)
                setStartYear(lower)
                setCurrentYear(lower)
                setStackedEndYear(upper)
                setStackedStartYear(lower)
                setStackedCurrentYear(lower)
                if (lower >= upper) {
                    lower = Math.floor(d0[0])
                    upper = Math.ceil(d0[1])
                }
                d3.select(".brush")
                    .call(brush.move, [x(lower), x(upper)]);

            }

            function brushended(event, d) {
                if (!getStartYear()) {
                    return;
                }
                if (!event.sourceEvent) return; // Only transition after input.

                const d0 = event.selection.map(x.invert);

                let lower = Math.round(d0[0])
                let upper = Math.round(d0[1])
                // d1 = Math.round(d0)
                // console.log('d1', d0)

                setStackedEndYear(upper)
                setStackedStartYear(lower)
                // your code here to handle the brushed year range
            }

            areaChart
                .append('g')
                .attr("class", "brush")
                .on("mousemove", function (event) {
                    const mouseX = d3.pointer(event, event.target)[0];
                    let year = x.invert(mouseX);

                    year = d3.scaleLinear()
                        .domain(x.domain())
                        .range(x.range())
                        .clamp(true)
                        .nice()
                        .invert(mouseX);

                    bisectorRect.attr("x", x(Math.round(year)))
                })
                // .call(brush)
                .attr("clip-path", "url(#clip)")
            // .on('mousemove', (e, d) => {
            //     mouseEvent(e, d, this.store.margin.top, this.store.margin.bottom, this.store.size.height)
            // });

            // areaChart
            //     .append('g')
            //     .attr("class", "brush")
            //     .call(brush)
            //     .attr("clip-path", "url(#clip)")
            // .on('mousemove', (e, d) => {
            //     mouseEvent(e, d, this.store.margin.top, this.store.margin.bottom, this.store.size.height)

            // tooltip
            //     .style('top', (e.pageY - 10) + 'px')
            //     .style('left', (e.pageX + 10) + 'px');
            // }).on("mouseover", function (event, d) {
            //     console.log('event:', event)
            //     console.log('d: ', d)
            //     d3.selectAll('.myArea').filter(function (d, i) {
            //         // console.log('ddddd: ', d)
            //         return d.key === 'Alameda'
            //     })

            //     // highlight(d.key.replaceAll(' ', ''))
            //     // tooltip.html(
            //     //     `<div>County: ${d.key}</div>`
            //     // )
            //     //     .style('visibility', 'visible');
            //     }
            //     )
            // .on("mouseleave", function (event, d) {
            // // noHighlight(d.key.replaceAll(' ', ''))
            // tooltip.html(``).style('visibility', 'hidden');
            // })


            // .attr('height', '90%')
            // .attr('width', '90%')
            // .attr("transform", `translate(${this.store.margin.left}, ${-this.store.margin.bottom})`);

            //////////
            // HIGHLIGHT GROUP //
            //////////

            let tooltip = d3
                .select('body')
                .append('div')
                .attr('class', 'd3-tooltip')
                .style('position', 'absolute')
                .style('z-index', '10')
                .style('visibility', 'hidden')
                .style('padding', '10px')
                .style('background', 'rgba(0,0,0,0.6)')
                .style('border-radius', '4px')
                .style('color', '#fff')
                .text('a simple tooltip');


            // What to do when one group is hovered
            var highlight = function (d: any) {
                // reduce opacity of all groups
                d3.selectAll(".myArea").style("opacity", .25)
                d3.selectAll(".legendRect").style("opacity", .25)
                d3.selectAll(".legendLabel").style("opacity", .25)

                d3.selectAll(".bubble").style("opacity", 0)

                // console.log('bubble selected: ', '.bubble.', d)

                // console.log('myArea selected: ', '.myArea.', d)
                // expect the one that is hovered

                d3.selectAll(".bubble." + d)
                    .style("opacity", 0.8)

                d3.selectAll("#" + d.replaceAll(' ', ''))
                    .style("opacity", 1)

                d3.select(".myArea." + d)
                    .style("stroke", "black").style("opacity", 1)

            }

            // And when it is not hovered anymore
            var noHighlight = function (d: any) {
                d3.selectAll(".myArea").style("opacity", 1).style("stroke", "none")

                d3.selectAll(".bubble").style("opacity", 0.8)
                d3.selectAll(".legendRect").style("opacity", 1)
                d3.selectAll(".legendLabel").style("opacity", 1)
            }

// Add a clipPath: everything out of this area won't be drawn.
const clip = svg.append("defs").append("svg:clipPath")
                .attr("id", "clip")
                
                .append("svg:rect")
                
                .attr("width", this.store.size.width - (this.store.margin.right + this.store.margin.left))
                .attr("height", this.store.size.height)
                .attr("transform", "translate(" + this.store.margin.left + ",0)")
                .attr("x", 0)
                .attr("y", 0);
            const bisectorLine = svg.append("line")
                .attr("x1", 0)
                .attr("y1", 0)
                .attr("x2", 0)
                .attr("y2", 1000)
                .attr("stroke", "white")
                .attr("opacity", 1)
                .attr("border", "1px solid black")
                .attr("stroke-width", 2)
                .style("display", "none");


                let isDragging = false;


                svg
            .on("mouseleave", function () {
                bisectorRect.attr("x", -100).attr('opacity', 0)
            })
            .on("mousedown", () => {
                    isDragging = true;
                })
                .on("mousemove", (e) => {
                    if (isDragging) {
                    clickYear(e, this.yearStore);
                    bisectorRect.attr("opacity", 0)
                    }
                    else {
                    if (event.srcElement.id !== 'backgroundRect' && event.srcElement.id !== 'selected') {
                        return;
                    }
                const mouseX = d3.pointer(event, event.target)[0];
                let year = x.invert(mouseX);
                year = d3.scaleLinear()
                    .domain(x.domain())
                    .range(x.range())
                    .clamp(true)
                    .nice()
                    .invert(mouseX);

                bisectorRect.attr("x", x(Math.round(year)))
                .attr('opacity', .5)}
                    
                })
                .on("mouseup", () => {
                    isDragging = false;

                    bisectorRect.attr("opacity", .5)
                })
                .on("click", (e) => {
                    clickYear(e, this.yearStore);
                    
                });

            
            const clickYear = function(event, yearStore) {
                
                if (event.srcElement.id !== 'backgroundRect' && event.srcElement.id !== 'selected') {
                        return;
                    }
                    const mouseX = d3.pointer(event, event.target)[0];
                let year = x.invert(mouseX);
                year = d3.scaleLinear()
                    .domain(x.domain())
                    .range(x.range())
                    .clamp(true)
                    .nice()
                    .invert(mouseX);

                    bisectorSelect.attr("x", x(Math.round(year)))
                .attr('opacity', 1)

                
                yearStore.setYear((Math.round(year)));
                // console.log('getCurrentYear: ', getCurrentYear())
                
            }

            const clickYearDrag = function(event, yearStore) {
                console.log('drag: ', event)
                if (event.srcElement.id !== 'backgroundRect' && event.srcElement.id !== 'selected') {
                        return;
                    }
                    const mouseX = d3.pointer(event, event.target)[0];
                let year = x.invert(mouseX);
                year = d3.scaleLinear()
                    .domain(x.domain())
                    .range(x.range())
                    .clamp(true)
                    .nice()
                    .invert(mouseX);

                    bisectorSelect.attr("x", x(Math.round(year)))
                .attr('opacity', 1)

                
                yearStore.setYear((Math.round(year)));
                // console.log('getCurrentYear: ', getCurrentYear())
                
            }

            let year = 1990;
            if (this.yearStore.year) {
                year = this.yearStore.year;
            }
            const bisectorSelect = svg.append("rect")
                .attr("id", "bisectorSelect")
                .attr("x", x(year))
                .attr("y", 0)
                .attr("width", 4)
                .attr("height", this.store.size.height - this.store.margin.top)
                .attr("transform", `translate(-2, ${100})`)
                .attr("pointer-events", "none")
                // .attr('z-index', '10000')
                // .attr("fill", "black")
                // .attr("stroke", "black")
                // .attr("opacity", 0)
                .attr("border", "1px dashed black")
                .attr("stroke-width", 1);


            const bisectorRect = svg.append("rect")
                .attr("id", "bisectorRect")
                .attr("x", x(this.yearStore.year))
                .attr("y", 0)
                .attr("width", 4)
                .attr("height", this.store.size.height - this.store.margin.top)
                .attr("transform", `translate(-2, ${100})`)
                .attr("pointer-events", "none")
                // .attr('z-index', '10000')
                // .attr("fill", "black")
                // .attr("stroke", "black")
                .attr("opacity", 0)
                .attr("border", "1px dashed black")
                .attr("stroke-width", 1);

            //             let years = d3.range(getStartYear(), getEndYear() + 1);
            //             function animate(height, marginTop) {
            //                 let years = d3.range(getStartYear(), getEndYear() + 1);
            //                 console.log('years: ', years)
            //                 let i = 0;
            //                 bisectorRect.data(years)
            //                 .transition()
            //                 .duration(2000)
            //                 .ease(d3.easeLinear)
            //                 .attr("x", () => {
            //                     console.log('years[i]: ', years[i])
            //                     return x(years[i])
            //                 })
            //                 .attr("y", marginTop)
            //                 .attr("width", 2)
            //                 .attr("height", 1000)
            //                 .on("end", function() {
            //                     i = (i + 1) % years.length;
            //                     if (i === 0) return;
            //                     bisectorRect
            //                     .transition()
            //                     .duration(0)
            //                     .ease(d3.easeLinear)
            //                     .attr("x", x(years[i+10]))
            //                     .on("end", function() { animate(height, marginTop); });
            //                 });
            //             }
            //         // console.log('before animate')
            //         animate( this.store.size.height, this.store.margin.top);

            const animater = () => {

                let startStackedYear = getStackedStartYear();
                let endStackedYear = getStackedEndYear();
                let currentStackedYear = getStackedCurrentYear();
                let years = d3.range(1990, 2018);
                let data = years.filter(d => parseInt(d) === parseInt(currentStackedYear)).map(d => {
                    return d;
                });
                // console.log('currentStackedYear: ', currentStackedYear)
                // console.log('data: ', data)


                // bubbles.data(productionData, d => d.city)
                //         .transition()
                //         .duration(2000)
                //         .ease(d3.easeLinear)

                bisectorRect.data(data)
                    .transition()
                    .duration(4000) // 2 second transition
                    .ease(d3.easeLinear) // linear transition
                    .attr("x", d => {
                        // console.log('x(d): ', d)

                        return x(d)
                    }) // start position
                    .attr("transform", `translate(0, ${100})`)
                    // .attr("color", "#" + JSON.stringify(Math.floor(Math.random() * 9)))
                    // .attr("width", 3) // width of rect
                    .attr("height", this.store.size.height - this.store.margin.top)// full height of rect
                // .on("end", () => {

                // bisectorRect.transition()
                //     .duration(0)
                //     .ease(d3.easeLinear)
                //     .attr("x", x(getStartYear() - 1)) // start position
                //     // .attr("width", 0)
                //     .on("end", loop);
                // });


                if (currentStackedYear === endStackedYear) {
                    currentStackedYear = startStackedYear;
                    // console.log('set year')
                    setStackedCurrentYear(currentStackedYear);
                }
                else {

                    currentStackedYear = currentStackedYear + 1;

                    // console.log('set year')
                    setStackedCurrentYear(currentStackedYear);
                }

                if (currentStackedYear <= endStackedYear) {
                    d3.timeout(animater, 4000);
                    // bisectorRect
                    //     .attr("x", x(getStackedStartYear()))
                    //     .attr("y", 0)
                    //     .attr("width", 3)
                    //     .attr("height", this.store.size.height - this.store.margin.top)
                    //     .attr("transform", `translate(0, ${100})`)
                    //     .attr('z-index', '-10')
                    //     // .attr("fill", "black")
                    //     // .attr("stroke", "black")
                    //     .attr("opacity", .3)
                    //     .attr("border", "1px dashed black")
                    //     .attr("stroke-width", 1);
                }
                else {
                }
            };

            // animater();


        },

        rerender() {

            d3.select('#stacked-svg').selectAll('*').remove() // Clean all the elements in the chart
            // d3.select('#my_dataviz').selectAll('*').remove()

            this.initChart()


        }
    },
    mounted() {
        window.addEventListener('resize', debounce(this.onResize, 100))
        this.onResize()
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    },

    watch: { // updated because a legend is added.

        resize(newSize) { // when window resizes
            if ((newSize.width !== 0) && (newSize.height !== 0)) {
                this.rerender()
            }
        },
        'store.housing'(data: string) { // when data changes
            if (!isEmpty(data)) {
                this.rerender()
            }
        },

        selectedMethod(newMethod) { // function triggered when a different method is selected via dropdown menu
            this.store.fetchHousing(newMethod)
        },
    }
}
</script>


<style scoped>
.chart-container {
    height: 100%;
    flex-direction: column;
    flex-wrap: center;
    width: 100%;

    /* border: 1px solid black; */
    /* adds a 1px black border */
}


.method-select {
    outline: solid;
    outline-width: 1px;
    outline-color: lightgray;
    border-radius: 2px;
    width: 100%;
    padding: 2px 5px;
}

.selected {
    fill: #afa2dc;
    stroke: #2f225d;
}

.outer {
    display: flex;
    justify-content: center;
    align-items: center;
    /* background-color: red; */
    height: 500px;
}
</style>