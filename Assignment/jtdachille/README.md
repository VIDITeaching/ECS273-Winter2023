Requires [node.js](https://nodejs.org/en/) and [Python](https://www.python.org/downloads/) <br />
Make sure the node.js version is either v14.18.0+ or v16.0.0+, which is **required** for Vite to work normally.

See ./preview.png for desired output

Install Python packages
```bash
cd jtdachille
pip3 install -r requirements.txt
```

Install packages from package.json
```bash
cd dashboard 
npm install
```

To start the application, under `./Assignment/jtdachille/dashboard`, run
```bash
npm run start
```
You can then visit `localhost:3000` in the browser to see the interface.

If server crashes with SIGSEGV, add ` --python=python3` option to `npm run` command