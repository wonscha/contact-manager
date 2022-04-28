"use strict";

const serverUrl = "http://127.0.0.1:8000";

class HttpError extends Error {
  constructor(response) {
    super(`${response.status} for ${response.url}`);
    this.name = "HttpError";
    this.response = response;
  }
}

const uploadImage = async () => {
  // encode input file as base64 string for upload
  let file = document.getElementById("file").files[0];
  let converter = new Promise(function(resolve, reject) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.toString().replace(/^data:(.*,)?/, ''));
    reader.onerror = (error) => reject(error);
  });
  let encodedString = await converter;

  // clear file upload input field
  document.getElementById("file").value = "";

  // make server call to upload images
  // and return the server upload promise
  const response = await fetch(serverUrl + "/images", {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({filename: file.name, filebytes: encodedString})
  })

  if (response.ok) return response.json();
  throw new HttpError(response);
}

const updateImage = (image) => {
  document.getElementById("view").style.display = "block";

  let imageElem = document.getElementById("image");
  imageElem.src = image["fileUrl"];
  imageElem.alt = image["fileId"];

  return image;
}

const extractInformation = async (image) => {
  // make server call to extract information
  // and return the server upload promise
  const response = await fetch(serverUrl + "/images/" + image["fileId"] + "/extract-info", {
    method: 'POST'
  })

  if (response.ok) return response.json();
  throw new HttpError(response);
} 

const populateFields = (extractions) => {
  let fields = ["name", "phone", "email", "website", "address"];
  fields.map(function(field) {
    if (field in extractions) {
      let element = document.getElementById(field);
      element.value = extractions[field].join(" ");
    }
    return field;
  });
  let saveBtn = document.getElementById("save");
  saveBtn.disabled = false;
}

const uploadAndExtract = async () => {
  try {
    const image = await uploadImage();
    updateImage(image);
    const translations = await extractInformation(image);
    populateFields(translations);
  } catch (error) {
    alert("Error: " + error);
  }
}

const saveContact = async () => {
  let contactInfo = {};
  let fields = ["name", "phone", "email", "website", "address"];
  fields.map(function(field) {
    let element = document.getElementById(field);
    if (element && element.value) {
      contactInfo[field] = element.value;
    }
    return field;
  });

  let imageElem = document.getElementById("image");
  contactInfo["image"] = imageElem.src;

  // make server call to save contact
  const response = await fetch(serverUrl + "/contacts", {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }, 
    body: JSON.stringify(contactInfo)
  })
  
  if (response.ok) {
    clearContact();
    return response.json();
  }

  throw new HttpError(response);
}

const clearContact = () => {
  let fields = ["name", "phone", "email", "website", "address"];
  fields.map(function(field) {
    let element = document.getElementById(field);
    element.value = "";
    return field;
  });

  let imageElem = document.getElementById("image");
  imageElem.src = "";
  imageElem.alt = "";

  let saveBtn = document.getElementById("save");
  saveBtn.disabled = true;
}

const retrieveContacts = async () => {
  // get search name
  const searchElem = document.getElementById("search-name");
  const searchName = searchElem.value

  if (!searchName) {
    alert('Please input name of the lead contact for search.')
    throw new Error('No search name')
  }

  // make server call to get all contacts
  const response = await fetch(`${serverUrl}/contacts/${searchName}`, {
    methods: "GET"
  })
  
  if (response.ok) return response.json();
  throw new HttpError(response);
}

const displayContacts = (contacts) => {
  let contactsElem = document.getElementById("contacts")
  while (contactsElem.firstChild) {
    contactsElem.removeChild(contactsElem.firstChild);
  }

  for (let i = 0; i < contacts.length; i++) {
    let contactElem = document.createElement("div");
    contactElem.className = "w3-display-container w3-left";
    contactElem.style = "width:45%;"
    let fields = ["name", "phone", "email", "website", "address"];
    fields.forEach(field => {
      if (contacts[i][field]) {
        contactElem.appendChild(document.createTextNode(contacts[i][field]));
        contactElem.appendChild(document.createElement("br"));
      }
    });

    let cardElem = document.createElement("div");
    cardElem.className = "w3-display-container w3-right";
    let imageElem = document.createElement("img");
    imageElem.src = contacts[i]["image"];
    imageElem.height = "150";
    cardElem.appendChild(imageElem);

    let buttonElem = document.createElement("button");
    buttonElem.innerHTML = "Send Email";
    buttonElem.addEventListener("click", function() {
      window.location = `mailto:${contacts[i]["email"]}`;
    });
    buttonElem.classList.add('w3-button', 'w3-theme-d1');
    buttonElem.style.cssText = "margin-left: 10px; width: 150px; border-radius: 1rem;"
    cardElem.appendChild(buttonElem);

    contactsElem.appendChild(document.createElement("hr"));
    contactsElem.appendChild(contactElem);
    contactsElem.appendChild(imageElem);
    contactsElem.appendChild(buttonElem);
    contactsElem.appendChild(document.createElement("hr"));
  }
}

const retrieveAndDisplayContacts = async () => {
  try {
    const contacts = await retrieveContacts()
    displayContacts(contacts)
  } catch (error) {
    alert("Error: " + error);
  }
}