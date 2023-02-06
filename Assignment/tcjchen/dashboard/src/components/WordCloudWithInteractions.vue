<script>
import * as d3 from 'd3'
import * as cloud from 'd3-cloud'

import { mapState, storeToRefs } from 'pinia';
import { debounce } from 'lodash';
import { useStore as useWordStore } from '../stores/WordStore';

function throttle(method, context) {
    clearTimeout(method.tid)
    method.tid = setTimeout(function () {
        method.call(context)
    }, 200)
}

const props = {
    margin: {
        type: Object,
        default: function () {
            return {
                top: 15,
                right: 15,
                bottom: 15,
                left: 15
            }
        }
    },
    rotate: {
        type: Object,
        default: function () {
            return {
                from: -60,
                to: 60,
                numOfOrientation: 5
            }
        }
    },
    fontSize: {
        type: Array,
        default: function () {
            return [10, 80]
        }
    },
    nameKey: {
        type: String,
        default: 'name'
    },
    val: {
        type: String,
        default: 'val'
    },
    polarity: {
        type: String,
        default: 'polarity'
    },
    subjectivity: {
        type: String,
        default: 'subjectivity'
    }
}
export default {
    name: "word-cloud",
    props,
    setup() {
        const store = useWordStore();
        // Alternative expression from computed
        const { resize } = storeToRefs(store);
        return {
            store,
            resize,
        };
    },
    created() {
        this.store.fetch(this.selectedPerson);
    },
    computed: {
        ...mapState(useWordStore, ["selectedPerson"]),
        size() {
            const { svgWidth, svgHeight } = this;
            const { margin } = this;
            const width = svgWidth - margin.left - margin.right;
            const height = svgHeight - margin.top - margin.bottom;
            return { width, height };
        },
        words() {
            // combine the arrays:
            const { store } = this;
            var words = [];
            for (var j = 0; j < store.names.length; j++)
                words.push({ "name": store.names[j], "val": store.vals[j][0], "polarity": store.vals[j][1], "subjectivity": store.vals[j][2] });
            words.sort(function (a, b) {
                return ((a.val > b.val) ? -1 : ((a.val == b.val) ? 0 : 1));
            });
            return words;
        }
    },
    mounted() {
        this.getSize()
        this.chart = this.createChart()
        this.renderChart()
        this.initLegend()

        window.addEventListener('resize', debounce(this.onResize, 100))
        this.onResize()
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    },
    watch: {
        words: {
            handler: function (val, oldVal) {
                this.update()
            },
            deep: false
        },
        selectedPerson(newPerson) {
            this.store.fetch(newPerson);
        }
    },
    methods: {
        onResize() {
            this.getSize();
            throttle(this.update);
        },
        getSize() {
            this.svgWidth = this.$refs.wordContainer.clientWidth;
            this.svgHeight = this.$refs.wordContainer.clientHeight;
        },
        createSvg() {
            const svg = d3.select(this.$refs.wordContainer).append("svg")
                .attr("width", "100%")
                .attr("height", "100%");
            return svg;
        },
        createChart() {
            const { margin } = this;
            const { width, height } = this.size;
            const svg = this.createSvg();
            const chart = svg.append("g")
                .attr("width", width)
                .attr("height", height)
                .attr("class", "chart")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
            return chart;
        },
        getRotation() {
            const { from: x1, to: x2, numOfOrientation: n } = this.rotate;
            const multiplier = ((Math.abs(x1) + Math.abs(x2)) / (n - 1)) || 1;
            return { a: n, b: (x1 / multiplier), c: multiplier };
        },
        setFontSizeScale() {
            const { fontSize, words, val } = this;
            this.fontSizeScale = d3.scaleSqrt();
            this.fontSizeScale.range(fontSize);
            if (words.length) {
                this.fontSizeScale.domain([+words[words.length - 1][val[0]] || 1, +words[0][val[0]]]);
            }
        },
        renderChart() {
            this.setFontSizeScale();
            const { fontSizeScale, words, nameKey, val } = this;
            const { width, height } = this.size;
            const { a, b, c } = this.getRotation();
            const layout = cloud()
                .size([width, height])
                .words(words)
                .fontSize(d => fontSizeScale(d[val]))
                .text(d => d[nameKey])
                .font("impact")
                .padding(3)
                .rotate(() => { return (~~(Math.random() * a) + b) * c; })
                .spiral("archimedean")
                .on("end", this.draw);
            this.layout = layout;
            layout.start();
        },
        draw(data) {
            const { layout, chart, nameKey, val, polarity, subjectivity } = this;
            // const fill = d3.scaleOrdinal(d3ScaleChromatic["scheme" + "Category10"]);

            const fill = d3.scaleOrdinal()
                .domain(['0', '1', '2', '3'])
                .range(['#065a94', '#1f77b4', '#629fc9', '#94bedb'])

            const centeredChart = chart.append("g")
                .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")");
            // Define the div for the tooltip
            const tooltip = d3.select("body").append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);
            const text = centeredChart.selectAll("text")
                .data(data)
                .enter().append("text")
                .style("font-size", d => d.size + "px")
                .style("font-family", d => d.font)
                .style("fill", (d, i) => {
                    if (data[i][val] >= 20) {
                        return fill("0")
                    }
                    else if (10 < data[i][val] && data[i][val] < 20) {
                        return fill("1")
                    }
                    else if (4 < data[i][val] && data[i][val] <= 10) {
                        return fill("2")
                    }
                    else if (data[i][val] < 5) {
                        return fill("3")
                    }
                })
                .attr("class", "text")
                .attr("text-anchor", "middle");
            text.transition()
                .duration(500)
                .attr("transform", (d) => { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
                .text(d => d.text);
            text.on("mouseover", function (d, i) {
                tooltip.transition()
                    .duration(200)
                    .style("opacity", 1);
                tooltip.html("Word: " + i[nameKey] + "<br/>" + "Occurence: " + i[val] + "<br/>" + "Polarity: " + i[polarity] + "<br/>" + "Subjectivity: " + i[subjectivity]);
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1);
            })
                .on("mousemove", function (d) {
                    const x = d.pageX;
                    const y = d.pageY;
                    tooltip
                        .style("left", (x) + "px")
                        .style("top", (y - 40) + "px");
                })
                .on("mouseout", function (d) {
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                    d3.select(this)
                        .style("stroke", "none");
                });
        },
        initLegend() {
            let data = ["Occurence >= 20", "11 to 20", "5 to 10", "1 to 4"]
            let legendContainer = d3.select('#wordCloud-legend-svg')

            const fill = d3.scaleOrdinal()
                .domain(data)
                .range(['#065a94', '#1f77b4', '#629fc9', '#94bedb'])

            const rectSize = 20;

            const legendGroups = legendContainer.append('g')
                .attr('transform', "translate(0, 10)") // this is applied to "g" element and will affect all the child elements.
                .selectAll('g')
                .data(data)
                .join((enter) => {
                    let select = enter.append('g');

                    select.append('rect')
                        .attr('width', rectSize).attr('height', rectSize)
                        .attr('x', 0).attr('y', (d, i) => i * rectSize * 1.3)
                        .style('fill', (d) => fill(d))

                    select.append('text')
                        .text((d) => d)
                        .style('font-size', '0.9rem')
                        .style('text-anchor', 'start')
                        .attr('x', rectSize / 1.5)
                        .attr('y', (d, i) => i * rectSize * 1.4)
                        .attr('dx', '0.7rem')
                        .attr('dy', '0.7rem')
                    return select
                })
        },
        update() {
            const { words, layout, fontSizeScale, chart, val } = this;
            // const { width, height } = this.size;
            const width = this.$refs.wordContainer.clientWidth;
            const height = this.$refs.wordContainer.clientHeight;
            if (words.length) {
                fontSizeScale.domain([+words[words.length - 1][val] || 1, +words[0][val]])
            }
            // clear chart
            chart.select('g').remove()
            // clear tooltip
            chart.select('body').remove()
            layout.stop().size([width, height]).words(words).start()
        }
    }
}
</script>

<template>
    <div class="viz-container d-flex">
        <div id="wordCloud" class="wordCloud-container d-flex" ref="wordContainer">
        </div>

        <div id="wordcloud-control-container" class="d-flex">
            <div class="d-flex">
                <label :style="{ fontSize: '1rem' }"> Select Person:
                    <select class="method-select" v-model="store.selectedPerson">
                        <option v-for="person in store.people" :value="person"
                            :selected="(person === store.selectedPerson) ? true : false">{{ person }}</option>
                    </select>
                </label>
            </div>

            <div class="wordCloud-title" ref="wordCloudTitle">
                <label :style="{ fontSize: '1rem', fontWeight: 'bold' }">Selected Person's
                    WordCloud</label>
            </div>
            <svg id="wordCloud-legend-svg" width="70%" height="80%">
            </svg>
        </div>

    </div>
</template>


<style scope>
.viz-container {
    height: 100%;
    flex-direction: column-reverse;
    flex-wrap: nowrap;
}

.wordCloud-container {
    width: 100%;
    height: 100%;
    background-color: antiquewhite;
    flex-direction: row;
}

.wordcloud-control-container {
    width: 100%;
    height: 70px;
}

div.tooltip {
    position: absolute;
    text-align: center;
    padding: 8px;
    font: 18px Arial;
    line-height: 24px;
    color: #313639;
    border: solid;
    border-width: 2px;
    border-radius: 2px;
    pointer-events: none;
    background-color: white;
}

.method-select {
    outline: solid;
    outline-width: 1px;
    outline-color: lightgray;
    border-radius: 2px;
    width: 100%;
    padding: 2px 5px;
}
</style>