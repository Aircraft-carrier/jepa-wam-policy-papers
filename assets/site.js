const input = document.querySelector('#search');
const cards = [...document.querySelectorAll('.paper-card')];
const empty = document.querySelector('#empty');
let active = 'all';

function update() {
  const query = (input?.value || '').toLowerCase().trim();
  let visible = 0;
  cards.forEach((card) => {
    const matchesText = card.dataset.search.includes(query);
    const matchesTag = active === 'all' || card.dataset.tags.split(' ').includes(active);
    card.style.display = matchesText && matchesTag ? '' : 'none';
    if (matchesText && matchesTag) visible += 1;
  });
  if (empty) empty.style.display = visible ? 'none' : 'block';
}

input?.addEventListener('input', update);
document.querySelectorAll('.filter').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelector('.filter.active')?.classList.remove('active');
    button.classList.add('active');
    active = button.dataset.filter;
    update();
  });
});
