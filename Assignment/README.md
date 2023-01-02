# Warmup for Developing Visualization Dashboards

In this assignment, you will be working on a visualization dashboard template to get prepared for the final project. <br />
Your task is to implement two visualization views, with at least one view allowing supporting one kind of user interactions, and place the two views side by side.

This dashboard template is a web-based application in TypeScript and Python, using Vue 3, Flask, D3.js, and [Vite](https://vitejs.dev/guide/). <br />

To begin, you need to first fork this repository. <br />
After the fork, clone the repository using the following commands:

```bash
    git clone https://github.com/<your-github-account-name>/ECS273-Winter2023
    cd ECS273-Winter2023/Assignment
```

Create a new folder inside the Assignment directory in the forked repository. The name of the folder should be the same as your UC Davis email account name (without ' @ucdavis.edu'). <br/>
**Inside this folder, you will add all your code.**

Before coding, please go over some of the following tutorials:
* D3: [Introduction](https://d3js.org/#introduction), [Core concepts](https://d3-graph-gallery.com/intro_d3js.html), [Selection](https://www.d3indepth.com/selections/), [Data Joins](https://www.d3indepth.com/datajoins/)

If you need to learn more about JavaScript, you can refer to [A re-introduction to JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript)



Besides the guidance in the code base, we provide a simple interactive visualization demo to support your exploration. <br />
This demo has 3 incremental examples to demonstrate the general logic. <br />
We recommend you spend time understanding the demo, as it will help you succeed in this assignment and the final project.

## Setting up Everything

### Step 1. Choose a Dataset
In this assignment, you can choose one of the datasets mentioned on any data type page in the [Pages](https://canvas.ucdavis.edu/courses/772842/pages).

To use a dataset, you can either
- download the data file from the respective URL above and put it in the `./Vue-Flask-Template/server/data` folder, or
- fetch the data via API or library functions (if applicable) in the `./Vue-Flask-Template/server/controller.py`


### Step 2. Set up the Application

To get started, we will be using the aforementioned framework, as seen in `./Assignment/Vue-Flask-Template`.

Note that you are free to use other existing frameworks and libraries (e.g., React), even in different languages, to implement the system. We pick Vue.js as it is easier to pick up. <br />
If you use a framework or library to create your system, please provide a README.md file explaining all the steps to run and view your system.


Install [node.js](https://nodejs.org/en/) and [Python](https://www.python.org/downloads/) if not yet. <br />
Make sure the node.js version is either v14.18.0+ or v16.0.0+, which is **required** for Vite to work normally.

Install Python packages
```bash
cd Vue-Flask-Template
pip3 install -r requirements.txt
```
Install packages from package.json
```bash
cd dashboard 
npm install
```
To start the application, under `./Assignment/Vue-Flask-Template/dashboard`, run
```bash
npm run start
```
You can then visit `localhost:3000` in the browser to see the interface.

Install additional packages for your needs
```bash
pip3 install <package-name> # for Python
# or for JavaScript 
npm install <package-name>
```

\*This template has been tested with Python3.10.8 and Node.js v19.3.0.

---

## Part 1. Create Two Static Visualizations

Your task is to implement two visualization views, with at least one view providing appropriate one kind of user interactions, and place the two views side by side. Detailed requirements are listed below.

### Examples of visualization methods

Note that you have to pick different methods. For example, creating a bar chart and a histogram only counts as using only one method, since their implementation is nearly the same. 

**Fundamental**
 - Bar chart or histogram
 - Pie or donut chart
 - Line and area chart
 - 2D heatmap or matrix view
 - Scatter plot
 - Node-link diagram
 - Geographical map

**Advanced**
 - Parallel set or parallel coordinates plot
 - Sankey or alluvial diagram
 - Star coordinates or plot
 - Chord diagram
 - Stream graph
 - Arc diagram
 - Dendrogram

## Part 2. Bring in Interactivity
You can focus on one of the views and provide at least one kind of appropriate user interactions. For example, zooming in/out a bar chart is not informative and is thus inappropriate; however, it is fine to zoom in/out a line chart or a scatter plot to provide detailed inspection or avoid visual clutter. <br />
In other words, your choice of user interaction shall benefit the user in some way, such as supporting the data exploration, drilling down critical details, or facilitate analytical reasoning; otherwise, don't implement it.

### Examples of user interactions
 * Interface widgets
   * Dropdown menu (e.g., select different techniques/hyperparameters)
   * Slider (e.g., filter based on data attributes)
   * Input (e.g., key in keywords)
 * Tooltip
 * Brush
 * Zoom (+ Pan)

# Requirements
 - The dashboard must have at least two visualizations, which should be created with at least two different visualization methods (see above).
 - At least one of the views should support one kind of appropriate user interactions at minimum (see above).
 - **Legends** for each view need to be provided as well as **axis labels** and **chart titles**.
 - The two visualizations should be placed **side by side** and fit on a fullscreen browser.
 - The data used in these visualizations **must** be fetched from the server. 
 - The demo examples **cannot** be counted as one of the views, even if it reads a different dataset.
 - Choose appropriate visual encodings.
 - Color choice matters and has an effect on the interpretability of the visualization. Depending on the data, the type of color scale you use will change (e.g., categorical, linear, etc).
 - Carefully consider the design for each encoding that you will use and its effectiveness for portraying the data. Depending on the data you are visualizing, certain pairings of marks and channels will be more effective.
 - Carefully choose the user interactions and consider their effectiveness for supporting data exploration and/or analytical reasoning. 
 - The visualizations should depict different dimensions or aspects of the dataset to be examined. So you are encouraged to perform data analysis with our templates (`./server/resources`) as they are helpful.


# Submission
To submit for this assignment, you need to first [fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) this [repository](https://github.com/VIDITeaching/ECS273-Winter2023). After the fork, clone the forked repository using the following commands: 

```bash
    git clone https://github.com/<your-github-account-name>/ECS273-Winter2023
    cd ECS273-Winter2023/Assignment
```

Create a new folder inside the Assignment directory in the forked repository. The name of the folder should be the same as your UC Davis email account name (without ' @ucdavis.edu'). Put all your codes inside this folder, and use "git add" to add all your codes, and then commit. 
```bash
git add <your-filename> 
git commit -m "Assignment" 
git push
```
After you push your code to your repository, follow the instruction [here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) to create a pull request for this repository. <br />
Finally, submit the hyperlink of the pull request to UCD Canvas. The hyperlink should look like this - "https://github.com/VIDITeaching/ECS273-Winter2023/pull/{your-pull-request-id}".