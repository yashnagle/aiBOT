import logo from "./logo.svg";
import "./App.css";
import robot_icon from "./robot_icon.png";
import React, { Component, useState } from "react";

function App() {
  const [val, setVal] = useState("");
  const click = () => {
    if (val === "") {
      console.log("No input!");
    } else {
      console.log("Query: ", val);
      console.log("Making API call!");
    }
    // make the API call to send the query
  };
  const change = (event) => {
    setVal(event.target.value);
  };
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
          onChange={change}
          placeholder="Enter query here"
        ></textarea>
        <button className="submit-button" onClick={click}>
          Submit
        </button>

        {/* <textarea
          className="query-input"
          placeholder="Enter query here"
        ></textarea> */}
      </div>
    </div>
  );
}

export default App;
