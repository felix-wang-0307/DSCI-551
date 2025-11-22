const { MongoClient, ServerApiVersion } = require('mongodb');

const uri = "mongodb+srv://felix-wang:ShuiGou0307@cluster0.r4we9.mongodb.net/?appName=Cluster0";
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function testCollectionAccess() {
  try {
    await client.connect();
    const db = client.db("world");
    
    console.log("=== 测试集合访问方式 ===");
    
    // 方式1: 使用 db.collection() 方法
    console.log("1. 使用 db.collection('countrylanguage'):");
    console.log("   类型:", typeof db.collection("countrylanguage"));
    console.log("   是否有 countDocuments 方法:", typeof db.collection("countrylanguage").countDocuments);
    
    // 方式2: 尝试直接访问属性
    console.log("\n2. 尝试使用 db.countrylanguage:");
    console.log("   类型:", typeof db.countrylanguage);
    console.log("   值:", db.countrylanguage);
    
    // 显示 db 对象的可用方法
    console.log("\n3. db 对象的可用方法:");
    console.log("   ", Object.getOwnPropertyNames(db).filter(name => typeof db[name] === 'function').slice(0, 10));
    
  } finally {
    await client.close();
  }
}

testCollectionAccess().catch(console.error);
