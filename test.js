fetch('metros.json')
    .then(response => response.json())
    .then(data => {
        console.log('data: ', data)
        // Do something with the data
    });