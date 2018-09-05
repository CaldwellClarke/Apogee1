function loadPartyDetailContainer(partyContainerID, fetchOneId){
  renderPartyDetail(partyContainerID, fetchOneId);
  addStarFunctionality();
}

function loadPartyListContainer(partyContainerID){
  renderPartyList(partyContainerID);
  // addStarFunctionality();
}

function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}