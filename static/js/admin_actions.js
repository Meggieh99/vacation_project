console.log('admin_actions.js loaded!');

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('.delete-btn');

  deleteButtons.forEach(button => {
    button.addEventListener('click', async function () {
      const vacationId = this.dataset.vacationId;

      if (!confirm('Are you sure you want to delete this vacation?')) {
        return;
      }

      try {
        const response = await fetch(`/api/vacations/${vacationId}/delete/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          },
          credentials: 'include'
        });

        if (response.ok) {
          location.reload();
        } else {
          const errorData = await response.json();
          alert('Error: ' + JSON.stringify(errorData));
        }
      } catch (err) {
        alert('Error: ' + err.message);
      }
    });
  });
});
