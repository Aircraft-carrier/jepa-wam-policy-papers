const tableRows = [...document.querySelectorAll('#comparison-body tr')];
const overviewSearch = document.querySelector('#overview-search');
const tableCount = document.querySelector('#table-count');
const overviewEmpty = document.querySelector('#overview-empty');
let selectedTag = 'all';
let selectedYear = 'all';

function updateOverview() {
  const query = (overviewSearch?.value || '').toLowerCase().trim();
  let visible = 0;
  tableRows.forEach((row) => {
    const textMatch = row.dataset.search.includes(query);
    const tagMatch = selectedTag === 'all' || row.dataset.tags.split(' ').includes(selectedTag);
    const yearMatch = selectedYear === 'all' || row.dataset.year === selectedYear;
    const show = textMatch && tagMatch && yearMatch;
    row.hidden = !show;
    if (show) visible += 1;
  });
  if (tableCount) tableCount.textContent = `显示 ${visible} / ${tableRows.length} 篇`;
  if (overviewEmpty) overviewEmpty.style.display = visible ? 'none' : 'block';
}

overviewSearch?.addEventListener('input', updateOverview);
document.querySelectorAll('[data-tag]').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelector('[data-tag].active')?.classList.remove('active');
    button.classList.add('active');
    selectedTag = button.dataset.tag;
    updateOverview();
  });
});
document.querySelectorAll('[data-year]').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelector('[data-year].active')?.classList.remove('active');
    button.classList.add('active');
    selectedYear = button.dataset.year;
    updateOverview();
  });
});
