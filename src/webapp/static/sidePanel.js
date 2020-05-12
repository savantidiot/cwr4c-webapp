function update_tags(id, attribute) {
  // Get the checkbox
  let checkBox = document.getElementById(id);
  let c_type = checkBox.getAttribute(attribute);

  let btnId = "btn" + id;
  let btnElement = document.getElementById(btnId);
  // If the checkbox is checked, display the output text
  if (checkBox.checked == true && (typeof(btnElement) == 'undefined' || btnElement == null)){
    let element = document.createElement("button");
    element.setAttribute("id", btnId);
    element.setAttribute("class", "filter-button");
    element.setAttribute("onclick", "remove_button(id)");
    element.innerHTML = c_type;

    // the close icon
    let icon = document.createElement("i");
    icon.setAttribute("class", "fa fa-close x-icon");
    element.appendChild(icon);

    document.getElementById("tags").appendChild(element);
  } else if (checkBox.checked == false && btnElement != null) {
    btnElement.remove();
  }
}

// remove the tag button- cancer and drug
function remove_button(id) {
  let type_id = id.replace('btn','');
  let checkBox = document.getElementById(type_id);
  let btnElement = document.getElementById(id);
  // remove button and uncheck if box is checked
  checkBox.checked = false;
  btnElement.remove();
}

function searchCancer() {
  // Declare variables
  var input, filter, cancerList, list, label, txtValue;
  input = document.getElementById("search-cancer");
  filter = input.value.toLowerCase();
  cancerList = document.getElementById("cancer-list");
  list = cancerList.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < list.length; i++) {
    label = list[i].getElementsByTagName("label")[0];
    txtValue = label.textContent || label.innerText;
    if (txtValue.toLowerCase().indexOf(filter) > -1) {
      list[i].style.display = "";
    } else {
      list[i].style.display = "none";
    }
  }
}

function searchDrug() {
  // Declare variables
  var input, filter, drugList, list, label, txtValue;
  input = document.getElementById("search-drug");
  filter = input.value.toLowerCase();
  console.log(filter);
  drugList = document.getElementById("drug-list");
  list = drugList.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < list.length; i++) {
    label = list[i].getElementsByTagName("label")[0];
    txtValue = label.textContent || label.innerText;
    if (txtValue.toLowerCase().indexOf(filter) > -1) {
      list[i].style.display = "";
    } else {
      list[i].style.display = "none";
    }
  }
}
