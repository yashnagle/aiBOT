import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="App">
      <div className="Header">
        <header className="title">
          <h1>aiBot</h1>
          <h2>Ask me anything!</h2>
        </header>
      </div>

      <div className="TextEntry">
        <input type="query" placeholder="Enter Text Here" />
      </div>
    </div>
  );
}

export default App;
