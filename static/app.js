// static/app.js

const API_URL = 'http://127.0.0.1:8000'; // Адрес вашего локального сервера

async function fetchSystemStatus() {
    try {
        const response = await fetch(`${API_URL}/api/status`);
        if (!response.ok) return;
        const data = await response.json();
        
        const currentDayElement = document.getElementById('currentDay');
        const totalMeasurementsElement = document.getElementById('totalMeasurements');
        
        if (currentDayElement) currentDayElement.innerText = data.current_day;
        if (totalMeasurementsElement) totalMeasurementsElement.innerText = data.measurements_count;
    } catch (error) {
        console.error('Ошибка подключения к серверу:', error);
    }
}

async function fetchStatistics() {
    try {
        const response = await fetch(`${API_URL}/api/statistics/`);
        if (!response.ok) return;
        const data = await response.json();
        
        const avgLevelElement = document.getElementById('avgLevel');
        const maxLevelElement = document.getElementById('maxLevel');
        
        if (avgLevelElement) avgLevelElement.innerText = data.average_level || '0';
        if (maxLevelElement) maxLevelElement.innerText = data.max_level || '0';
    } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
    }
}

async function saveMeasurement() {
    const levelField = document.getElementById('levelField');
    const notesField = document.getElementById('notesField');
    const outputBox = document.getElementById('outputBox');
    
    if (!levelField || !levelField.value) {
        alert('Пожалуйста, укажите уровень напряжения.');
        return;
    }

    const payload = {
        level: parseInt(levelField.value, 10),
        notes: notesField ? notesField.value : null
    };

    try {
        const response = await fetch(`${API_URL}/api/measurements/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Не удалось сохранить данные.');
        }

        const data = await response.json();
        if (outputBox) {
            outputBox.innerHTML = `
                <strong>Запись успешно сохранена:</strong><br>
                День: ${data.day} | Уровень: ${data.level} | Система: ${data.system_verdict}
            `;
        }

        // Обновляем статистику и статус
        fetchSystemStatus();
        fetchStatistics();
    } catch (error) {
        alert(`Ошибка: ${error.message}`);
    }
}

async function clearDatabase() {
    try {
        const response = await fetch(`${API_URL}/api/measurements/`, {
            method: 'DELETE'
        });

        if (response.ok) {
            const outputBox = document.getElementById('outputBox');
            if (outputBox) outputBox.innerHTML = 'Архив данных очищен.';
            
            const avgLevelElement = document.getElementById('avgLevel');
            const maxLevelElement = document.getElementById('maxLevel');
            
            if (avgLevelElement) avgLevelElement.innerText = '0';
            if (maxLevelElement) maxLevelElement.innerText = '0';
            
            fetchSystemStatus();
        }
    } catch (error) {
        console.error('Ошибка очистки:', error);
    }
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    fetchSystemStatus();
    fetchStatistics();
});
