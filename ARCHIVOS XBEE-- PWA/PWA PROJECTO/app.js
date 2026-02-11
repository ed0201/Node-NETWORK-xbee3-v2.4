let port;
let reader;
let inputDone;
let inputStream;
let chart;

// CONFIGURACIÓN DE LA GRÁFICA (CHART.JS)
const ctx = document.getElementById('sensorChart').getContext('2d');
chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Tiempo
        datasets: [{
            label: 'Temperatura (°C)',
            borderColor: '#e74c3c',
            data: [],
            yAxisID: 'y',
        }, {
            label: 'Humedad (%)',
            borderColor: '#3498db',
            data: [],
            yAxisID: 'y1',
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false, // Desactivar animación para mejor rendimiento real-time
        scales: {
            y: { position: 'left', title: {display: true, text: 'Temp °C'} },
            y1: { position: 'right', title: {display: true, text: 'Humedad %'}, grid: {drawOnChartArea: false} }
        }
    }
});

// --- LÓGICA DE CONEXIÓN SERIAL (WEB SERIAL API) ---
document.getElementById('connectBtn').addEventListener('click', async () => {
    
    try {
        port = await navigator.serial.requestPort();
        await port.open({ baudRate: 115200 }); 
        
        document.getElementById('statusLog').innerText = "Conectado. Esperando datos...";
        document.getElementById('connectBtn').disabled = true;
        document.getElementById('connectBtn').innerText = "Conectado";

       
        const textDecoder = new TextDecoderStream();
        inputDone = port.readable.pipeTo(textDecoder.writable);
        inputStream = textDecoder.readable;
        reader = inputStream.getReader();

        readLoop();
    } catch (err) {
        console.error("Error al conectar:", err);
        document.getElementById('statusLog').innerText = "Error: " + err;
    }
});

// BUCLE DE LECTURA
async function readLoop() {
    let buffer = ""; 
    
    while (true) {
        const { value, done } = await reader.read();
        if (done) { break; }
        
        buffer += value;
        
        let lines = buffer.split('\n');
        buffer = lines.pop(); 
        for (const line of lines) {
            processData(line.trim());
        }
    }
}

// PROCESAR EL MENSAJE: "T:23.50,H:40.20"
function processData(line) {
    
    if (line.includes("T:") && line.includes("H:")) {
        try {
            
            const parts = line.split(','); 
            const tempStr = parts[0].split(':')[1]; 
            const humStr = parts[1].split(':')[1];  

            const temp = parseFloat(tempStr);
            const hum = parseFloat(humStr);

            updateDashboard(temp, hum);
        } catch (e) {
            console.log("Error parseando línea:", line);
        }
    } else {
        
        document.getElementById('statusLog').innerText = "Log: " + line;
    }
}

function updateDashboard(temp, hum) {
    // 1. Actualizar números a la izquierda
    document.getElementById('tempValue').innerText = temp.toFixed(1);
    document.getElementById('humValue').innerText = hum.toFixed(1);

    // 2. Actualizar Gráfica
    const now = new Date().toLocaleTimeString();
    
    // Agregar datos nuevos
    chart.data.labels.push(now);
    chart.data.datasets[0].data.push(temp);
    chart.data.datasets[1].data.push(hum);

    // Mantener solo los últimos 20 puntos para que la gráfica no se sature
    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }
    
    chart.update();
}