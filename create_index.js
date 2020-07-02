
const elasticsearch = require('elasticsearch');
const client = new elasticsearch.Client({
   hosts: [ 'http://localhost:9200']
});

client.ping({
     requestTimeout: 30000,
 }, function(error) {

     if (error) {
         console.error('Elasticsearch cluster is down!');
     } else {
         console.log('Everything is ok');
     }
 });

 // create a new index called sinhalasongs. If the index has already been created, this function fails safely
client.indices.create({
    index: 'sinhalasongs'
}, function(error, response, status) {
    if (error) {
        console.log(error);
    } else {
        console.log("created a new index", response);
    }
});

// add a data to the index that has already been created
client.index({
    index: 'sinhalasongs',
    id: '1',
    type: 'songs_list',
    body: {
        "album_name_en": "Content for key one",
        "album_name_si": "Content for key one",
        "artist_name_en": "Content for key two",
        "artist_name_si": "Content for key two",
        "artist_rating": "Content for key two",
        "lyrics": "Content for key three",
        "track_id": "Content for key three",
        "track_name_en": "Content for key three",
        "track_name_si": "Content for key three",
        "track_rating": "Content for key three",
    }
}, function(err, resp, status) {
    console.log(resp);
});


const songs = require('./newSongs.json');

var bulk = [];

songs.forEach(song =>{
    console.log("success") 
    bulk.push({index:{ 
            _index:"sinhalasongs", 
            _type:"songs_list",
        }          
    })
  bulk.push(song)
})
//perform bulk indexing of the data passed
client.bulk({body:bulk}, function( err, response  ){
    
    if( err ){ 
        console.log("fail") 
        console.log("Failed Bulk operation".red, err) 
    } else { 
        console.log("pass") 
        console.log("Successfully imported %s".green, songs.length); 
    } 
}); 
