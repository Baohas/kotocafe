        /**
         * Открыть модалку добавления смены
         */
        function openAddModal(date) {
            document.getElementById('modal-date').value = date;
            document.getElementById('modal-date-display').textContent = date.split('-').reverse().join('.');
            document.getElementById('addModal').classList.add('show');
        }

        /**
         * Закрыть модалку
         */
        function closeModal() {
            document.getElementById('addModal').classList.remove('show');
        }

        /**
         * Сохранить новую смену в БД через AJAX (POST /schedule)
         */

    function saveNewShift() {
    const date = document.getElementById('modal-date').value;
    const employee = document.getElementById('modal-employee').value;
    const startTime = document.getElementById('modal-start').value;
    const endTime = document.getElementById('modal-end').value;

    if (!employee || !startTime || !endTime) {
        alert('Заполните все поля!');
        return;
    }

    const payload = {
        date: date,
        employee: employee,
        start_time: startTime,
        end_time: endTime
    };

    console.log('Отправляем:', payload);

    fetch('/schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(payload)     // ← обязательно!
    })
    .then(response => {
        console.log('Статус:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Ответ сервера:', data);
        if (data.success) {
            closeModal();
            location.reload();
        } else {
            alert('Ошибка: ' + (data.error || 'Неизвестно'));
        }
    })
    .catch(err => {
        console.error('Ошибка:', err);
        alert('Не удалось сохранить. Смотрите консоль (F12)');
    });
}

        /**
         * Перейти на текущий месяц/год
         */
        function goToToday() {
            const now = new Date();
            const y = now.getFullYear();
            const m = now.getMonth() + 1;
            window.location.href = `/schedule?year=${y}&month=${m}`;
        }

        /**
         * Простая клиентская фильтрация по сотруднику (по желанию)
         */
        function filterByEmployee() {
            const selected = document.getElementById('employee-select').value;
            const allShifts = document.querySelectorAll('.shift');

            allShifts.forEach(shift => {
                if (!selected) {
                    shift.style.display = 'block';
                } else {
                    shift.style.display = shift.querySelector('.shift-employee').textContent === selected ? 'block' : 'none';
                }
            });
        }

        // Закрытие модалки по клику вне окна
        document.addEventListener('DOMContentLoaded', () => {
            const modal = document.getElementById('addModal');
            modal.addEventListener('click', (e) => {
                if (e.target === modal) closeModal();
            });

            console.log('%c✅ HTML-шаблон графика смен загружен и готов к работе с SQLite', 'color: #8d5f3f; font-weight: bold');
        });