export const createClient = ({ endpointUrl }) => {

  const query = async (queryString) => {
    const url = encodeURI(endpointUrl +'?query='+ queryString);
    console.log(url)
    const response = await fetch(url);
    if(!response.ok){
      return {
        status: "error",
        result: await response.text()
      }
    }
    const content = await response.json()
    return {
      status: "ok",
      result: content?.results?.bindings
    };
    
  }

  return {
    query
  }
}