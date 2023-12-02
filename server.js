var sqlite3 = require("sqlite3");
var express = require("express");
var bodyParser = require('body-parser');
var crypto = require('crypto');
const cookieParser = require('cookie-parser');

var app = express();
app.set('view engine', 'ejs');
app.use(express.json());
app.use(bodyParser.urlencoded({'extended':true}));
app.use(cookieParser());

const dbFilePath = "core/dbs/accounts.db";
const dbFilePathCache = "core/dbs/cache.db";

app.use('/bootstrap', express.static(__dirname + '/node_modules/bootstrap/dist'))
app.use('/bootstrap-icons', express.static(__dirname + '/node_modules/bootstrap-icons/font'))
app.use('/jquery', express.static(__dirname + '/node_modules/jquery/dist'))
app.use('/plugins', express.static(__dirname + '/plugins'))

app.get('/', function(req, res) {
    var cookie = req.cookies.session;
    if (cookie === undefined) {
        res.render('index');
    } else{
        // cookie exists, check if valid
        var db = new sqlite3.Database(dbFilePathCache);
        db.get("SELECT * FROM sessions WHERE code = ?", [Buffer.from(cookie, 'base64').toString('ascii')], function(err, row) {
            if (row === undefined) {
                res.render('index');
            } else {
                // check if cookie expired
                var now = new Date();
                var expiry = new Date(row.expiry);
                if (now > expiry) {
                    res.render('index');
                } else {
                    res.redirect('/dashboard');
                }
            }
        });
    }
});

app.get('/dashboard',(req,res)=>{
    var cookie = req.cookies.session;
    if (cookie === undefined) {
        res.redirect('/');
    } else{
        // cookie exists, check if valid
        let db = new sqlite3.Database(dbFilePathCache);
        db.get("SELECT * FROM sessions WHERE code = ?", [Buffer.from(cookie, 'base64').toString('ascii')], function(err, row) {
            if (row === undefined) {
                res.redirect('index');
            } else {
                // check if cookie expired
                var now = new Date();
                var expiry = new Date(row.expiry);
                if (now > expiry) {
                    res.redirect('/');
                }
            }
        });
    }
    let db = new sqlite3.Database(dbFilePath,(err)=>{
        if(!err){
            db.all('SELECT * FROM users', (err,data)=>{
                if(err){
                    console.log(err);
                }else{
                    res.render('dashboard', { users: data });
                }
            });
            db.close()
        }else{
            console.log("ERROR: " + err.message);
        }
    })
})

// create post route /login to handle login request
app.post('/login', (req, res) => {
    // check if user exists
    let db = new sqlite3.Database(dbFilePath,(err)=>{
        if(!err){
            db.all('SELECT * FROM admins WHERE username = ? AND password = ?', [req.body.username, crypto.createHash('sha512').update(req.body.password).digest('hex')], (err,data)=>{
                if(err){
                    console.log(err);
                }else{
                    if(data.length > 0){
                        var session_code = crypto.createHash('sha512').update(req.body.username + Date.now() + "g2S%hbJ9RN#7TJwu").digest('hex'); 
                        var based_session = Buffer.from(session_code).toString('base64')
                        res.cookie('session', based_session, { maxAge: 1000 * 60 * 60})
                        let db = new sqlite3.Database(dbFilePathCache,(err)=>{
                            if(!err){
                                db.run('INSERT INTO sessions (code, expiry) VALUES (?, ?)', [session_code, new Date(Date.now() + 1000 * 60 * 60)], function(err) {
                                    if (err) {
                                        return console.log(err.message);
                                    }
                                });
                                db.close()
                            }
                        });
                        res.redirect('/dashboard');
                    }else{
                        res.redirect('/');
                    }
                }
            });
            db.close()
        }else{
            console.log("ERROR: " + err.message);
        }
    })
})


app.post("/create_user",(req,res)=>{
    let fname = req.body.fname
    let lname = req.body.lname
    let uid = req.body.uid
    let locker = req.body.locker
    let db = new sqlite3.Database(dbFilePath,(err)=>{
        if(!err) {
            db.run(`INSERT INTO users(first_name, last_name, uid, locker) VALUES(?, ?, ?, ?)`, [fname, lname, uid, locker], function(err) {
                if (err) {
                  console.log(err.message);
                  return res.sendStatus(500)
                }
                
                return res.sendStatus(200)
              })
              db.close()
        }else {
            return res.sendStatus(500)
        }
    }) 
})

app.post("/delete_user",(req,res)=>{
    let uid = req.body.uid
    let db = new sqlite3.Database(dbFilePath,(err)=>{
        if(!err) {
            db.run(`DELETE FROM users WHERE uid=?`, [uid], function(err) {
                if (err) {
                  console.log(err.message)
                  return res.sendStatus(500)
                }
                
                return res.sendStatus(200)
              })
              db.close()
        }else {
            return res.sendStatus(500)
        }
    })
})

app.post("/update_user",(req,res)=>{
    let fname = req.body.fname
    let lname = req.body.lname
    let uid = req.body.uid
    let new_uid = req.body.new_uid
    let locker = req.body.locker
    let db = new sqlite3.Database(dbFilePath,(err)=>{
        if(!err){
            db.run('UPDATE users SET first_name=?, last_name=?, uid=?, locker=? WHERE uid=?', [fname, lname, new_uid, locker, uid], (err)=>{
                if (err) {
                    console.log(err.message);
                    return res.sendStatus(500)
                }
                  
                return res.sendStatus(200)
            })
            db.close()
        }
    })
})


app.listen(8181, () => {
    console.log("RFID Locker System | Webinterface is running on port 8181");
})