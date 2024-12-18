const express = require('express');
const mysql = require('mysql2/promise');
const pythonScriptPath = '241217.py'; // Python 파일 경로
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path'); // 경로 모듈 추가
const app = express();
const port = 3000;

app.use(express.json()); // JSON 요청 처리
app.use(cors()); // CORS 설정

const { exec } = require('child_process');
const util = require('util');

// exec를 Promise 기반으로 사용하기 위해 promisify
const pythonExecutable = '/Users/wang-wooseok/Downloads/fixcode/myenv/bin/python3';
const execPromise = util.promisify(exec);

// Python 스크립트 실행 함수
async function runPythonScript() {
  const pythonScriptPath = '241217.py'; // Python 스크립트 파일 경로
  console.log('Python 스크립트를 실행합니다...');

  try {
    // Python 실행
    const { stdout, stderr } = await execPromise(`${pythonExecutable} ${pythonScriptPath}`);
    if (stderr) {
      console.error('Python stderr:', stderr);
      throw new Error(stderr);
    }
    console.log('Python 실행 결과:', stdout);
    return stdout; // Python 실행 결과 반환
  } catch (error) {
    console.error('Python 실행 중 오류 발생:', error.message);
    throw error; // 오류를 호출한 함수에 전달
  }
}


// 한국어 -> 영어 매핑 객체
const styleMapping = {
  '캐주얼': 'Casual',
  '스트릿': 'Street',
  '미니멀': 'Minimal',
  '아메카지': 'Amekaji',
  // 다른 스타일을 추가할 수 있습니다.
};

const seasonMapping = {
  '봄': 'Spring',
  '여름': 'Summer',
  '가을': 'Autumn',
  '겨울': 'Winter',
  // 다른 계절을 추가할 수 있습니다.
};

const colorMapping = {
  '베이지': 'Beige',
  '네이비': 'Navy',
  '올리브': 'Olive',
  '브라운': 'Brown',
  '화이트': 'White',
  '연청': 'Light Blue',
  '청바지': 'Denim',
  '카키': 'Khaki',
  '버건디': 'Burgundy',
  '파스텔': 'Pastel',
  '회색': 'Gray',
  '블랙': 'Black',
  '블루': 'Blue'
};

function mapToEnglish(value, mapping) {
  return mapping[value] || value; // 매핑에 없으면 원래 값을 반환
}

// CSV 로그 파일 경로
const logFilePath = path.join(__dirname, 'logs.csv');

// 로그 데이터를 CSV 파일에 저장하는 함수
async function logToCSV(logData) {
  const timestamp = new Date().toISOString();
  const logEntry = `${timestamp},${logData}\n`;

  try {
    await fs.appendFile(logFilePath, logEntry, 'utf8');
    console.log('로그가 CSV 파일에 저장되었습니다:', logEntry);
  } catch (err) {
    console.error('CSV 파일에 로그 저장 중 오류 발생:', err);
  }
}

// MySQL 연결
const dbConfig = {
  host: '127.0.0.1',
  user: 'root',
  password: '1234qwer',
  database: 'clothing_recommendation' // 데이터베이스 명시
};

// MySQL 연결 풀 생성
let db;
(async () => {
  try {
    db = await mysql.createPool(dbConfig); // createPool만 사용
    console.log('MySQL 데이터베이스에 연결되었습니다.');
  } catch (err) {
    console.error('데이터베이스 연결 오류:', err.message);
    process.exit(1); // 연결 실패 시 프로세스 종료
  }
})();


// **1. Submit API**
app.post('/submit', async (req, res) => {
  const { season, style, color, height, weight, waist } = req.body;

  if (!season || !style || !height || !weight || !waist) {
    return res.status(400).send('Missing required fields.');
  }


  try {
    const query = 'INSERT INTO TempInput (season, height_cm, weight_kg, waist_cm, style, preferred_color) VALUES (?, ?, ?, ?, ?, ?)';
    await db.execute(query, [season, height, weight, waist, style, color || null]);

    logToCSV(`Submit Success: ${JSON.stringify(req.body)}`);
    res.status(200).json({ message: 'Data successfully inserted into TempInput.' });
  } catch (err) {
    logToCSV(`Submit Error: ${err.message}`);
    res.status(500).json({ error: 'Error inserting data into TempInput.' });
  }
});

// **2. get-data API**
app.get('/get-data', async (req, res) => {
  try {
    const [results] = await db.execute('SELECT * FROM TempInput');
    logToCSV(`Get Data Success: ${JSON.stringify(results)}`);
    res.status(200).json(results);
  } catch (err) {
    logToCSV(`Get Data Error: ${err.message}`);
    res.status(500).json({ error: 'Error fetching TempInput data.' });
  }
});

// **4. get-waist API**
app.get('/get-waist', async (req, res) => {
  try {
    const [result] = await db.execute('SELECT waist_cm FROM TempInput ORDER BY temp_id DESC LIMIT 1');

    if (result.length === 0) {
      return res.status(404).json({ error: 'No data found in TempInput.' });
    }
    logToCSV(`Get Waist Success: ${JSON.stringify(result[0])}`);
    res.status(200).json({ waist_cm: result[0].waist_cm });
  } catch (err) {
    logToCSV(`Get Waist Error: ${err.message}`);
    res.status(500).json({ error: 'Error fetching waist data.' });
  }
});

// **5. get-size-info API**
app.get('/get-size-info', async (req, res) => {
  try {
    const [result] = await db.execute('SELECT outer_size, top_size FROM SizeInfo ORDER BY size_id DESC LIMIT 1');

    if (result.length === 0) {
      return res.status(404).json({ error: 'No size info found.' });
    }
    logToCSV(`Get Size Info Success: ${JSON.stringify(result[0])}`);
    res.status(200).json(result[0]);
  } catch (err) {
    logToCSV(`Get Size Info Error: ${err.message}`);
    res.status(500).json({ error: 'Error fetching size info.' });
  }
});

// **6. get-outfit-recommendations API**
app.get('/get-outfit-recommendations', async (req, res) => {
  try {
    const [tempInput] = await db.execute('SELECT style, season FROM TempInput ORDER BY temp_id DESC LIMIT 1');
    if (tempInput.length === 0) return res.status(404).json({ error: 'No TempInput data found.' });

    const style = mapToEnglish(tempInput[0].style, styleMapping);
    const season = mapToEnglish(tempInput[0].season, seasonMapping);

    const [outfits] = await db.execute('SELECT outerwear, top, bottom FROM OutfitRecommendation WHERE style = ? AND season = ? LIMIT 3', [style, season]);
    if (outfits.length === 0) return res.status(404).json({ error: 'No outfit recommendations found.' });

    logToCSV(`Outfit Recommendations Success: ${JSON.stringify(outfits)}`);
    res.status(200).json(outfits);
  } catch (err) {
    logToCSV(`Outfit Recommendations Error: ${err.message}`);
    res.status(500).json({ error: 'Error fetching outfit recommendations.' });
  }
});



// **7. get-color-matching API**
app.get('/get-color-matching', async (req, res) => {
  try {
    // 1. TempInput에서 최근 데이터 조회
    const [tempInput] = await db.execute(
      'SELECT style, season, preferred_color FROM TempInput ORDER BY temp_id DESC LIMIT 1'
    );

    if (tempInput.length === 0) {
      logToCSV('No TempInput data found');
      return res.status(404).json({ error: 'No TempInput data found.' });
    }

    console.log('TempInput 데이터:', tempInput);

    // 2. 스타일, 계절, 선호 색상 매핑
    const style = mapToEnglish(tempInput[0].style, styleMapping);
    const season = mapToEnglish(tempInput[0].season, seasonMapping);
    const preferredColor = mapToEnglish(tempInput[0].preferred_color, colorMapping);

    console.log('매핑된 데이터:', { style, season, preferredColor });

    // 3. ColorMatching 테이블 조회
    const [colors] = await db.execute(
      'SELECT top_color, bottom_color, outer_color FROM ColorMatching WHERE style = ? AND season = ? AND (top_color = ? OR bottom_color = ?) LIMIT 3',
      [style, season, preferredColor, preferredColor]
    );

    if (colors.length === 0) {
      logToCSV('No color matching recommendations found');
      console.log('ColorMatching 데이터 없음');
      return res.status(404).json({ error: 'No color matching recommendations found.' });
    }

    console.log('ColorMatching 데이터:', colors);

    // 4. 로그 파일에 데이터 저장
    logToCSV(`Color Matching Success: ${JSON.stringify(colors)}`);

    // **5. Python 스크립트 실행**
    console.log('Python 스크립트 실행 시작...');
    const pythonOutput = await runPythonScript();
    console.log('Python 실행 결과:', pythonOutput);

    // 6. 최종 결과 반환
    res.status(200).json({
      colorMatching: colors,
      pythonOutput: pythonOutput.trim(), // Python 출력 결과
    });

  } catch (err) {
    // 오류 발생 시 처리
    logToCSV(`Color Matching or Python Error: ${err.message}`);
    console.error('에러 발생:', err.message);
    res.status(500).json({ error: 'Error fetching color matching or running Python script.', details: err.message });
  }
});



// 서버 실행
app.listen(port, () => {
  console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
  logToCSV(`Server started at http://localhost:${port}`); // 로그 저장
});

