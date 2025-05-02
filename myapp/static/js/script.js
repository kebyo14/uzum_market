document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('searchInput');
    const productCards = document.querySelectorAll('.product-card');
  
    input.addEventListener('input', function () {
      const query = input.value.toLowerCase();
  
      productCards.forEach(card => {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        if (title.includes(query)) {
          card.style.display = 'block';  // показать
        } else {
          card.style.display = 'none';   // скрыть
        }
      });
    });
  });
