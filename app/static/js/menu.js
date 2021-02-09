const menu = document.querySelector('.menu');
const option = document.querySelector('.menu span')

menu.addEventListener('click', e => {
  if (e.target.classList.contains('menu') || e.target.classList.contains('select') || e.target.classList.contains('menu__icon')) {
      menu.classList.toggle('menu__active');
  }

  if (e.target.classList.contains('menu__dropdown-option')) {
      option.innerHTML = e.target.textContent;
      menu.classList.remove('menu__active');
  }
})