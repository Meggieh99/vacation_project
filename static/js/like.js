console.log('like.js loaded!');

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
  const buttons = document.querySelectorAll('.like-btn');

  buttons.forEach(button => {
    button.addEventListener('click', async function () {
      const vacationId = this.dataset.vacationId;
      const liked = this.dataset.liked === 'true';

      const url = liked
        ? `/api/vacations/${vacationId}/unlike/`
        : `/api/vacations/${vacationId}/like/`;

      try {
        const response = await fetch(url, {
          method: 'POST',
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
