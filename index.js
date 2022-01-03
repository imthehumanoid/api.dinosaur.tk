// Dependancies
const express = require('express');
const axios = require('axios');
const app = express();
const dinos = require('./dinosaurs');
const facts = require('./facts');
const trivia = require('./trivia');
const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));

// Similarity
const srch = (search) => {
  let opts = new Array();
  for (const [key, value] of Object.entries(search)) {
    opts.push(`d.${key.toLowerCase()} === "${value.toLowerCase()}"`);
  };
  return dinos.filter(d => eval(opts.join(' && ')));
};

// Server
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.get('/random', (req, res) => {
  let rand = Math.floor(Math.random() * dinos.length);
  res.json([dinos[rand]]);
});

app.get('/dino/:name', (req, res) => {
  try {
    let yourDino = dinos.filter(d => d.name.split(' ').join('_') === req.params.name);
    if (yourDino.length > 0) {
      res.json(yourDino);
    } else {
      res.sendStatus(404);
    };
    } catch (err) {
      res.sendStatus(404);
    };
});

app.get('/search', (req, res) => {
  try {
    let searchRes = srch(req.query);
    res.json(searchRes);
  } catch (err) {
    res.sendStatus(404);
  }
});

app.get('/fact', (req, res) => {
  let rand = Math.floor(Math.random() * facts.length);
  res.json(facts[rand]);
});

app.get('/trivia', (req, res) => {
  let rand = Math.floor(Math.random() * trivia.length);
  res.json(trivia[rand]);
});

// Examples

app.post('/random-example', async (req, res) => {
  let rand = Math.floor(Math.random() * dinos.length);
  let data = await encodeURIComponent(JSON.stringify([dinos[rand]]));
  res.sendFile(__dirname + '/index.html', {
    headers: {
      random: data
    }
  });
});

const thisDino = new Array();
app.post('/dino-example', async (req, res) => {
  if (req.body.name) {
    thisDino[0] = req.body.name;
  };
  try {
    let yourDino = dinos.filter(d => d.name.split(' ').join('_') === thisDino[0]);
    if (yourDino.length > 0) {
  res.sendFile(__dirname + '/index.html', {
    headers: {
      dino: encodeURIComponent(JSON.stringify(yourDino))
    }
  });
    } else {
  res.sendFile(__dirname + '/index.html', {
    headers: {
      dino: 'Not Found'
    }
  });
    };
    } catch (err) {
      console.log(err)
  res.sendFile(__dirname + '/index.html', {
    headers: {
      dino: 'Not Found'
    }
  });
    };
});

app.post('/search-example', async (req, res) => {
  try {
    let searchRes = srch(req.body.query);
    res.sendFile(__dirname + '/index.html', {
      headers: {
        search: encodeURIComponent(JSON.stringify(searchRes))
      }
    });
  } catch (err) {
    res.sendStatus(404);
  }
});

app.post('/trivia-example', (req, res) => {
  let rand = Math.floor(Math.random() * trivia.length);
  res.sendFile(__dirname + '/index.html', {
    headers: {
      trivia:  encodeURIComponent(JSON.stringify(trivia[rand]))
    }
  });
});

app.listen(3000);
