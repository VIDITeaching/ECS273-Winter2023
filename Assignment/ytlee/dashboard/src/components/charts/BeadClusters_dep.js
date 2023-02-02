function beadClusters() {
    d3.select("#chart").selectAll("svg").remove()
    
    // defined via accessor functions
    var data,
        width,
        height,
        padding,
        maxRadius,
        labelRadius,
        simulation,
        velocityDecay = 0.4
  
    // --- chart generator ---------------------------------------
    function chart(selection) {
      selection.each(function() {
        var m = data.groups.length,    // total number of clusters
            n = 0,                     // total number of nodes
            clusters = new Array(m),   // cluster nodes destination array
            nodes = []                 // all nodes destination array
  
        // generate nodes
        data.groups.forEach((group, i) => {
          // count nodes in this group
          n += group.numNodes
  
          // generate nodes in this group
          let _nodes = d3.range(group.numNodes).map(() => {
            var r = Math.sqrt((maxRadius) / m * -Math.log(Math.random())) * maxRadius,
                d = {
                  cluster: i,
                  radius: r,
                  x: Math.cos(i / m * 2 * Math.PI) * width / 4 + Math.random(),
                  y: Math.sin(i / m * 2 * Math.PI) * height / 4 + Math.random()
                }
  
            return d
          })
  
          // generate cluster node that other nodes in this group orbit around
          let clusterNode = clusters[i] = {
            isClusterNode: true,
            key: group.key,
            label: group.label,
            cluster: i,
            radius: labelRadius,
            x: width / 2,
            y: height / 2
          }
  
          // add cluster node to nodes in this group
          _nodes.push(clusterNode)
  
          // add nodes in this group to all nodes
          nodes = nodes.concat(_nodes)
        })
  
        // define color scale corresponding to clusters
        var color = d3.scaleOrdinal(d3.schemeCategory10)
  
        // define separate forces
        var forceCenter = d3.forceCenter(width / 2, height / 2),
            forceCluster = d3.forceCluster().centers((d) => clusters[d.cluster]).strength(0.5),
            forceCollide = d3.forceCollide((d) => d.radius + padding)
  
        // compose simulation with all forces
        simulation = d3.forceSimulation()
          .force('center', forceCenter)
          .force('cluster', forceCluster)
          .force('collide', forceCollide)
          .velocityDecay(velocityDecay)
          .on('tick', tick)
          .nodes(nodes)
  
        // set up svg
        var svg = selection.append('svg')
          .attr('width', width)
          .attr('height', height)
  
        var nodeElements = svg.append('g')
          .attr('class', 'nodes')
          .selectAll('circle')
          .data(nodes)
          .enter().append('circle')
            .style('fill', (d) => (d.isClusterNode) ? 'none' : color(d.cluster / 10))
            .style('stroke', (d) => (d.isClusterNode) ? '#eee' : 'none')
            .style('stroke-width', (d) => (d.isClusterNode) ? '1px' : 'none')
  
        var labelElements = svg.append('g')
          .attr('class', 'cluster-node-labels')
          .selectAll('text')
          .data(clusters)
          .enter().append('text')
            .style('fill', (d) => color(d.cluster / 10))
            .attr('text-anchor', 'middle')
            .text((d) => d.label)
            .each(function() {
              d3.select(this).call(wrap, { radius: labelRadius })
            })
  
        function tick(e) {
          nodeElements
            .attr('cx', (d) => d.x)
            .attr('cy', (d) => d.y)
            .attr('r', (d) => d.radius)
  
          labelElements
            .attr('transform', (d) => `translate(${d.x}, ${d.y})`)
        }
      })
    }
  
    // --- helpers -----------------------------------------
  
    // wrap text
    function wrap(selection, params) {
      let scaleFactor = (params && params.scaleFactor) ? params.scaleFactor : 0.6,
          lineHeight = (params && params.lineHeight) ? params.lineHeight : 16,
          radius = (params && params.radius) ? params.radius : 100,
          text = selection.text(),
          _words = words(text),
          _targetWidth = targetWidth(text),
          _lines = lines(_words, _targetWidth),
          _textRadius = textRadius(_lines)
  
      // split text into words
      function words(text) {
        let words = text.split(/\s+/g); // To hyphenate: /\s+|(?<=-)/
        if (!words[words.length - 1]) words.pop();
        if (!words[0]) words.shift();
        return words;
      }
  
      // measure simulated text width
      function measureWidth(text) {
        const context = document.createElement("canvas").getContext("2d");
        return context.measureText(text).width;
      }
  
      // calculate target width
      function targetWidth(text) {
        return Math.sqrt(measureWidth(text.trim()) * lineHeight)
      }
  
      // split text into lines
      function lines(words, targetWidth) {
        let line;
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
      function textRadius(lines) {
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
        .attr("y", (d, i) => (i - _lines.length / 2 + 0.8) * lineHeight)
        .text(d => d.text)
    }
  
    // --- accessors ---------------------------------------
    chart.data = function(value) {
      if (!arguments.length) return data
      data = value
      return chart
    }
  
    chart.width = function(value) {
      if (!arguments.length) return width
      width = value
      return chart
    }
  
    chart.height = function(value) {
      if (!arguments.length) return height
      height = value
      return chart
    }
  
    chart.padding = function(value) {
      if (!arguments.length) return padding
      padding = value
      return chart
    }
  
    chart.maxRadius = function(value) {
      if (!arguments.length) return maxRadius
      maxRadius = value
      return chart
    }
  
    chart.labelRadius = function(value) {
      if (!arguments.length) return labelRadius
      labelRadius = value
      return chart
    }
  
    chart.velocityDecay = function(value) {
      if (!arguments.length) return velocityDecay
      velocityDecay = value
      return chart
    }
  
    // --- updater ---------------------------------------
    chart.fadeOut = function(cb) {
      d3.select('.nodes').selectAll('circle')
        .transition()
        .duration(300)
        .attr('r', 0)
        .remove()
  
      d3.select('.cluster-node-labels').selectAll('text')
        .transition()
        .duration(500)
        .style('opacity', 0)
        .remove()
  
      setTimeout(cb, 500)
    }
  
    return chart
  }