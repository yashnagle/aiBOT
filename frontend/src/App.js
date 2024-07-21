import logo from "./logo.svg";
import "./App.css";
import robot_icon from "./robot_icon.png";
import React, { Component, useState, useEffect } from "react";

function App() {
  const [val, setVal] = useState("");
  const [query, setQuery] = useState("");
  const api_url = "http://127.0.0.1:5000";

  const get_request = async () => {
    const response = await fetch(api_url, {
      method: "POST",
    });
    const body = await response.json();
    console.log(body);
  };

  const click1 = () => {
    if (val === "") {
      console.log("No input!");
    } else {
      console.log("Query: ", val);
      console.log("Making API call!");
    }

    setQuery("");
    // making the API call to send the query
    get_request();
  };

  const change1 = (event) => {
    setVal(event.target.value);
    setQuery(event.target.value);
  };

  async function uploadFile(event) {
    const fileInput = event.target;
    const file = event.target.files[0];

    if (file) {
      console.log("Uploading..");
      // console.log(file);
      const formData = new FormData();
      formData.append("file", file);
      try {
        const result = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });
        const data = await result.json();
        console.log(data);
      } catch (error) {
        console.error(error);
      } finally {
        setTimeout(() => {
          fileInput.value = "";
        }, 2500);
      }
    }
  }

  return (
    <div className="App">
      <div className="Header">
        <header className="title">
          <div className="icon-title">
            <img className="icon" src={robot_icon} alt="aiBot logo" />
            <h1 className="icon_title">aiBot</h1>
          </div>
          <h2 className="subtitle">Ask me anything!</h2>
        </header>
      </div>
      <div className="TextEntry">
        <textarea
          className="query-input"
          value={query}
          onChange={change1}
          placeholder="Enter query here"
        ></textarea>
        <button className="submit-button" onClick={click1}>
          Submit
        </button>
        <input type="file" className="file-upload" onChange={uploadFile} />
      </div>
    </div>
  );
}

export default App;
