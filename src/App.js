import logo from "./logo.svg";
import "./App.css";
import robot_icon from "./robot_icon.png";
import React, { Component, useState } from "react";

function App() {
  const [val, setVal] = useState("");
  const [query, setQuery] = useState("");

  const click1 = () => {
    if (val === "") {
      console.log("No input!");
    } else {
      console.log("Query: ", val);
      console.log("Making API call!");
    }

    setQuery("");
    // make the API call to send the query
  };

  const change1 = (event) => {
    setVal(event.target.value);
    setQuery(event.target.value);
  };

  function uploadFile(event) {
    const file = event.target.files[0];
    console.log(file);
    // You can now handle the file upload logic here
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
