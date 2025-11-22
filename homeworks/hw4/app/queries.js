
const { MongoClient, ServerApiVersion } = require('mongodb');
const fs = require('fs');
const uri = "mongodb+srv://felix-wang:ShuiGou0307@cluster0.r4we9.mongodb.net/?appName=Cluster0";

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function loadFile(filePath, collection) {
  const lines = fs.readFileSync(filePath, 'utf-8').split('\n');
  const insertPromises = [];
  
  lines.forEach(data => {
    if (data.trim()) {
      try {
        const doc = JSON.parse(data);
        insertPromises.push(collection.insertOne(doc));
      } catch (error) {
        console.error(`Error parsing JSON: ${data}`, error);
      }
    }
  });
  
  await Promise.all(insertPromises);
}

async function insertData(client) {
  const db = client.db("world");
  
  const cities = db.collection("city");
  // If the collection is not empty, skip insertion
  const cityCount = await cities.countDocuments();
  if (cityCount === 0) {
    console.log("Inserting cities...");
    await loadFile("./data/city-mongodb.json", cities);
  }

  const countries = db.collection("country");
  // If the collection is not empty, skip insertion
  const countryCount = await countries.countDocuments();
  if (countryCount === 0) {
    console.log("Inserting countries...");
    await loadFile("./data/country-mongodb.json", countries);
  }

  const languages = db.collection("countrylanguage");
  // If the collection is not empty, skip insertion
  const languageCount = await languages.countDocuments();
  if (languageCount === 0) {
    console.log("Inserting languages...");
    await loadFile("./data/countrylanguage-mongodb.json", languages);
  }
}

async function queryData(client) {
  const db = client.db("world");

  const result1 = await db.collection("countrylanguage").countDocuments({ IsOfficial: "T", Percentage: { $gt: 0.5 } });
  console.log(`Number of official languages with more than 50% speakers: ${result1}`);

  const result2 = await db.collection("country").find({ Continent: /America/, GNP: { $gt: 100000 } }, { Name: 1, GNP: 1, _id: 0 }).toArray();
  result2.forEach(doc => {
    console.log(`Country: ${doc.Name}, GNP: ${doc.GNP}`);
  });

}

async function run() {
  try {
    // Connect the client to the server	(optional starting in v4.7)
    await client.connect();
    // Send a ping to confirm a successful connection
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");

    // Insert data
    await insertData(client);
    console.log("Data insertion completed.");

    // Query data
    await queryData(client);
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
run().catch(console.dir);
