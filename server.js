const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());
app.use(cors()); // CORS 허용

// MySQL 연결
const db = mysql.createConnection({
  host: '127.0.0.1',
  user: 'root',
  password: '1234qwer',
  database: 'clothing_recommendation',
});

db.connect(err => {
  if (err) {
    console.error('데이터베이스 연결 오류:', err);
    return;
  }
  console.log('MySQL 데이터베이스에 연결되었습니다.');
});

// 데이터 삽입 API
app.post('/submit', (req, res) => {
  const { season, style, color, height, weight, waist } = req.body;

  console.log('요청 데이터:', req.body);

  if (!season || !style || !height || !weight || !waist) {
    console.error('필수 필드가 누락되었습니다.');
    return res.status(400).send('Missing required fields.');
  }

  const query = 'INSERT INTO TempInput (season, height_cm, weight_kg, waist_cm, style, preferred_color) VALUES (?, ?, ?, ?, ?, ?)';
  const values = [season, height, weight, waist, style, color || null];

  db.query(query, values, (err, result) => {
    if (err) {
      console.error('데이터 삽입 중 오류 발생:', err);
      return res.status(500).send('Error inserting data into the database.');
    }
    console.log('삽입 결과:', result);
    res.status(200).send('Data successfully inserted into the database.');
  });
});

// 데이터 조회 API (기존 내용 유지)
app.get('/get-data', (req, res) => {
  db.query('SELECT * FROM TempInput', (err, results) => {
    if (err) {
      console.error('Error fetching data:', err);
      return res.status(500).send('Error fetching data from the database.');
    }

    const formattedResults = results.map(row => {
      for (let key in row) {
        if (typeof row[key] === 'bigint') {
          row[key] = row[key].toString();
        }
      }
      return row;
    });

    console.log('Formatted Results:', formattedResults);
    res.status(200).json(formattedResults);
  });
});

// 서버 실행
app.listen(port, () => {
  console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
});
