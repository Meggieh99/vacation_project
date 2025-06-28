document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/vacations/')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('vacations');
        data.forEach(vacation => {
            container.innerHTML += `<div>${vacation.description} (${vacation.price}$)</div>`;
        });
    })
    .catch(err => console.error(err));
});
