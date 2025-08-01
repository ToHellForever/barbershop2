// Динамическая подгрузка услуг выбранного мастера на форме заказа
document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.querySelector('.js-master-select');
    const servicesContainer = document.getElementById('services-container');

    if (!masterSelect || !servicesContainer) return;

    function loadServices(masterId) {
        fetch(`/api/master_services/?master_id=${masterId}`)
            .then(response => response.json())
            .then(data => {
                let html = '';
                if (data.services.length > 0) {
                    html += '<p class="mb-1">Выберите услуги:</p><div class="row">';
                    data.services.forEach(service => {
                        html += `
                            <div class="col-6 form-check">
                                <input type="checkbox" name="services" value="${service.id}" class="form-check-input" id="service_${service.id}">
                                <label class="form-check-label" for="service_${service.id}">${service.name}</label>
                            </div>
                        `;
                    });
                    html += '</div>';
                } else {
                    html = '<p class="text-muted">Услуги не найдены для выбранного мастера.</p>';
                }
                servicesContainer.innerHTML = html;
            });
    }

    masterSelect.addEventListener('change', function() {
        loadServices(this.value);
    });
    // Подгрузить услуги сразу, если мастер выбран
    if (masterSelect.value) {
        loadServices(masterSelect.value);
    }
});

// Fункция для обновления текущего года в подвале
document.addEventListener("DOMContentLoaded", function() {
    var yearElement = document.getElementById("current-year");
    if (yearElement) {
        var currentYear = new Date().getFullYear();
        yearElement.textContent = currentYear;
    }
});