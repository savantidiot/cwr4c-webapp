var drugs = [];
var cancers = [];

function filterResults() {
 $.ajax({
      url : "/home",
      type : "POST",
      // data: "hello",
      data : { drugs : JSON.stringify(drugs), cancers: JSON.stringify(cancers) }

  }).done(function(data) {
      window.location.reload();
      console.log("done");
  })
  .fail(function(err) {
      console.log("fail");
  });
}

function addTags(type, tag) {
  tag = tag.toLowerCase();
  if (type == 'cancer') {
    cancers.push(tag);
  } else if (type == 'drug') {
    drugs.push(tag);
  }
}

function removeTags(type, tag) {
  tag = tag.toLowerCase();
  if (type == 'cancer') {
    removeFromArr(cancers, tag);
  } else if (type == 'drug') {
    removeFromArr(drugs, tag);
  }
}

function removeFromArr(arr, val) {
    let index = arr.indexOf(val);
    if (index > -1) {
        arr.splice(index, 1);
    }
}

// Attempt to show tags on back button press
// window.addEventListener('DOMContentLoaded', () => {
//    loadTags();
// }, false);
//
// function loadTags() {
//   let checkboxes = document.getElementsByClassName('form-check-input"');
//   console.log(checkboxes);
//   Array.from(checkboxes).forEach((c) => {
//     update_tags(c.id)
//     console.log(c.id);
//   });
// }

// Update the tags that exist when a user interacts with the checkboxes
function update_tags(id, type) {
  // Get the checkbox
  const checkBox = document.getElementById(id);
  const tag = checkBox.getAttribute('data');

  let btnId = "btn" + id;
  let btnElement = document.getElementById(btnId);
  // If the checkbox is checked, display the output text
  if (checkBox.checked == true && (typeof(btnElement) == 'undefined' || btnElement == null)){
    let element = document.createElement("button");
    element.setAttribute("id", btnId);
    element.setAttribute("class", "filter-button");
    element.setAttribute("data-type", type);
    element.setAttribute("onclick", "removeButton(id)");
    element.innerHTML = tag;

    // the close icon
    let icon = document.createElement("i");
    icon.setAttribute("class", "fa fa-close x-icon");
    element.appendChild(icon);

    document.getElementById("tags").appendChild(element);

    addTags(type, tag);

  } else if (checkBox.checked == false && btnElement != null) {
    btnElement.remove();
    removeTags(type, tag);
  }
  filterResults();
}

// remove the tag button- cancer and drug
function removeButton(id) {
  const typeId = id.replace('btn','');
  const checkBox = document.getElementById(typeId);
  const tag = checkBox.getAttribute('data');
  const btnElement = document.getElementById(id);
  type = btnElement.getAttribute("data-type");
  // remove button and uncheck if box is checked
  checkBox.checked = false;
  btnElement.remove();

  removeTags(type, tag);
  filterResults();
}

function searchCancer() {
  let input, filter, cancerList, list, label, txtValue;
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
  let input, filter, drugList, list, label, txtValue;
  input = document.getElementById("search-drug");
  filter = input.value.toLowerCase();
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
