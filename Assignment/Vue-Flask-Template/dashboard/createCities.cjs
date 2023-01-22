const fs = require('fs');
const path = require('path');
const { pushScopeId } = require('vue');

const  run = async () => {



    let data = await fs.readFileSync(path.join(__dirname, 'citiesWithCoords.json'));


    let metroData = await fs.readFileSync(path.join(__dirname, 'metros.json'));
        // console.log(data)
        const citiesWithCoords = JSON.parse(data);
        const metros = JSON.parse(metroData);

        let newJson = {
            cities: []
        }
        for (let city of citiesWithCoords.cities) {
            for (let metro of metros) {
                // console.log(metro)
                if (city.name === metro.city) {
                    console.log('found one')
                    city.totalproduction = metro.totalproduction
                    city.year = metro.year
                    city.county = metro.county
                    city.sfproduction = metro.sfproduction
                    city.mfproduction = metro.mfproduction
                    city.mhproduction = metro.mhproduction
                    newJson.cities.push({ ...city })
                }
            }
            // city.totalProduction = metros.city
            // citiesWithCoords[city].totalproduction
        }
        console.log('newJson: ', newJson)
        // let uniqueCities = []
        

        
        // for (let record of jsonData) {
        //     console.log(record.city)
            
        //     // if (!Object.keys(uniqueCities).includes()) {
        //     //     let newRecord = { city: record.city,  lat: '', long: ''  }
        //     //     uniqueCities.push(newRecord)
        //     // }
        // }
        // console.log(uniqueCities)

        fs.writeFile('citiesWithCoords2.json', JSON.stringify(newJson), (err) => {
            if (err) throw err;
            console.log('Data written to file');
        });

          
}
run();