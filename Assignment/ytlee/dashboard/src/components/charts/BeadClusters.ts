import * as d3 from 'd3'
import { lab } from 'd3';
import { forceCluster } from 'd3-force-cluster'


export class BeadClusterConfig {
    width: any;
    height: any;
    padding: any;
    maxRadius: any;
    labelRadius: any;
    velocityDecay: any = 0.4;
}

export class BeadClusters {
    data: any;
    nodes: any;
    clusters: any;
    config: BeadClusterConfig;

    public constructor(beadClustersConfig: BeadClusterConfig) {
        this.config = beadClustersConfig
        this.nodes = []                 // all nodes destination array
        this.clusters = []
    }

    

    // --- chart generator ---------------------------------------
    chart(selection: any, data: any, nodeSizeScale: any, emit: any) {
        d3.select("#chart").selectAll("*").remove()
        this.nodes = []
        this.data = data
        let self = this
        selection.each(function() {
            let m = self.data.groups.length,    // total number of clusters
                n = 0                       // total number of nodes
            self.clusters = new Array(m)   // cluster nodes destination array
  
            // generate nodes
            self.data.groups.forEach((group: any, i: any) => {
                // count nodes in this group
                n += group.numNodes
        
                // generate nodes in this group
                let _nodes = d3.range(group.numNodes).map((nodeIndex) => {
                    // let r = Math.sqrt((self.config.maxRadius) / m * -Math.log(Math.random())) * self.config.maxRadius,
                    // let r = Math.sqrt((self.config.maxRadius) / m * -Math.log(Math.random())) * self.config.maxRadius,
                    let r = nodeSizeScale(group.nodeData[nodeIndex]),
                        d = {
                            cluster: i,
                            radius: r,
                            label: group.label,
                            data: group.nodeData[nodeIndex],
                            summary: group.summary[nodeIndex],
                            kill: group.kill[nodeIndex],
                            wound: group.wound[nodeIndex],
                            attack_type: group.attack_type[nodeIndex],
                            target: group.target[nodeIndex],
                            motive: group.motive[nodeIndex],
                            notes: group.notes[nodeIndex],
                            x: Math.cos(i / m * 2 * Math.PI) * self.config.width / 4 + Math.random(),
                            y: Math.sin(i / m * 2 * Math.PI) * self.config.height / 4 + Math.random()
                        }
        
                    return d
                })
    
                const sum = (list: any[]) => list.reduce((partialSum, a) => partialSum + a, 0); 
                const count = (list: any[]) => {
                    let counts: any = {}
                    for (const num of list) {
                        counts[num] = counts[num] ? counts[num] + 1 : 1;
                    }
                    return counts
                }

                // generate cluster node that other nodes in this group orbit around
                let clusterNode = self.clusters[i] = {
                    isClusterNode: true,
                    key: group.key,
                    label: group.label,
                    cluster: i,
                    radius: self.config.labelRadius,
                    x: self.config.width / 2,
                    y: self.config.height / 2,
                    // data
                    summary: group.summary.length, // total events
                    kill: sum(group.kill),
                    wound: sum(group.wound),
                    attack_type: count(group.attack_type),
                    target: count(group.target),
                    notes: "", 
                }
        
                // add cluster node to nodes in this group
                _nodes.push(clusterNode)
        
                // add nodes in this group to all nodes
                self.nodes = self.nodes.concat(_nodes)
            })
    
            // define color scale corresponding to clusters
            // let color = d3.scaleOrdinal(d3.schemeCategory10)
            const keys = data.groups.map((ele: any) => ele.label)
            var color = d3.scaleOrdinal()
                .domain(keys.sort())
                .range(d3.schemeSet2);

            // define separate forces
            let forceCenter = d3.forceCenter(self.config.width / 2, self.config.height / 2),
                vforceCluster = forceCluster().centers((d: any) => self.clusters[d.cluster]).strength(1),
                forceCollide = d3.forceCollide((d: any) => d.radius + self.config.padding)


            // set up svg
            let svg = selection.append('svg')
                .attr('width', "100%")
                .attr('height', "100%")
                .attr("viewBox", `0 0 ${self.config.width} ${self.config.height}`)

            // compose simulation with all forces
            const simulation = d3.forceSimulation()
                .force('center', forceCenter)
                .force('cluster', vforceCluster)
                .force('collide', forceCollide)
                .velocityDecay(self.config.velocityDecay)
                .on('tick', tick)
                .nodes(self.nodes)
            let nodeElements = svg.append('g')
                .attr('class', 'nodes')
                .raise()
                .selectAll('circle')
                .data(self.nodes)
                .enter().append('circle')
                    .attr("class", "node_circle")
                    .style('fill', (d: any) => (d.isClusterNode) ? 'none' : color(d.label))
                    // .style('stroke', (d: any) => (d.isClusterNode) ? '#eee' : 'none')
                    // .style('stroke-width', (d: any) => (d.isClusterNode) ? '1px' : 'none')
                    .style("cursor", "pointer")
                    .style("pointer-events", "all")
                    .on("click", (e: any, d: any) => emit("node-selected", d))
                    .on("mouseover", function(this: any, e: any, d: any) {
                        d3.select(this).attr("stroke", "black").attr("stroke-width", 2)
                    })
                    .on("mouseout", function(this: any, e: any, d: any) {
                        d3.select(this).attr("stroke-width", 0)
                    })

            let labelElements = svg.append('g')
                .attr('class', 'cluster-node-labels')
                .style("pointer-events", "none")
                .selectAll('text')
                .data(self.clusters)
                .enter().append('text')
                    .attr("class", "node_label")
                    .style('fill', (d:any ) => color(d.label))
                    .attr('text-anchor', 'middle')
                    .text((d: any) => d.label)
                    .each(function(this: any) {
                        d3.select(this).call(wrap, { radius: self.config.labelRadius })
                    })
                    .style("pointer-events", "none")
    
        })
    }
}

function tick() {
    const nodeElements = d3.selectAll('.node_circle')
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y)
        .attr('r', (d: any) => d.radius)

    const labelElements = d3.selectAll('.node_label')
        .attr('transform', (d: any) => `translate(${d.x}, ${d.y})`)
}

function wrap(selection: any, params: any) {
    let scaleFactor = (params && params.scaleFactor) ? params.scaleFactor : 0.6,
        lineHeight = (params && params.lineHeight) ? params.lineHeight : 16,
        radius = (params && params.radius) ? params.radius : 100,
        text = selection.text(),
        _words = words(text),
        _targetWidth = targetWidth(text),
        _lines = lines(_words, _targetWidth),
        _textRadius = textRadius(_lines)

    // split text into words
    function words(text: any) {
        let words = text.split(/\s+/g); // To hyphenate: /\s+|(?<=-)/
        if (!words[words.length - 1]) words.pop();
        if (!words[0]) words.shift();
        return words;
    }

    // measure simulated text width
    function measureWidth(text: any) {
        const context: any = document.createElement("canvas").getContext("2d");
        return context.measureText(text).width;
    }

    // calculate target width
    function targetWidth(text: any) {
        return Math.sqrt(measureWidth(text.trim()) * lineHeight)
    }

    // split text into lines
    function lines(words: any, targetWidth: any) {
        let line:any;
        let lineWidth0 = Infinity;
        const lines = [];
        for (let i = 0, n = words.length; i < n; ++i) {
            let lineText1 = (line ? line.text + " " : "") + words[i];
            let lineWidth1 = measureWidth(lineText1);
            if ((lineWidth0 + lineWidth1) / 2 < targetWidth) {
                line.width = lineWidth0 = lineWidth1;
                line.text = lineText1;
            } else {
                lineWidth0 = measureWidth(words[i]);
                line = {width: lineWidth0, text: words[i]};
                lines.push(line);
            }
        }
        return lines;
    }

    // calculate simulated text radius
    function textRadius(lines: any) {
        let radius = 0;
        for (let i = 0, n = lines.length; i < n; ++i) {
            const dy = (Math.abs(i - n / 2 + 0.5) + 0.5) * lineHeight;
            const dx = lines[i].width / 2;
            radius = Math.max(radius, Math.sqrt(dx ** 2 + dy ** 2));
        }
        return radius;
    }

    return selection
    .text("")
    .attr("transform", `scale(${radius / _textRadius * scaleFactor})`)
    .selectAll("tspan")
    .data(_lines)
    .enter().append("tspan")
    .attr("x", 0)
    .attr("y", (d: any, i: any) => (i - _lines.length / 2 + 0.8) * lineHeight)
    .text((d: any) => d.text)
    .style("pointer-events", "none")
}
