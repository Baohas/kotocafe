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
         * Простая клиентская фильтрация по сотруднику
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

            console.log('Все ок!');
        });
/**
 * Открыть модалку редактирования
 */
function openEditModal(element) {
    const id       = element.dataset.id;
    const date     = element.dataset.date;
    const employee = element.dataset.employee;
    const start    = element.dataset.start;
    const end      = element.dataset.end;

    document.getElementById('edit-id').value = id;
    document.getElementById('edit-date').value = date;
    document.getElementById('edit-date-display').textContent = date.split('-').reverse().join('.');

    document.getElementById('edit-employee').value = employee;
    document.getElementById('edit-start').value = start;
    document.getElementById('edit-end').value = end;

    document.getElementById('editModal').classList.add('show');
}

/**
 * Закрыть модалку редактирования
 */
function closeEditModal() {
    document.getElementById('editModal').classList.remove('show');
}

/**
 * Сохранить изменения смены
 */
function saveEditShift() {
    const id        = document.getElementById('edit-id').value;
    const date      = document.getElementById('edit-date').value;
    const employee  = document.getElementById('edit-employee').value;
    const startTime = document.getElementById('edit-start').value;
    const endTime   = document.getElementById('edit-end').value;

    const payload = {
        id: id,
        date: date,
        employee: employee,
        start_time: startTime,
        end_time: endTime
    };

    fetch('/schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeEditModal();
            location.reload();
        } else {
            alert('Ошибка: ' + (data.error || 'Неизвестно'));
        }
    })
    .catch(err => {
        console.error(err);
        alert('Не удалось сохранить изменения');
    });
}