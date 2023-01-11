import createClient from "./sparql-client/index.js";

const endpointUrl = 'http://localhost:3000/sparql';
const sparql = createClient({endpointUrl});

const sendQueryClickHandler = async () => {
  const errorTextArea = document.getElementById("error-text-area");
  errorTextArea.classList.add("hidden");

  const queryInput = document.getElementById("input-textarea").value;
  localStorage.setItem("queryValue", queryInput);
  const result = await sparql.query(queryInput);
  if(result.status == "error"){
    errorTextArea.value = result.result
    errorTextArea.classList.remove("hidden");
    return;
  }
  const resultTable = document.getElementById("result-table");
  fillResultTable(resultTable, result.result);

  
}

function removeAllChildNodes(parent) {
  while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
  }
}

const fillResultTable = (table, results) => {
  const columns = Object.keys(results[0]);
  const head = table.querySelector("thead");
  removeAllChildNodes(head);
  const headRow = document.createElement("tr");
  head.appendChild(headRow);
  for( let column of columns){
    const cell = document.createElement("th");
    cell.innerText = column;
    headRow.appendChild(cell);
  }
  
  const body = table.querySelector("tbody"); 
  removeAllChildNodes(body);
  for(let result of results){
    const bodyRow = document.createElement("tr");
    body.appendChild(bodyRow);
    for( let column of columns){
      const cell = document.createElement("td");
      cell.innerText = result[column].value;
      bodyRow.appendChild(cell);
    }
  }
}

const main = async () => {
  /*
  const query = `
  PREFIX ns0: <http://purl.org/heals/food/>

  SELECT ?rec ?ing WHERE {
    ?rec ns0:hasIngredient ?ing.
  }`;
  const sparql = createClient({endpointUrl});
  const result = await sparql.query(query);
  console.log(result);*/

  const sendButton = document.getElementById("send-query-button");
  sendButton.addEventListener("click", sendQueryClickHandler);

  const queryInputTextArea = document.getElementById("input-textarea");
  queryInputTextArea.value = localStorage.getItem("queryValue");

}
main();


const wikiData = {
  endpointUrl: 'https://query.wikidata.org/sparql',
  query: `
  PREFIX wd: <http://www.wikidata.org/entity/>
  PREFIX p: <http://www.wikidata.org/prop/>
  PREFIX ps: <http://www.wikidata.org/prop/statement/>
  PREFIX pq: <http://www.wikidata.org/prop/qualifier/>

  SELECT ?s ?value WHERE {
    ?s p:P2048 ?height.

    ?height pq:P518 wd:Q24192182;
      ps:P2048 ?value .
  }`
}

const foodKg = {
  endpointUrl: '',
  query: `
  @PREFIX food: <http://purl.org/heals/food/>
  @PREFIX ingredient: <http://purl.org/heals/ingredient/>
  SELECT DISTINCT ?recipe
  WHERE {
  ?recipe food:hasIngredient ingredient:Beef .
  }
  `
}