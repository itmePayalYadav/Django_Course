const LoginForm = document.getElementById("login-form");
const ContentContainer = document.getElementById("content-container");

const baseEndPoint = "http://localhost:8000/api";

if (LoginForm) {
  LoginForm.addEventListener("submit", handleLogin);
}

function handleLogin(event) {
  event.preventDefault();
  const loginEndPoint = `${baseEndPoint}/token/`;
  let LoginFormData = new FormData(LoginForm);
  let LoginObjectData = Object.fromEntries(LoginFormData);
  let bodyString = JSON.stringify(LoginObjectData);
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: bodyString,
  };
  fetch(loginEndPoint, options)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Login failed: " + response.status);
      }
      return response.json();
    })
    .then(handleAuthData)
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function handleAuthData(authData) {
  if (authData.access && authData.refresh) {
    localStorage.setItem("access_token", authData.access);
    localStorage.setItem("refresh_token", authData.refresh);
    console.log("Login success");
    getProductList();
  } else {
    console.error("Login failed", authData);
    writeToContainer(authData);
  }
}

function writeToContainer(data) {
  if (ContentContainer) {
    ContentContainer.innerHTML =
      "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
  }
}

function getProductList() {
  const endpoint = `${baseEndPoint}/products/`;
  const accessToken = localStorage.getItem("access_token");
  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + accessToken,
    },
  };
  fetch(endpoint, options)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch products: " + response.status);
      }
      return response.json();
    })
    .then((data) => {
      console.log("Products:", data);
      writeToContainer(data);
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}
