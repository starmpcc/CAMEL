const algoliaClient = algoliasearch(
  '',
  ''
);

const searchClient = {
  search(requests) {
    if (requests.every(({ params }) => !params.query)) {
      return Promise.resolve({
        results: requests.map(() => ({
          hits: [],
          nbHits: 0,
          nbPages: 0,
        })),
      });
    }

    return algoliaClient.search(requests);
  },
};

const search = instantsearch({
  indexName: '',
  searchClient,
});


function imgurl(p1) {
  if (p1 === undefined){
    return " "
  } else if (p1.indexOf("./") === 0) {
    return p1.replace("./", "http://localhost:4000/");
  } else if (p1.indexOf("/") === 0) {
    return p1.replace("/", "http://localhost:4000/");
  } else {
    return p1
  }
}

function parsecontent(hit) {
  if (hit.html === undefined){
    return " "
  } else {
    return hit._highlightResult.html.value
  }
}
function parsetitle(hit) {
  if (hit.title === undefined){
    return "---------"
  } else {
    return hit._highlightResult.title.value
  }
}

function parseimg(img1, img2){
if (img1 === undefined){
  return img2;
  } else {
    return img1;
  }
}

const hitTemplate = function(hit) {
  const url = hit.url;
  const title = parsetitle(hit);
  const content = parsecontent(hit);
  const img = parseimg(hit.og_image, hit.header_img);
  const imglink = imgurl(img);
  if (img === undefined){
  return `
          <article class="my-2 text-left">
          <div class="row">
          <div class="col">
          <h5 class="chulapa-links-hover-only"><a href="http://localhost:4000/${url}">${title}</a></h5>
          </div>
          </div>
          <div class="row mt-2">
          <div class="col">
          <p>${content}</p>
          </div>
          </div>
          <hr>
          </article>
          `;
    } else {
    return `
    <article class="my-2 text-left">
      <div class="row">
        <div class="col">
          <h5 class="chulapa-links-hover-only"><a href="http://localhost:4000/${url}">${title}</a></h5>
        </div>
      <div class="col-4 col-md-3">
      <a href="http://localhost:4000/${url}">
        <div class="rounded-lg chulapa-overlay-img chulapa-gradient chulapa-min-h-10" style="background-image: url('${imglink}')" ></div>
        </a>
        </div>
    </div>
    <div class="row mt-2">
    <div class="col">
    <p>${content}</p>
    </div>
    </div>
    <hr>
    </article>
    `;
    }
}



search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
    placeholder: 'Search...', 
    showReset: false,
    showSubmit: false,
    showLoadingIndicator: false,
    cssClasses: {
      root: ['input-group'],
      form: ['input-group'],
      input: ['form-control', 'rounded'],
    },
  }),
  
  
  instantsearch.widgets.hits({
    container: '#hits',
    escapeHTML: false,
    templates: {
      empty: `
        {{#query}}
          <h6 class="text-center">No results found</h6>
        {{/query}}
      `,
      item: hitTemplate
    },
  }),
  
]);
search.start();
