/*
  THIS ENSURES THAT CONTENT (CONTRIBUTORS AND FEEDBACK) IS HIDDEN BY DEFAULT VIA CSS,
  AND ONLY SHOWN ON PAGES THAT ARE NOT OVERVIEW/INDEX PAGES.
  OVERVIEW PAGES INCLUDE: HOME (/), SECTION INDEX PAGES (e.g. /network/, /lab/),
  AND PAGES UNDER 'categories' OR 'tags' SECTIONS.
  THE CONTENT REMAINS IN THE DOM BUT IS CONTROLLED BY A CLASS ADDED/REMOVED BY JAVASCRIPT,
  MAKING IT EASY TO SHOW OR HIDE WHEN NECESSARY BASED ON THE PAGE URL.
*/

document.addEventListener('DOMContentLoaded', function () {
  const path = window.location.pathname;
  
  const overviewSlugs = ['/', '/network/', '/databases/', '/java/', '/spring/', '/lab/', '/blog/', '/categories/', '/tags/'];
  const isOverviewPage = overviewSlugs.includes(path)
    || path.endsWith('/index.html')
    || ['categories', 'tags'].some(p => path.includes(p));

  if (!isOverviewPage) {
    document.body.classList.add('show-contrib-feedback');
  } else {
    document.body.classList.remove('show-contrib-feedback');
  }
});

// Translate Page Widget
function addTranslateWidget() {
  const script = document.createElement('script');
  script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
  document.body.appendChild(script);
  
  window.googleTranslateElementInit = function() {
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'fr,ar,es',
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
  };
}