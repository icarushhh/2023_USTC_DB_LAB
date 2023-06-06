function showDiv(id1,id2) {
  var divs = document.getElementsByTagName("div");
  for (var i = 0; i < divs.length; i++) {
    if (divs[i].id == id1) {
      divs[i].style.display = "block";
    } else if(divs[i].id == id2){
      divs[i].style.display = "none";
    }
  }
}